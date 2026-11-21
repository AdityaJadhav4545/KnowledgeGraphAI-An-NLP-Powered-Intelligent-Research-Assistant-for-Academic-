"""Local Streamlit interface for human relevance annotation."""

import csv
import json
import math
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence, Tuple

import streamlit as st
import requests

from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_annotation_workflow import (
    CHUNK_FIELDS,
    CHUNK_WORKSHEET,
    PAPER_FIELDS,
    PAPER_WORKSHEET,
    _parse_label,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.assisted_annotation import (
    AUTOMATED_LABELS,
    suggest_relevance,
)
from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_annotation_workflow import (
    RESULTS_PATH,
)

PAPER_KEY_FIELDS = ("query_id", "benchmark_paper_id")
CHUNK_KEY_FIELDS = ("query_id", "chunk_id")
AUTOMATED_FIELDS = (
    "automated_label",
    "automated_confidence",
    "automated_explanation",
    "automated_model",
    "automated_generated_at",
    "automated_suggestion_history",
)
HUMAN_FIELDS = ("human_label", "verification_method")
EXTENDED_FIELDS = (*AUTOMATED_FIELDS, "automated_suggestion_history", *HUMAN_FIELDS)
FILTER_OPTIONS = (
    "All",
    "Unreviewed",
    "Uncertain suggestions",
    "Human relevant",
    "Human not_relevant",
    "Suggested relevant",
    "Suggested not_relevant",
    "Disagreement",
)

JUDGMENT_FIELDS = (
    "relevance_judgment",
    "grade_0_to_3",
    "reviewer",
    "reviewed_at",
    "independent_review_attested",
    "review_notes",
)


def load_worksheet(
    path: Path, required_fields: Sequence[str], key_fields: Sequence[str]
) -> Tuple[List[Dict[str, str]], List[str]]:
    """Load a worksheet without dropping columns, rejecting malformed identities."""
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        fields = list(reader.fieldnames or [])
        missing = set(required_fields) - set(EXTENDED_FIELDS) - set(fields)
        if missing:
            raise ValueError(f"{path.name} is missing columns: {sorted(missing)}")
        rows = list(reader)
    for row in rows:
        for field in EXTENDED_FIELDS:
            row.setdefault(field, "")
        if not row["human_label"]:
            row["human_label"] = row.get("relevance_judgment", "")
        if row["human_label"] and not row["verification_method"]:
            row["verification_method"] = "manual_legacy"

    seen = set()
    for row_number, row in enumerate(rows, start=2):
        key = tuple((row.get(field) or "").strip() for field in key_fields)
        if any(not value for value in key):
            raise ValueError(f"{path.name}:{row_number} has an empty record identity")
        if key in seen:
            raise ValueError(f"{path.name}:{row_number} duplicates record identity {key}")
        seen.add(key)
        label = (row.get("human_label") or "").strip()
        if label:
            _parse_label(row, f"{path.name}:{row_number}")
        automated_label = (row.get("automated_label") or "").strip()
        if automated_label and automated_label not in AUTOMATED_LABELS:
            raise ValueError(
                f"{path.name}:{row_number} has invalid automated_label"
            )
        confidence = (row.get("automated_confidence") or "").strip()
        if confidence:
            try:
                parsed_confidence = float(confidence)
            except ValueError as exc:
                raise ValueError(
                    f"{path.name}:{row_number} has invalid automated_confidence"
                ) from exc
            if not math.isfinite(parsed_confidence) or not 0 <= parsed_confidence <= 1:
                raise ValueError(
                    f"{path.name}:{row_number} has invalid automated_confidence"
                )
        if automated_label and not row.get("automated_explanation", "").strip():
            raise ValueError(
                f"{path.name}:{row_number} automated suggestion has no explanation"
            )
        if automated_label and not confidence:
            raise ValueError(
                f"{path.name}:{row_number} automated suggestion has no confidence"
            )
    return rows, fields


def worksheet_progress(rows: Sequence[Mapping[str, str]]) -> Dict[str, int]:
    reviewed = sum(
        bool((row.get("human_label") or row.get("relevance_judgment") or "").strip())
        for row in rows
    )
    return {
        "total": len(rows),
        "reviewed": reviewed,
        "remaining": len(rows) - reviewed,
    }


def _create_backup(path: Path) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = path.with_name(f"{path.name}.{timestamp}.bak")
    shutil.copy2(path, backup)
    return backup


def _write_rows_safely(path: Path, fields: Sequence[str], rows: Sequence[Mapping[str, str]]) -> None:
    backup_path = _create_backup(path)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8-sig",
            newline="",
            delete=False,
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
        ) as output:
            temporary_path = Path(output.name)
            writer = csv.DictWriter(output, fieldnames=fields, extrasaction="raise")
            writer.writeheader()
            writer.writerows(rows)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary_path, path)
    except Exception:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise
    return backup_path


