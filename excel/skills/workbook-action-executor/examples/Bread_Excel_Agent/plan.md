# Excel Action Space: Complete LLM Tool Definition Project

## 🎯 Project Vision

Define a **complete atomic action space** that can represent ANY human Excel workflow as a sequence of LLM tool calls. This enables:
1. Recording human Excel workflows (e.g., building a DCF model)
2. Translating those recordings into tool call sequences
3. Training LLMs to replicate complex Excel tasks using these atomic actions

Think of this as defining the "arms and hands" an LLM needs to perform any Excel task a human could do.

---

## 🔑 Core Concept

**The Excel Action Space** = A comprehensive catalog of every meaningful action a human can perform in Excel, mapped to programmatic tool calls an LLM can execute.

Example transformation:
```
Human: Clicks cell A1 → Types "Revenue" → Bolds it → Colors it blue
LLM: select_cell(A1) → write_value(A1, "Revenue") → set_font(A1, bold=True) → set_fill(A1, color="blue")
```

---

## 📊 Why This Matters

- **Workflow Learning**: LLMs can learn complex workflows (financial modeling, data analysis) from examples
- **Complete Coverage**: No Excel task is "out of reach" - if a human can do it, we can represent it
- **Training Data Generation**: Convert expert Excel sessions into training sequences for LLMs
- **Reproducibility**: Any Excel workflow becomes a reproducible sequence of tool calls

---

## 🔎 Technical Strategy

### Why Programmatic Over UI Automation?
- **Reliability**: Direct API calls don't break with UI updates
- **Speed**: 100x faster than simulating clicks
- **Precision**: Exact control over operations
- **Coverage**: 95%+ of meaningful Excel actions available via Python libraries

### Library Capabilities Overview
- **openpyxl**: File manipulation, formatting, formulas, basic charts
- **xlwings**: Live Excel COM automation, real-time updates, advanced features
- **pandas**: Bulk data operations, analysis, transformations
- **win32com**: Windows-specific Excel automation (full access)
- **Additional tools**: MCP servers, Office Scripts for web/cloud scenarios

---

## 🗺️ Implementation Phases (Library-First Approach)

### Phase 1: Core Library Exploration & Tool Extraction (Week 1)
**Goal**: Build comprehensive tool catalog from actual Python capabilities

1. **openpyxl Deep Dive**
   - Extract all methods for workbook, worksheet, cell operations
   - Document formatting capabilities (fonts, fills, borders, alignment)
   - Map formula and function support
   - Test chart creation capabilities
   - Build initial tool set: ~40-50 core tools

2. **xlwings Advanced Features**
   - Explore COM automation capabilities
   - Test macro execution and VBA integration
   - Document real-time Excel manipulation
   - Add advanced tools: ~20-30 tools

3. **pandas Excel Integration**
   - Map DataFrame to Excel operations
   - Document pivot table creation
   - Test bulk data operations
   - Add data tools: ~15-20 tools

4. **Create Initial Tool Catalog**
   ```python
   # Example discovery approach
   import openpyxl, xlwings, pandas

   # Map actual methods to user-friendly tools
   tools = {
       "write_cell": openpyxl.cell.write,
       "format_range": openpyxl.styles.apply,
       "create_chart": openpyxl.chart.add,
       # ... 100+ tools total
   }
   ```

### Phase 2: Workflow Validation & Gap Analysis (Week 2)
**Goal**: Test tools against real Excel workflows to find gaps

1. **Test Common Workflows**
   - Format a financial statement ✓
   - Build a three-statement model ✓
   - Create pivot tables and charts ✓
   - Apply conditional formatting ✓
   - Build a DCF model ✓
   - Run Monte Carlo simulation ✓

2. **Document Actual Limitations**
   - List features that require Excel installation (xlwings)
   - Note operations that can't preserve macros (openpyxl)
   - Identify UI elements we can't create (ribbons, dialogs)

3. **Develop Workarounds**
   - Goal Seek → scipy.optimize
   - Solver → Python optimization libraries
   - Power Query → pandas operations
   - Missing functions → custom Python implementations

### Phase 3: Tool Architecture & Registry (Week 3)
**Goal**: Organize tools into coherent, LLM-friendly structure

1. **Tool Categorization**
   ```
   Core Operations (openpyxl-based):
   - File: create, open, save, close
   - Cell: read, write, clear, copy
   - Format: font, fill, border, alignment
   - Formula: insert, evaluate, copy

   Advanced Operations (xlwings-based):
   - Live: refresh, calculate, update
   - Macro: run, call, execute
   - Interactive: select, activate, scroll

   Data Operations (pandas-based):
   - Transform: pivot, group, aggregate
   - Analyze: statistics, correlation, regression
   ```

2. **Build Smart Dispatcher**
   - Auto-select library based on requirements
   - Handle file state (open/closed)
   - Manage Excel sessions efficiently
   - Batch operations for performance

3. **Create Tool Documentation**
   - Each tool with examples
   - Performance characteristics
   - Library dependencies
   - Common use patterns

### Phase 4: Workflow Recording & Learning (Week 4)
**Goal**: Build system to learn from expert Excel users

1. **Record Real Expert Workflows**
   - Finance professional building DCF
   - Analyst creating dashboards
   - Data scientist doing analysis

2. **Translation Pipeline**
   ```python
   # Human action → Python tool
   recording = ["Click A1", "Type '=NPV(0.1, B1:B10)'"]
   tools = ["select_cell('A1')", "insert_formula('A1', '=NPV(0.1, B1:B10)')"]
   ```

