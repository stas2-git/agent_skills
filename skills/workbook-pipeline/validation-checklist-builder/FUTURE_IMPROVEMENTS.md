# Future Improvements

## Near-term improvements

- Add stronger mapping from request type to exact OCR labels or formulas to check.
- Add severity levels beyond `must_pass` and `informational`, such as `warning`.
- Add support for checklist templates keyed by workbook role, such as pricing or diagnostics-heavy workbooks.

## Accuracy and automation

- Attach concrete sheet names and labels from the semantic brief instead of generic workbook surfaces.
- Emit checks that can be consumed directly by screen-interaction or workbook-inspection scripts without extra translation.
- Detect duplicate or redundant checks and merge them automatically.

## Pipeline integration

- Accept a batch of change plans and emit one checklist per workbook.
- Feed checklist output directly into a future validation runner.
- Add a mode that compares executed results back against the checklist schema.
- Default checklist outputs into workbook-local `llm_work/checklists/` folders.
- Add explicit run linkage so each checklist knows which plan and run folder it came from.