def _find_row(
    rows: Sequence[Dict[str, str]],
    key_fields: Sequence[str],
    identity: Mapping[str, str],
) -> Dict[str, str]:
    identity_key = tuple(str(identity.get(field, "")).strip() for field in key_fields)
    matches = [
        row
        for row in rows
        if tuple((row.get(field) or "").strip() for field in key_fields)
        == identity_key
    ]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one worksheet record for {identity_key}")
    return matches[0]


def save_judgment(
    path: Path,
    required_fields: Sequence[str],
    key_fields: Sequence[str],
    identity: Mapping[str, str],
    label: str,
    grade: str,
    reviewer: str,
    notes: str,
    independent_attestation: bool,
    verification_method: str = "manual",
) -> Path:
    """Validate, back up, and atomically save one explicit human judgment."""
    normalized_label = label.strip().lower()
    normalized_grade = grade.strip()
    _parse_label(
        {
            "relevance_judgment": normalized_label,
            "grade_0_to_3": normalized_grade,
        },
        "submitted judgment",
    )
    reviewer = reviewer.strip()
    if not reviewer:
        raise ValueError("reviewer name is required")

    if verification_method not in {"manual", "bulk_confirmed"}:
        raise ValueError("verification_method must be manual or bulk_confirmed")
    rows, fields = load_worksheet(path, required_fields, key_fields)
    row = _find_row(rows, key_fields, identity)
    fields = list(dict.fromkeys([*fields, *required_fields, *EXTENDED_FIELDS]))
    row.update(
        {
            "relevance_judgment": normalized_label,
            "human_label": normalized_label,
            "grade_0_to_3": normalized_grade,
            "reviewer": reviewer,
            "reviewed_at": datetime.now(timezone.utc).isoformat(),
            "independent_review_attested": "yes" if independent_attestation else "",
            "review_notes": notes.strip(),
            "verification_method": verification_method,
        }
    )
    return _write_rows_safely(path, fields, rows)


def save_suggestion(
    path: Path,
    required_fields: Sequence[str],
    key_fields: Sequence[str],
    identity: Mapping[str, str],
    suggestion: Mapping[str, object],
) -> Path:
    label = suggestion.get("label")
    confidence = suggestion.get("confidence")
    explanation = suggestion.get("explanation")
    if not isinstance(label, str) or label not in AUTOMATED_LABELS:
        raise ValueError("automated label must be relevant, not_relevant, or uncertain")
    if (
        isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
        or not math.isfinite(float(confidence))
        or not 0 <= float(confidence) <= 1
    ):
        raise ValueError("automated confidence must be a finite number from 0 to 1")
    if not isinstance(explanation, str) or not explanation.strip():
        raise ValueError("automated explanation is required")
    generated_at = str(
        suggestion.get("generated_at") or datetime.now(timezone.utc).isoformat()
    )
    return save_suggestions(
        path,
        required_fields,
        key_fields,
        [
            {
                **identity,
                "label": str(label),
                "confidence": float(confidence),
                "explanation": explanation.strip(),
                "model": str(suggestion.get("model", "")),
                "generated_at": generated_at,
                "query_id": str(identity.get("query_id", "")),
                "candidate_id": str(identity.get(key_fields[-1], "")),
                "annotation_type": "chunk" if key_fields[-1] == "chunk_id" else "paper",
            }
        ],
    )