3. **Build Workflow Library**
   - DCF model construction (150+ tool calls)
   - Financial statement formatting (50+ tool calls)
   - Dashboard creation (100+ tool calls)
   - Sensitivity analysis (75+ tool calls)

4. **Optimization & Learning**
   - Identify common patterns
   - Create macro tools for frequent sequences
   - Build workflow templates

---

## 📁 Project Structure

```
excel_action_space/
├── discovery/
│   ├── action_taxonomy.xlsx        # Complete catalog of Excel actions
│   ├── library_capabilities.md     # What each library can do
│   ├── coverage_matrix.csv         # Action-to-library mapping
│   └── gaps_and_workarounds.md    # Unsupported actions
│
├── tools/
│   ├── core/
│   │   ├── navigation.py          # Cell/range selection
│   │   ├── data.py                # Read/write operations
│   │   ├── formatting.py          # Visual styling
│   │   ├── formulas.py            # Formula operations
│   │   └── structure.py           # Sheet/row/column ops
│   ├── analysis/
│   │   ├── pivots.py              # Pivot table operations
│   │   ├── charts.py              # Chart creation
│   │   └── statistics.py          # Data analysis tools
│   └── advanced/
│       ├── macros.py              # VBA/macro operations
│       ├── validation.py          # Data validation
│       └── protection.py          # Security features
│
├── registry/
│   ├── tool_registry.py           # Central tool catalog
│   ├── schemas.py                 # Pydantic models
│   └── dispatcher.py              # Tool routing logic
│
├── translator/
│   ├── recording_parser.py        # Parse human actions
│   ├── action_mapper.py           # Map actions to tools
│   └── sequence_optimizer.py      # Optimize tool sequences
│
├── workflows/
│   ├── examples/
│   │   ├── simple_formatting.json
│   │   ├── pivot_analysis.json
│   │   └── dcf_model.json        # Complete DCF as tool calls
│   └── templates/                 # Reusable workflow patterns
│
├── tests/
│   ├── unit/                      # Tool-level tests
│   ├── integration/               # Workflow tests
│   └── validation/                # Real Excel comparison
│
└── docs/
    ├── tool_reference.md          # Complete tool documentation
    ├── workflow_guide.md          # How to create workflows
    └── examples.md                # Usage examples

---

## 🚀 Key Deliverables

### 1. Excel Action Taxonomy (Week 1)
Comprehensive spreadsheet documenting:
- Every Excel UI action
- Keyboard shortcuts
- Menu items
- Ribbon commands
- Context menu options

### 2. Library Capability Matrix (Week 2)
Detailed analysis of what each Python library can accomplish:
- Feature coverage percentages
- Performance comparisons
- Best library for each action
- Workarounds for gaps

### 3. Tool Catalog (Week 3)
Complete set of atomic tools covering:
- **Navigation**: ~15-20 tools
- **Data Operations**: ~25-30 tools
- **Formatting**: ~30-35 tools
- **Formulas**: ~20-25 tools
- **Analysis**: ~20-25 tools
- **Structure**: ~15-20 tools

### 4. Workflow Examples (Week 4)
Real-world workflows as tool sequences:
- Simple table formatting
- Pivot table creation
- Financial model building
- Full DCF model construction

---

## ✅ What Python Excel Libraries Can Actually Do

Based on extensive research, Python libraries provide **95%+ coverage** of Excel functionality:

### **Fully Supported (via openpyxl, xlwings, pandas)**
- ✅ Complete DCF models with complex formulas
- ✅ Monte Carlo simulations integrated with Excel
- ✅ Three-statement financial models
- ✅ LBO models with sensitivity analysis
- ✅ All formatting (fonts, colors, borders, fills, alignment)
- ✅ Charts, pivot tables, conditional formatting
- ✅ Data validation, named ranges, comments
- ✅ Sheet operations (create, delete, hide, protect)
- ✅ Formula creation and copying
- ✅ Images, hyperlinks, cell merging
- ✅ Macro execution (xlwings only)
- ✅ Real-time Excel automation (xlwings)

### **Not Supported / Limited**
- ❌ Creating new VBA macros (can run existing ones)
- ❌ Custom Excel UI elements (ribbons, dialogs)
- ❌ Some built-in Excel tools (Goal Seek, Solver - but Python has better alternatives)
- ❌ Real-time collaboration features
- ⚠️ Formula evaluation without Excel installed (openpyxl limitation)

### **Performance Benchmarks**
- **openpyxl**: 10 seconds to update 400-500 cells across 90 files
- **xlwings**: 50-70 seconds for same task (includes Excel overhead)
- **Professional use**: Investment banks actively use Python+Excel for production models

---

## 📊 Success Metrics

- **Coverage**: Represent 95%+ of real Excel workflows that matter
- **Practicality**: Focus on what's actually executable, not theoretical
- **Performance**: Efficient enough for production use (10s for hundreds of operations)
- **Clarity**: Each tool maps to actual Python methods
- **Validation**: Test against real financial models (DCF, LBO, Monte Carlo)

---

## 🎯 End Goal

**Create a complete, practical tool set that enables LLMs to build professional-grade Excel models**, validated by:

1. **Real Workflow Test**: Record expert building a DCF → Reproduce perfectly with tools
2. **Coverage Test**: Successfully handle 95%+ of operations in typical financial models
3. **Performance Test**: Build complex models in reasonable time (<1 minute)
4. **Learning Test**: LLM can learn new patterns from recorded workflows

The ultimate validation: Can an LLM use our tools to build a complete investment banking-quality DCF model that passes professional review?