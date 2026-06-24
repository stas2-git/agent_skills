# Future Improvements

- Add a real script for live cell edits, formatting, sheet creation, and save actions through `xlwings` or another Excel automation bridge.
- Add explicit batching for multiple cell writes so one run can describe a compact change set.
- Log workbook path, active sheet, edited ranges, save status, and validation hints into the active run log.
- Add a dry-run mode that inspects the target area and reports the intended edit plan before writing.
- Add screen-automation fallback recipes for VDI sessions where object-model automation is blocked.
