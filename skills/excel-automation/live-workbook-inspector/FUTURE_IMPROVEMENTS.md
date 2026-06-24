# Future Improvements

- Add a real script that can inspect ranges, formulas, number formats, fill colors, freeze panes, and named ranges from the live Excel session.
- Support both object-model inspection and screen-based fallback checks when Excel automation APIs are unavailable.
- Add narrow inspection presets like `--summary`, `--headers-only`, and `--used-range`.
- Log inspected workbook/sheet/range and a short result summary into the active run log.
- Add diff-friendly output so the inspector can compare pre-edit and post-edit range state.
