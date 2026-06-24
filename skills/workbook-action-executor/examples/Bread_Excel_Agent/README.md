# Excel Action Space 📊

**LLM-powered Excel automation with 109 atomic tools**

A comprehensive system that enables AI models to create, modify, and analyze Excel files through natural language. Built on a three-tier architecture combining openpyxl (formatting), pandas (analysis), and intelligent bridging between them.

---

## Overview

### What is this?

Excel Action Space defines a **complete atomic action space** that can represent ANY human Excel workflow as a sequence of LLM tool calls.

Think of this as defining the "arms and hands" an LLM needs to perform any Excel task a human could do.

**Example transformation:**
```
Human Workflow:
  Click cell A1 → Type "Revenue" → Bold it → Color it blue → Enter formula

LLM Tool Calls:
  openpyxl_worksheet_set_item("A1", "Revenue")
  → openpyxl_cell_set_style("A1", font='{"bold": true}', fill='{"color": "0000FF"}')
  → openpyxl_worksheet_set_item("A2", "=SUM(B2:B10)")
```

Every click, keystroke, and menu selection in Excel maps to a precise tool call. This project catalogs all 109 atomic operations needed to replicate human Excel expertise.

### Core Concept

**The Excel Action Space** = A comprehensive catalog of every meaningful action a human can perform in Excel, mapped to programmatic tool calls an LLM can execute.

**Key Principles:**
- **Completeness**: If a human can do it in Excel, we can represent it as tool calls
- **Atomicity**: Each tool performs one fundamental operation (write cell, set color, add chart)
- **Composability**: Complex workflows = sequences of simple atomic actions
- **Executable**: All tools map directly to openpyxl/pandas/xlwings methods

### Why This Matters

1. **Workflow Learning**: LLMs can learn complex patterns (building DCF models, creating dashboards) from example sequences
2. **Complete Coverage**: No Excel task is "out of reach" - 95%+ of real-world operations are represented
3. **Training Data Generation**: Record expert Excel sessions → Convert to tool call sequences → Train LLMs
4. **Reproducibility**: Any Excel workflow becomes a reproducible, version-controlled sequence

**Vision**: Enable LLMs to build investment banking-quality financial models by providing them the complete set of atomic operations humans use.

### The Implementation: openpyxl + pandas

The action space is implemented using two battle-tested Python libraries that together provide comprehensive Excel capabilities:

**openpyxl** (74 tools) - The Formatting Layer:
- Covers 95%+ of everyday Excel operations
- File manipulation, cell formatting, charts, formulas, worksheet management
- Everything you'd accomplish clicking through Excel's UI
- Works **without Excel installed** (pure Python implementation)
- Creates professional-looking spreadsheets programmatically

**pandas** (30 tools) - The Analysis Layer:
- Advanced data operations beyond Excel's native capabilities
- Bulk transformations on massive datasets (millions of rows)
- Statistical analysis Excel can't perform efficiently
- Complex aggregations, pivots, and merges
- Transforms that would take hours manually

