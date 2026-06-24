# Relation To The Older Screen OCR Skill

`screen-ocr-interaction` was built earlier as a composed workflow:

- capture
- OCR
- find text
- click text

`region-ocr` extracts just the OCR layer from that broader skill so it can be reused cleanly by:

- `text-target-actions`
- `wait-and-assert`
- any future workflow skill that needs OCR without automatic clicking

So this skill is intentionally narrower, even though some code is reused from the older combined implementation.
