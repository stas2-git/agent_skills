# Region OCR Game Plan

## Goal

Create a text extraction skill that takes an image or region capture and returns:

- text
- confidence
- bounding boxes
- screen coordinates when an origin is known

## Reviewed examples

- [ocrmac_ocrmac.py](/Users/stan/Documents/actuarial%20model/skills/screen-interaction/region-ocr/example_codes/ocrmac_ocrmac.py)
- [screenshot_ocr_ocr.py](/Users/stan/Documents/actuarial%20model/skills/screen-interaction/region-ocr/example_codes/screenshot_ocr_ocr.py)

## What looked useful

- `ocrmac` is the best foundation for us on macOS:
  - Apple Vision OCR
  - confidence thresholds
  - recognition levels
  - coordinate conversion helpers
- `screenshot-ocr` reinforces the value of a small OCR wrapper with clean I/O boundaries.

## Proposed first version

- `ocr-image`
- `ocr-screen`
- `ocr-region`
- `--contains`
- `--json`
- confidence filtering

## Guardrails

- prefer Apple Vision over Tesseract on macOS
- return structured OCR records, not only raw text blobs
- keep OCR separate from clicking

## Open questions

- whether to expose both Vision and LiveText modes
- whether line-level and token-level output should be separate commands or flags
