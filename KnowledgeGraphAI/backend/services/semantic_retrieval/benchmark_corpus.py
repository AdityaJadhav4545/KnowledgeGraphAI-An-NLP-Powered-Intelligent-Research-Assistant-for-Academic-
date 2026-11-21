"""Reproducible arXiv corpus manifest and resumable open-access PDF fetcher."""

import hashlib
import json
import re
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


PROJECT_ROOT = Path(__file__).resolve().parents[4]
BENCHMARK_ROOT = PROJECT_ROOT / "KnowledgeGraphAI" / "data" / "benchmark"
PDF_ROOT = BENCHMARK_ROOT / "pdfs"
MANIFEST_PATH = BENCHMARK_ROOT / "benchmark_manifest.json"
FAILURES_PATH = BENCHMARK_ROOT / "benchmark_failures.json"
ARXIV_API = "https://export.arxiv.org/api/query"
USER_AGENT = "KnowledgeGraphAI-SemanticBenchmark/1.0 (academic retrieval evaluation)"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

PAPER_SELECTION = (
    ("1706.03762", ["nlp", "deep_learning"]),
    ("1810.04805", ["nlp", "deep_learning"]),
    ("1903.10676", ["nlp", "scientific_text"]),
    ("2004.12832", ["information_retrieval", "nlp"]),
    ("2004.04906", ["information_retrieval", "nlp"]),
    ("2104.08663", ["information_retrieval"]),
    ("2005.11401", ["nlp", "information_retrieval"]),
    ("1609.02907", ["graph_learning", "deep_learning"]),
    ("1710.10903", ["graph_learning", "deep_learning"]),
    ("1512.03385", ["computer_vision", "deep_learning"]),
    ("1506.01497", ["computer_vision", "deep_learning"]),
    ("1505.04597", ["computer_vision", "biomedical_imaging"]),
)


def _request(url: str, timeout: int = 60) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def _benchmark_paper_id(arxiv_id: str) -> int:
    """Create a stable benchmark-local numeric key; not a Neo4j canonical ID."""
    return int.from_bytes(hashlib.sha256(arxiv_id.encode("utf-8")).digest()[:7], "big")


def _normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title).strip().casefold()


def validate_manifest(manifest: Dict[str, Any]) -> None:
    if manifest.get("schema_version") != 1:
        raise ValueError("manifest schema_version must be 1")
    papers = manifest.get("papers")
    if not isinstance(papers, list) or not papers:
        raise ValueError("manifest papers must be a non-empty list")
    arxiv_ids = []
    benchmark_ids = []
    normalized_titles = []
    dois = []
    for paper in papers:
        for field in ("arxiv_id", "title", "source_url", "local_pdf_path", "topics"):
            if not paper.get(field):
                raise ValueError(f"paper entry is missing {field}")
        arxiv_id = str(paper["arxiv_id"]).split("v")[0]
        if not re.fullmatch(r"\d{4}\.\d{4,5}", arxiv_id):
            raise ValueError(f"invalid arXiv identifier: {arxiv_id}")
        arxiv_ids.append(arxiv_id)
        benchmark_ids.append(paper.get("benchmark_paper_id"))
        normalized_titles.append(_normalize_title(paper["title"]))
        doi = (paper.get("doi") or "").strip().casefold()
        if doi:
            dois.append(doi)
        local_path = Path(paper["local_pdf_path"])
        if local_path.is_absolute() or ".." in local_path.parts:
            raise ValueError("local_pdf_path must be a safe path relative to benchmark data")
    for name, identifiers in (
        ("arXiv ID", arxiv_ids),
        ("benchmark paper ID", benchmark_ids),
        ("normalized title", normalized_titles),
        ("DOI", dois),
    ):
        present = [identifier for identifier in identifiers if identifier is not None]
        if len(present) != len(set(present)):
            raise ValueError(f"duplicate {name} detected in benchmark manifest")


def load_manifest(path: Path = MANIFEST_PATH) -> Dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    validate_manifest(manifest)
    return manifest


