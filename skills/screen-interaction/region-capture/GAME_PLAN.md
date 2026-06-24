# Region Capture Game Plan

## Goal

Create a focused capture skill for:

- full-screen screenshot
- explicit region capture
- app-relative or window-relative region capture later
- writing captures to predictable local file paths

## Reviewed examples

- [pyscreeze_init.py](/Users/stan/Documents/actuarial%20model/skills/screen-interaction/region-capture/example_codes/pyscreeze_init.py)
- [mss_fps_example.py](/Users/stan/Documents/actuarial%20model/skills/screen-interaction/region-capture/example_codes/mss_fps_example.py)

## What looked useful

- `pyscreeze` handles region cropping explicitly and shows cross-platform screenshot edge cases.
- `mss` highlights the value of fast region-grab patterns when repeated capture is needed.
- The most useful design idea is to treat region as a first-class input everywhere.

## Proposed first version

- `capture-fullscreen`
- `capture-region --x --y --width --height`
- `capture-front-window` later if window-control becomes a dependency
- optional `--output`

## Guardrails

- on macOS, keep using `screencapture` or Pillow-backed screen grabs where they are reliable
- do not combine OCR into this skill
- optimize for predictable file output and coordinate correctness

## Open questions

- whether repeated captures belong here or in a separate streaming/watch skill
- whether window-relative capture should depend on the window-control skill
