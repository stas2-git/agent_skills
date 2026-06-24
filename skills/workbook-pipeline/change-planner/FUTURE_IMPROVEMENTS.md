# Future Improvements

## Near-term improvements

- Add stronger task classification so the planner can distinguish readability changes from true model-logic changes more accurately.
- Score candidate sheets and modules instead of only selecting them heuristically.
- Add a mode that emits a very short execution plan for direct use by downstream agents.

## Accuracy and safety

- Use the workbook brief's formula samples and defined names more deeply when identifying risk.
- Add explicit rollback guidance tied to backup-versioning artifacts.
- Flag when a task appears to require human review before autonomous execution.

## Pipeline integration

- Accept a workbook manifest and create one plan per workbook.
- Emit a structured validation seed that the validation-checklist builder can consume directly.
- Add support for planning against a "before" and "after" brief pair to constrain refactors.
- Default plan outputs into workbook-local `llm_work/plans/` folders.
- Add explicit run metadata so each plan records which `llm_work/runs/<timestamp>/` context it belongs to.