def write_json_atomic(path: Path, value: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(path.suffix + ".tmp")
    temporary_path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(path)


def _license_from_abs_page(arxiv_id: str) -> Dict[str, Optional[str]]:
    try:
        html = _request(f"https://arxiv.org/abs/{arxiv_id}").decode("utf-8", "replace")
    except (OSError, urllib.error.URLError, TimeoutError):
        return {"license_url": None, "license_note": "License metadata lookup failed; review source page."}
    links = re.findall(
        r'<a\b[^>]*href=["\']([^"\']*arxiv\.org/licenses/[^"\']+)["\'][^>]*>(.*?)</a>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    license_url = None
    for href, _label in links:
        license_url = href.replace("&amp;", "&")
        break
    if license_url:
        note = (
            "License link recorded from arXiv. Download is for local evaluation; "
            "redistribution is not performed."
        )
    else:
        note = (
            "No per-paper license link detected in the source page; review it "
            "before reuse or redistribution."
        )
    return {"license_url": license_url, "license_note": note}


def fetch_arxiv_metadata(
    arxiv_ids: Sequence[str],
) -> Dict[str, Dict[str, Any]]:
    if not arxiv_ids or len(arxiv_ids) != len(set(arxiv_ids)):
        raise ValueError("arxiv_ids must be a non-empty list without duplicates")
    url = f"{ARXIV_API}?id_list={','.join(arxiv_ids)}&max_results={len(arxiv_ids)}"
    root = ET.fromstring(_request(url))
    metadata: Dict[str, Dict[str, Any]] = {}
    for entry in root.findall("atom:entry", ATOM_NS):
        entry_id = entry.findtext("atom:id", namespaces=ATOM_NS) or ""
        arxiv_id = entry_id.rsplit("/abs/", 1)[-1].split("v", 1)[0]
        title = re.sub(r"\s+", " ", entry.findtext("atom:title", namespaces=ATOM_NS) or "").strip()
        abstract = re.sub(r"\s+", " ", entry.findtext("atom:summary", namespaces=ATOM_NS) or "").strip()
        authors = [
            author.findtext("atom:name", namespaces=ATOM_NS) or ""
            for author in entry.findall("atom:author", ATOM_NS)
        ]
        published = entry.findtext("atom:published", namespaces=ATOM_NS) or ""
        doi = entry.findtext("arxiv:doi", namespaces=ATOM_NS)
        primary_category = entry.find("arxiv:primary_category", ATOM_NS)
        categories = [
            category.attrib.get("term", "")
            for category in entry.findall("atom:category", ATOM_NS)
        ]
        if not arxiv_id or not title or not abstract or not published:
            raise ValueError(f"Incomplete arXiv Atom metadata for entry {entry_id}")
        metadata[arxiv_id] = {
            "arxiv_id": arxiv_id,
            "title": title,
            "authors": authors,
            "publication_year": int(published[:4]),
            "published": published,
            "doi": doi,
            "abstract": abstract,
            "source_url": f"https://arxiv.org/abs/{arxiv_id}",
            "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}",
            "primary_category": (
                primary_category.attrib.get("term")
                if primary_category is not None else None
            ),
            "categories": categories,
        }
    missing = sorted(set(arxiv_ids) - set(metadata))
    if missing:
        raise ValueError(f"arXiv API returned no records for IDs: {missing}")
    return metadata


def create_manifest(
    data_root: Path = BENCHMARK_ROOT,
    *,
    refresh_metadata: bool = False,
) -> Dict[str, Any]:
    manifest_path = data_root / "benchmark_manifest.json"
    if manifest_path.exists() and not refresh_metadata:
        existing = load_manifest(manifest_path)
        expected = [item[0] for item in PAPER_SELECTION]
        actual = [paper["arxiv_id"] for paper in existing["papers"]]
        if actual == expected:
            return existing

    ids = [item[0] for item in PAPER_SELECTION]
    metadata = fetch_arxiv_metadata(ids)
    papers = []
    for position, (arxiv_id, topics) in enumerate(PAPER_SELECTION):
        record = metadata[arxiv_id]
        if position:
            time.sleep(3)
        license_info = _license_from_abs_page(arxiv_id)
        papers.append({
            **record,
            **license_info,
            "topics": topics,
            "benchmark_paper_id": _benchmark_paper_id(arxiv_id),
            "canonical_neo4j_paper_id": None,
            "local_pdf_path": f"pdfs/{arxiv_id}.pdf",
            "pdf_sha256": None,
            "download_status": "pending",
            "index_status": "pending",
            "index_pdf_sha256": None,
            "chunk_count": 0,
            "index_error": None,
        })
    manifest = {
        "schema_version": 1,
        "dataset_version": "phase4.3-arxiv-pilot-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_api": ARXIV_API,
        "corpus_license_policy": (
            "Per-paper source license links are recorded when available. PDFs are "
            "downloaded only for local evaluation and are excluded from Git; no "
            "redistribution is intended."
        ),
        "papers": papers,
    }
    validate_manifest(manifest)
    write_json_atomic(manifest_path, manifest)
    return manifest


def download_papers(
    manifest: Dict[str, Any],
    data_root: Path = BENCHMARK_ROOT,
    *,
    minimum_request_interval: float = 3.0,
) -> Dict[str, Any]:
    """Download only missing/invalid PDFs; persist per-paper success/failure."""
    if minimum_request_interval < 0:
        raise ValueError("minimum_request_interval must be non-negative")
    validate_manifest(manifest)
    failures: List[Dict[str, str]] = []
    last_request = 0.0
    for paper in manifest["papers"]:
        local_path = data_root / paper["local_pdf_path"]
        if local_path.is_file():
            contents = local_path.read_bytes()
            if contents.startswith(b"%PDF"):
                paper["pdf_sha256"] = hashlib.sha256(contents).hexdigest()
                paper["download_status"] = "downloaded"
                paper["download_error"] = None
                write_json_atomic(data_root / "benchmark_manifest.json", manifest)
                continue
        local_path.parent.mkdir(parents=True, exist_ok=True)
        wait = minimum_request_interval - (time.monotonic() - last_request)
        if last_request and wait > 0:
            time.sleep(wait)
        temporary_path = local_path.with_suffix(local_path.suffix + ".part")
        try:
            contents = _request(paper["pdf_url"], timeout=120)
            last_request = time.monotonic()
            if not contents.startswith(b"%PDF"):
                raise ValueError("source response did not contain a PDF signature")
            temporary_path.write_bytes(contents)
            temporary_path.replace(local_path)
            paper["pdf_sha256"] = hashlib.sha256(contents).hexdigest()
            paper["download_status"] = "downloaded"
            paper["download_error"] = None
        except Exception as exc:
            temporary_path.unlink(missing_ok=True)
            paper["download_status"] = "failed"
            paper["download_error"] = f"{type(exc).__name__}: {exc}"
            failures.append({
                "arxiv_id": paper["arxiv_id"],
                "error": paper["download_error"],
            })
        write_json_atomic(data_root / "benchmark_manifest.json", manifest)
        write_json_atomic(data_root / "benchmark_failures.json", {"failures": failures})
    return {"manifest": manifest, "failures": failures}


def validate_query_dataset(dataset: Dict[str, Any]) -> None:
    queries = dataset.get("queries")
    if not isinstance(queries, list) or not queries:
        raise ValueError("benchmark query dataset must contain a non-empty queries list")
    identifiers = [query.get("query_id") for query in queries]
    if any(not identifier for identifier in identifiers):
        raise ValueError("every benchmark query must have a query_id")
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("duplicate benchmark query IDs detected")
    for query in queries:
        if not isinstance(query.get("query_text"), str) or not query["query_text"].strip():
            raise ValueError(f"query {query.get('query_id')} has empty query_text")
        if not isinstance(query.get("target_areas"), list) or not query["target_areas"]:
            raise ValueError(f"query {query.get('query_id')} needs target_areas")


def validate_annotations(
    annotations: Dict[str, Any],
    query_ids: Iterable[str],
    paper_ids: Iterable[int],
    chunk_ids: Optional[Iterable[str]] = None,
) -> None:
    if annotations.get("schema_version") != 1:
        raise ValueError("annotation schema_version must be 1")
    known_queries = set(query_ids)
    known_papers = set(paper_ids)
    entries = annotations.get("queries")
    if not isinstance(entries, list):
        raise ValueError("annotations must contain a queries list")
    entry_ids = [entry.get("query_id") for entry in entries]
    if len(entry_ids) != len(set(entry_ids)):
        raise ValueError("duplicate annotation query IDs")
    if set(entry_ids) != known_queries:
        raise ValueError("annotations must contain exactly one entry per benchmark query")
    for entry in entries:
        status = entry.get("judgment_status")
        if status not in {"pending_human_review", "human_verified"}:
            raise ValueError(f"invalid judgment_status for {entry['query_id']}")
        source = entry.get("annotation_source")
        if status == "human_verified" and not source:
            raise ValueError("human-verified entries require annotation_source")
        if status == "human_verified" and not entry.get("annotation_notes"):
            raise ValueError("human-verified entries require annotation_notes")
        if status == "human_verified" and (
            not entry.get("annotator")
            or not entry.get("reviewed_at")
            or not isinstance(entry.get("independent_review_attested"), bool)
        ):
            raise ValueError(
                "human-verified entries require reviewer identity, timestamp, "
                "and a boolean independent-review state"
            )
        if status == "human_verified" and entry.get(
            "verification_method", "manual"
        ) not in {
            "manual",
            "bulk_confirmed",
        }:
            raise ValueError(
                "human-verified entries require a manual or bulk_confirmed "
                "verification_method"
            )
        judged_papers = entry.get("judged_paper_ids", [])
        if not isinstance(judged_papers, list) or not set(judged_papers) <= known_papers:
            raise ValueError(f"invalid judged_paper_ids for {entry['query_id']}")
        unjudged_papers = entry.get("unjudged_paper_ids", [])
        if not isinstance(unjudged_papers, list) or not set(unjudged_papers) <= known_papers:
            raise ValueError(f"invalid unjudged_paper_ids for {entry['query_id']}")
        if set(judged_papers) & set(unjudged_papers):
            raise ValueError("a paper cannot be both judged and unjudged")
        if set(judged_papers) | set(unjudged_papers) != known_papers:
            raise ValueError("judged and unjudged papers must partition the benchmark corpus")
        if status == "human_verified" and unjudged_papers:
            raise ValueError("human-verified paper judgments must cover the benchmark corpus")
        relevant = entry.get("relevant_paper_ids", [])
        if not isinstance(relevant, list):
            raise ValueError("relevant_paper_ids must be a list")
        if not set(relevant) <= set(judged_papers):
            raise ValueError("relevant paper IDs must be explicitly judged")
        if not set(relevant) <= known_papers:
            raise ValueError(f"unknown relevant paper ID for {entry['query_id']}")
        grades = entry.get("paper_relevance_grades", {})
        if not isinstance(grades, dict):
            raise ValueError("paper_relevance_grades must be an object")
        if any(
            isinstance(value, bool) or not isinstance(value, int)
            for value in grades.values()
        ):
            raise ValueError("paper relevance grades must be integers from 0 to 3")
        try:
            grade_ids = {int(value) for value in grades}
            grade_values = [int(value) for value in grades.values()]
        except (TypeError, ValueError) as exc:
            raise ValueError("paper relevance grades must use numeric IDs and grades") from exc
        if any(grade < 0 or grade > 3 for grade in grade_values):
            raise ValueError("paper relevance grades must be integers from 0 to 3")
        if not grade_ids <= known_papers:
            raise ValueError(f"unknown graded paper ID for {entry['query_id']}")
        if not grade_ids <= set(judged_papers):
            raise ValueError("graded papers must be explicitly judged")
        if {
            paper_id for paper_id, grade in (
                (int(paper_id), grade) for paper_id, grade in grades.items()
            ) if grade > 0
        } != set(relevant) & grade_ids:
            raise ValueError("positive graded papers must match graded relevant_paper_ids")
        judged_chunks = entry.get("judged_chunk_ids", [])
        if not isinstance(judged_chunks, list):
            raise ValueError("judged_chunk_ids must be a list")
        if chunk_ids is not None and not set(judged_chunks) <= set(chunk_ids):
            raise ValueError(f"unknown judged chunk ID for {entry['query_id']}")
        relevant_chunks = entry.get("relevant_chunk_ids", [])
        if not isinstance(relevant_chunks, list):
            raise ValueError("relevant_chunk_ids must be a list")
        if not set(relevant_chunks) <= set(judged_chunks):
            raise ValueError("relevant chunk IDs must be explicitly judged")
        chunk_grades = entry.get("chunk_relevance_grades", {})
        if not isinstance(chunk_grades, dict):
            raise ValueError("chunk_relevance_grades must be an object")
        if any(
            isinstance(value, bool) or not isinstance(value, int) or value < 0 or value > 3
            for value in chunk_grades.values()
        ):
            raise ValueError("chunk relevance grades must be integers from 0 to 3")
        if not set(chunk_grades) <= set(judged_chunks):
            raise ValueError("graded chunks must be explicitly judged")
        if {
            chunk_id for chunk_id, grade in chunk_grades.items() if grade > 0
        } != set(relevant_chunks) & set(chunk_grades):
            raise ValueError("positive graded chunks must match graded relevant_chunk_ids")


def write_annotation_template(
    query_dataset: Dict[str, Any],
    manifest: Dict[str, Any],
    output_path: Path,
) -> Dict[str, Any]:
    validate_query_dataset(query_dataset)
    if output_path.exists():
        return json.loads(output_path.read_text(encoding="utf-8"))
    annotations = {
        "schema_version": 1,
        "label_type": "human_annotated",
        "provenance": (
            "Template only. No relevance judgments have been assigned. A human "
            "annotator must inspect the query, paper title/abstract, and passages "
            "before changing judgment_status to human_verified."
        ),
        "papers_for_review": [
            {
                "benchmark_paper_id": paper["benchmark_paper_id"],
                "arxiv_id": paper["arxiv_id"],
                "title": paper["title"],
                "abstract": paper["abstract"],
            }
            for paper in manifest["papers"]
        ],
        "queries": [
            {
                "query_id": query["query_id"],
                "query_text": query["query_text"],
                "judgment_status": "pending_human_review",
                "judged_paper_ids": [],
                "relevant_paper_ids": [],
                "judged_chunk_ids": [],
                "relevant_chunk_ids": [],
                "paper_relevance_grades": {},
                "annotation_source": None,
                "annotation_notes": None,
                "unjudged_paper_ids": [
                    paper["benchmark_paper_id"] for paper in manifest["papers"]
                ],
            }
            for query in query_dataset["queries"]
        ],
    }
    validate_annotations(
        annotations,
        (query["query_id"] for query in query_dataset["queries"]),
        (paper["benchmark_paper_id"] for paper in manifest["papers"]),
    )
    write_json_atomic(output_path, annotations)
    return annotations
