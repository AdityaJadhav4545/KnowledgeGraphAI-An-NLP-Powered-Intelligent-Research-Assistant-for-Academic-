# KnowledgeGraphAI

KnowledgeGraphAI is an AI-powered Knowledge Graph Research Assistant for scientific PDFs and pasted research text.

## Core User Workflow

1. **Analyze Document** — Upload a research PDF or paste a paragraph/article and click **Generate Analysis**.
2. **Explore Knowledge** — Inspect the interactive, color-coded knowledge graph (zoom, pan, filter by category, focus on entity neighborhoods, inspect connected relationships) and chat with a document-scoped AI Research Assistant backed by source citations.
3. **Generate Report** — View the structured 11-section academic report (with embedded graph diagram and traceability table) and click **Download PDF Report**.

## Architecture

```text
Streamlit (3-section UI) ──HTTP──> FastAPI
                                     ├─ DocumentAnalysisService: unified PDF & pasted-text workflow
                                     ├─ Scientific NLP: PyMuPDF, cleaning, segmentation, rule NER, relation extraction
                                     ├─ Knowledge Graph: isolated per-analysis graph + optional Neo4j persistence
                                     ├─ Retrieval & AI Assistant: scoped passages + SPECTER2/FAISS + Ollama (llama3.1)
                                     └─ ReportGenerationService: NetworkX/Matplotlib graph + ReportLab academic PDF
```

- Pasted-text analyses are isolated per analysis and work without requiring Neo4j or FAISS.
- Existing paper library, Neo4j graph, production FAISS index, and benchmark datasets remain preserved in their respective directories.

## Running Locally (Python 3.10.11)

From the parent directory containing `KnowledgeGraphAI`:

```powershell
# Optional: start Neo4j if graph persistence across papers is desired
docker start knowledgegraphai-neo4j

# Start FastAPI backend
$env:PYTHONPATH = (Get-Location).Path
& "C:\Users\tanaj\AppData\Local\Programs\Python\Python310\python.exe" -m uvicorn KnowledgeGraphAI.backend.main:app --host 127.0.0.1 --port 8000

# Start Streamlit assistant (in a separate terminal)
$env:PYTHONPATH = (Get-Location).Path
& "C:\Users\tanaj\AppData\Local\Programs\Python\Python310\python.exe" -m streamlit run KnowledgeGraphAI/frontend/app.py --server.port 8501
```

## Key API Endpoints

- `POST /api/analyses/pdf` — upload and analyze a PDF document.
- `POST /api/analyses/text` — analyze pasted research text.
- `GET /api/analyses` & `GET /api/analyses/{analysis_id}` — list and inspect isolated analyses.
- `POST /api/analyses/{analysis_id}/ask` — ask a document-scoped question to the AI Research Assistant.
- `GET /api/analyses/{analysis_id}/report` & `GET /api/analyses/{analysis_id}/report/pdf` — retrieve the 11-section report and download the generated PDF.
- `GET /health`, `GET /ready` — service liveness and readiness.

## Testing

Run the isolated regression suite from the parent directory:

```powershell
$env:PYTHONPATH = (Get-Location).Path
$tmp = Join-Path $env:TEMP "kgai_test_run"
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
$env:DATABASE_URL = "sqlite:///" + ($tmp -replace '\\','/') + "/test.db"
$env:UPLOAD_DIR = Join-Path $tmp "raw"
$env:PROCESSED_DIR = Join-Path $tmp "processed"
$env:FAISS_INDEX_DIR = Join-Path $tmp "vector_store"
$env:REQUIRE_NEO4J = "false"
& "C:\Users\tanaj\AppData\Local\Programs\Python\Python310\python.exe" -m pytest KnowledgeGraphAI/tests --ignore=KnowledgeGraphAI/tests/test_neo4j_integration.py -v
```