def save_suggestions(
    path: Path,
    required_fields: Sequence[str],
    key_fields: Sequence[str],
    suggestions: Sequence[Mapping[str, object]],
) -> Path:
    """Persist suggestions in one backed-up write without changing human fields."""
    rows, fields = load_worksheet(path, required_fields, key_fields)
    fields = list(dict.fromkeys([*fields, *required_fields, *EXTENDED_FIELDS]))
    seen = set()
    for suggestion in suggestions:
        identity = {
            field: str(suggestion.get(field, ""))
            for field in key_fields
        }
        identity_key = tuple(identity[field].strip() for field in key_fields)
        if identity_key in seen:
            raise ValueError(f"duplicate suggestion identity {identity_key}")
        seen.add(identity_key)
        row = _find_row(rows, key_fields, identity)
        previous_history = row.get("automated_suggestion_history", "").strip()
        try:
            history = json.loads(previous_history) if previous_history else []
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"invalid automated_suggestion_history for {identity_key}"
            ) from exc
        if not isinstance(history, list):
            raise ValueError(
                f"automated_suggestion_history for {identity_key} must be a list"
            )
        previous_label = row.get("automated_label", "").strip()
        previous_timestamp = row.get("automated_generated_at", "")
        already_in_history = any(
            isinstance(item, dict)
            and item.get("generated_at") == previous_timestamp
            and item.get("label") == previous_label
            for item in history
        )
        if previous_label and not already_in_history:
            history.append({
                "annotation_type": (
                    "chunk" if key_fields[-1] == "chunk_id" else "paper"
                ),
                "query_id": identity_key[0],
                "candidate_id": identity_key[-1],
                "label": previous_label,
                "confidence": row.get("automated_confidence", ""),
                "explanation": row.get("automated_explanation", ""),
                "model": row.get("automated_model", ""),
                "generated_at": previous_timestamp,
            })
        label = suggestion.get("label")
        confidence = suggestion.get("confidence")
        explanation = suggestion.get("explanation")
        if not isinstance(label, str) or label not in AUTOMATED_LABELS:
            raise ValueError("automated label must be relevant, not_relevant, or uncertain")
        if (
            isinstance(confidence, bool)
            or not isinstance(confidence, (int, float))
            or not math.isfinite(float(confidence))
            or not 0 <= float(confidence) <= 1
        ):
            raise ValueError("automated confidence must be a finite number from 0 to 1")
        if not isinstance(explanation, str) or not explanation.strip():
            raise ValueError("automated explanation is required")
        generated_at = str(
            suggestion.get("generated_at") or datetime.now(timezone.utc).isoformat()
        )
        history_record = {
            "annotation_type": str(
                suggestion.get("annotation_type")
                or ("chunk" if key_fields[-1] == "chunk_id" else "paper")
            ),
            "query_id": str(suggestion.get("query_id") or identity_key[0]),
            "candidate_id": str(
                suggestion.get("candidate_id") or identity_key[-1]
            ),
            "label": label,
            "confidence": float(confidence),
            "explanation": explanation.strip(),
            "model": str(suggestion.get("model", "")),
            "generated_at": generated_at,
        }
        history.append(history_record)
        row.update(
            {
                "automated_label": label,
                "automated_confidence": str(float(confidence)),
                "automated_explanation": explanation.strip(),
                "automated_model": str(suggestion.get("model", "")),
                "automated_generated_at": generated_at,
                "automated_suggestion_history": json.dumps(
                    history, ensure_ascii=False
                ),
            }
        )
    if not suggestions:
        raise ValueError("no suggestions were supplied")
    return _write_rows_safely(path, fields, rows)


