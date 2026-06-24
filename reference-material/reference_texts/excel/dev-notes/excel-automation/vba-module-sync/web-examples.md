# Web Examples

Web scan date: 2026-04-11

## Potentially useful references

- `mattpalermo/VBA-Import-Export`
  https://github.com/mattpalermo/VBA-Import-Export
  Why it matters: strong reference for import/export workflow, config-driven module lists, and backup warnings when syncing VBA to disk.

- xlwings repository
  https://github.com/xlwings/xlwings
  Why it matters: the main cross-platform Excel automation library with macOS support.

- xlwings example that adds a VBA module and runs it
  https://gist.github.com/Sven-Bo/4253ad6ff739aa10137ce5d7185b119c
  Why it matters: concrete example of using `wb.api.VBProject.VBComponents.Add(...)` and then executing the macro.

- xlwings "Missing Features" docs
  https://docs.xlwings.org/en/0.26.2/missing_features.html
  Why it matters: explains the `.api` escape hatch, including that Mac uses appscript under the hood. Important for platform-specific VBA project operations.

## Takeaway

There is good prior art for config-driven VBA sync. The likely build path is xlwings plus targeted `.api` calls, with careful handling of trust settings and workbook format.
