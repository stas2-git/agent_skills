"""
pandas Tool Executor for LLM Integration
Executes pandas tool calls and manages DataFrame state
"""

import pandas as pd
import numpy as np
import json
import io
from typing import Any, Dict, Optional, List, Union

class PandasToolExecutor:
    """
    Executes pandas tool calls from LLM
    Manages DataFrame state and Excel operations
    """

    def __init__(self):
        """Initialize the pandas executor"""
        self.dataframes = {}  # Store DataFrames by ID
        self.excel_writers = {}  # Store ExcelWriter objects
        self.last_df_id = None  # Track last created/modified DataFrame
        self.df_counter = 0  # For generating unique DataFrame IDs

    def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a pandas tool based on the tool name and parameters

        Args:
            tool_name: Name of the pandas tool to execute
            params: Parameters for the tool

        Returns:
            Dict with status and result/error
        """
        try:
            # Remove 'pandas_' prefix if present
            if tool_name.startswith('pandas_'):
                method_name = tool_name[7:]  # Remove 'pandas_' prefix
            else:
                method_name = tool_name

            # Map tool name to executor method
            method = getattr(self, f'_execute_{method_name}', None)

            if method:
                result = method(params)
                return {'status': 'success', 'result': result}
            else:
                # Try to handle it generically
                return self._execute_generic(tool_name, params)

        except Exception as e:
            return {'status': 'error', 'error': str(e), 'tool': tool_name}

    def _get_dataframe(self, df_id: str = None) -> pd.DataFrame:
        """Get DataFrame by ID or return last DataFrame"""
        if df_id:
            if df_id in self.dataframes:
                return self.dataframes[df_id]
            else:
                raise ValueError(f"DataFrame '{df_id}' not found")
        elif self.last_df_id:
            return self.dataframes[self.last_df_id]
        else:
            raise ValueError("No DataFrame available")

    def _store_dataframe(self, df: pd.DataFrame, df_id: str = None) -> str:
        """Store DataFrame and return its ID"""
        if df_id is None:
            self.df_counter += 1
            df_id = f"df_{self.df_counter}"

        self.dataframes[df_id] = df
        self.last_df_id = df_id
        return df_id

    # ==========================================
    # I/O OPERATIONS
    # ==========================================

    def _execute_read_excel(self, params: Dict[str, Any]) -> str:
        """Read Excel file into DataFrame"""
        io_path = params.get('io')
        if not io_path:
            raise ValueError("'io' parameter required for read_excel")

        # Build kwargs from params
        kwargs = {}
        for key in ['sheet_name', 'header', 'index_col', 'usecols', 'dtype',
                    'skiprows', 'nrows', 'parse_dates']:
            if key in params:
                kwargs[key] = params[key]

        # Read Excel file
        result = pd.read_excel(io_path, **kwargs)

        # Handle multiple sheets (returns dict)
        if isinstance(result, dict):
            # Store each sheet as separate DataFrame
            sheet_ids = []
            for sheet_name, df in result.items():
                df_id = self._store_dataframe(df, f"sheet_{sheet_name}")
                sheet_ids.append(f"{sheet_name}: {df_id}")
            return f"Read {len(result)} sheets: {', '.join(sheet_ids)}"
        else:
            # Single DataFrame
            df_id = self._store_dataframe(result)
            return f"Read Excel file into {df_id} with shape {result.shape}"

    def _execute_to_excel(self, params: Dict[str, Any]) -> str:
        """Write DataFrame to Excel file"""
        excel_writer = params.get('excel_writer')
        if not excel_writer:
            raise ValueError("'excel_writer' parameter required")

        # Get DataFrame
        df = self._get_dataframe(params.get('dataframe_id'))

        # Build kwargs
        kwargs = {}
        for key in ['sheet_name', 'index', 'columns', 'header', 'startrow',
                    'startcol', 'float_format', 'freeze_panes']:
            if key in params:
                kwargs[key] = params[key]

        # Check if excel_writer is a writer ID or file path
        if excel_writer in self.excel_writers:
            writer = self.excel_writers[excel_writer]
        else:
            writer = excel_writer

        # Write to Excel
        df.to_excel(writer, **kwargs)

        return f"Wrote DataFrame to {excel_writer}"

    def _execute_excelwriter_create(self, params: Dict[str, Any]) -> str:
        """Create ExcelWriter object"""
        path = params.get('path')
        if not path:
            raise ValueError("'path' parameter required")

        # Build kwargs
        kwargs = {}

        # Append mode requires openpyxl engine (pandas requirement)
        if params.get('mode') == 'a':
            kwargs['engine'] = 'openpyxl'
        elif params.get('engine'):
            kwargs['engine'] = params['engine']

        for key in ['mode', 'if_sheet_exists']:
            if key in params and params[key] is not None:
                kwargs[key] = params[key]

        # Create ExcelWriter
        writer = pd.ExcelWriter(path, **kwargs)

        # Store writer
        writer_id = f"writer_{len(self.excel_writers) + 1}"
        self.excel_writers[writer_id] = writer

        return f"Created ExcelWriter {writer_id} for {path}"

    def _execute_excelwriter_close(self, params: Dict[str, Any]) -> str:
        """Close ExcelWriter object"""
        writer_id = params.get('writer_id', None)

        if writer_id and writer_id in self.excel_writers:
            writer = self.excel_writers[writer_id]
            writer.close()
            del self.excel_writers[writer_id]
            return f"Closed and saved ExcelWriter {writer_id}"
        elif self.excel_writers:
            # Close the most recent writer
            writer_id = list(self.excel_writers.keys())[-1]
            writer = self.excel_writers[writer_id]
            writer.close()
            del self.excel_writers[writer_id]
            return f"Closed and saved ExcelWriter {writer_id}"
        else:
            raise ValueError("No ExcelWriter to close")

    # ==========================================
    # DATA TRANSFORMATION OPERATIONS
    # ==========================================

    def _execute_pivot_table(self, params: Dict[str, Any]) -> str:
        """Create pivot table"""
        df = self._get_dataframe(params.get('dataframe_id'))

        kwargs = {}
        for key in ['values', 'index', 'columns', 'aggfunc', 'fill_value', 'margins']:
            if key in params:
                kwargs[key] = params[key]

        result = df.pivot_table(**kwargs)
        df_id = self._store_dataframe(result)

        return f"Created pivot table {df_id} with shape {result.shape}"

    def _execute_merge(self, params: Dict[str, Any]) -> str:
        """Merge two DataFrames"""
        left_df = self._get_dataframe(params.get('left_id'))
        right_df = self._get_dataframe(params.get('right'))

        kwargs = {}
        for key in ['how', 'on', 'left_on', 'right_on', 'suffixes']:
            if key in params:
                kwargs[key] = params[key]

        result = left_df.merge(right_df, **kwargs)
        df_id = self._store_dataframe(result)

        return f"Merged DataFrames into {df_id} with shape {result.shape}"

    def _execute_groupby(self, params: Dict[str, Any]) -> str:
        """Group by and aggregate"""
        df = self._get_dataframe(params.get('dataframe_id'))

        by = params.get('by')
        if not by:
            raise ValueError("'by' parameter required for groupby")

        # Perform groupby
        grouped = df.groupby(by, as_index=params.get('as_index', True))

        # Apply aggregation
        agg = params.get('agg', 'mean')
        if agg:
            result = grouped.agg(agg)
        else:
            result = grouped.mean()  # Default to mean

        df_id = self._store_dataframe(result)
        return f"Grouped by {by} into {df_id} with shape {result.shape}"

    def _execute_sort_values(self, params: Dict[str, Any]) -> str:
        """Sort DataFrame values"""
        df = self._get_dataframe(params.get('dataframe_id'))

        by = params.get('by')
        if not by:
            raise ValueError("'by' parameter required for sort_values")

        kwargs = {'by': by}
        for key in ['ascending', 'na_position']:
            if key in params:
                kwargs[key] = params[key]

        result = df.sort_values(**kwargs)
        df_id = self._store_dataframe(result)

        return f"Sorted DataFrame by {by} into {df_id}"

    def _execute_query(self, params: Dict[str, Any]) -> str:
        """Filter DataFrame with query"""
        df = self._get_dataframe(params.get('dataframe_id'))

        expr = params.get('expr')
        if not expr:
            raise ValueError("'expr' parameter required for query")

        result = df.query(expr)
        df_id = self._store_dataframe(result)

        return f"Filtered DataFrame into {df_id} with {len(result)} rows (from {len(df)} rows)"

    def _execute_drop_duplicates(self, params: Dict[str, Any]) -> str:
        """Drop duplicate rows"""
        df = self._get_dataframe(params.get('dataframe_id'))

        kwargs = {}
        for key in ['subset', 'keep']:
            if key in params:
                kwargs[key] = params[key]

        result = df.drop_duplicates(**kwargs)
        df_id = self._store_dataframe(result)

        rows_dropped = len(df) - len(result)
        return f"Dropped {rows_dropped} duplicate rows, result in {df_id}"

    # ==========================================
    # DATA MANIPULATION OPERATIONS
    # ==========================================

    def _execute_assign(self, params: Dict[str, Any]) -> str:
        """Add new column to DataFrame"""
        df = self._get_dataframe(params.get('dataframe_id'))

        column_name = params.get('column_name')
        expression = params.get('expression')

        if not column_name or expression is None:
            raise ValueError("'column_name' and 'expression' required")

        # Handle expression evaluation
        if isinstance(expression, str):
            # Try to evaluate as pandas expression
            try:
                # If it references other columns, use eval
                if any(col in expression for col in df.columns):
                    df[column_name] = df.eval(expression)
                else:
                    # Otherwise treat as literal value
                    df[column_name] = expression
            except:
                # Fallback to literal value
                df[column_name] = expression
        else:
            df[column_name] = expression

        df_id = self._store_dataframe(df)
        return f"Added column '{column_name}' to {df_id}"

    def _execute_drop(self, params: Dict[str, Any]) -> str:
        """Drop columns or rows"""
        df = self._get_dataframe(params.get('dataframe_id'))

        labels = params.get('labels')
        if not labels:
            raise ValueError("'labels' parameter required")

        axis = params.get('axis', 1)
        result = df.drop(labels=labels, axis=axis)
        df_id = self._store_dataframe(result)

        axis_name = 'columns' if axis == 1 else 'rows'
        return f"Dropped {labels} from {axis_name}, result in {df_id}"

    def _execute_rename(self, params: Dict[str, Any]) -> str:
        """Rename columns"""
        df = self._get_dataframe(params.get('dataframe_id'))

        columns = params.get('columns')
        if not columns:
            raise ValueError("'columns' parameter required")

        result = df.rename(columns=columns)
        df_id = self._store_dataframe(result)

        return f"Renamed columns in {df_id}"

    def _execute_fillna(self, params: Dict[str, Any]) -> str:
        """Fill missing values"""
        df = self._get_dataframe(params.get('dataframe_id'))

        kwargs = {}
        for key in ['value', 'method']:
            if key in params and params[key] is not None:
                kwargs[key] = params[key]

        result = df.fillna(**kwargs)
        df_id = self._store_dataframe(result)

        return f"Filled missing values in {df_id}"

    # ==========================================
    # STATISTICAL OPERATIONS
    # ==========================================

    def _execute_describe(self, params: Dict[str, Any]) -> str:
        """Get descriptive statistics"""
        df = self._get_dataframe(params.get('dataframe_id'))

        kwargs = {}
        for key in ['include', 'percentiles']:
            if key in params:
                kwargs[key] = params[key]

        result = df.describe(**kwargs)
        df_id = self._store_dataframe(result)

        return f"Generated statistics in {df_id} with shape {result.shape}"

    def _execute_corr(self, params: Dict[str, Any]) -> str:
        """Calculate correlation matrix"""
        df = self._get_dataframe(params.get('dataframe_id'))

        method = params.get('method', 'pearson')
        result = df.corr(method=method)
        df_id = self._store_dataframe(result)

        return f"Calculated correlation matrix in {df_id} with shape {result.shape}"

    def _execute_value_counts(self, params: Dict[str, Any]) -> str:
        """Count unique values in column"""
        df = self._get_dataframe(params.get('dataframe_id'))

        column = params.get('column')
        if not column:
            raise ValueError("'column' parameter required")

        kwargs = {}
        for key in ['normalize', 'dropna']:
            if key in params:
                kwargs[key] = params[key]

        result = df[column].value_counts(**kwargs)

        # Convert Series to DataFrame
        result_df = result.to_frame(name='count')
        df_id = self._store_dataframe(result_df)

        return f"Value counts for '{column}' in {df_id} with {len(result)} unique values"

    # ==========================================
    # RESHAPING OPERATIONS
    # ==========================================

    def _execute_pivot(self, params: Dict[str, Any]) -> str:
        """Pivot DataFrame"""
        df = self._get_dataframe(params.get('dataframe_id'))

        kwargs = {}
        for key in ['index', 'columns', 'values']:
            if key in params:
                kwargs[key] = params[key]

        result = df.pivot(**kwargs)
        df_id = self._store_dataframe(result)

        return f"Pivoted DataFrame into {df_id} with shape {result.shape}"

    def _execute_melt(self, params: Dict[str, Any]) -> str:
        """Melt DataFrame from wide to long format"""
        df = self._get_dataframe(params.get('dataframe_id'))

        kwargs = {}
        for key in ['id_vars', 'value_vars', 'var_name', 'value_name']:
            if key in params:
                kwargs[key] = params[key]

        result = df.melt(**kwargs)
        df_id = self._store_dataframe(result)

        return f"Melted DataFrame into {df_id} with shape {result.shape}"

    def _execute_stack(self, params: Dict[str, Any]) -> str:
        """Stack DataFrame"""
        df = self._get_dataframe(params.get('dataframe_id'))

        kwargs = {}
        for key in ['level', 'dropna']:
            if key in params:
                kwargs[key] = params[key]

        result = df.stack(**kwargs)

        # Convert Series to DataFrame if needed
        if isinstance(result, pd.Series):
            result = result.to_frame()

        df_id = self._store_dataframe(result)
        return f"Stacked DataFrame into {df_id}"

    # ==========================================
    # UTILITY OPERATIONS
    # ==========================================

    def _execute_dataframe_create(self, params: Dict[str, Any]) -> str:
        """Create new DataFrame"""
        data = params.get('data')
        if data is None:
            raise ValueError("'data' parameter required")

        kwargs = {'data': data}
        for key in ['columns', 'index']:
            if key in params:
                kwargs[key] = params[key]

        df = pd.DataFrame(**kwargs)
        df_id = self._store_dataframe(df)

        return f"Created DataFrame {df_id} with shape {df.shape}"

    def _execute_concat(self, params: Dict[str, Any]) -> str:
        """Concatenate multiple DataFrames"""
        objs = params.get('objs')
        if not objs:
            raise ValueError("'objs' parameter required")

        # Get DataFrames
        dfs = [self._get_dataframe(df_id) for df_id in objs]

        kwargs = {}
        for key in ['axis', 'ignore_index']:
            if key in params:
                kwargs[key] = params[key]

        result = pd.concat(dfs, **kwargs)
        df_id = self._store_dataframe(result)

        return f"Concatenated {len(objs)} DataFrames into {df_id} with shape {result.shape}"

    def _execute_info(self, params: Dict[str, Any]) -> str:
        """Get DataFrame info"""
        df = self._get_dataframe(params.get('dataframe_id'))

        # Capture info output
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()

        return f"DataFrame Info:\n{info_str}"

    def _execute_shape(self, params: Dict[str, Any]) -> str:
        """Get DataFrame shape"""
        df = self._get_dataframe(params.get('dataframe_id'))
        return f"Shape: {df.shape} (rows: {df.shape[0]}, columns: {df.shape[1]})"

    def _execute_head(self, params: Dict[str, Any]) -> str:
        """Get first n rows"""
        df = self._get_dataframe(params.get('dataframe_id'))
        n = params.get('n', 5)

        result = df.head(n)

        # Return as string representation
        return f"First {n} rows:\n{result.to_string()}"

    def _execute_sample(self, params: Dict[str, Any]) -> str:
        """Get random sample"""
        df = self._get_dataframe(params.get('dataframe_id'))

        kwargs = {}
        for key in ['n', 'frac', 'random_state']:
            if key in params and params[key] is not None:
                kwargs[key] = params[key]

        result = df.sample(**kwargs)
        df_id = self._store_dataframe(result)

        return f"Sampled {len(result)} rows into {df_id}"

    def _execute_to_csv(self, params: Dict[str, Any]) -> str:
        """Export DataFrame to CSV"""
        df = self._get_dataframe(params.get('dataframe_id'))

        path_or_buf = params.get('path_or_buf')
        if not path_or_buf:
            raise ValueError("'path_or_buf' parameter required")

        kwargs = {'path_or_buf': path_or_buf}
        for key in ['index', 'sep']:
            if key in params:
                kwargs[key] = params[key]

        df.to_csv(**kwargs)
        return f"Exported DataFrame to CSV: {path_or_buf}"

    # ==========================================
    # GENERIC HANDLER
    # ==========================================

    def _execute_generic(self, tool_name: str, params: Dict[str, Any]) -> str:
        """Generic handler for DataFrame methods not explicitly implemented"""
        df = self._get_dataframe(params.get('dataframe_id'))

        # Try to call the method on the DataFrame
        if hasattr(df, tool_name):
            method = getattr(df, tool_name)
            if callable(method):
                result = method(**params)

                if isinstance(result, pd.DataFrame):
                    df_id = self._store_dataframe(result)
                    return f"Executed {tool_name}, result in {df_id}"
                else:
                    return f"Executed {tool_name}: {str(result)}"

        raise ValueError(f"Unknown tool: {tool_name}")

    def _execute_list_dataframes(self, params: Dict[str, Any]) -> str:
        """List all DataFrames currently in memory"""
        if not self.dataframes:
            return "No DataFrames currently in memory"

        result = {}
        for df_id, df in self.dataframes.items():
            result[df_id] = {
                'shape': list(df.shape),  # Convert tuple to list for JSON
                'columns': list(df.columns),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
            }

        return json.dumps(result, indent=2)

    def _execute_get_active(self, params: Dict[str, Any]) -> str:
        """Get information about the currently active DataFrame"""
        if not self.last_df_id:
            return "No active DataFrame. Use pandas_read_excel or pandas_dataframe_create first."

        df = self.dataframes[self.last_df_id]

        info = {
            'dataframe_id': self.last_df_id,
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
            'head': df.head().to_dict(orient='records'),
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB",
            'null_counts': df.isnull().sum().to_dict()
        }

        return json.dumps(info, indent=2)

    def _execute_set_active(self, params: Dict[str, Any]) -> str:
        """Set a specific DataFrame as the active one"""
        df_id = params.get('dataframe_id')
        if not df_id:
            raise ValueError("'dataframe_id' parameter is required")

        if df_id not in self.dataframes:
            available_dfs = list(self.dataframes.keys())
            return f"Error: DataFrame '{df_id}' not found. Available DataFrames: {available_dfs}"

        self.last_df_id = df_id
        df = self.dataframes[df_id]
        return f"Set DataFrame '{df_id}' as active (shape: {df.shape}, columns: {list(df.columns)[:5]}{'...' if len(df.columns) > 5 else ''})"

    def get_state(self) -> Dict[str, Any]:
        """Get current state of the executor"""
        return {
            'dataframes': list(self.dataframes.keys()),
            'excel_writers': list(self.excel_writers.keys()),
            'last_df_id': self.last_df_id,
            'total_dataframes': len(self.dataframes)
        }

    def clear_state(self):
        """Clear all stored DataFrames and writers"""
        # Close any open writers
        for writer in self.excel_writers.values():
            try:
                writer.close()
            except:
                pass

        self.dataframes.clear()
        self.excel_writers.clear()
        self.last_df_id = None
        self.df_counter = 0