def bulk_accept_suggestions(
    path: Path,
    required_fields: Sequence[str],
    key_fields: Sequence[str],
    identities: Sequence[Mapping[str, str]],
    reviewer: str,
    minimum_confidence: float,
    *,
    confirmed: bool,
    independent_attestation: bool = False,
) -> Dict[str, object]:
    if not confirmed:
        raise ValueError("explicit reviewer confirmation is required")
    reviewer = reviewer.strip()
    if not reviewer:
        raise ValueError("reviewer name is required")
    if not math.isfinite(minimum_confidence) or not 0 <= minimum_confidence <= 1:
        raise ValueError("minimum_confidence must be from 0 to 1")
    rows, fields = load_worksheet(path, required_fields, key_fields)
    fields = list(dict.fromkeys([*fields, *required_fields, *EXTENDED_FIELDS]))
    seen = set()
    accepted = []
    skipped_human = []
    for identity in identities:
        row = _find_row(rows, key_fields, identity)
        identity_key = tuple(str(identity[field]).strip() for field in key_fields)
        if identity_key in seen:
            raise ValueError(f"duplicate bulk identity {identity_key}")
        seen.add(identity_key)
        label = row.get("automated_label", "").strip()
        try:
            confidence = float(row.get("automated_confidence", ""))
        except ValueError:
            continue
        if (
            label not in {"relevant", "not_relevant"}
            or confidence < minimum_confidence
        ):
            continue
        if (row.get("human_label") or row.get("relevance_judgment") or "").strip():
            skipped_human.append(identity_key)
            continue
        row.update(
            {
                "relevance_judgment": label,
                "human_label": label,
                "grade_0_to_3": "",
                "reviewer": reviewer,
                "reviewed_at": datetime.now(timezone.utc).isoformat(),
                "independent_review_attested": (
                    "yes" if independent_attestation else ""
                ),
                "review_notes": (
                    "Human explicitly accepted the automated suggestion "
                    f"(confidence {confidence:.3f})."
                ),
                "verification_method": "bulk_confirmed",
            }
        )
        accepted.append(identity_key)
    backup = _write_rows_safely(path, fields, rows) if accepted else None
    return {
        "accepted_count": len(accepted),
        "skipped_existing_human_count": len(skipped_human),
        "accepted_identities": accepted,
        "backup_path": str(backup) if backup else None,
    }


def _query_rows(rows: Sequence[Dict[str, str]], query_id: str) -> List[Dict[str, str]]:
    return [row for row in rows if row["query_id"] == query_id]


def _best_retrieval_rank(row: Mapping[str, str]) -> int:
    try:
        hits = json.loads(row.get("retrieval_hits") or "[]")
        ranks = [
            int(hit["rank"])
            for hit in hits
            if isinstance(hit, dict) and int(hit.get("rank", 0)) > 0
        ]
        return min(ranks) if ranks else 2**31 - 1
    except (TypeError, ValueError, json.JSONDecodeError):
        return 2**31 - 1


def _filter_candidates(
    rows: Sequence[Dict[str, str]], selected_filter: str
) -> List[Dict[str, str]]:
    if selected_filter == "All":
        return list(rows)
    if selected_filter == "Unreviewed":
        return [
            row for row in rows
            if not (row.get("human_label") or row.get("relevance_judgment") or "").strip()
        ]
    if selected_filter == "Uncertain suggestions":
        return [row for row in rows if row.get("automated_label") == "uncertain"]
    if selected_filter == "Human relevant":
        return [row for row in rows if row.get("human_label") == "relevant"]
    if selected_filter == "Human not_relevant":
        return [row for row in rows if row.get("human_label") == "not_relevant"]
    if selected_filter == "Suggested relevant":
        return [row for row in rows if row.get("automated_label") == "relevant"]
    if selected_filter == "Suggested not_relevant":
        return [row for row in rows if row.get("automated_label") == "not_relevant"]
    return [
        row for row in rows
        if row.get("human_label") in {"relevant", "not_relevant"}
        and row.get("automated_label") in {"relevant", "not_relevant"}
        and row["human_label"] != row["automated_label"]
    ]


