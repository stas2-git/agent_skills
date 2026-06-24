# Future Improvements

## Near-term improvements

- Add typed argument coercion so macro args can be passed as numbers, booleans, or strings explicitly.
- Add a timeout mode that can detect macros that appear stuck and return a clearer failure.
- Add an option to capture the active worksheet name after the macro finishes.

## Reliability and diagnostics

- Save a structured run log with workbook path, macro name, elapsed time, and error text.
- Capture visible Excel alert text when a macro fails and a dialog appears.
- Add a retry mode for transient workbook-open issues.

## Pipeline integration

- Accept a backup mapping file and run against working copies automatically.
- Add support for a job manifest that runs different macros per workbook.
- Emit a machine-readable result schema that downstream validation steps can consume directly.
