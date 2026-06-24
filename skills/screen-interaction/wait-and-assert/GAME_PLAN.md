# Wait And Assert Game Plan

## Goal

Create a stability skill for polling screen state until a condition is true, such as:

- text exists
- text disappears
- OCR output matches expectation
- image or text target becomes clickable

## Reviewed examples

- [rpa_tagui.py](/Users/stan/Documents/actuarial%20model/skills/screen-interaction/wait-and-assert/example_codes/rpa_tagui.py)
- [pyscreeze_init.py](/Users/stan/Documents/actuarial%20model/skills/screen-interaction/wait-and-assert/example_codes/pyscreeze_init.py)

## What looked useful

- `rpa_tagui.py` shows a good pattern for:
  - timeout defaults
  - polling loops
  - `exist()` before acting
  - clear error messages when the target never appears
- `pyscreeze` shows locate-on-screen retry patterns and region-limited searching.

## Proposed first version

- `wait-for-text`
- `text-exists`
- `assert-text`
- `wait-for-no-text`
- configurable timeout and poll interval

## Guardrails

- keep waiting logic separate from click logic
- support region-limited checks to avoid slow whole-screen polling
- return structured success/failure rather than only printing logs

## Open questions

- whether this skill should support both OCR text and image-template waiting from day one
- whether failed assertions should exit nonzero by default
