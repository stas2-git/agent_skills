# Excel Skills

This folder contains the Excel/workbook-oriented Codex skills copied from the
local Codex skill directories.

## Included

- `excel-decompose`
- `excel-automation`
- `workbook-action-executor`
- `workbook-pipeline`
- `spreadsheets`
- `screen-interaction`
- `_shared`

`screen-interaction` is included because some workbook validation and live Excel
workflows refer to visible-screen checks.

`_shared` is included because the workbook scripts import shared audit/logging
helpers from `_shared.llm_work_audit`.

## Excluded

Machine-local/generated files were intentionally left out:

- `.venv/`
- `.DS_Store`
- prior decomposition/output workbook artifacts
- prior drop-folder workbook artifacts

On another machine, copy or symlink the needed folders from this `excel/skills/`
directory into the target Codex skills directory, usually:

```bash
~/.codex/skills/
```

For example:

```bash
cp -R excel/skills/excel-decompose ~/.codex/skills/
cp -R excel/skills/excel-automation ~/.codex/skills/
cp -R excel/skills/workbook-action-executor ~/.codex/skills/
cp -R excel/skills/workbook-pipeline ~/.codex/skills/
cp -R excel/skills/screen-interaction ~/.codex/skills/
cp -R excel/skills/spreadsheets ~/.codex/skills/
cp -R excel/skills/_shared ~/.codex/skills/
```

The `spreadsheets` skill came from the bundled primary runtime cache, so install
it wherever your work Codex setup expects bundled or user-provided skills.

## Validate

Run the local checks after adding, moving, or editing Excel skills:

```bash
python3 excel/skills/scripts/validate_excel_skills.py
```

The validator checks frontmatter, expected eval prompts, linked resources, stale machine-local paths, code fences, active reference size, and known folder/name exceptions.
