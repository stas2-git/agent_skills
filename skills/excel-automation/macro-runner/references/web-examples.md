# Web Examples

Web scan date: 2026-04-11

## Potentially useful references

- xlwings App API docs
  https://docs.xlwings.org/en/latest/api/app.html
  Why it matters: documents `app.macro(...)`, which is directly relevant to a macro-runner skill.

- xlwings `RunPython` docs
  https://docs.xlwings.org/en/0.11.6/vba.html
  Why it matters: useful if the workflow ever flips from "Python runs VBA" to "VBA calls Python" for parts of the pipeline.

- xlwings example that inserts and runs a macro
  https://gist.github.com/Sven-Bo/4253ad6ff739aa10137ce5d7185b119c
  Why it matters: concrete end-to-end example of create workbook, add VBA, reopen, and execute macro.

- xlwings CLI docs
  https://docs.xlwings.org/en/0.18.0/command_line.html
  Why it matters: useful setup notes for macOS, especially around add-in and `runpython` installation behavior.

## Takeaway

This looks very buildable on top of xlwings. The biggest likely issues are trust settings, workbook attachment, and surfacing Excel/VBA runtime errors cleanly.
