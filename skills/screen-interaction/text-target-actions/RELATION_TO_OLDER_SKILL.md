# Relation To The Older Screen OCR Skill

`screen-ocr-interaction` combined:

- capture
- OCR
- text lookup
- click

`text-target-actions` extracts the action layer from that older combined workflow.

It still performs OCR internally in the first pass so it can be used directly, but its responsibility is:

- choose the right text match
- expose the match clearly
- click or dry-run that match

Over time, this should be the preferred action layer that pairs with `region-ocr`.
