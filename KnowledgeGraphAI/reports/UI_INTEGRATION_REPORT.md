# UI Integration Report

Date: 2026-11-07

## Integration status

The Streamlit UI uses the shared `APIClient` for backend requests and the main application navigation runs the selected API-backed page. The API was launched with temporary storage for this smoke test; the displayed empty paper and production-index counts are from that isolated database, not the existing research library.

| Area | Status | Observed integration |
|---|---|---|
| Dashboard | PARTIALLY COMPLETE | Reads papers, API health, semantic-index status, graph health/counts when available, and assistant/Ollama status. Correctly showed a zero-paper temporary library and marked Neo4j unavailable rather than showing graph counts. |
| Upload and paper library | PARTIALLY COMPLETE | Use backend upload, process, list/detail, source-download, and archive endpoints. No upload or processing was attempted in the smoke test. |
| Scientific NER | PARTIALLY COMPLETE | Calls the NER API for a selected paper and displays backend entities/evidence; browser-confirmed empty-library guard prevents fabricated examples. |
| Knowledge graph | PARTIALLY COMPLETE / BLOCKED | Connected to graph search, paper/entity detail, neighbors, and graph rendering; Neo4j was unavailable, so live graph retrieval is unverified. |
| Semantic search | PARTIALLY COMPLETE / BLOCKED | Calls semantic-search API and renders provenance/results; isolated index has 0 chunks, so retrieval results cannot be validated. |
| Research assistant | PARTIALLY COMPLETE / BLOCKED | Calls GraphRAG API and displays citations/evidence/status. Ollama/model were reachable, but zero indexed chunks prevented end-to-end grounded generation validation. |
| Evaluation | PARTIALLY COMPLETE | Reads benchmark status and label counts. The benchmark remains provisional pending human and independent review. |
| Experiments | PARTIALLY COMPLETE | Reads registered configurations and recorded results; no measured experiment was launched. |
| Settings | PARTIALLY COMPLETE | Displays service readiness and non-secret settings; browser smoke test passed against the isolated backend. |

## Runtime observations

- FastAPI `/health` and `/ready` returned HTTP 200 in the test configuration.
- Neo4j was unavailable, and no graph operations were performed.
- Semantic retrieval reported 0 indexed chunks in the isolated production index.
- Ollama and the configured `llama3.1` model were available; this does not establish successful retrieval-grounded generation.
- The isolated database contained no papers.

## Remaining verification

1. Run UI journeys with a non-benchmark test PDF and isolated test services.
2. Verify graph search and GraphRAG after connecting the existing Neo4j instance and creating a separate production FAISS index.
3. Exercise upload, processing, retry, search, citation display, and archive confirmation in the browser.
4. Verify benchmark annotations and only publish human retrieval metrics after independent labels are complete.
