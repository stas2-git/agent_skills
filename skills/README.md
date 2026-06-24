# Skills

This folder contains the Excel/workbook-oriented Codex skills copied from the
local Codex skill directories.

## Included

- `excel-decompose`
- `excel-automation`
- `workbook-action-executor`
- `workbook-pipeline`
- `spreadsheets`
- `screen-interaction`

`screen-interaction` is included because some workbook validation and live Excel
workflows refer to visible-screen checks.

## Excluded

Machine-local/generated files were intentionally left out:

- `.venv/`
- `.DS_Store`
- prior decomposition/output workbook artifacts
- prior drop-folder workbook artifacts

On another machine, copy or symlink the needed folders from this `skills/`
directory into the target Codex skills directory, usually:

```bash
~/.codex/skills/
```

For example:

```bash
cp -R skills/excel-decompose ~/.codex/skills/
cp -R skills/excel-automation ~/.codex/skills/
cp -R skills/workbook-action-executor ~/.codex/skills/
cp -R skills/workbook-pipeline ~/.codex/skills/
cp -R skills/screen-interaction ~/.codex/skills/
```

The `spreadsheets` skill came from the bundled primary runtime cache, so install
it wherever your work Codex setup expects bundled or user-provided skills.