def _render_worksheet(
    kind: str,
    path: Path,
    required_fields: Sequence[str],
    key_fields: Sequence[str],
    query_text_by_id: Mapping[str, str],
) -> None:
    rows, _fields = load_worksheet(path, required_fields, key_fields)
    query_ids = list(dict.fromkeys(row["query_id"] for row in rows))
    if not query_ids:
        st.info("This worksheet contains no candidate records.")
        return

    query_id = st.selectbox(
        "Query",
        query_ids,
        format_func=lambda value: f"{value} — {query_text_by_id.get(value, '')}",
        key=f"{kind}_query",
    )
    st.markdown(f"**Query text:** {query_text_by_id.get(query_id, rows[0]['query_text'])}")
    query_records = _query_rows(rows, query_id)
    progress = worksheet_progress(query_records)
    metric_columns = st.columns(3)
    metric_columns[0].metric("Reviewed", progress["reviewed"])
    metric_columns[1].metric("Remaining", progress["remaining"])
    metric_columns[2].metric("Candidates", progress["total"])
    st.progress(
        progress["reviewed"] / progress["total"] if progress["total"] else 0.0
    )
    selected_filter = st.selectbox(
        "Candidate filter",
        FILTER_OPTIONS,
        key=f"{kind}_candidate_filter_{query_id}",
    )
    confidence_range = st.slider(
        "Automated suggestion confidence range",
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.01,
        key=f"{kind}_confidence_range_{query_id}",
    )
    batch_column, _ = st.columns([1, 2])
    with batch_column:
        batch_size = st.number_input(
            "Batch size",
            min_value=1,
            max_value=50,
            value=8,
            key=f"{kind}_batch_size_{query_id}",
        )
        rate_limit = st.number_input(
            "Rate limit delay (seconds)",
            min_value=0.0,
            max_value=30.0,
            value=0.0,
            step=0.25,
            key=f"{kind}_rate_limit_{query_id}",
        )
        if st.button(
            f"Generate missing {kind} suggestions for this query",
            key=f"{kind}_batch_generate_{query_id}",
        ):
            from KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_batch_annotation import (
                run_batch_annotation,
            )

            progress_bar = st.progress(0.0)
            progress_text = st.empty()

            def update_progress(state: Mapping[str, object]) -> None:
                total = int(state["total"])
                progress_bar.progress(
                    int(state["completed"]) / total if total else 1.0
                )
                progress_text.write(
                    f"{kind}: {state['completed']}/{total}, "
                    f"generated {state['generated']}, "
                    f"recovered {state['recovered_from_checkpoint']}, "
                    f"failed {state['failed']}"
                )

            try:
                outcome = run_batch_annotation(
                    annotation_type=kind,
                    query_id=query_id,
                    batch_size=int(batch_size),
                    rate_limit_seconds=float(rate_limit),
                    progress=update_progress,
                )
            except Exception as error:
                st.error(f"Batch suggestion run failed: {error}")
            else:
                st.success(
                    f"Batch complete. See checkpoint: {outcome['checkpoint_path']}"
                )
                st.json(outcome["results"][kind])
                st.rerun()
    if kind == "chunk":
        top_k = st.number_input(
            "Top-K chunks to review",
            min_value=1,
            max_value=max(1, len(query_records)),
            value=min(5, max(1, len(query_records))),
            step=1,
            key=f"{kind}_top_k_{query_id}",
        )
        query_records = sorted(query_records, key=_best_retrieval_rank)[:int(top_k)]
    candidates = _filter_candidates(query_records, selected_filter)
    if confidence_range != (0.0, 1.0):
        candidates = [
            row for row in candidates
            if row.get("automated_confidence", "").strip()
            and confidence_range[0]
            <= float(row["automated_confidence"])
            <= confidence_range[1]
        ]
    prioritize_uncertain = st.checkbox(
        "Prioritize uncertain suggestions",
        value=True,
        key=f"{kind}_prioritize_uncertain_{query_id}",
    )
    if prioritize_uncertain:
        candidates.sort(
            key=lambda row: (
                0 if row.get("automated_label") == "uncertain" else 1,
                0
                if row.get("human_label") in {"relevant", "not_relevant"}
                and row.get("automated_label") in {"relevant", "not_relevant"}
                and row["human_label"] != row["automated_label"]
                else 1,
                -float(row.get("automated_confidence") or 0.0),
            )
        )

    st.subheader("Bulk confirmation of high-confidence suggestions")
    bulk_candidates = [
        row for row in query_records
        if row.get("automated_label") in {"relevant", "not_relevant"}
        and not (row.get("human_label") or row.get("relevance_judgment") or "").strip()
    ]
    with st.form(f"{kind}_bulk_form_{query_id}"):
        threshold = st.slider(
            "Minimum suggestion confidence",
            min_value=0.50,
            max_value=1.00,
            value=0.85,
            step=0.01,
            key=f"{kind}_bulk_threshold_{query_id}",
        )
        bulk_reviewer = st.text_input(
            "Reviewer name for bulk confirmation",
            value=st.session_state.get("reviewer_name", ""),
            key=f"{kind}_bulk_reviewer_{query_id}",
        )
        eligible = [
            row for row in bulk_candidates
            if float(row.get("automated_confidence") or 0.0) >= threshold
        ]
        st.caption(
            f"{len(eligible)} unreviewed, non-uncertain suggestions meet the "
            "confidence threshold within the selected query/Top-K."
        )
        confirm_bulk = st.checkbox(
            "I reviewed these suggestions and explicitly accept their labels "
            "as human judgments.",
            key=f"{kind}_bulk_confirm_{query_id}",
        )
        bulk_submitted = st.form_submit_button("Confirm eligible suggestions")
    if bulk_submitted:
        identities = [
            {field: row[field] for field in key_fields} for row in eligible
        ]
        try:
            outcome = bulk_accept_suggestions(
                path,
                required_fields,
                key_fields,
                identities,
                bulk_reviewer,
                threshold,
                confirmed=confirm_bulk,
            )
        except (OSError, ValueError) as error:
            st.error(f"Bulk confirmation was not saved: {error}")
        else:
            st.session_state["reviewer_name"] = bulk_reviewer.strip()
            st.success(
                f"Human-confirmed {outcome['accepted_count']} suggestions; "
                f"preserved {outcome['skipped_existing_human_count']} existing judgments."
            )
            st.rerun()

    if not candidates:
        st.info("No candidates match this filter and review scope.")
        return

    candidate_key = f"{kind}_candidate_{query_id}"
    selector_key = f"{kind}_candidate_selector_{query_id}"
    candidate_ids = [str(row[key_fields[-1]]) for row in candidates]
    current_id = st.session_state.get(
        selector_key, st.session_state.get(candidate_key, candidate_ids[0])
    )
    if current_id not in candidate_ids:
        current_id = candidate_ids[0]
        if selector_key in st.session_state:
            st.session_state[selector_key] = current_id
    current_index = candidate_ids.index(current_id)
    navigation = st.columns([1, 4, 1])
    if navigation[0].button(
        "← Previous", disabled=current_index == 0, key=f"{kind}_previous"
    ):
        st.session_state[selector_key] = candidate_ids[current_index - 1]
        st.rerun()
    if navigation[2].button(
        "Next →",
        disabled=current_index == len(candidates) - 1,
        key=f"{kind}_next",
    ):
        st.session_state[selector_key] = candidate_ids[current_index + 1]
        st.rerun()
    selected_id = navigation[1].selectbox(
        "Candidate",
        candidate_ids,
        index=current_index,
        format_func=lambda value: next(
            row["title"] for row in candidates if str(row[key_fields[-1]]) == value
        ),
        key=selector_key,
    )
    st.session_state[candidate_key] = selected_id
    selected_index = candidate_ids.index(selected_id)
    record = next(
        row for row in candidates if str(row[key_fields[-1]]) == selected_id
    )
    st.caption(f"Candidate {selected_index + 1} of {len(candidates)} in this view")

    if kind == "paper":
        st.subheader(record["title"])
        st.write(f"arXiv ID: {record['arxiv_id']}")
        st.markdown(f"[Open source paper]({record['source_url']})")
        st.caption(
            "Retrieved by: "
            + (record.get("retrieved_by") or "No retrieval strategy returned this paper")
        )
        with st.expander("Paper abstract", expanded=True):
            st.write(record["abstract"])
        passage_for_suggestion = None
    else:
        st.subheader(record["title"])
        st.write(f"arXiv ID: {record['arxiv_id']}")
        st.write(f"Page: {record.get('page_number') or 'Not available'}")
        st.write(f"Section: {record.get('section_title') or 'Not available'}")
        st.write(
            f"Source: {record.get('source_document', '')} "
            f"({record.get('source_identifier', '')})"
        )
        st.markdown(
            f"[Open source paper](https://arxiv.org/abs/{record['arxiv_id']})"
        )
        with st.expander("Paper abstract", expanded=True):
            st.write(record["abstract"])
        show_passage = st.checkbox(
            "Show and include retrieved passage",
            value=False,
            key=f"{kind}_show_passage_{query_id}_{selected_id}",
        )
        passage_for_suggestion = record.get("passage_text", "") if show_passage else None
        if show_passage:
            st.text_area(
                "Retrieved passage",
                value=record.get("passage_text", ""),
                height=240,
                disabled=True,
                key=f"{kind}_passage_{query_id}_{selected_id}",
            )

    st.markdown("#### Automated suggestion")
    automated_label = record.get("automated_label", "").strip()
    if automated_label:
        st.write(f"**Suggested judgment:** {automated_label}")
        st.write(f"**Confidence:** {float(record['automated_confidence']):.3f}")
        st.write(f"**Explanation:** {record.get('automated_explanation', '')}")
        st.caption(
            f"Model: {record.get('automated_model') or 'not recorded'} · "
            f"Generated: {record.get('automated_generated_at') or 'not recorded'}"
        )
        if row_history := record.get("automated_suggestion_history", "").strip():
            try:
                history = json.loads(row_history)
            except json.JSONDecodeError:
                st.warning("Suggestion history is malformed and was preserved.")
            else:
                with st.expander(f"Suggestion audit history ({len(history)} prior/current entries)"):
                    st.json(history)
    else:
        st.info("No automated suggestion exists for this candidate.")
    human_label = record.get("human_label") or record.get("relevance_judgment", "")
    if human_label:
        st.info(
            f"Saved human judgment: {human_label} · "
            f"Reviewer: {record.get('reviewer') or 'not recorded'} · "
            f"Method: {record.get('verification_method') or 'manual_legacy'}"
        )
        if human_label != automated_label and automated_label in {"relevant", "not_relevant"}:
            st.warning("This candidate disagrees with the automated suggestion.")
    st.caption(
        "Suggestion generation sends the displayed query and candidate text to "
        "the configured LLM endpoint. Default endpoint: local Ollama at "
        "http://localhost:11434."
    )
    if st.button(
        "Generate/update LLM suggestion",
        key=f"{kind}_suggest_{query_id}_{selected_id}",
    ):
        try:
            suggestion = suggest_relevance(
                record["query_text"],
                record["title"],
                record["abstract"],
                passage_for_suggestion,
            )
            backup = save_suggestion(
                path,
                required_fields,
                key_fields,
                {field: record[field] for field in key_fields},
                suggestion,
            )
        except (requests.RequestException, OSError, ValueError) as error:
            st.error(f"Could not generate or save suggestion: {error}")
        else:
            st.success(f"Suggestion saved. Backup: {backup.name}")
            st.rerun()

    label_key = f"{kind}_label_{query_id}_{selected_id}"
    grade_key = f"{kind}_grade_{query_id}_{selected_id}"
    reviewer_key = f"{kind}_reviewer_{query_id}_{selected_id}"
    notes_key = f"{kind}_notes_{query_id}_{selected_id}"
    attestation_key = f"{kind}_attest_{query_id}_{selected_id}"
    label_default = record.get("human_label") or record.get("relevance_judgment", "")
    if label_default not in ("", "relevant", "not_relevant"):
        label_default = ""
    grade_default = record.get("grade_0_to_3", "")
    if grade_default not in ("", "0", "1", "2", "3"):
        grade_default = ""

    with st.form(f"{kind}_judgment_form_{query_id}_{selected_id}"):
        judgment = st.radio(
            "Relevance judgment",
            ("", "relevant", "not_relevant"),
            index=("", "relevant", "not_relevant").index(label_default),
            key=label_key,
            horizontal=True,
            format_func=lambda value: value or "Not reviewed",
        )
        grade = st.selectbox(
            "Optional relevance grade (0 = not relevant, 3 = highly relevant)",
            ("", "0", "1", "2", "3"),
            index=("", "0", "1", "2", "3").index(grade_default),
            key=grade_key,
            format_func=lambda value: value or "No grade",
        )
        reviewer = st.text_input(
            "Reviewer name",
            value=record.get("reviewer") or st.session_state.get("reviewer_name", ""),
            key=reviewer_key,
        )
        notes = st.text_area(
            "Review notes",
            value=record.get("review_notes", ""),
            key=notes_key,
        )
        attested = st.checkbox(
            "I explicitly attest that this review was independent",
            value=record.get("independent_review_attested", "").strip().lower()
            == "yes",
            key=attestation_key,
        )
        submitted = st.form_submit_button("Save judgment")

    if submitted:
        if not judgment:
            st.error("Choose relevant or not_relevant before saving.")
        else:
            try:
                backup = save_judgment(
                    path,
                    required_fields,
                    key_fields,
                    {field: record[field] for field in key_fields},
                    judgment,
                    grade,
                    reviewer,
                    notes,
                    attested,
                )
            except (OSError, ValueError) as error:
                st.error(f"Could not save judgment: {error}")
            else:
                st.session_state["reviewer_name"] = reviewer.strip()
                st.success(f"Judgment saved. Backup: {backup.name}")
                st.rerun()


