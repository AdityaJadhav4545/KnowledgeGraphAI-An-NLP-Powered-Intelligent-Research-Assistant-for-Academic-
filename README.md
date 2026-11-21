# KnowledgeGraph AI

KnowledgeGraph AI is an NLP-powered intelligent research assistant that automatically extracts knowledge from academic research papers and constructs knowledge graphs.

## Prerequisites

- Python 3.10+
- Neo4j (Optional, for graph features)

## Setup

1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Neo4j by copying `KnowledgeGraphAI/.env.example` to
   `KnowledgeGraphAI/.env` and setting `NEO4J_PASSWORD`. The application loads
   this file before initializing backend services. Values already supplied by
   the deployment environment take precedence. `.env` is ignored by Git.

## Running the Application

### Backend

```bash
uvicorn KnowledgeGraphAI.backend.main:app --reload
```

### Frontend

```bash
streamlit run KnowledgeGraphAI/frontend/app.py
```

## Semantic Retrieval

The semantic retrieval service chunks preprocessed scientific-paper text,
encodes passages with SPECTER2's proximity adapter and queries with its
adhoc-query adapter, then searches normalized vectors with FAISS. Chunk
metadata and vector payloads are persisted in the configured SQLAlchemy
database so the FAISS index can be rebuilt after it is lost. Set
`FAISS_INDEX_DIR` to move the generated index; vector-store files are excluded
from Git. The model and adapters are downloaded lazily on the first embedding
request.

`SemanticRetrievalService.index_pdf(path, paper_id)` requires a matching
`Paper.paper_id` in Neo4j. `search(query, top_k=5)` returns ranked chunks with
paper, page, section, and character-offset metadata. Optional `paper_id`,
`page_number`, `section_title`, and `min_similarity` arguments filter results;
`aggregate_by_paper=True` returns the best chunk per paper and its matched
chunk count. `diversity=True` enables MMR ordering with `reranking_score`,
while the original FAISS cosine remains in `similarity_score`. Configure the
model, chunking, device, and index settings with the `SPECTER2_*`, `SEMANTIC_*`,
and `FAISS_*` variables in `.env.example`.

The regular semantic-retrieval tests use a small injected embedding model and
real FAISS/SQLite storage. To run the real Neo4j/PDF/FAISS integration test,
set `RUN_SEMANTIC_NEO4J_INTEGRATION=1` before pytest; it creates and removes a
uniquely identified temporary `Paper` node. To download and smoke-test actual
SPECTER2 weights and perform a FAISS retrieval run on the synthetic fixture:

```powershell
$env:RUN_SPECTER2_MODEL_TESTS = "1"
py -3.10 -m pytest KnowledgeGraphAI/tests/test_semantic_retrieval.py -m real_model -s
```

Or run the report-producing validator directly:

```powershell
py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.validation
```

Both commands explicitly opt into model downloads. The bundled evaluation
fixture is synthetic and its metrics are software checks, not human relevance
judgments or a benchmark claim.

### Phase 4.3 Real-Paper Benchmark

The pilot benchmark uses a separate SQLite database and FAISS index under
`KnowledgeGraphAI/data/benchmark/`; PDFs, SQLite files, FAISS files, and partial
downloads are excluded from Git. Preparation downloads the selected arXiv PDFs
only when explicitly invoked. Indexing uses the real SPECTER2 model and does
not create or mutate Neo4j graph records. Neo4j traceability, when enabled, is
read-only.

Run these commands from the repository root in PowerShell:

```powershell
py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_runner prepare
py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_runner index --no-trace-neo4j
py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_runner benchmark --no-download
py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_graph_ingest
py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_annotation_workflow prepare
```

The generated manifest records arXiv metadata, source/license links, and local
PDF hashes. Review `KnowledgeGraphAI/data/benchmark/benchmark_annotations.json`
independently: explicitly list every reviewed paper in `judged_paper_ids`,
record unreviewed papers in `unjudged_paper_ids`, and only set
`judgment_status` to `human_verified` after review. Paper-level evaluation
requires every corpus paper to be judged. Chunk-level metrics are limited to
the explicitly judged candidate pool; unjudged results are excluded rather
than considered non-relevant. Results and the error-analysis report are written
under `KnowledgeGraphAI/reports/semantic_retrieval/`. The report remains
provisional until all papers are indexed and all query/paper judgments are
human-verified.

The annotation `prepare` command creates a paper-level CSV (every query ×
corpus paper), a chunk-level CSV (unique passages retrieved by any evaluated
strategy), and a Markdown review report. Empty judgments are intentional. Do
not edit retrieval source fields or infer labels from scores. Once every row
has an explicit judgment and reviewer provenance, import them with:

