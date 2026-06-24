"""
Generate LiteLLM tool definitions for pandas Excel operations
Based on systematic discovery from previous steps
"""

import json
import pandas as pd

def generate_pandas_tools():
    """Generate comprehensive pandas tool definitions for LiteLLM"""

    tools = []

    # ==========================================
    # 1. EXCEL I/O OPERATIONS
    # ==========================================

    # Read Excel
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_read_excel",
            "description": "[PANDAS] Read an Excel file into a pandas DataFrame. Supports xlsx, xls, xlsm, xlsb, odf, ods and odt files. Can read single sheet, multiple sheets, or all sheets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "io": {
                        "type": "string",
                        "description": "Path to Excel file, URL, or file-like object"
                    },
                    "sheet_name": {
                        "type": ["string", "integer", "array", "null"],
                        "description": "Sheet name/index to read. None reads all sheets into dict"
                    },
                    "header": {
                        "type": ["integer", "array", "null"],
                        "description": "Row number(s) to use as column names"
                    },
                    "index_col": {
                        "type": ["integer", "string", "array", "null"],
                        "description": "Column(s) to use as row labels"
                    },
                    "usecols": {
                        "type": ["string", "array", "null"],
                        "description": "Columns to parse (e.g., 'A:E' or ['A', 'C', 'E'])"
                    },
                    "dtype": {
                        "type": ["object", "null"],
                        "description": "Data type for columns (dict mapping column names to types)"
                    },
                    "skiprows": {
                        "type": ["integer", "array", "null"],
                        "description": "Rows to skip at the beginning"
                    },
                    "nrows": {
                        "type": ["integer", "null"],
                        "description": "Number of rows to read"
                    },
                    "parse_dates": {
                        "type": ["boolean", "array", "object"],
                        "description": "Parse date columns"
                    }
                },
                "required": ["io"]
            }
        }
    })

    # Write Excel
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_to_excel",
            "description": "[PANDAS] Write DataFrame to an Excel file. Creates xlsx files with formatting options.",
            "parameters": {
                "type": "object",
                "properties": {
                    "excel_writer": {
                        "type": "string",
                        "description": "Path to Excel file or ExcelWriter object"
                    },
                    "sheet_name": {
                        "type": "string",
                        "description": "Name of sheet to write DataFrame to",
                        "default": "Sheet1"
                    },
                    "index": {
                        "type": "boolean",
                        "description": "Write row names/index",
                        "default": True
                    },
                    "columns": {
                        "type": ["array", "null"],
                        "description": "Columns to write (None writes all)"
                    },
                    "header": {
                        "type": ["boolean", "array"],
                        "description": "Write column names",
                        "default": True
                    },
                    "startrow": {
                        "type": "integer",
                        "description": "Upper left cell row to start writing",
                        "default": 0
                    },
                    "startcol": {
                        "type": "integer",
                        "description": "Upper left cell column to start writing",
                        "default": 0
                    },
                    "float_format": {
                        "type": ["string", "null"],
                        "description": "Format string for floating point numbers"
                    },
                    "freeze_panes": {
                        "type": ["array", "null"],
                        "description": "Tuple of (row, column) to freeze panes"
                    }
                },
                "required": ["excel_writer"]
            }
        }
    })

    # ExcelWriter Context Manager Start
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_excelwriter_create",
            "description": "[PANDAS] Create an ExcelWriter object for writing multiple DataFrames to Excel. Use this to write multiple sheets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to Excel file"
                    },
                    "engine": {
                        "type": ["string", "null"],
                        "description": "Excel writer engine (openpyxl, xlsxwriter)",
                    },
                    "mode": {
                        "type": "string",
                        "description": "File mode ('w' for write, 'a' for append)",
                        "default": "w"
                    },
                    "if_sheet_exists": {
                        "type": ["string", "null"],
                        "description": "How to handle existing sheets when appending ('error', 'new', 'replace', 'overlay')"
                    }
                },
                "required": ["path"]
            }
        }
    })

    # ExcelWriter Save/Close
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_excelwriter_close",
            "description": "[PANDAS] Save and close the ExcelWriter object. Must be called after writing all sheets.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    })

    # ==========================================
    # 2. DATA TRANSFORMATION OPERATIONS
    # ==========================================

    # Pivot Table
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_pivot_table",
            "description": "[PANDAS] Create a spreadsheet-style pivot table as a DataFrame. Aggregates data by grouping rows and columns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "values": {
                        "type": ["string", "array", "null"],
                        "description": "Column(s) to aggregate"
                    },
                    "index": {
                        "type": ["string", "array", "null"],
                        "description": "Column(s) to group by for rows"
                    },
                    "columns": {
                        "type": ["string", "array", "null"],
                        "description": "Column(s) to group by for columns"
                    },
                    "aggfunc": {
                        "type": ["string", "array", "object"],
                        "description": "Aggregation function(s) (mean, sum, count, etc.)",
                        "default": "mean"
                    },
                    "fill_value": {
                        "type": ["number", "string", "null"],
                        "description": "Value to replace missing values"
                    },
                    "margins": {
                        "type": "boolean",
                        "description": "Add row/column margins (subtotals)",
                        "default": False
                    }
                },
                "required": []
            }
        }
    })

    # Merge DataFrames
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_merge",
            "description": "[PANDAS] Merge two DataFrames using database-style join operations (similar to VLOOKUP in Excel).",
            "parameters": {
                "type": "object",
                "properties": {
                    "right": {
                        "type": "string",
                        "description": "Name/ID of the right DataFrame to merge"
                    },
                    "how": {
                        "type": "string",
                        "description": "Type of merge (left, right, outer, inner, cross)",
                        "default": "inner"
                    },
                    "on": {
                        "type": ["string", "array", "null"],
                        "description": "Column(s) to join on"
                    },
                    "left_on": {
                        "type": ["string", "array", "null"],
                        "description": "Column(s) from left DataFrame to join on"
                    },
                    "right_on": {
                        "type": ["string", "array", "null"],
                        "description": "Column(s) from right DataFrame to join on"
                    },
                    "suffixes": {
                        "type": "array",
                        "description": "Suffixes for overlapping columns",
                        "default": ["_x", "_y"]
                    }
                },
                "required": ["right"]
            }
        }
    })

    # Group By
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_groupby",
            "description": "[PANDAS] Group DataFrame by one or more columns and compute aggregate statistics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "by": {
                        "type": ["string", "array"],
                        "description": "Column(s) to group by"
                    },
                    "agg": {
                        "type": ["string", "array", "object"],
                        "description": "Aggregation operations (sum, mean, count, min, max, etc.)"
                    },
                    "as_index": {
                        "type": "boolean",
                        "description": "Use group labels as index",
                        "default": True
                    }
                },
                "required": ["by"]
            }
        }
    })

    # Sort Values
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_sort_values",
            "description": "[PANDAS] Sort DataFrame by one or more columns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "by": {
                        "type": ["string", "array"],
                        "description": "Column(s) to sort by"
                    },
                    "ascending": {
                        "type": ["boolean", "array"],
                        "description": "Sort ascending (True) or descending (False)",
                        "default": True
                    },
                    "na_position": {
                        "type": "string",
                        "description": "Where to place NaN values ('first' or 'last')",
                        "default": "last"
                    }
                },
                "required": ["by"]
            }
        }
    })

    # Filter/Query
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_query",
            "description": "[PANDAS] Filter DataFrame rows using a query expression (similar to Excel filters).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expr": {
                        "type": "string",
                        "description": "Query expression (e.g., 'Age > 30 and City == \"NYC\"')"
                    }
                },
                "required": ["expr"]
            }
        }
    })

    # Drop Duplicates
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_drop_duplicates",
            "description": "[PANDAS] Remove duplicate rows from DataFrame.",
            "parameters": {
                "type": "object",
                "properties": {
                    "subset": {
                        "type": ["array", "null"],
                        "description": "Column(s) to consider for duplicates"
                    },
                    "keep": {
                        "type": "string",
                        "description": "Which duplicates to keep ('first', 'last', False)",
                        "default": "first"
                    }
                },
                "required": []
            }
        }
    })

    # ==========================================
    # 3. DATA MANIPULATION OPERATIONS
    # ==========================================

    # Add Column
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_assign",
            "description": "[PANDAS] Add new column(s) to DataFrame with calculated values.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column_name": {
                        "type": "string",
                        "description": "Name of new column"
                    },
                    "expression": {
                        "type": "string",
                        "description": "Expression or value for new column"
                    }
                },
                "required": ["column_name", "expression"]
            }
        }
    })

    # Drop Columns
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_drop",
            "description": "[PANDAS] Drop specified columns or rows from DataFrame.",
            "parameters": {
                "type": "object",
                "properties": {
                    "labels": {
                        "type": ["string", "array"],
                        "description": "Column or row labels to drop"
                    },
                    "axis": {
                        "type": "integer",
                        "description": "0 for rows, 1 for columns",
                        "default": 1
                    }
                },
                "required": ["labels"]
            }
        }
    })

    # Rename Columns
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_rename",
            "description": "[PANDAS] Rename DataFrame columns or index.",
            "parameters": {
                "type": "object",
                "properties": {
                    "columns": {
                        "type": "object",
                        "description": "Dictionary mapping old names to new names"
                    }
                },
                "required": ["columns"]
            }
        }
    })

    # Fill Missing Values
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_fillna",
            "description": "[PANDAS] Fill missing values in DataFrame.",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": ["number", "string", "object", "null"],
                        "description": "Value to use for filling"
                    },
                    "method": {
                        "type": ["string", "null"],
                        "description": "Method for filling ('ffill', 'bfill')"
                    }
                },
                "required": []
            }
        }
    })

    # ==========================================
    # 4. STATISTICAL OPERATIONS
    # ==========================================

    # Describe Statistics
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_describe",
            "description": "[PANDAS] Generate descriptive statistics summary of DataFrame.",
            "parameters": {
                "type": "object",
                "properties": {
                    "include": {
                        "type": ["string", "array", "null"],
                        "description": "Data types to include ('all', 'number', 'object')"
                    },
                    "percentiles": {
                        "type": ["array", "null"],
                        "description": "Percentiles to include (default [.25, .5, .75])"
                    }
                },
                "required": []
            }
        }
    })

    # Correlation Matrix
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_corr",
            "description": "[PANDAS] Compute correlation matrix between numeric columns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "method": {
                        "type": "string",
                        "description": "Correlation method ('pearson', 'kendall', 'spearman')",
                        "default": "pearson"
                    }
                },
                "required": []
            }
        }
    })

    # Value Counts
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_value_counts",
            "description": "[PANDAS] Count unique values in a column (similar to Excel COUNTIF).",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {
                        "type": "string",
                        "description": "Column name to count values"
                    },
                    "normalize": {
                        "type": "boolean",
                        "description": "Return proportions instead of counts",
                        "default": False
                    },
                    "dropna": {
                        "type": "boolean",
                        "description": "Exclude NaN values",
                        "default": True
                    }
                },
                "required": ["column"]
            }
        }
    })

    # ==========================================
    # 5. RESHAPING OPERATIONS
    # ==========================================

    # Pivot (Simple)
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_pivot",
            "description": "[PANDAS] Reshape data using pivot (simpler than pivot_table, no aggregation).",
            "parameters": {
                "type": "object",
                "properties": {
                    "index": {
                        "type": ["string", "array"],
                        "description": "Column(s) to use as new index"
                    },
                    "columns": {
                        "type": "string",
                        "description": "Column to use for new columns"
                    },
                    "values": {
                        "type": ["string", "array", "null"],
                        "description": "Column(s) to use for values"
                    }
                },
                "required": ["columns"]
            }
        }
    })

    # Melt (Unpivot)
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_melt",
            "description": "[PANDAS] Unpivot DataFrame from wide to long format (opposite of pivot).",
            "parameters": {
                "type": "object",
                "properties": {
                    "id_vars": {
                        "type": ["string", "array", "null"],
                        "description": "Column(s) to use as ID variables"
                    },
                    "value_vars": {
                        "type": ["string", "array", "null"],
                        "description": "Column(s) to unpivot"
                    },
                    "var_name": {
                        "type": "string",
                        "description": "Name for variable column",
                        "default": "variable"
                    },
                    "value_name": {
                        "type": "string",
                        "description": "Name for value column",
                        "default": "value"
                    }
                },
                "required": []
            }
        }
    })

    # Stack
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_stack",
            "description": "[PANDAS] Stack columns into rows, creating a multi-level index.",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": ["integer", "string", "array"],
                        "description": "Level(s) to stack",
                        "default": -1
                    },
                    "dropna": {
                        "type": "boolean",
                        "description": "Drop rows with missing values",
                        "default": True
                    }
                },
                "required": []
            }
        }
    })

    # ==========================================
    # 6. UTILITY OPERATIONS
    # ==========================================

    # Create DataFrame
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_dataframe_create",
            "description": "[PANDAS] Create a new pandas DataFrame from data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": ["array", "object"],
                        "description": "Data for DataFrame (dict, list of lists, etc.)"
                    },
                    "columns": {
                        "type": ["array", "null"],
                        "description": "Column names"
                    },
                    "index": {
                        "type": ["array", "null"],
                        "description": "Row index labels"
                    }
                },
                "required": ["data"]
            }
        }
    })

    # Concat DataFrames
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_concat",
            "description": "[PANDAS] Concatenate multiple DataFrames along rows or columns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "objs": {
                        "type": "array",
                        "description": "List of DataFrame names/IDs to concatenate"
                    },
                    "axis": {
                        "type": "integer",
                        "description": "0 to concat rows, 1 to concat columns",
                        "default": 0
                    },
                    "ignore_index": {
                        "type": "boolean",
                        "description": "Reset index after concatenation",
                        "default": False
                    }
                },
                "required": ["objs"]
            }
        }
    })

    # Get Info
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_info",
            "description": "[PANDAS] Get concise summary of DataFrame including data types and memory usage.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    })

    # Get Shape
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_shape",
            "description": "[PANDAS] Get dimensions of DataFrame (rows, columns).",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    })

    # Head/Tail
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_head",
            "description": "[PANDAS] Get first n rows of DataFrame.",
            "parameters": {
                "type": "object",
                "properties": {
                    "n": {
                        "type": "integer",
                        "description": "Number of rows to return",
                        "default": 5
                    }
                },
                "required": []
            }
        }
    })

    # Sample
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_sample",
            "description": "[PANDAS] Get random sample of rows from DataFrame.",
            "parameters": {
                "type": "object",
                "properties": {
                    "n": {
                        "type": ["integer", "null"],
                        "description": "Number of rows to sample"
                    },
                    "frac": {
                        "type": ["number", "null"],
                        "description": "Fraction of rows to sample"
                    },
                    "random_state": {
                        "type": ["integer", "null"],
                        "description": "Random seed for reproducibility"
                    }
                },
                "required": []
            }
        }
    })

    # To CSV (for exporting)
    tools.append({
        "type": "function",
        "function": {
            "name": "pandas_to_csv",
            "description": "[PANDAS] Export DataFrame to CSV file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path_or_buf": {
                        "type": "string",
                        "description": "File path to write CSV"
                    },
                    "index": {
                        "type": "boolean",
                        "description": "Write row index",
                        "default": True
                    },
                    "sep": {
                        "type": "string",
                        "description": "Field delimiter",
                        "default": ","
                    }
                },
                "required": ["path_or_buf"]
            }
        }
    })

    return tools