def main() -> None:
    st.set_page_config(
        page_title="Phase 4.3 Relevance Annotation",
        page_icon="📝",
        layout="wide",
    )
    st.title("Phase 4.3 Human Relevance Annotation")
    st.warning(
        "Judgments are manual. Retrieval ranks and similarity scores are context "
        "only; they never assign relevance."
    )
    try:
        import json

        query_path = Path(__file__).with_name("benchmark_queries.json")
        with query_path.open("r", encoding="utf-8") as source:
            queries = json.load(source)["queries"]
        query_text_by_id = {
            query["query_id"]: query["query_text"] for query in queries
        }
        tabs = st.tabs(["Paper judgments", "Chunk judgments"])
        with tabs[0]:
            _render_worksheet(
                "paper",
                PAPER_WORKSHEET,
                PAPER_FIELDS,
                ("query_id", "benchmark_paper_id"),
                query_text_by_id,
            )
        with tabs[1]:
            _render_worksheet(
                "chunk",
                CHUNK_WORKSHEET,
                CHUNK_FIELDS,
                ("query_id", "chunk_id"),
                query_text_by_id,
            )
        st.divider()
        if st.button("Generate separate exploratory automated-label report"):
            from KnowledgeGraphAI.backend.services.semantic_retrieval.annotation_evaluation import (
                build_automated_exploratory_report,
                write_automated_exploratory_report,
            )

            try:
                benchmark_results = json.loads(
                    RESULTS_PATH.read_text(encoding="utf-8")
                )
                report = build_automated_exploratory_report(
                    PAPER_WORKSHEET,
                    CHUNK_WORKSHEET,
                    benchmark_results,
                )
                report_path = write_automated_exploratory_report(report)
            except (OSError, ValueError, KeyError) as error:
                st.error(f"Could not create exploratory report: {error}")
            else:
                st.warning(
                    "This report uses automated suggestions only and is not a "
                    "human-verified benchmark result."
                )
                st.success(f"Exploratory report saved to {report_path}")
    except (OSError, ValueError, KeyError) as error:
        st.error(f"Unable to load annotation data: {error}")


if __name__ == "__main__":
    main()
