# Web Examples

Web scan date: 2026-04-11

## Potentially useful references

- `Fmajor/rsync-rotate-backup`
  https://github.com/Fmajor/rsync-rotate-backup
  Why it matters: useful snapshot naming and retention ideas, plus explicit logging of what each backup run did.

- `hkbakke/rsync-backup`
  https://github.com/hkbakke/rsync-backup
  Why it matters: shows verification and reporting patterns for backups. The workbook version can be much simpler, but the safety mindset is relevant.

## Takeaway

I did not find a workbook-specific backup/versioning tool worth adopting directly. This skill should probably stay small and use Python stdlib file-copy primitives, but these examples are helpful for naming, logs, and retention ideas.
