# Future Improvements

## Near-term improvements

- Add support for syncing a whole folder of modules from a manifest instead of one file at a time.
- Add an `export-module` subcommand for just one named module.
- Add a `remove-module` subcommand for deliberate cleanup flows.
- Add a screen-automation playbook for VBE navigation, module creation, paste, save, and run.

## Reliability and safety

- Detect whether the target workbook is already open in another Excel instance and report that more clearly.
- Add a dry-run mode that lists the modules that would be replaced.
- Export a pre-change snapshot automatically before any write-side injection flow.
- Add clipboard verification and OCR confirmation after pasting VBA into the VBE.
- Add guardrails for common VDI problems such as focus loss, latency, and unexpected dialogs.

## Coverage

- Add support for preserving `.frx` sidecar files when exporting forms.
- Add a safer path for document modules such as `ThisWorkbook` and sheet code-behind modules.
- Add dedicated screen-automation support for code-behind modules such as `ThisWorkbook` and sheet objects.
- Capture richer diagnostics for VBE state, editor focus, and macro execution after injection.
