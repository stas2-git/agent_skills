# Future Improvements

## Near-term improvements

- Add retention rules so old backup runs can be pruned automatically.
- Add a dry-run mode that shows planned copy destinations without writing files.
- Support hashing copied workbooks so later steps can confirm provenance.

## Safety and ergonomics

- Add an option to refuse copying workbooks that are currently open in Excel.
- Preserve more source metadata in the mapping file, including size and modified time.
- Add a stricter mode that fails if any manifest workbook is missing.

## Pipeline integration

- Allow backup metadata to be merged back into the original manifest.
- Add a restore helper that can rebuild originals from a selected backup run.
- Add a naming option for "working copy suffix" workflows such as `_working.xlsm`.
- Add a mode that automatically nests backups and working copies under workbook-local `llm_work/` roots.
- Add helpers for selecting the latest prior run versus creating a fresh run root explicitly.
