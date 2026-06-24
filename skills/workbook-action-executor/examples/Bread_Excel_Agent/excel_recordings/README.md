# Excel Recordings

Pre-recorded Excel workflows for training, testing, and learning how to use the Excel Agent.

## What Are Recordings?

Recordings are JSON files that capture sequences of tool calls used to build complex Excel spreadsheets. They serve as:

- **Training data** for the LLM to learn Excel patterns
- **Test cases** for validating tool functionality
- **Examples** for users to understand tool usage
- **Benchmarks** for measuring agent performance

## Available Recordings

### Income Statement Workflows

- **`recording_IncomeStatement.json`** (138 KB, 60 steps)
  - Basic income statement structure
  - Revenue, COGS, operating expenses
  - Basic formulas and formatting

- **`recording_IncomeStatement_complete.json`** (2.1 MB, 123 steps)
  - Full multi-year income statement
  - Advanced formatting and calculations
  - Professional styling

- **`recording_IncomeStatement_complete_tools.json`** (138 KB, 123 tool calls)
  - Same as complete, optimized format
  - Clean tool call sequence
  - Ready for replay

### Balance Sheet Workflows

- **`recording_BalanceSheet.json`** (134 KB, 58 steps)
  - Basic balance sheet structure
  - Assets, liabilities, equity
  - Simple formulas

- **`recording_BalanceSheet_complete.json`** (2.1 MB, 124 steps)
  - Full balance sheet with multiple years
  - Advanced formatting
  - Professional presentation

- **`recording_BalanceSheet_complete_tools.json`** (137 KB, 124 tool calls)
  - Optimized tool call sequence
  - Clean replay format

## Recording Format

Each recording follows this JSON structure:

```json
{
  "task_description": "Human-readable description",
  "total_steps": 123,
  "tool_sequence": [
    {
      "step": 1,
      "tool": "openpyxl_workbook",
      "parameters": {}
    },
    {
      "step": 2,
      "tool": "openpyxl_worksheet_set_item",
      "parameters": {
        "cell": "A1",
        "value": "Revenue"
      }
    }
    // ... more tool calls
  ]
}
```

### Snapshot Directories

Some recordings include `*_snapshots/` directories with Excel files captured at each step. These show the progressive build of the spreadsheet:

- `recording_IncomeStatement_snapshots/` - Income statement snapshots
- `recording_BalanceSheet_snapshots/` - Balance sheet snapshots

## Using Recordings

### Replay a Recording

```bash
python run.py --recording-file excel_recordings/recording_IncomeStatement_complete_tools.json --log
```

This will:
1. Load the recording
2. Execute each tool call in sequence
3. Generate the final Excel file
4. Save execution log to `model_logs/`

### Learn from Recordings

Study recordings to understand:
- Which tools to use for specific tasks
- Common patterns (headers → data → formatting → formulas)
- How to structure complex spreadsheets
- Professional formatting techniques

### Example: Understanding a Recording

```python
import json

with open('excel_recordings/recording_IncomeStatement_complete_tools.json') as f:
    recording = json.load(f)

# See what tools are used
tools_used = set(step['tool'] for step in recording['tool_sequence'])
print(f"Tools used: {tools_used}")

# See the sequence
for step in recording['tool_sequence'][:10]:  # First 10 steps
    print(f"{step['step']}: {step['tool']}")
```

## Creating Your Own Recordings

To record your own workflows:

1. **Enable logging** during interactive sessions:
   ```bash
   python run.py --log
   ```

2. **Perform your Excel workflow**
   - The system will record all tool calls

3. **Find your recording** in `model_logs/run_*.json`

4. **Extract tool sequence** for replay:
   ```python
   import json

   with open('model_logs/run_2026-02-05_10-30-00.json') as f:
       log = json.load(f)

   recording = {
       "task_description": "Your description",
       "total_steps": len(log['tool_calls']),
       "tool_sequence": log['tool_calls']
   }

   with open('my_recording.json', 'w') as f:
       json.dump(recording, f, indent=2)
   ```

## Recording Statistics

| Recording | File Size | Steps | Categories |
|-----------|-----------|-------|------------|
| Income Statement (basic) | 138 KB | 60 | Structure, formulas, basic formatting |
| Income Statement (complete) | 2.1 MB | 123 | Multi-year, advanced formatting, charts |
| Balance Sheet (basic) | 134 KB | 58 | Assets/liabilities, simple layout |
| Balance Sheet (complete) | 2.1 MB | 124 | Multi-year, professional styling |

## Common Patterns

### Pattern 1: Financial Statement Structure
```
1. Create workbook
2. Set up headers (row 1)
3. Add section titles (Revenue, COGS, etc.)
4. Input historical data
5. Add formulas for calculations
6. Apply formatting (fonts, colors, borders)
7. Set number formats (currency, percentages)
8. Freeze panes
9. Save workbook
```

### Pattern 2: Multi-Year Analysis
```
1. Create column headers for years (2020, 2021, 2022...)
2. Input data for each year
3. Add growth rate formulas
4. Create summary statistics
5. Add conditional formatting for trends
6. Generate charts
```

## Contributing Recordings

Have a great workflow? Share it!

1. Create a clean recording following the format above
2. Add a descriptive `task_description`
3. Test replay to ensure it works
4. Submit a PR with your recording in this directory

See [CONTRIBUTING.md](../CONTRIBUTING.md) for details.

## License

These recordings are provided as examples under the same MIT License as the Excel Agent project.
