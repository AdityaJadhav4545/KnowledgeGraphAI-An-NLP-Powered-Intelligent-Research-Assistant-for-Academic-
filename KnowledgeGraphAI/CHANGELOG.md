# Changelog

## 2026-11-07 — UI navigation and verification

- Added the API-backed Scientific NER view to the main application navigation and hid Streamlit's automatic page list so the disconnected legacy graph placeholder is not promoted as a supported workflow.
- Smoke-tested the dashboard, NER empty state, and settings page in a browser against a temporary isolated backend database.
- Recorded test results, service status, and integration limitations in `reports/UI_TEST_REPORT.md` and `reports/UI_INTEGRATION_REPORT.md`.

## 2026-11-07 — Integrated pipeline and product completion pass

- Added centralized settings, `.env` loading without overrides, production validation, safe CORS, API-key write protection, and readiness reporting.
- Added additive SQLite Paper processing fields with verified pre-migration backups.
- Repaired PDF preprocessing page totals/section assignment and the paragraph segmenter import.
- Replaced the empty-default relation extractor path with the documented rule-based baseline.
- Added `PaperProcessingService` to execute and persist the PDF-to-graph-to-FAISS workflow.
- Repaired canonical Neo4j paper identity usage and removed import-time Neo4j connection side effects.
- Mounted semantic search, GraphRAG assistant, evaluation, experiment, NLP, and NER API routes.
- Replaced placeholder Streamlit search, assistant, graph, evaluation, and experiment pages.
- Added dependency manifests, environment template, README, project status, and experiment scaffolding.
- Changed paper deletion to non-destructive archive behavior to preserve research PDFs and data.
