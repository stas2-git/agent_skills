# Web Examples

Web scan date: 2026-04-11

## Potentially useful references

- openpyxl defined names docs
  https://openpyxl.readthedocs.io/en/3.1.2/defined_names.html
  Why it matters: named ranges are important workbook semantics and should show up in summaries.

- openpyxl `load_workbook` docs
  https://openpyxl.readthedocs.io/en/3.1.2/api/openpyxl.reader.excel.html
  Why it matters: documents `keep_vba`, `data_only`, and workbook loading flags that shape decomposition and summary output.

- openpyxl tutorial
  https://openpyxl.readthedocs.io/en/3.1/tutorial.html
  Why it matters: quick reference for workbook structure, sheet enumeration, and worksheet metadata access.

- olevba wiki
  https://github.com/decalage2/oletools/wiki/olevba
  Why it matters: strong reference for extracting VBA source from `.xlsm` files.

- Quick example of extracting VBA with olevba
  https://gist.github.com/decalage2/844ce29eff0ab6e4c799ebf30f27b0f0
  Why it matters: tiny example that can inform a focused extractor inside summary or decomposition steps.

## Takeaway

This skill can mostly stand on openpyxl plus olevba. The missing part is not extraction but summarization logic that compresses large workbook structure into task-relevant context.
