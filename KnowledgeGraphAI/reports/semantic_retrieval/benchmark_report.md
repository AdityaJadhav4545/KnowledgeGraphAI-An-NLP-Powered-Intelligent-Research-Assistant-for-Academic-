# Phase 4.3 Scientific Semantic Retrieval Benchmark

Status: **provisional_pending_human_review**

The benchmark remains provisional because human annotations are incomplete.

## Corpus and model

- Publications in manifest: 12
- Successfully indexed: 12
- Failed: 0
- Chunks/embeddings: 428
- Embedding dimension: 768
- Model/adapters: `allenai/specter2_base` / `allenai/specter2` / `allenai/specter2_adhoc_query`
- Device: cpu
- Benchmark index bytes: 1318330

## Retrieval strategy comparison

| Strategy | Mean / median end-to-end query latency (s) | Mean distinct papers / 10 | Mean duplicate chunks / 10 | Relevance metrics available |
|---|---:|---:|---:|---|
| faiss_cosine | 0.1012 / 0.0921 | 1.08 | 0.00 | False |
| metadata_filtered_cosine | 0.0882 / 0.0880 | 1.08 | 0.00 | False |
| paper_aggregation | 0.1119 / 0.1118 | 10.00 | 0.00 | False |
| mmr_diversity | 0.1082 / 0.1092 | 2.58 | 0.00 | False |

Unjudged documents are excluded from metric rankings, not treated as irrelevant. Chunk-level metrics are conditional on the judged candidate pool; recall/MAP denominators include only explicitly labeled relevant IDs.

### Human-judged macro metrics

| Strategy | Unit | K | P@K | Recall@K | MRR | MAP@K | nDCG@K | P@K eligible queries |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| faiss_cosine | chunk | 1 | n/a | n/a | n/a | n/a | n/a | 0 |
| faiss_cosine | chunk | 3 | n/a | n/a | n/a | n/a | n/a | 0 |
| faiss_cosine | chunk | 5 | n/a | n/a | n/a | n/a | n/a | 0 |
| faiss_cosine | chunk | 10 | n/a | n/a | n/a | n/a | n/a | 0 |
| faiss_cosine | paper | 1 | n/a | n/a | n/a | n/a | n/a | 0 |
| faiss_cosine | paper | 3 | n/a | n/a | n/a | n/a | n/a | 0 |
| faiss_cosine | paper | 5 | n/a | n/a | n/a | n/a | n/a | 0 |
| faiss_cosine | paper | 10 | n/a | n/a | n/a | n/a | n/a | 0 |
| metadata_filtered_cosine | chunk | 1 | n/a | n/a | n/a | n/a | n/a | 0 |
| metadata_filtered_cosine | chunk | 3 | n/a | n/a | n/a | n/a | n/a | 0 |
| metadata_filtered_cosine | chunk | 5 | n/a | n/a | n/a | n/a | n/a | 0 |
| metadata_filtered_cosine | chunk | 10 | n/a | n/a | n/a | n/a | n/a | 0 |
| metadata_filtered_cosine | paper | 1 | n/a | n/a | n/a | n/a | n/a | 0 |
| metadata_filtered_cosine | paper | 3 | n/a | n/a | n/a | n/a | n/a | 0 |
| metadata_filtered_cosine | paper | 5 | n/a | n/a | n/a | n/a | n/a | 0 |
| metadata_filtered_cosine | paper | 10 | n/a | n/a | n/a | n/a | n/a | 0 |
| paper_aggregation | chunk | 1 | n/a | n/a | n/a | n/a | n/a | 0 |
| paper_aggregation | chunk | 3 | n/a | n/a | n/a | n/a | n/a | 0 |
| paper_aggregation | chunk | 5 | n/a | n/a | n/a | n/a | n/a | 0 |
| paper_aggregation | chunk | 10 | n/a | n/a | n/a | n/a | n/a | 0 |
| paper_aggregation | paper | 1 | n/a | n/a | n/a | n/a | n/a | 0 |
| paper_aggregation | paper | 3 | n/a | n/a | n/a | n/a | n/a | 0 |
| paper_aggregation | paper | 5 | n/a | n/a | n/a | n/a | n/a | 0 |
| paper_aggregation | paper | 10 | n/a | n/a | n/a | n/a | n/a | 0 |
| mmr_diversity | chunk | 1 | n/a | n/a | n/a | n/a | n/a | 0 |
| mmr_diversity | chunk | 3 | n/a | n/a | n/a | n/a | n/a | 0 |
| mmr_diversity | chunk | 5 | n/a | n/a | n/a | n/a | n/a | 0 |
| mmr_diversity | chunk | 10 | n/a | n/a | n/a | n/a | n/a | 0 |
| mmr_diversity | paper | 1 | n/a | n/a | n/a | n/a | n/a | 0 |
| mmr_diversity | paper | 3 | n/a | n/a | n/a | n/a | n/a | 0 |
| mmr_diversity | paper | 5 | n/a | n/a | n/a | n/a | n/a | 0 |
| mmr_diversity | paper | 10 | n/a | n/a | n/a | n/a | n/a | 0 |


## Runtime

- Recorded PDF processing + embedding time: 157.03 seconds across indexed papers
- Index command time in this run: 0.00 seconds
- Mean document embedding seconds/batch: None
- Document embedding timing note: Not separately recorded because this run reused indexed vectors; recorded per-paper times include PDF extraction and embedding.
- Query embedding seconds/call (mean / median): 0.07796201666739459 / 0.07636135001666844
- FAISS search seconds/call (mean / median): 0.008169800006726291 / 0.008307100040838122
- Process memory before/after: {'working_set_bytes': 322707456, 'peak_working_set_bytes': 322707456} / {'working_set_bytes': 863387648, 'peak_working_set_bytes': 863469568}

## Relevance evaluation

- Annotation status: pending_human_review
- Human-verified queries: 0
- Queries without judged relevant documents: 0
- Macro metrics report eligible-query denominators per measure; undefined recall/MRR/MAP values for queries with no judged relevant items are omitted.

## Neo4j traceability

- Sampled retrieved papers found in Neo4j: 12
- Not found: 0
- Ambiguous title matches: 0
- Benchmark indexing uses benchmark-local numeric IDs; canonical Neo4j IDs are recorded only when an exact title match exists.

## Limitations

- The arXiv corpus is a curated pilot, not a representative scientific IR benchmark.
- Relevance labels require independent human inspection; pending papers are unjudged, not irrelevant.
- The ranking comparison's metadata filter uses each query's predeclared target-area tags; this is a controlled filter condition, not an automatic intent classifier.
- Full-text PDFs remain local and are excluded from Git.

## Reproduction

See the PowerShell commands in README.md; model download and benchmark indexing are explicit commands and do not run during ordinary pytest.
