# Window Control Game Plan

## Goal

Create a small macOS-focused skill for:

- activating an app
- bringing a window to the front
- finding windows by title
- optionally saving and restoring the previously frontmost app
- optionally saving and restoring window bounds

## Reviewed examples

- [pywinctl_macos.py](/Users/stan/Documents/actuarial%20model/skills/screen-interaction/window-control/example_codes/pywinctl_macos.py)
- [xfocus.py](/Users/stan/Documents/actuarial%20model/skills/screen-interaction/window-control/example_codes/xfocus.py)

## What looked useful

- `xfocus.py` is a very small proof that window-title activation via AppleScript is realistic.
- `pywinctl_macos.py` shows much better edge-case coverage:
  - permission checks
  - getting the frontmost window
  - listing windows and titles
  - tracking position and size
  - fuzzy title matching ideas

## Proposed first version

- `activate-app`
- `activate-window-by-title`
- `get-frontmost-app`
- `save-state`
- `restore-state`
- `get-window-bounds`

## Guardrails

- stay macOS-specific at first
- prefer AppleScript / System Events over a heavy abstraction layer
- do not try to implement true always-on-top behavior as a core feature

## Open questions

- whether title matching should support only exact/contains initially
- whether we want one generic state file format shared with other screen skills