```powershell
py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_annotation_workflow import
py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_runner benchmark --no-download
```

#### Interactive annotation dashboard

Launch the local Streamlit reviewer from the repository root:

```powershell
py -3.10 -m streamlit run KnowledgeGraphAI\backend\services\semantic_retrieval\annotation_dashboard.py
```

The dashboard has separate paper- and chunk-level tabs, query/candidate
navigation, unreviewed filtering, and per-query progress. It saves each
submitted judgment to the existing worksheet after creating a timestamped
backup. Labels and optional grades follow the annotation importer's validation
rules. Reviewer name is required; the independent-review attestation remains
unchecked unless explicitly selected. Saving a judgment never assigns labels
to other rows, and retrieval scores are shown only as context.

Assisted suggestions are opt-in per candidate and use an Ollama-compatible
chat endpoint. By default, requests go to a local Ollama server at
`http://localhost:11434` using model `llama3.1`; set
`ANNOTATION_LLM_BASE_URL` and `ANNOTATION_LLM_MODEL` to configure another
endpoint/model. Review the endpoint's privacy policy before using a remote
service because query and paper text are sent to it. Model confidence is an
uncalibrated suggestion, not a relevance metric. The dashboard stores model
labels separately from human labels; uncertain suggestions are excluded from
exploratory metrics. Bulk acceptance requires reviewer identity and an
explicit confirmation, records `verification_method=bulk_confirmed`, and does
not claim independent review.

For the default local provider, start Ollama and make the configured model
available before clicking **Generate/update LLM suggestion**:

```powershell
ollama serve
ollama pull llama3.1
```

No model download or LLM request occurs when the dashboard starts.

To create a separate exploratory report from automated suggestions, use the
dashboard's report button. It writes
`KnowledgeGraphAI/reports/semantic_retrieval/automated_annotation_exploratory_report.json`.
This pseudo-labeled report is separate from the benchmark runner's human-only
metrics and must not be reported as human-verified effectiveness.

#### Resumable batch annotation and reporting

The batch command evaluates paper and chunk candidates independently from the
12-query dataset. It checkpoints each response under
`KnowledgeGraphAI/data/benchmark/automated_annotation_checkpoint.json`, skips
existing suggestions by default, records suggestion history, and backs up each
worksheet before batched CSV writes. It never writes an automated label into a
human-label field.

Validate a small sample first (at most one new paper suggestion and one new
chunk suggestion; previously suggested candidates are skipped):

```powershell
py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_batch_annotation --type both --limit 1 --batch-size 1 --rate-limit-seconds 0.25
```

After inspecting the sample outputs, run the remaining candidates. Re-running
the command resumes from the checkpoint and skips existing suggestions:

```powershell
py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.benchmark_batch_annotation --type both --batch-size 8 --rate-limit-seconds 0.25 --timeout-seconds 180 --max-retries 2
```

Add `--force` only to deliberately regenerate existing suggestions; the prior
suggestions remain in the row's audit history and in the timestamped CSV
backups. To process a single query or candidate, pass `--query-id` and
`--candidate-id`. Each result records annotation type, query/candidate IDs,
model, generation time, label, confidence, and explanation.

Generate a versioned report (JSON, Markdown, and a local Plotly visualization)
without re-embedding or altering Neo4j:

```powershell
py -3.10 -m KnowledgeGraphAI.backend.services.semantic_retrieval.phase43_reporting
```

The report keeps human benchmark metrics, exploratory pseudo-label metrics,
and LLM/human agreement separate. Agreement metrics exclude uncertain
suggestions; Cohen's kappa is withheld unless there are overlapping
independent human raters. Human retrieval metrics remain pending until the
annotation manifest and benchmark results are validated as complete.

The live Ollama integration test is opt-in; ordinary pytest uses mocked
responses:

```powershell
$env:RUN_OLLAMA_ANNOTATION_TESTS = "1"
py -3.10 -m pytest KnowledgeGraphAI/tests/test_ollama_annotation_integration.py -q
Remove-Item Env:RUN_OLLAMA_ANNOTATION_TESTS
```

The graph ingestion command uses the application’s canonical SQLite
`Paper.id`, existing PDF/preprocessing/NER/relation extraction services, and
`GraphConstructionService`. It checks Neo4j identity conflicts and records
benchmark-local/arXiv references; it does not reset or delete graph data.

Run the isolated unit coverage without downloading PDFs or model weights:

```powershell
py -3.10 -m pytest KnowledgeGraphAI/tests/test_semantic_benchmark.py -q
```
