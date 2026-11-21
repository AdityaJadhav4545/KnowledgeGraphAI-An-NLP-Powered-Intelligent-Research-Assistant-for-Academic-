# UI and Regression Test Report

Date: 2026-11-07

## Scope and data safety

The FastAPI and Streamlit processes used for this smoke test were launched with a temporary SQLite database and temporary upload, processed-file, and FAISS paths. No PDFs were uploaded or processed. Neo4j was not initialized or modified. Benchmark judgments, PDFs, indexes, and metadata were not used as write targets.

## Results

| Check | Result | Evidence / limitation |
|---|---|---|
| Python syntax | PASS | `ast.parse` succeeded for 113 Python source files. |
| Dependency consistency | PASS | `py -3.10 -m pip check` reported no broken requirements. |
| New frontend client and annotation tests | PASS | 4 tests passed. |
| Isolated project regression suite | PARTIAL | 155 passed, 1 failed, 3 skipped. The Neo4j integration module was excluded because Neo4j was unavailable. |
| Graph schema mapping assertion | FAIL | `test_graph_schema.py::TestGraphSchema::test_valid_relationships_mapping` expects `"Model"` for `PROPOSES.from`; the current schema returns a list of allowed source labels. Contract resolution remains open. |
| API smoke checks | PASS / DEGRADED | `/health`, `/ready`, semantic-search status, graph health, and assistant status responded with HTTP 200. Neo4j was reported unavailable; semantic index contained 0 chunks; Ollama and configured model `llama3.1` were available. |
| Browser dashboard | PASS | Rendered live status against the isolated empty database, including zero papers/chunks and unavailable Neo4j. |
| Browser Scientific NER | PASS | Main navigation opened the page; with no papers, the UI displayed “Upload a paper before requesting entity extraction.” No fabricated results were shown. |
| Browser settings | PASS | Rendered isolated API/database, Neo4j, embedding, Ollama, and configuration status without exposing secrets. |
| Full interaction workflows | NOT RUN | No upload/process/search/generation/graph mutation was attempted. The production library and index were intentionally not used. |

## Notes

- Launching Streamlit from inside the package caused the expected absolute-package import to fail. Relaunching from the documented parent directory resolved it.
- The app's custom navigation now includes Scientific NER and hides Streamlit's automatically discovered `pages/` list, which otherwise exposed a disconnected legacy graph placeholder alongside the supported application navigation.
- No screenshots were captured.
