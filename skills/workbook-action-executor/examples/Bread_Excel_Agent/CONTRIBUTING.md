# Contributing to Excel Agent

Thank you for your interest in contributing to Excel Agent! This document provides guidelines for contributions.

## Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Excel_Agent.git
   cd Excel_Agent
   ```
3. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Test thoroughly**
6. **Commit with clear messages**
7. **Push and create a Pull Request**

## Development Setup

1. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

3. **Run tests:**
   ```bash
   python run.py
   # Choose option 2 for interactive testing
   ```

## Contribution Areas

We welcome contributions in:

### 1. **New Tools**
Add Excel operations to executors:
- `excel_action_space/tools/openpyxl_executor.py` - Formatting, charts, formulas
- `excel_action_space/tools/pandas_executor.py` - Data analysis, transformations
- `excel_action_space/tools/pdf_executor.py` - PDF operations
- `excel_action_space/tools/bridge_functions.py` - Integration tools

### 2. **Example Workflows**
Share interesting use cases in `excel_recordings/`

### 3. **Documentation**
Improve guides, add examples, fix typos

### 4. **Bug Fixes**
Fix issues and edge cases

### 5. **Tests**
Increase test coverage in `excel_action_space/tests/`

## Adding New Tools

### Step 1: Implement the Tool

Add your function to the appropriate executor:

```python
# In excel_action_space/tools/openpyxl_executor.py
def _your_new_tool(self, param1, param2=None):
    """
    Brief description of what this tool does.

    Args:
        param1: Description of param1
        param2: Description of param2 (optional)

    Returns:
        dict: Success/error message with result data
    """
    if not self.workbook:
        return {
            "status": "error",
            "message": "No workbook loaded. Use openpyxl_load_workbook first."
        }

    try:
        # Your implementation here
        self.modified = True
        return {
            "status": "success",
            "message": "Operation completed successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}"
        }
```

### Step 2: Add Tool Definition

Add to `excel_action_space/tools/unified_definitions.json`:

```json
{
  "type": "function",
  "function": {
    "name": "openpyxl_your_new_tool",
    "description": "Clear, concise description of what the tool does and when to use it",
    "parameters": {
      "type": "object",
      "properties": {
        "param1": {
          "type": "string",
          "description": "Detailed description of param1"
        },
        "param2": {
          "type": "string",
          "description": "Detailed description of param2 (optional)"
        }
      },
      "required": ["param1"]
    }
  }
}
```

### Step 3: Register in Executor

Ensure your tool is called in `execute_tool()` method:

```python
elif tool_name == "openpyxl_your_new_tool":
    return self._your_new_tool(**params)
```

### Step 4: Test

Test your tool in interactive mode:
```bash
python run.py
# Choose option 2: Interactive mode
> Use my new tool to...
```

## Code Style

- **Follow PEP 8** Python style guidelines
- **Add docstrings** to all functions (Google style preferred)
- **Type hints** are encouraged but not required
- **Keep functions atomic** - one operation per tool
- **Return consistent format** - always return dict with `status` and `message`

## Pull Request Process

1. **Ensure your code runs without errors**
2. **Update documentation** if adding features
3. **Add yourself to contributors** (optional)
4. **Write clear PR description:**
   - What does this PR do?
   - Why is this change needed?
   - How has it been tested?
5. **Link related issues** if applicable

## Commit Message Guidelines

Write clear, descriptive commit messages:

```
Add new tool for conditional formatting

- Implement openpyxl_add_conditional_formatting tool
- Add support for color scales and data bars
- Update unified_definitions.json with tool definition
- Add usage example to documentation
```

## Security

⚠️ **NEVER commit:**
- API keys or credentials
- `.env` files
- Personal file paths
- Sensitive data in examples

✅ **Always:**
- Use `.env.example` for templates
- Use placeholder values in documentation
- Report security issues privately (see [SECURITY.md](SECURITY.md))

## Testing Guidelines

Before submitting:
- [ ] Code runs without errors
- [ ] New features work as expected
- [ ] Existing functionality not broken
- [ ] Documentation updated
- [ ] No sensitive data in commits

## Questions?

- **General questions**: Open a [Discussion](https://github.com/Bread-Technologies/Excel_Agent/discussions)
- **Bug reports**: Open an [Issue](https://github.com/Bread-Technologies/Excel_Agent/issues)
- **Feature requests**: Open an [Issue](https://github.com/Bread-Technologies/Excel_Agent/issues) with `enhancement` label

## Code of Conduct

Be respectful, constructive, and professional. We're all here to build something awesome together.

---

Thank you for contributing to Excel Agent! 🎉
