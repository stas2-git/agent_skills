# Future Improvements

- Add a real script that can attach through `xlwings` and fall back to AppleScript or screen automation when needed.
- Log the active workbook, active sheet, frontmost-app status, and save result into `llm_work/current/run_log.json`.
- Support workbook matching by partial title for VDI sessions where the displayed name differs from the file name.
- Add "re-focus Excel" and "recover from popup" helper actions for fragile screen-automation flows.
- Add read-only inspection mode so later skills can confirm session state before editing.
