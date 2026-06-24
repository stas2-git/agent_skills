# Future Improvements

## Near-term improvements

- Add task-aware summarization so the brief can emphasize pricing, diagnostics, or data-generation areas depending on the request.
- Improve role classification using formulas and defined names, not only sheet names and sample labels.
- Add a shorter "prompt pack" mode optimized for direct LLM context windows.

## Accuracy and coverage

- Extract clearer VBA procedure metadata, including private helper procedures and function names.
- Summarize formula patterns, not just labels and cell counts.
- Detect named tables, charts, and pivot tables from decomposition artifacts when present.

## Pipeline integration

- Accept a workbook manifest and generate one brief per workbook in a batch.
- Feed summary output directly into `change-planner` without extra glue code.
- Add an option to compare two briefs and highlight semantic drift over time.
- Default summary outputs into workbook-local `llm_work/summaries/` folders.
- Add freshness checks so the skill can decide whether to reuse a prior run's summary or generate a new one automatically.