def main():
    """Generate and save pandas tools"""

    print("=" * 60)
    print("Generating pandas Tools for LiteLLM")
    print("=" * 60)

    # Generate tools
    tools = generate_pandas_tools()

    print(f"\n✅ Generated {len(tools)} pandas tools")

    # Categorize tools
    categories = {
        'I/O': [],
        'Transform': [],
        'Manipulate': [],
        'Statistics': [],
        'Reshape': [],
        'Utility': []
    }

    for tool in tools:
        name = tool['function']['name']
        if 'read' in name or 'write' in name or 'excel' in name or 'csv' in name:
            categories['I/O'].append(name)
        elif any(x in name for x in ['pivot', 'merge', 'group', 'sort', 'query', 'filter', 'drop_dup']):
            categories['Transform'].append(name)
        elif any(x in name for x in ['assign', 'drop', 'rename', 'fill']):
            categories['Manipulate'].append(name)
        elif any(x in name for x in ['describe', 'corr', 'value_counts']):
            categories['Statistics'].append(name)
        elif any(x in name for x in ['melt', 'stack', 'pivot']):
            categories['Reshape'].append(name)
        else:
            categories['Utility'].append(name)

    print("\n📊 Tool Categories:")
    for category, tool_names in categories.items():
        print(f"  {category}: {len(tool_names)} tools")
        for name in tool_names[:3]:  # Show first 3
            print(f"    - {name}")
        if len(tool_names) > 3:
            print(f"    ... and {len(tool_names) - 3} more")

    # Save tools
    output = {
        "tools": tools,
        "metadata": {
            "total_count": len(tools),
            "categories": {k: len(v) for k, v in categories.items()},
            "description": "pandas tools for Excel-like operations with DataFrames"
        }
    }

    output_file = 'pandas_scripts/outputs/pandas_litellm_tools.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Saved to {output_file}")

    return output

if __name__ == "__main__":
    main()