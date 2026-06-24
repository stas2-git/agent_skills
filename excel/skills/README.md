# Excel Skills Group

This folder is a grouped Excel skill package. `SKILL.md` is the high-level router
that chooses the focused workbook, spreadsheet, live Excel, VBA, pipeline, or
screen-interaction skill to load next.

## Included

- `SKILL.md` router: `excel-skills-router`
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

## Install

Recommended grouped install:

```bash
cp -R excel/skills ~/.codex/skills/excel
```

This installs one Excel group folder with the router at:

```text
~/.codex/skills/excel/SKILL.md
```

Focused skills remain inside that group folder, for example:

```text
~/.codex/skills/excel/excel-decompose/SKILL.md
~/.codex/skills/excel/workbook-action-executor/SKILL.md
~/.codex/skills/excel/excel-automation/live-workbook-editor/SKILL.md
```

If a Codex setup expects flat skill folders instead, copy the focused skills
individually:

```bash
cp -R excel/skills/excel-decompose ~/.codex/skills/
cp -R excel/skills/excel-automation ~/.codex/skills/
cp -R excel/skills/workbook-action-executor ~/.codex/skills/
cp -R excel/skills/workbook-pipeline ~/.codex/skills/
cp -R excel/skills/screen-interaction ~/.codex/skills/
cp -R excel/skills/spreadsheets ~/.codex/skills/
cp -R excel/skills/_shared ~/.codex/skills/
```

## Excluded

Machine-local/generated files were intentionally left out:

- `.venv/`
- `.DS_Store`
- prior decomposition/output workbook artifacts
- prior drop-folder workbook artifacts

The `spreadsheets` skill came from the bundled primary runtime cache, so install
it wherever your work Codex setup expects bundled or user-provided skills.

## Validate

Run the local checks after adding, moving, or editing Excel skills:

```bash
python3 excel/skills/scripts/validate_excel_skills.py
```

The validator checks frontmatter, expected eval prompts, linked resources, stale machine-local paths, code fences, active reference size, folder/name alignment, and installable-skill clutter such as examples, dev notes, and generated artifacts.
