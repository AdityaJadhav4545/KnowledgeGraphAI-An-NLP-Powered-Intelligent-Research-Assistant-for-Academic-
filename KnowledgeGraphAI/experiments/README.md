# Experiments

Experiments are baseline-first and reproducible. Configurations live in `configs/`; measured outcomes belong in `results/` and must identify the data and seed used. `experiment_runner.py` can record a `not_run` state, but it deliberately cannot manufacture metrics.

The current Phase 4.3 report contains latency and diversity comparisons. Relevance metrics remain pending until human labels are completed; automated suggestions are not ground truth.