**Bridge Tools** (3 tools) - Seamless Integration:
- Connect both worlds: use Excel formulas, analyze with pandas power
- Calculate formulas via xlwings (leverages Excel's calculation engine)
- Transfer data bidirectionally while maintaining integrity

**What This Enables:**
- ✅ Everything desktop Excel can do (formatting, charts, pivot tables, data validation)
- ✅ Advanced operations **beyond** Excel (complex statistical analysis, ML-ready transformations)
- ✅ Professional financial models (DCF valuations, LBO models, Monte Carlo simulations)
- ✅ 10-100x faster than manual clicking through Excel UI

---

## Quick Start ⚡

Follow these steps:

### Prerequisites

- Python 3.8+
- An LLM API key (OpenAI, Anthropic, Claude, or any LiteLLM-compatible provider)

### Installation

1. **Clone and navigate to the project:**
   ```bash
   git clone <your-repo-url>
   cd Excel_Agent
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

**⚠️ IMPORTANT: Never commit API keys to version control!**

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your credentials:**
   ```bash
   # Open in your favorite editor
   nano .env
   ```

3. **Fill in your API details:**
   ```bash
   OPENAI_API_BASE=https://api.openai.com/v1
   OPENAI_API_KEY=sk-your-actual-key-here
   OPENAI_MODEL_NAME=gpt-4
   ```

4. **The `.env` file is in `.gitignore` and will never be committed**

**Supported LLM Providers** (via [LiteLLM](https://docs.litellm.ai/docs/)):
- **OpenAI**: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Anthropic**: `claude-opus-4-6`, `claude-sonnet-4-5`
- **Custom endpoints**: Any OpenAI-compatible API

For other providers, see the [LiteLLM documentation](https://docs.litellm.ai/docs/providers).

### Run Your First Automation

**Interactive Mode** (recommended for learning):
```bash
python run.py
# Choose option 2 for interactive mode
```

Example commands to try:
```
> Create a spreadsheet with quarterly sales data and save it as sales.xlsx
> Load Apple_DCF_Model.xlsx and explain the key assumptions
> Create a financial model with 5-year revenue projections
```

**Programmatic Usage:**
```python
from excel_action_space.integration.llm_client import LLMExcelAutomation

automation = LLMExcelAutomation()
automation.process_user_request(
    "Create a financial model with revenue projections for 2024-2028. "
    "Include rows for Revenue, COGS, Gross Profit, and Operating Expenses. "
    "Use formulas and format as currency. Save as financial_model.xlsx"
)
```

### Start Hacking 🚀

You're now set up! Here's how to explore:

1. **See available tools:**
   - Open `excel_action_space/tools/unified_definitions.json` to see all 109 tools
   - Each tool has name, description, and parameters

2. **Extend functionality:**
   - Add new openpyxl tools: `excel_action_space/tools/openpyxl_executor.py`
   - Add new pandas tools: `excel_action_space/tools/pandas_executor.py`
   - Add bridge operations: `excel_action_space/tools/bridge_functions.py`

3. **Test your changes:**
   ```bash
   python run.py  # Interactive mode for quick testing
   ```

4. **Understand the flow:**
   - User request → LLM (via LiteLLM) → Tool calls → UnifiedExcelExecutor → Excel files

---

## Architecture Overview

### Three-Tier System

**109 tools** organized into three complementary categories:

#### 1. **Openpyxl Tools** (66 tools) - Formatting & Excel Features
- File operations (create, load, save, close)
- Cell operations (read, write, copy, access)
- Formatting (fonts, colors, borders, alignment, number formats)
- Charts (bar, line, pie, scatter, area + inspection)
- Formulas (insert, copy, fill ranges efficiently)
- Worksheet management (create, delete, copy sheets)
- Excel features (data validation, protection, freezing, comments)
- **Prefix:** `openpyxl_*`

#### 2. **Pandas Tools** (30 tools) - Data Analysis & Transformation
- File I/O (read Excel, CSV, write to Excel with multiple sheets)
- DataFrame operations (filter, sort, group, pivot)
- Data transformations (merge, join, aggregate)
- Statistical analysis (describe, correlate, calculate)
- DataFrame management (select, list, inspect)
- **Prefix:** `pandas_*`

#### 3. **Bridge Tools** (3 tools) - Seamless Integration
- `bridge_openpyxl_to_pandas` - Load Excel with calculated formulas into pandas
- `bridge_pandas_to_openpyxl` - Transfer DataFrame to openpyxl for formatting
- `bridge_sync_file` - Synchronize data between both systems
- **Prefix:** `bridge_*`

### Critical Workflow Pattern ⚠️

**Save-Before-Bridge Rule** (enforced by error):

When using formulas with pandas analysis, you **MUST** follow this sequence:

```
1. Load or create workbook (openpyxl)
2. Add formulas and formatting
3. SAVE the workbook ← MANDATORY (openpyxl_workbook_save)
4. Bridge to pandas (bridge_openpyxl_to_pandas)
5. Analyze data with pandas
```

**Why is this enforced?**
- The bridge uses xlwings to calculate Excel formulas
- xlwings breaks openpyxl's file handle (unavoidable)
- We reload from disk to fix the handle
- Without saving first, all your changes are **LOST**

**What happens if you skip the save?**
```
Error: "CRITICAL: Workbook has UNSAVED changes. You MUST call 
openpyxl_workbook_save first to prevent data loss..."
```

The LLM will see this error and automatically correct the workflow.

### How It Works

```
User Request
    ↓
LiteLLM (with 109 tools)
    ↓
Tool Call(s) Generated
    ↓
UnifiedExcelExecutor
    ↓
┌───────────────────┼───────────────────┐
↓                   ↓                   ↓
OpenpyxlExecutor    PandasExecutor    BridgeConnector
(74 tools)          (30 tools)         (3 tools)
    ↓                   ↓                   ↓
Excel Files        DataFrames         Synced Data
```

**State Management:**
- Single openpyxl workbook active at a time
- Multiple pandas DataFrames (tracked by ID: df_1, df_2, etc.)
- Bridge coordinates between both systems
- Modified flag tracks unsaved changes

---

## Project Structure

```
Excel_Agent/
├── excel_action_space/
│   ├── tools/                      # Core tool implementation
│   │   ├── openpyxl_executor.py    # 66 openpyxl tools (formatting, charts, formulas)
│   │   ├── pandas_executor.py      # 30 pandas tools (analysis, transformations)
│   │   ├── bridge_functions.py     # 3 bridge tools (openpyxl ↔ pandas)
│   │   ├── unified_executor.py     # Routes tool calls to correct executor
│   │   └── unified_definitions.json # All 109 tool definitions (LiteLLM format)
│   │
│   ├── integration/
│   │   └── llm_client.py           # LiteLLM integration + interactive mode
│   │
│   ├── discovery/                  # Research & exploration
│   │   ├── research/               # Background on Python Excel libraries
│   │   └── exploration/            # Scripts that discovered tool definitions
│   │
│   ├── workflows/                  # Example workflows (currently empty - contribute!)
│   ├── tests/                      # Unit and integration tests
│   ├── outputs/                    # Generated Excel files
│   └── README.md                   # Detailed documentation
│
├── run.py                          # Quick entry point for testing
├── requirements.txt                # All dependencies
├── plan.md                         # Original project vision
└── README.md                       # This file
```

**Key Files Explained:**
- **`unified_executor.py`**: Routes tool calls to the right executor (openpyxl/pandas/bridge)
- **`openpyxl_executor.py`**: Implements all 66 openpyxl tools (the formatting/Excel features layer)
- **`pandas_executor.py`**: Implements all 30 pandas tools (the analysis layer)
- **`bridge_functions.py`**: Implements the 3 critical bridge tools (connects the layers)
- **`unified_definitions.json`**: All 109 tool definitions in LiteLLM format (read this!)
- **`llm_client.py`**: Connects LiteLLM to the executor, handles conversation flow

---

## Development Guide

### Adding New Tools

#### 1. Add an Openpyxl Tool

**File:** `excel_action_space/tools/openpyxl_executor.py`

```python
def _your_new_tool(self, param1, param2=None):
    """
    Your tool description
    
    Args:
        param1: Description
        param2: Optional description
    """
    if not self.workbook:
        return error("No workbook loaded")
    
    # Your implementation
    self.modified = True  # Mark as modified if changes made
    return success("Operation completed")
```

Then add to `unified_definitions.json`:
```json
{
  "type": "function",
  "function": {
    "name": "openpyxl_your_new_tool",
    "description": "Clear description of what it does",
    "parameters": {
      "type": "object",
      "properties": {
        "param1": {
          "type": "string",
          "description": "What this parameter does"
        }
      },
      "required": ["param1"]
    }
  }
}
```

#### 2. Add a Pandas Tool

**File:** `excel_action_space/tools/pandas_executor.py`

Similar process - add method, update `unified_definitions.json`.

#### 3. Add a Bridge Tool

**File:** `excel_action_space/tools/bridge_functions.py`

Be careful with state management between openpyxl and pandas.

### Testing Changes

1. **Interactive testing:**
   ```bash
   python run.py
   # Option 2: Interactive mode
   > Test your new tool here
   ```

2. **Programmatic testing:**
   ```python
   automation = LLMExcelAutomation()
   automation.process_user_request("Use my new tool to...")
   ```

3. **Check state:**
   ```python
   state = automation.get_executor_state()
   print(state)
   ```

### Understanding the Executor Flow

1. **User prompt** → `LLMExcelAutomation.process_user_request()`
2. **LiteLLM generates tool calls** → Based on 109 tool definitions
3. **UnifiedExcelExecutor routes** → Checks tool prefix (openpyxl_, pandas_, bridge_)
4. **Individual executor executes** → Returns `{'status': 'success'/'error', 'result': ...}`
5. **Result fed back to LLM** → LLM can call more tools or respond
6. **Loop until complete** → Max 100 iterations

### Key Design Principles

1. **Atomic Operations** - Each tool does one thing well
2. **Explicit State** - Track modified flag, filenames, DataFrame IDs
3. **Fail-Safe** - Enforce save-before-bridge to prevent data loss
4. **LLM-Friendly** - Clear error messages that guide the LLM
5. **Composable** - Complex workflows = sequences of simple tools

---

## Documentation

- **This README** - Quick start and overview
- **`excel_action_space/README.md`** - Detailed system architecture
- **`excel_action_space/tools/unified_definitions.json`** - Complete tool catalog
- **`plan.md`** - Original project vision and research
- **`excel_action_space/OPTION2_IMPLEMENTATION_COMPLETE.md`** - Save-before-bridge implementation details
- **`excel_action_space/discovery/`** - Research on Python Excel libraries

---

## Contributing

Contributions welcome! Areas of interest:

1. **Example workflows** - Add to `excel_action_space/workflows/examples/`
2. **Test coverage** - Add to `excel_action_space/tests/`
3. **New tools** - Extend executor functionality
4. **Documentation** - Improve guides and examples
5. **Bug fixes** - Especially around edge cases

### Contribution Guidelines

1. Ensure you're on the `pandas` branch
2. Test changes in interactive mode
3. Update `unified_definitions.json` if adding tools
4. Follow existing code patterns
5. Add clear docstrings

---

## License

MIT License - See project repository for details

---

## Credits

Built with comprehensive research into Python Excel libraries and real-world financial modeling requirements. See `excel_action_space/discovery/research/` for background research.

**Key Technologies:**
- [openpyxl](https://openpyxl.readthedocs.io/) - Excel file manipulation
- [pandas](https://pandas.pydata.org/) - Data analysis
- [xlwings](https://www.xlwings.org/) - Excel automation
- [LiteLLM](https://github.com/BerriAI/litellm) - LLM integration

---

## Support

For bugs or feature requests, use the project's issue tracker.

---

**Now go build something awesome! 🚀**
