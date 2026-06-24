# Borrow Audit

Generated: 2026-04-12 America/New_York

This folder contains selected reference files copied from:

- `https://github.com/Bread-Technologies/Bread_Excel_Agent`

The goal is not to run these files directly inside the local skill stack. The goal is to keep only the source files that are directly relevant to the `workbook-action-executor` skill while we adapt ideas into that specific skill.

## Selection Rule

Files were copied here because they contain patterns that are likely worth adapting into `workbook-action-executor` specifically:

- deterministic action routing
- explicit workbook state tracking
- safer save and recovery behavior
- consolidated style operations
- action consolidation and deduplication
- command-surface naming and parameter design
- helper utilities for normalization and type conversion

## Copied Files

### `unified_executor.py`

Source:

- `examples/Bread_Excel_Agent/excel_action_space/tools/unified_executor.py`

Why copied:

- clean routing by tool prefix
- explicit executor composition
- good example of separating action domains within an executor layer

Most relevant patterns:

- prefix-based dispatch
- system-level state commands
- unified error envelope

### `unified_definitions.json`

Source:

- `examples/Bread_Excel_Agent/excel_action_space/tools/unified_definitions.json`

Why copied:

- shows the full command surface and parameter naming choices
- useful for comparing our subcommands against a broader action-space design

Most relevant patterns:

- command naming
- parameter naming
- action taxonomy
- useful future operations we may want to add selectively

### `openpyxl_executor.py`

Source:

- `examples/Bread_Excel_Agent/excel_action_space/tools/openpyxl_executor.py`

Why copied:

- strongest direct overlap with `workbook-action-executor`
- contains workbook state tracking and safer save logic
- includes a consolidated `cell_set_style` pattern
- includes insert/delete row and column operations
- includes formula fill logic

Most relevant patterns:

- `current_filename`
- `modified`
- `check_workbook_status`
- `cell_set_style`
- `worksheet_insert_rows`
- `worksheet_delete_rows`
- `worksheet_insert_cols`
- `worksheet_delete_cols`
- `worksheet_set_column_width`
- `worksheet_set_row_height`
- `worksheet_freeze_panes`
- defensive save handling

### `translate_recording.py`

Source:

- `examples/Bread_Excel_Agent/translate_recording.py`

Why copied:

- good example of translating workbook events into reusable action calls

Most relevant patterns:

- formatting consolidation
- deduplication of repeated actions
- normalized cell references
- compact action sequence generation

### `utils.py`

Source:

- `examples/Bread_Excel_Agent/excel_action_space/tools/utils.py`

Why copied:

- likely helper code for normalization and conversion that overlaps with executor concerns

Most relevant patterns:

- value conversion
- normalization helpers
- shared helper design for executor code

## What This Folder Is Not

- not a local runtime dependency
- not a vendored third-party package
- not an instruction to copy all logic blindly

This is a reference subset for targeted borrowing and future comparison.

## Expected Next Adaptations

Likely local follow-up work:

1. add `check-workbook-status` to `workbook-action-executor`
2. add insert/delete rows and columns
3. add a consolidated style command
4. add formula fill support
