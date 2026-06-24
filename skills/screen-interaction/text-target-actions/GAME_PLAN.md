# Text Target Actions Game Plan

## Goal

Create an action skill that consumes OCR output or live screen OCR to:

- find text
- choose the best match
- click it
- optionally move only or dry-run

## Reviewed examples

- [ocr_clicker_click.py](/Users/stan/Documents/actuarial%20model/skills/screen-interaction/text-target-actions/example_codes/ocr_clicker_click.py)
- [rpa_tagui.py](/Users/stan/Documents/actuarial%20model/skills/screen-interaction/text-target-actions/example_codes/rpa_tagui.py)

## What looked useful

- `ocr_clicker_click.py` shows the basic loop:
  - capture region
  - OCR
  - normalize text
  - trigger action
- `rpa_tagui.py` has the stronger interface idea:
  - `exist()`
  - `click()`
  - `read()`
  - coordinate and text targets under one model

## Proposed first version

- `find-text`
- `click-text`
- `click-text --index`
- `click-text --dry-run`
- exact vs contains matching

## Guardrails

- do not hardcode coordinates in the skill logic
- use OCR bbox centers for clicks
- require the target app to be frontmost or provide an activation option

## Open questions

- whether fuzzy matching belongs in v1
- whether double-click/right-click should be added immediately or later
