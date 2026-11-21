# KnowledgeGraphAI UI Audit

Audit date: 2026-11-07

This audit was completed before the UI repair work. It records current
workspace behavior, not a claim that every route or external dependency is
available at runtime.

## Page-by-page findings

| Page | Status | Existing integration and observed gaps |
|---|---|---|
| Dashboard (`frontend/pages/dashboard.py`) | Partially functional | Reads the paper list and `/health` and derives paper/page/status counts. The API helper turns errors into `None`, which is rendered like empty data. It does not show graph counts, semantic index status, Ollama status, or distinguish unavailable services from zero counts. |
| Upload (`frontend/pages/upload.py`) | Partially functional | Calls the upload endpoint, handles common HTTP statuses, and offers a complete-pipeline action with a spinner. Upload progress is not reported; processing is synchronous; no detailed stage/result view or retry state beyond the last-upload button. |
| Paper library (`frontend/pages/library.py`) | Partially functional | Lists papers, fetches details and extracted text, and invokes processing/archive endpoints. No title/author search or status filter; no archive confirmation; failures can be shown as an empty library. |
| Graph explorer (`frontend/pages/graph.py`) | Partially functional / blocked by infrastructure | Calls graph health, entity/paper search, and paper graph endpoints and renders a basic graph. Neo4j is unavailable in the audit environment. No type/relationship filtering in the graph rendering, no entity detail/neighbor workflow, and graph API errors can be reduced to generic messages. |
| Legacy graph page (`frontend/pages/knowledge_graph.py`) | Non-functional | Not selected by app navigation. Contains placeholder copy and a blank export download; it is disconnected from the actual graph APIs. |
| Semantic search (`frontend/pages/search.py`) | Partially functional / blocked by empty production index | Submits real queries to `/api/semantic-search`, displays returned passages/scores/provenance, and links source PDFs. The production index is empty. Source PDF access requires authentication in production, but a normal Streamlit link cannot attach the API key. |
| Research assistant (`frontend/pages/assistant.py`) | Partially functional / blocked by empty production index | Calls `/api/assistant/ask`, preserves session history, and displays citations, evidence, graph context, and generation mode. It displays request errors but has no retry action or query clear/feedback persistence. End-to-end generation is unverified. |
| Evaluation (`frontend/pages/eval.py`) | Partially functional | Reads `/api/evaluation/benchmark` and avoids presenting unavailable human metrics as scores. Does not expose annotation counts, independent-review status, judgments, or candidate counts in a useful summary. |
| Experiments (`frontend/pages/experiments.py`) | Partially functional | Reads configurations and saved results from `/api/experiments`; correctly shows no-run state. No configuration selection/editing or execution/comparison actions exist in the API. |
| NER (`frontend/pages/ner.py`) | Non-functional / misleading | Uses fabricated sample entities and a simulated success path instead of calling the NER API. It expects session state that is not populated by the app. Model/threshold controls are not applied. |
| Settings (`frontend/pages/settings.py`) | Partially functional | Displays health/readiness and API base URL. Credential text is instructional placeholder content, not live settings. No secret values are fetched from the backend. |

## Navigation and shared frontend behavior

- `frontend/app.py` provides a single sidebar radio navigation and dynamically
  executes the selected page source.
- The frontend centralizes its base URL and request wrappers in `app.py`, but
  wrappers broadly catch errors and return `None` or `(None, ...)`. Several
  pages treat request failure as an empty result.
- The API key is injected by the Streamlit server from environment variables;
  it is not supplied by browser code. Direct source links cannot attach that
  header.
- `frontend/components/` has no shared UI/API components.
- The separate legacy `knowledge_graph.py` and demo `ner.py` are not coherent
  with navigation and must not be presented as working workflows.

## Backend endpoint map reviewed

| UI workflow | Backend endpoints | Audit result |
|---|---|---|
| Dashboard | `GET /api/papers`, `GET /health`, `GET /ready`, `GET /api/graph/stats`, `GET /api/semantic-search/status`, Ollama local tags | Most information endpoints exist, but dashboard initially consumed only a subset. |
| Upload/process/library | `POST /api/papers/upload`, `POST /api/papers/{id}/process`, `GET /api/papers`, `GET /api/papers/{id}`, `DELETE /api/papers/{id}` | Real upload and integrated processing exist. Archive is non-destructive. |
| NER | `POST /api/nlp/ner/extract/{id}`, `GET /api/nlp/ner/entities/{id}`, `GET /api/nlp/ner/model-info` | Endpoint exists; NER page was using mock data instead. |
| Graph | `/api/graph/health`, `/stats`, `/search`, `/paper/{id}`, `/entity/{id}`, `/entity/{id}/neighbors` | Relevant routes exist; live graph checks are blocked if Neo4j is offline. |
| Semantic search | `GET /api/semantic-search/status`, `GET|POST /api/semantic-search` | Real API exists; production index currently has no indexed chunks. |
| GraphRAG | `GET /api/assistant/status`, `POST /api/assistant/ask` | Service and API exist. Requires semantic evidence; Neo4j is supplemental context. |
| Evaluation | `GET /api/evaluation/benchmark` | Read-only summary exists; source artifact is the retained benchmark report. |
| Experiments | `GET /api/experiments` | Read-only registry only; no experiment execution endpoint exists. |

## Runtime and data observations

- FastAPI, Streamlit, Neo4j Browser/Bolt were not listening on their usual
  localhost ports at audit time. Ollama was reachable.
- Neo4j was not reachable on port 7687. Do not initialize, reset, or recreate
  its container or volume as part of UI work.
- The application SQLite database had 12 papers, all in `uploaded` status,
  and zero production semantic chunks. The production FAISS index was absent.
- The isolated benchmark index and metadata database contained 428 consistent
  vectors; benchmark assets and judgments are out of scope for modifications.
- No button or workflow may claim successful graph/retrieval operations when
  the backing service/index is unavailable.

## Audit priorities

1. Replace demo NER data with the real NER endpoint.
2. Make shared API failures visible and distinguish unavailable data from an
   empty collection.
3. Use real health/index/graph/Ollama signals on the dashboard.
4. Add paper search/status filtering, safe confirmation, and actual artifact
   details to the library/processing view.
5. Improve graph entity and relationship exploration without substituting
   sample data when Neo4j is unavailable.
6. Display annotation progress and evidence-backed evaluation status.
7. Keep experiments read-only unless an implemented safe run API exists.
8. Test the actual Streamlit browser pages and document infrastructure blocks.
