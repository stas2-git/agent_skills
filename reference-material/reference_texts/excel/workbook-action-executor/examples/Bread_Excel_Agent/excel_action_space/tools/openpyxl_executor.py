"""
Tool Executor for openpyxl
Maps LLM tool calls to actual openpyxl functions
"""

import json
import openpyxl
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, GradientFill, Border, Side, Alignment, Protection
from openpyxl.chart import BarChart, LineChart, PieChart, ScatterChart, AreaChart, Reference
from openpyxl.drawing.image import Image
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, IconSetRule, DataBarRule
from openpyxl.utils import get_column_letter, column_index_from_string, coordinate_to_tuple, range_boundaries

from .utils import convert_value_type


# Number format preset mapping for compression
NUMBER_FORMAT_PRESETS = {
    "_(* #,##0_);_(* \\(#,##0\\);_(* \"-\"_);_(@_)": "accounting",
    "_($* #,##0_);_($* \\(#,##0\\);_($* \"-\"_);_(@_)": "accounting_usd",
    "0.00%": "percentage",
    "0%": "percentage_whole",
    "$#,##0.00": "currency",
    "$#,##0": "currency_whole",
    "m/d/yy": "date_short",
    "mm/dd/yyyy": "date_long",
    "d-mmm-yy": "date_medium",
    "h:mm AM/PM": "time_12h",
    "h:mm:ss": "time_24h",
    "#,##0": "number_comma",
    "#,##0.00": "number_comma_2dec",
    "0.00": "number_2dec",
    "General": None  # Omit if General
}

# Reverse lookup for applying styles by preset name
PRESET_TO_FORMAT = {v: k for k, v in NUMBER_FORMAT_PRESETS.items() if v}


class OpenpyxlToolExecutor:
    """
    Executes openpyxl tool calls from LLM
    Maintains state between calls (workbook, active sheet, etc.)
    """

    def __init__(self):
        self.workbook = None
        self.active_sheet = None
        self.created_objects = {}  # Store created objects like charts, styles, etc.
        self.last_result = None
        self.current_filename = None  # Track loaded file path
        self.modified = False  # Track if changes made since last save
        self.style_palette = {}  # Store style palette for compressed format

    def execute_tool(self, tool_name, arguments):
        """
        Execute a tool call and return the result

        Args:
            tool_name: Name of the tool (e.g., 'openpyxl_load_workbook')
            arguments: Dictionary of arguments from the LLM

        Returns:
            Dict with status and result/error
        """
        try:
            # Remove the 'openpyxl_' prefix if present
            if tool_name.startswith('openpyxl_'):
                tool_name = tool_name[9:]  # Remove 'openpyxl_' prefix

            # Map tool names to actual functions
            if tool_name == 'load_workbook':
                result = self._load_workbook(**arguments)
            elif tool_name == 'workbook' or tool_name == 'create_workbook':
                result = self._create_workbook(**arguments)
            elif tool_name == 'workbook_save':
                result = self._save_workbook(**arguments)
            elif tool_name == 'workbook_close':
                result = self._close_workbook(**arguments)
            elif tool_name == 'check_workbook_status':
                result = self._check_workbook_status()
            elif tool_name == 'workbook_create_sheet':
                result = self._create_sheet(**arguments)
            elif tool_name == 'workbook_remove':
                result = self._remove_sheet(**arguments)
            elif tool_name == 'workbook_copy_worksheet':
                result = self._copy_worksheet(**arguments)
            elif tool_name == 'worksheet_append':
                result = self._append_row(**arguments)
            elif tool_name == 'worksheet_cell':
                result = self._access_cell(**arguments)
            elif tool_name == 'worksheet_insert_rows':
                result = self._insert_rows(**arguments)
            elif tool_name == 'worksheet_delete_rows':
                result = self._delete_rows(**arguments)
            elif tool_name == 'worksheet_insert_cols':
                result = self._insert_cols(**arguments)
            elif tool_name == 'worksheet_delete_cols':
                result = self._delete_cols(**arguments)
            elif tool_name == 'worksheet_merge_cells':
                result = self._merge_cells(**arguments)
            elif tool_name == 'worksheet_unmerge_cells':
                result = self._unmerge_cells(**arguments)
            elif tool_name == 'worksheet_iter_rows':
                result = self._iter_rows(**arguments)
            elif tool_name == 'worksheet_get_item':
                result = self._get_worksheet_item(**arguments)
            elif tool_name == 'workbook_get_item':
                result = self._get_workbook_item(**arguments)
            elif tool_name == 'workbook_list_sheets':
                result = self._list_sheets()
            elif tool_name == 'worksheet_iter_cols':
                result = self._iter_cols(**arguments)
            elif tool_name == 'worksheet_set_item':
                result = self._set_worksheet_item(**arguments)
            elif tool_name == 'worksheet_fill_formula':
                result = self._fill_formula(**arguments)
            elif tool_name == 'cell_set_style':
                result = self._cell_set_style(**arguments)
            elif tool_name == 'worksheet_add_data_validation':
                result = self._add_data_validation(**arguments)
            elif tool_name.endswith('_add_data'):
                # Handle chart add_data methods
                chart_type = tool_name.replace('_add_data', '')
                # Extract chart_id from arguments and pass it along with chart_type
                chart_id = arguments.pop('chart_id', None)
                if not chart_id:
                    raise ValueError("chart_id is required for chart add_data operations")
                result = self._chart_add_data(chart_type, chart_id, **arguments)
            elif tool_name.endswith('_set_categories'):
                # Handle chart set_categories methods
                chart_type = tool_name.replace('_set_categories', '')
                # Extract chart_id from arguments and pass it along with chart_type
                chart_id = arguments.pop('chart_id', None)
                if not chart_id:
                    raise ValueError("chart_id is required for chart set_categories operations")
                result = self._chart_set_categories(chart_type, chart_id, **arguments)
            elif tool_name.startswith('create_'):
                # Handle all style/chart/advanced object creation
                result = self._create_object(tool_name, **arguments)
            elif tool_name == 'list_charts':
                result = self._list_charts()
            elif tool_name == 'get_chart_info':
                result = self._get_chart_info(**arguments)
            elif tool_name == 'get_worksheet_charts':
                result = self._get_worksheet_charts()
            elif tool_name == 'get_sheet_complete':
                result = self._get_sheet_complete(**arguments)
            elif tool_name == 'add_conditional_formatting':
                result = self._add_conditional_formatting(**arguments)
            elif tool_name == 'worksheet_add_chart':
                result = self._add_chart(**arguments)
            elif tool_name == 'worksheet_add_image':
                result = self._add_image(**arguments)
            elif tool_name == 'worksheet_add_table':
                result = self._add_table(**arguments)
            elif tool_name == 'get_column_letter':
                # Convert col_idx to int if it's a string
                if 'col_idx' in arguments and isinstance(arguments['col_idx'], str):
                    arguments['col_idx'] = int(arguments['col_idx'])
                result = get_column_letter(**arguments)
            elif tool_name == 'column_index_from_string':
                result = column_index_from_string(**arguments)
            elif tool_name == 'coordinate_to_tuple':
                result = coordinate_to_tuple(**arguments)
            elif tool_name == 'range_boundaries':
                result = range_boundaries(**arguments)
            # New worksheet feature tools
            elif tool_name == 'cell_set_number_format':
                result = self._set_number_format(**arguments)
            elif tool_name == 'worksheet_set_column_width':
                result = self._set_column_width(**arguments)
            elif tool_name == 'worksheet_set_row_height':
                result = self._set_row_height(**arguments)
            elif tool_name == 'worksheet_set_auto_filter':
                result = self._set_auto_filter(**arguments)
            elif tool_name == 'cell_add_comment':
                result = self._add_comment(**arguments)
            elif tool_name == 'cell_add_hyperlink':
                result = self._add_hyperlink(**arguments)
            elif tool_name == 'worksheet_freeze_panes':
                result = self._freeze_panes(**arguments)
            elif tool_name == 'workbook_define_name':
                result = self._define_name(**arguments)
            elif tool_name == 'worksheet_set_protection':
                result = self._set_protection(**arguments)
            elif tool_name == 'worksheet_set_visibility':
                result = self._set_visibility(**arguments)
            else:
                return {
                    'status': 'error',
                    'error': f'Unknown tool: {tool_name}'
                }

            return {
                'status': 'success',
                'result': str(result) if result is not None else 'Operation completed'
            }

        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

    # Core workbook operations
    def _create_workbook(self, **kwargs):
        """Create a new workbook"""
        self.workbook = Workbook()
        self.active_sheet = self.workbook.active
        self.modified = True
        return "Created new workbook"

    def _load_workbook(self, filename, **kwargs):
        """Load an existing workbook"""
        # Convert string boolean parameters to actual booleans
        for key in ['read_only', 'keep_vba', 'data_only', 'keep_links', 'rich_text']:
            if key in kwargs and isinstance(kwargs[key], str):
                kwargs[key] = kwargs[key].lower() in ['true', '1', 'yes']

        self.workbook = load_workbook(filename, **kwargs)
        self.active_sheet = self.workbook.active
        self.current_filename = filename
        self.modified = False
        return f"Loaded workbook: {filename}"

    def _save_workbook(self, filename, **kwargs):
        """Save the current workbook"""
        if self.workbook is None:
            raise ValueError("No workbook loaded. Use openpyxl_load_workbook first or check status with openpyxl_check_workbook_status.")

        # Pre-flight checks before attempting save
        # Check if workbook is in read-only mode
        if getattr(self.workbook, 'read_only', False):
            raise ValueError(
                f"Cannot save - workbook is in read-only mode. "
                f"Close and reload '{self.current_filename}' with read_only=False before making changes."
            )

        # Check if workbook is in data_only mode
        if getattr(self.workbook, 'data_only', False):
            raise ValueError(
                f"Cannot save - workbook is in data_only mode. "
                f"Close and reload '{self.current_filename}' with data_only=False before making changes."
            )

        # Try to save - may still fail due to permissions or file locks
        try:
            self.workbook.save(filename)
            self.modified = False
            return f"Saved workbook as: {filename}"
        except (IOError, ValueError, PermissionError, AttributeError) as e:
            # Save failed - provide helpful error
            error_msg = str(e).lower()

            # Check if it's a file handle issue
            if 'i/o operation' in error_msg or 'closed file' in error_msg:
                raise ValueError(
                    f"CRITICAL: Cannot save - workbook file handle is broken/closed. "
                    f"This usually happens after bridge operations or when Excel opened the file externally. "
                    f"Your changes are LOST. You must:\n"
                    f"1. Close this workbook\n"
                    f"2. Reload '{self.current_filename}' fresh\n"
                    f"3. Redo your changes\n"
                    f"Original error: {str(e)}"
                )
            elif 'permission' in error_msg or 'read' in error_msg:
                raise ValueError(
                    f"Cannot save - file is locked or read-only. "
                    f"Close and reload '{self.current_filename}' with read_only=False.\n"
                    f"Original error: {str(e)}"
                )
            else:
                # Some other error
                raise ValueError(f"Failed to save workbook: {str(e)}")

    def _close_workbook(self, **kwargs):
        """Close the current workbook"""
        if self.workbook:
            self.workbook.close()
            self.workbook = None
            self.active_sheet = None
            self.current_filename = None
            self.modified = False
        return "Closed workbook"

    def _check_workbook_status(self):
        """Check current workbook state"""
        # Check if workbook is read-only
        is_read_only = False
        if self.workbook is not None:
            # Check if workbook has read_only attribute set
            is_read_only = getattr(self.workbook, 'read_only', False)
            # Also check if it's data_only mode
            is_data_only = getattr(self.workbook, 'data_only', False)
            if is_data_only:
                is_read_only = True  # data_only also blocks saving

        return {
            'is_open': self.workbook is not None,
            'filename': self.current_filename,
            'active_sheet': self.workbook.active.title if self.workbook else None,
            'sheets': self.workbook.sheetnames if self.workbook else [],
            'has_unsaved_changes': self.modified,
            'is_read_only': is_read_only,
            'warning': 'Workbook is in read-only mode - cannot save changes!' if is_read_only else None
        }

    # Sheet operations
    def _create_sheet(self, title=None, index=None):
        """Create a new sheet"""
        if not self.workbook:
            raise ValueError("No workbook loaded")
        sheet = self.workbook.create_sheet(title=title, index=index)
        self.active_sheet = sheet
        self.modified = True
        return f"Created sheet: {sheet.title}"

    def _remove_sheet(self, sheet=None):
        """Remove a sheet"""
        if not self.workbook:
            raise ValueError("No workbook loaded")
        if sheet is None:
            sheet = self.active_sheet
        elif isinstance(sheet, str):
            sheet = self.workbook[sheet]
        self.workbook.remove(sheet)
        self.active_sheet = self.workbook.active
        return "Removed sheet"

    def _copy_worksheet(self, from_worksheet=None):
        """Copy a worksheet"""
        if not self.workbook:
            raise ValueError("No workbook loaded")
        if from_worksheet is None:
            from_worksheet = self.active_sheet
        elif isinstance(from_worksheet, str):
            from_worksheet = self.workbook[from_worksheet]
        new_sheet = self.workbook.copy_worksheet(from_worksheet)
        self.active_sheet = new_sheet
        self.modified = True
        return f"Copied worksheet to: {new_sheet.title}"

    # Cell operations
    def _append_row(self, iterable):
        """Append a row of data"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Handle case where iterable comes as a string representation of a list
        if isinstance(iterable, str):
            try:
                import ast
                iterable = ast.literal_eval(iterable)
            except:
                pass  # Keep as string if parsing fails

        self.active_sheet.append(iterable)
        self.modified = True
        return f"Appended row with {len(iterable)} values"

    def _access_cell(self, row, column, value=None):
        """Access or set a cell value"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Convert string parameters to integers
        row = int(row) if isinstance(row, str) else row
        column = int(column) if isinstance(column, str) else column

        cell = self.active_sheet.cell(row=row, column=column)
        if value is not None:
            cell.value = value
            self.modified = True
            return f"Set cell ({row},{column}) to: {value}"
        return f"Cell ({row},{column}) value: {cell.value}"

    def _insert_rows(self, idx, amount=1):
        """Insert rows"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Convert string parameters to integers
        idx = int(idx) if isinstance(idx, str) else idx
        amount = int(amount) if isinstance(amount, str) else amount

        self.active_sheet.insert_rows(idx=idx, amount=amount)
        self.modified = True
        return f"Inserted {amount} row(s) at position {idx}"

    def _delete_rows(self, idx, amount=1):
        """Delete rows"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Convert string parameters to integers
        idx = int(idx) if isinstance(idx, str) else idx
        amount = int(amount) if isinstance(amount, str) else amount

        self.active_sheet.delete_rows(idx=idx, amount=amount)
        self.modified = True
        return f"Deleted {amount} row(s) at position {idx}"

    def _insert_cols(self, idx, amount=1):
        """Insert columns"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Convert string parameters to integers
        idx = int(idx) if isinstance(idx, str) else idx
        amount = int(amount) if isinstance(amount, str) else amount

        self.active_sheet.insert_cols(idx=idx, amount=amount)
        self.modified = True
        return f"Inserted {amount} column(s) at position {idx}"

    def _delete_cols(self, idx, amount=1):
        """Delete columns"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Convert string parameters to integers
        idx = int(idx) if isinstance(idx, str) else idx
        amount = int(amount) if isinstance(amount, str) else amount

        self.active_sheet.delete_cols(idx=idx, amount=amount)
        self.modified = True
        return f"Deleted {amount} column(s) at position {idx}"

    def _merge_cells(self, range_string=None, start_row=None, start_column=None,
                     end_row=None, end_column=None):
        """Merge cells"""
        if not self.active_sheet:
            raise ValueError("No active sheet")
        self.active_sheet.merge_cells(range_string=range_string,
                                     start_row=start_row, start_column=start_column,
                                     end_row=end_row, end_column=end_column)
        self.modified = True
        self.modified = True
        return f"Merged cells"

    def _unmerge_cells(self, range_string=None, start_row=None, start_column=None,
                       end_row=None, end_column=None):
        """Unmerge cells"""
        if not self.active_sheet:
            raise ValueError("No active sheet")
        self.active_sheet.unmerge_cells(range_string=range_string,
                                       start_row=start_row, start_column=start_column,
                                       end_row=end_row, end_column=end_column)
        return f"Unmerged cells"

    # Additional worksheet/workbook operations
    def _iter_rows(self, min_row=None, max_row=None, min_col=None, max_col=None, values_only=False):
        """Iterate through rows - direct call to openpyxl worksheet.iter_rows()"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Convert string parameters to proper types
        if min_row is not None:
            min_row = int(min_row) if isinstance(min_row, str) else min_row
        if max_row is not None:
            max_row = int(max_row) if isinstance(max_row, str) else max_row
        if min_col is not None:
            min_col = int(min_col) if isinstance(min_col, str) else min_col
        if max_col is not None:
            max_col = int(max_col) if isinstance(max_col, str) else max_col
        if isinstance(values_only, str):
            values_only = values_only.lower() in ['true', '1', 'yes']

        # Direct call to openpyxl's iter_rows method
        rows = list(self.active_sheet.iter_rows(
            min_row=min_row, max_row=max_row,
            min_col=min_col, max_col=max_col,
            values_only=values_only
        ))

        return str(rows)

    def _get_worksheet_item(self, key):
        """Direct call to worksheet['A1'] - openpyxl's __getitem__"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Direct call to openpyxl's worksheet.__getitem__
        cell_or_range = self.active_sheet[key]

        # Check if single cell or range
        if hasattr(cell_or_range, 'value'):
            return f"Cell {key} value: {cell_or_range.value}"
        else:
            # It's a range - extract values
            values = [[cell.value for cell in row] for row in cell_or_range]
            return f"Range {key} values: {values}"

    def _get_workbook_item(self, key):
        """Direct call to workbook['SheetName'] - openpyxl's __getitem__"""
        if not self.workbook:
            raise ValueError("No workbook loaded")

        # Direct call to openpyxl's workbook.__getitem__
        self.active_sheet = self.workbook[key]
        return f"Selected worksheet: {key}"

    def _list_sheets(self):
        """List all worksheet names in the workbook"""
        if not self.workbook:
            raise ValueError("No workbook loaded")

        sheets = self.workbook.sheetnames
        active_sheet_name = self.active_sheet.title if self.active_sheet else None

        return {
            'sheets': sheets,
            'active_sheet': active_sheet_name,
            'total_sheets': len(sheets)
        }

    def _iter_cols(self, min_col=None, max_col=None, min_row=None, max_row=None, values_only=False):
        """Iterate through columns - direct call to openpyxl worksheet.iter_cols()"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Convert string parameters to proper types
        if min_col is not None:
            min_col = int(min_col) if isinstance(min_col, str) else min_col
        if max_col is not None:
            max_col = int(max_col) if isinstance(max_col, str) else max_col
        if min_row is not None:
            min_row = int(min_row) if isinstance(min_row, str) else min_row
        if max_row is not None:
            max_row = int(max_row) if isinstance(max_row, str) else max_row
        if isinstance(values_only, str):
            values_only = values_only.lower() in ['true', '1', 'yes']

        # Direct call to openpyxl's iter_cols method
        cols = list(self.active_sheet.iter_cols(
            min_col=min_col, max_col=max_col,
            min_row=min_row, max_row=max_row,
            values_only=values_only
        ))

        return str(cols)

    def _set_worksheet_item(self, key, value):
        """Direct call to worksheet['A1'] = value - openpyxl's __setitem__"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Smart type conversion: convert numeric strings to numbers
        # This prevents "Number Stored as Text" errors in Excel
        converted_value = convert_value_type(value)
        
        # Direct call to openpyxl's worksheet.__setitem__
        self.active_sheet[key] = converted_value
        self.modified = True
        return f"Set {key} to: {value}"

    def _fill_formula(self, source_cell, target_range):
        """Fill formula from source cell across target range with automatic reference adjustment"""
        from openpyxl.formula.translate import Translator
        from openpyxl.utils import range_boundaries

        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Get source cell and its formula
        source = self.active_sheet[source_cell]
        if not source.value or not str(source.value).startswith('='):
            return f"Source cell {source_cell} doesn't contain a formula (value: {source.value})"

        # Parse target range
        min_col, min_row, max_col, max_row = range_boundaries(target_range)

        # Count cells that will be filled
        cells_filled = 0

        # Fill the range
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                # Skip if this is the source cell itself
                if row == source.row and col == source.column:
                    continue

                # Create translator with the source formula
                translator = Translator(
                    source.value,
                    origin=source.coordinate
                )

                # Translate the formula with proper offset
                translated_formula = translator.translate_formula(
                    row_delta=row - source.row,
                    col_delta=col - source.column
                )

                # Set the translated formula to the target cell
                self.active_sheet.cell(row=row, column=col).value = translated_formula
                cells_filled += 1
        self.modified = True

        return f"Filled formula from {source_cell} to {target_range} ({cells_filled} cells)"

    def _cell_set_style(self, cell_reference, style_id=None, font=None, fill=None, border=None, 
                        alignment=None, number_format=None):
        """
        Apply comprehensive styling to cell(s) in one call.
        
        Accepts style palette IDs or inline style definitions.
        
        Args:
            cell_reference: Cell or range (e.g., 'A1' or 'A1:B10')
            style_id: Style ID from palette (e.g., 's1', 's2'). If provided, applies that complete style.
            font: Font ID ('font_1') or inline dict/JSON {'bold': True, 'size': 12}
            fill: Fill ID ('fill_1') or inline dict/JSON {'color': 'FFFF00'}
            border: Border ID ('border_1') or inline dict/JSON {'style': 'thin', 'sides': 'all'}
            alignment: Alignment ID ('align_1') or inline dict/JSON {'horizontal': 'center'}
            number_format: Number format string or preset name (e.g., 'accounting')
        
        Returns:
            Success/error message with styling results
        """
        if not self.workbook or not self.active_sheet:
            return "Error: No active worksheet. Use openpyxl_load_workbook or openpyxl_workbook first."
        
        try:
            # If style_id provided, expand from palette
            if style_id:
                if not self.style_palette:
                    return f"Error: Style palette not loaded. Cannot use style_id '{style_id}'."
                
                if style_id not in self.style_palette:
                    return f"Error: Style ID '{style_id}' not found in palette. Available: {list(self.style_palette.keys())}"
                
                # Expand style from palette
                style_dict = self.style_palette[style_id]
                font = style_dict.get('font')
                fill = style_dict.get('fill')
                border = style_dict.get('border')
                alignment = style_dict.get('alignment')
                number_format = style_dict.get('number_format')
            
            # Validate at least one style parameter provided
            if not any([font, fill, border, alignment, number_format]):
                return "Error: No style parameters provided. Specify style_id or at least one: font, fill, border, alignment, number_format"
            
            # Convert number format presets to actual formats
            if number_format and isinstance(number_format, str) and number_format in PRESET_TO_FORMAT:
                number_format = PRESET_TO_FORMAT[number_format]
            
            # Parse cell reference to get cells
            cells = self._get_cells_from_reference(cell_reference)
            if not cells:
                return f"Error: Invalid cell reference: {cell_reference}"
            
            cells_styled = 0
            
            for cell in cells:
                # Apply font
                if font is not None:
                    try:
                        font_obj = self._resolve_style_object(font, 'font')
                        if font_obj:
                            cell.font = font_obj
                    except Exception as e:
                        return f"Error applying font: {str(e)}"
                
                # Apply fill
                if fill is not None:
                    try:
                        fill_obj = self._resolve_style_object(fill, 'fill')
                        if fill_obj:
                            cell.fill = fill_obj
                    except Exception as e:
                        return f"Error applying fill: {str(e)}"
                
                # Apply border
                if border is not None:
                    try:
                        border_obj = self._resolve_style_object(border, 'border')
                        if border_obj:
                            cell.border = border_obj
                    except Exception as e:
                        return f"Error applying border: {str(e)}"
                
                # Apply alignment
                if alignment is not None:
                    try:
                        align_obj = self._resolve_style_object(alignment, 'alignment')
                        if align_obj:
                            cell.alignment = align_obj
                    except Exception as e:
                        return f"Error applying alignment: {str(e)}"
                
                # Apply number format
                if number_format:
                    try:
                        cell.number_format = number_format
                    except Exception as e:
                        return f"Error applying number_format: {str(e)}"
                
                cells_styled += 1
            
            self.modified = True
            
            style_summary = []
            if font: style_summary.append("font")
            if fill: style_summary.append("fill")
            if border: style_summary.append("border")
            if alignment: style_summary.append("alignment")
            if number_format: style_summary.append("number_format")
            
            return f"Applied {', '.join(style_summary)} to {cells_styled} cell(s) in range {cell_reference}"
            
        except Exception as e:
            return f"Error applying style: {str(e)}"

    def _get_cells_from_reference(self, cell_reference):
        """
        Parse cell reference and return list of cells.
        
        Args:
            cell_reference: 'A1' for single cell or 'A1:B10' for range
        
        Returns:
            List of cell objects (flattened if range)
        """
        try:
            if ':' in cell_reference:
                # It's a range - need to flatten the tuple structure
                cells = []
                for row in self.active_sheet[cell_reference]:
                    if isinstance(row, tuple):
                        cells.extend(row)
                    else:
                        cells.append(row)
                return cells
            else:
                # It's a single cell
                return [self.active_sheet[cell_reference]]
        except Exception as e:
            return []

    def _resolve_style_object(self, style_input, style_type):
        """
        Convert style ID or inline JSON/dict to openpyxl style object.
        
        Args:
            style_input: Style object ID (e.g., 'font_1') or JSON string/dict
            style_type: 'font', 'fill', 'border', or 'alignment'
        
        Returns:
            openpyxl style object or None
        """
        # If it's a string that looks like an ID, try to retrieve it
        if isinstance(style_input, str) and style_input in self.created_objects:
            return self.created_objects[style_input]
        
        # Otherwise, try to parse as JSON and create inline
        try:
            if isinstance(style_input, str):
                style_dict = json.loads(style_input)
            elif isinstance(style_input, dict):
                style_dict = style_input
            else:
                return None
            
            return self._create_style_from_dict(style_dict, style_type)
            
        except (json.JSONDecodeError, ValueError) as e:
            # If it's neither an ID nor valid JSON, return None
            return None

    def _create_style_from_dict(self, style_dict, style_type):
        """
        Create openpyxl style object from dictionary.
        
        Args:
            style_dict: Dictionary with style properties
            style_type: 'font', 'fill', 'border', or 'alignment'
        
        Returns:
            openpyxl style object
        """
        if style_type == 'font':
            # Build font kwargs only with provided values
            kwargs = {}
            if 'name' in style_dict and style_dict['name'] is not None:
                kwargs['name'] = style_dict['name']
            if 'size' in style_dict and style_dict['size'] is not None:
                kwargs['size'] = float(style_dict['size'])
            if 'bold' in style_dict and style_dict['bold'] is not None:
                kwargs['bold'] = style_dict['bold']
            if 'italic' in style_dict and style_dict['italic'] is not None:
                kwargs['italic'] = style_dict['italic']
            if 'underline' in style_dict and style_dict['underline'] is not None:
                kwargs['underline'] = style_dict['underline']
            if 'strikethrough' in style_dict and style_dict['strikethrough'] is not None:
                kwargs['strike'] = style_dict['strikethrough']
            if 'color' in style_dict and style_dict['color'] is not None:
                # Convert color - handle both hex strings and dict format
                color_val = style_dict['color']
                if isinstance(color_val, dict):
                    # Serialized color from palette: {"type": "rgb", "value": "#00F"}
                    kwargs['color'] = self._deserialize_color(color_val)
                elif isinstance(color_val, str):
                    # Direct hex string: "#00F" or "FF0000"
                    kwargs['color'] = color_val.lstrip('#')
                else:
                    kwargs['color'] = color_val
            
            return Font(**kwargs)
        
        elif style_type == 'fill':
            # Handle both fg_color (from palette) and color (from inline)
            fg_color = style_dict.get('fg_color') or style_dict.get('color')
            if fg_color:
                # Convert color if it's a dict
                if isinstance(fg_color, dict):
                    fg_color = self._deserialize_color(fg_color)
                elif isinstance(fg_color, str):
                    fg_color = fg_color.lstrip('#')
                
                pattern_type = style_dict.get('pattern_type', 'solid')
                return PatternFill(start_color=fg_color, end_color=fg_color, fill_type=pattern_type)
            return None
        
        elif style_type == 'border':
            style = style_dict.get('style', 'thin')
            sides = style_dict.get('sides', 'all')
            
            side_obj = Side(style=style)
            
            if sides in ['all', 'outline']:
                return Border(left=side_obj, right=side_obj, top=side_obj, bottom=side_obj)
            else:
                # Handle individual sides
                kwargs = {}
                if 'left' in sides or sides == 'left':
                    kwargs['left'] = side_obj
                if 'right' in sides or sides == 'right':
                    kwargs['right'] = side_obj
                if 'top' in sides or sides == 'top':
                    kwargs['top'] = side_obj
                if 'bottom' in sides or sides == 'bottom':
                    kwargs['bottom'] = side_obj
                return Border(**kwargs)
        
        elif style_type == 'alignment':
            # Build alignment kwargs only with provided values
            kwargs = {}
            if 'horizontal' in style_dict and style_dict['horizontal'] is not None:
                kwargs['horizontal'] = style_dict['horizontal']
            if 'vertical' in style_dict and style_dict['vertical'] is not None:
                kwargs['vertical'] = style_dict['vertical']
            if 'text_rotation' in style_dict and style_dict['text_rotation'] is not None:
                kwargs['text_rotation'] = int(style_dict['text_rotation'])
            if 'wrap_text' in style_dict and style_dict['wrap_text'] is not None:
                kwargs['wrap_text'] = style_dict['wrap_text']
            if 'shrink_to_fit' in style_dict and style_dict['shrink_to_fit'] is not None:
                kwargs['shrink_to_fit'] = style_dict['shrink_to_fit']
            if 'indent' in style_dict and style_dict['indent'] is not None:
                kwargs['indent'] = int(style_dict['indent'])
            
            return Alignment(**kwargs)
        
        return None

    def _add_data_validation(self, data_validation):
        """Add data validation to worksheet"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # If data_validation is a string ID, get it from created_objects
        if isinstance(data_validation, str):
            data_validation = self.created_objects.get(data_validation)

        self.active_sheet.add_data_validation(data_validation)
        self.modified = True
        return "Added data validation to worksheet"

    def _chart_add_data(self, chart_type, chart_id, data, from_rows=False, titles_from_data=False):
        """Add data to a chart"""
        # Get the chart from created objects
        if chart_id not in self.created_objects:
            raise ValueError(f"Chart {chart_id} not found")

        chart = self.created_objects[chart_id]

        # Convert string boolean parameters to actual booleans
        if isinstance(from_rows, str):
            from_rows = from_rows.lower() in ['true', '1', 'yes']
        if isinstance(titles_from_data, str):
            titles_from_data = titles_from_data.lower() in ['true', '1', 'yes']

        # Handle data parameter - can be Reference ID or range string
        if isinstance(data, str):
            if data in self.created_objects:
                # It's a Reference ID - get the object and we're done
                data = self.created_objects[data]
            else:
                # It's a range string - create a Reference object
                from openpyxl.chart import Reference
                from openpyxl.utils import range_boundaries

                # If the range string doesn't include sheet name, add the active sheet
                if '!' not in data:
                    # Parse the range to get boundaries
                    min_col, min_row, max_col, max_row = range_boundaries(data)
                    data = Reference(self.active_sheet, min_col=min_col, min_row=min_row,
                                   max_col=max_col, max_row=max_row)
                else:
                    # Has sheet name - parse it
                    sheet_name, range_str = data.split('!')
                    sheet = self.workbook[sheet_name]
                    min_col, min_row, max_col, max_row = range_boundaries(range_str)
                    data = Reference(sheet, min_col=min_col, min_row=min_row,
                                   max_col=max_col, max_row=max_row)

        # Direct call to chart's add_data method
        chart.add_data(data, from_rows=from_rows, titles_from_data=titles_from_data)
        return f"Added data to {chart_type}"

    def _chart_set_categories(self, chart_type, chart_id, labels):
        """Set categories for a chart"""
        # Get the chart from created objects
        if chart_id not in self.created_objects:
            raise ValueError(f"Chart {chart_id} not found")

        chart = self.created_objects[chart_id]

        # Handle labels parameter - can be Reference ID or range string
        if isinstance(labels, str):
            if labels in self.created_objects:
                # It's a Reference ID
                labels = self.created_objects[labels]
            else:
                # It's a range string - create a Reference object
                from openpyxl.chart import Reference
                from openpyxl.utils import range_boundaries

                # If the range string doesn't include sheet name, add the active sheet
                if '!' not in labels:
                    # Parse the range to get boundaries
                    min_col, min_row, max_col, max_row = range_boundaries(labels)
                    labels = Reference(self.active_sheet, min_col=min_col, min_row=min_row,
                                     max_col=max_col, max_row=max_row)
                else:
                    # Has sheet name - parse it
                    sheet_name, range_str = labels.split('!')
                    sheet = self.workbook[sheet_name]
                    min_col, min_row, max_col, max_row = range_boundaries(range_str)
                    labels = Reference(sheet, min_col=min_col, min_row=min_row,
                                     max_col=max_col, max_row=max_row)

        # Direct call to chart's set_categories method
        chart.set_categories(labels)
        return f"Set categories for {chart_type}"

    def _add_conditional_formatting(self, range, rule_type, operator=None, formula=None,
                                     fill=None, font=None, border=None, stopIfTrue=False,
                                     icon_style=None, color=None, min_color=None, 
                                     mid_color=None, max_color=None):
        """
        Add conditional formatting to a range in ONE call
        
        Supports all rule types:
        - cell_is: Value comparisons (equal, greaterThan, etc.)
        - color_scale: Color gradients (2 or 3 colors)
        - data_bar: Horizontal bars
        - icon_set: Icons (arrows, traffic lights, etc.)
        
        Args:
            range: Cell range (e.g., 'A1:A10')
            rule_type: 'cell_is', 'color_scale', 'data_bar', 'icon_set'
            operator: For cell_is - comparison operator
            formula: For cell_is - JSON array of values
            fill, font, border: For cell_is - styling
            stopIfTrue: For cell_is - stop if matched
            icon_style: For icon_set - icon type
            color: For data_bar - bar color
            min_color, mid_color, max_color: For color_scale - gradient colors
        """
        import json
        from openpyxl.styles import Font, PatternFill, Border
        from openpyxl.formatting.rule import ColorScaleRule, DataBarRule, IconSetRule
        
        if not self.active_sheet:
            raise ValueError("No active sheet")
        
        # Create rule based on type
        if rule_type == 'cell_is':
            # Parse formula
            if isinstance(formula, str):
                formula = json.loads(formula)
            
            # Build rule kwargs
            rule_kwargs = {
                'operator': operator,
                'formula': formula,
                'stopIfTrue': stopIfTrue
            }
            
            # Parse and add fill
            if fill:
                fill_dict = json.loads(fill) if isinstance(fill, str) else fill
                pattern_type = fill_dict.get('pattern_type', 'solid')
                fg_color = fill_dict.get('fg_color')
                
                fill_kwargs = {'fill_type': pattern_type}
                if fg_color:
                    if isinstance(fg_color, dict):
                        fg_color = fg_color.get('value', fg_color.get('rgb', 'FFFFFF'))
                    fill_kwargs['start_color'] = fg_color
                    fill_kwargs['end_color'] = fg_color
                
                rule_kwargs['fill'] = PatternFill(**fill_kwargs)
            
            # Parse and add font
            if font:
                font_dict = json.loads(font) if isinstance(font, str) else font
                font_kwargs = {}
                if 'color' in font_dict:
                    color_val = font_dict['color']
                    if isinstance(color_val, dict):
                        color_val = color_val.get('value', color_val.get('rgb', '000000'))
                    font_kwargs['color'] = color_val
                if 'bold' in font_dict:
                    font_kwargs['bold'] = font_dict['bold']
                if 'italic' in font_dict:
                    font_kwargs['italic'] = font_dict['italic']
                if 'size' in font_dict:
                    font_kwargs['size'] = font_dict['size']
                
                rule_kwargs['font'] = Font(**font_kwargs)
            
            # Parse and add border
            if border:
                border_dict = json.loads(border) if isinstance(border, str) else border
                rule_kwargs['border'] = Border(**border_dict)
            
            rule = CellIsRule(**rule_kwargs)
        
        elif rule_type == 'color_scale':
            # 2-color or 3-color scale
            if mid_color:
                rule = ColorScaleRule(
                    start_type='min', start_color=min_color,
                    mid_type='percentile', mid_value=50, mid_color=mid_color,
                    end_type='max', end_color=max_color
                )
            else:
                rule = ColorScaleRule(
                    start_type='min', start_color=min_color,
                    end_type='max', end_color=max_color
                )
        
        elif rule_type == 'data_bar':
            rule = DataBarRule(
                start_type='min', end_type='max',
                color=color if color else '638EC6'
            )
        
        elif rule_type == 'icon_set':
            rule = IconSetRule(
                icon_style=icon_style if icon_style else '3TrafficLights1',
                type='percent',
                values=[0, 33, 67],
                showValue=True
            )
        
        else:
            raise ValueError(f"Unknown rule_type: {rule_type}")
        
        # Apply rule to range
        self.active_sheet.conditional_formatting.add(range, rule)
        
        return f"Applied {rule_type} conditional formatting to {range}"

    # Object creation (styles, charts, etc.)
    def _create_object(self, object_type, **kwargs):
        """Create style/chart/advanced objects"""
        object_type = object_type.replace('create_', '')

        # Helper function to resolve object references
        def resolve_references(params):
            """Replace string IDs with actual objects from created_objects"""
            resolved = {}
            for key, value in params.items():
                if isinstance(value, str) and value in self.created_objects:
                    # This is a reference to a created object
                    resolved[key] = self.created_objects[value]
                else:
                    resolved[key] = value
            return resolved


        # Resolve any object references in kwargs
        kwargs = resolve_references(kwargs)

        # Style objects
        if object_type == 'font':
            obj = Font(**kwargs)
        elif object_type == 'patternfill':
            obj = PatternFill(**kwargs)
        elif object_type == 'gradientfill':
            obj = GradientFill(**kwargs)
        elif object_type == 'border':
            obj = Border(**kwargs)
        elif object_type == 'side':
            obj = Side(**kwargs)
        elif object_type == 'alignment':
            obj = Alignment(**kwargs)
        elif object_type == 'protection':
            obj = Protection(**kwargs)
        # Chart objects
        elif object_type == 'barchart':
            obj = BarChart(**kwargs)
        elif object_type == 'linechart':
            obj = LineChart(**kwargs)
        elif object_type == 'piechart':
            obj = PieChart(**kwargs)
        elif object_type == 'scatterchart':
            obj = ScatterChart(**kwargs)
        elif object_type == 'areachart':
            obj = AreaChart(**kwargs)
        elif object_type == 'reference':
            obj = Reference(**kwargs)
        # Advanced objects
        elif object_type == 'image':
            obj = Image(**kwargs)
        elif object_type == 'table':
            obj = Table(**kwargs)
        elif object_type == 'tablestyleinfo':
            obj = TableStyleInfo(**kwargs)
        elif object_type == 'datavalidation':
            obj = DataValidation(**kwargs)
        elif object_type == 'colorscalerule':
            obj = ColorScaleRule(**kwargs)
        elif object_type == 'cellisrule':
            obj = CellIsRule(**kwargs)
        elif object_type == 'iconsetrule':
            obj = IconSetRule(**kwargs)
        elif object_type == 'databarrule':
            obj = DataBarRule(**kwargs)
        else:
            raise ValueError(f"Unknown object type: {object_type}")

        # Store the created object with a unique ID
        obj_id = f"{object_type}_{len(self.created_objects)}"
        self.created_objects[obj_id] = obj
        return f"Created {object_type} with ID: {obj_id}"

    def _add_chart(self, chart, anchor):
        """Add a chart to the worksheet"""
        if not self.active_sheet:
            raise ValueError("No active sheet")
        # If chart is a string ID, get it from created_objects
        if isinstance(chart, str):
            chart = self.created_objects.get(chart)
        self.active_sheet.add_chart(chart, anchor)
        self.modified = True
        return f"Added chart at {anchor}"

    def _add_image(self, img, anchor):
        """Add an image to the worksheet"""
        if not self.active_sheet:
            raise ValueError("No active sheet")
        # If img is a string ID, get it from created_objects
        if isinstance(img, str) and img in self.created_objects:
            img = self.created_objects.get(img)
        self.active_sheet.add_image(img, anchor)
        self.modified = True
        return f"Added image at {anchor}"

    def _add_table(self, table):
        """Add a table to the worksheet"""
        if not self.active_sheet:
            raise ValueError("No active sheet")
        # If table is a string ID, get it from created_objects
        if isinstance(table, str):
            table = self.created_objects.get(table)
        self.active_sheet.add_table(table)
        self.modified = True
        return f"Added table"

    # New worksheet feature methods
    def _set_number_format(self, cell_reference, format_string):
        """Set number format for cells"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Handle range or single cell
        if ':' in cell_reference:
            # It's a range
            for row in self.active_sheet[cell_reference]:
                for cell in row:
                    cell.number_format = format_string
            return f"Set number format for range {cell_reference} to: {format_string}"
        else:
            # Single cell
            self.active_sheet[cell_reference].number_format = format_string
            self.modified = True
            return f"Set number format for {cell_reference} to: {format_string}"

    def _set_column_width(self, column, width):
        """Set column width"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Convert width to float
        width = float(width) if isinstance(width, str) else width

        # Handle column index or letter
        if column.isdigit():
            column = get_column_letter(int(column))

        self.active_sheet.column_dimensions[column].width = width
        self.modified = True
        return f"Set column {column} width to: {width}"

    def _set_row_height(self, row, height):
        """Set row height"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Convert to numbers
        row = int(row) if isinstance(row, str) else row
        height = float(height) if isinstance(height, str) else height

        self.active_sheet.row_dimensions[row].height = height
        self.modified = True
        return f"Set row {row} height to: {height}"

    def _set_auto_filter(self, range_string):
        """Set AutoFilter on a range"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        self.active_sheet.auto_filter.ref = range_string
        self.modified = True
        return f"Set AutoFilter on range: {range_string}"

    def _add_comment(self, cell_reference, comment_text, author="User"):
        """Add a comment to a cell"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        from openpyxl.comments import Comment

        comment = Comment(comment_text, author)
        self.active_sheet[cell_reference].comment = comment
        self.modified = True
        return f"Added comment to {cell_reference} by {author}"

    def _add_hyperlink(self, cell_reference, url, display_text=""):
        """Add a hyperlink to a cell"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        cell = self.active_sheet[cell_reference]
        cell.hyperlink = url

        # Set display text if provided
        if display_text:
            cell.value = display_text
        elif not cell.value:
            # If no display text and cell is empty, use URL
            cell.value = url
        self.modified = True

        return f"Added hyperlink to {cell_reference}: {url}"

    def _freeze_panes(self, cell_reference):
        """Freeze panes at specified cell"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        self.active_sheet.freeze_panes = cell_reference
        self.modified = True
        return f"Froze panes at: {cell_reference}"

    def _define_name(self, name, reference):
        """Define a named range"""
        if not self.workbook:
            raise ValueError("No workbook loaded")

        from openpyxl.workbook.defined_name import DefinedName

        # Create defined name
        defined_name = DefinedName(name, attr_text=reference)
        self.workbook.defined_names.add(defined_name)
        self.modified = True
        return f"Defined name '{name}' for range: {reference}"

    def _set_protection(self, enable="true", password=""):
        """Set worksheet protection"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        # Convert string boolean to actual boolean
        if isinstance(enable, str):
            enable = enable.lower() in ['true', '1', 'yes']

        self.active_sheet.protection.sheet = enable

        if password and enable:
            self.active_sheet.protection.password = password
            self.modified = True
            return f"{'Enabled' if enable else 'Disabled'} sheet protection with password"
        else:
            return f"{'Enabled' if enable else 'Disabled'} sheet protection"

    def _set_visibility(self, sheet_name, state="visible"):
        """Set worksheet visibility"""
        if not self.workbook:
            raise ValueError("No workbook loaded")

        if sheet_name not in self.workbook.sheetnames:
            raise ValueError(f"Sheet '{sheet_name}' not found")

        sheet = self.workbook[sheet_name]

        # Map state strings to worksheet states
        state_map = {
            'visible': 'visible',
            'hidden': 'hidden',
            'veryhidden': 'veryHidden',
            'veryHidden': 'veryHidden'
        }

        if state.lower() not in [k.lower() for k in state_map.keys()]:
            raise ValueError(f"Invalid state: {state}. Use 'visible', 'hidden', or 'veryHidden'")

        # Find the correct state value
        for key, value in state_map.items():
            if key.lower() == state.lower():
                sheet.sheet_state = value
                self.modified = True
                break

        return f"Set sheet '{sheet_name}' visibility to: {state}"

    def _list_charts(self):
        """List all charts in the workbook"""
        charts = {}

        # First, check charts in created_objects (newly created charts)
        for obj_id, obj in self.created_objects.items():
            if obj_id.startswith(('barchart_', 'linechart_', 'piechart_', 'scatterchart_', 'areachart_')):
                chart_type = obj_id.split('_')[0]
                charts[obj_id] = {
                    'type': chart_type,
                    'title': getattr(obj, 'title', None),
                    'has_data': len(obj.series) > 0 if hasattr(obj, 'series') else False,
                    'location': 'Created (not yet added to sheet)'
                }

        # Then, check charts already in the workbook sheets
        if self.workbook:
            for sheet_name in self.workbook.sheetnames:
                sheet = self.workbook[sheet_name]
                if hasattr(sheet, '_charts') and sheet._charts:
                    for i, chart in enumerate(sheet._charts):
                        # Generate an ID for existing charts
                        chart_class = chart.__class__.__name__.lower().replace('chart', '')
                        chart_id = f"existing_{chart_class}chart_{sheet_name}_{i}"

                        charts[chart_id] = {
                            'type': chart.__class__.__name__,
                            'title': chart.title if hasattr(chart, 'title') else None,
                            'has_data': len(chart.series) > 0 if hasattr(chart, 'series') else False,
                            'location': f'Sheet: {sheet_name}'
                        }

        if not charts:
            return "No charts found. Use create_[type]chart tools to create charts."

        return f"Charts in workbook: {json.dumps(charts, indent=2)}"

    def _get_chart_info(self, chart_id):
        """Get detailed information about a specific chart"""
        chart = None

        # First check created_objects
        if chart_id in self.created_objects:
            chart = self.created_objects[chart_id]
        # Then check if it's an existing chart reference
        elif chart_id.startswith('existing_') and self.workbook:
            # Parse the ID: existing_[type]chart_[sheet]_[index]
            parts = chart_id.split('_')
            if len(parts) >= 4:
                sheet_name = '_'.join(parts[2:-1])  # Handle sheet names with underscores
                chart_index = int(parts[-1])

                if sheet_name in self.workbook.sheetnames:
                    sheet = self.workbook[sheet_name]
                    if hasattr(sheet, '_charts') and chart_index < len(sheet._charts):
                        chart = sheet._charts[chart_index]

        if not chart:
            # List all available charts
            available_charts = list(self.created_objects.keys())
            if self.workbook:
                for sheet_name in self.workbook.sheetnames:
                    sheet = self.workbook[sheet_name]
                    if hasattr(sheet, '_charts') and sheet._charts:
                        for i, _ in enumerate(sheet._charts):
                            available_charts.append(f"existing_*chart_{sheet_name}_{i}")
            return f"Chart {chart_id} not found. Available charts: {available_charts}"
        info = {
            'id': chart_id,
            'type': chart.__class__.__name__,
            'title': chart.title if hasattr(chart, 'title') else None,
            'series_count': len(chart.series) if hasattr(chart, 'series') else 0,
            'x_axis_title': chart.x_axis.title if hasattr(chart.x_axis, 'title') else None,
            'y_axis_title': chart.y_axis.title if hasattr(chart.y_axis, 'title') else None,
            'has_legend': chart.legend is not None if hasattr(chart, 'legend') else False,
            'style': chart.style if hasattr(chart, 'style') else None
        }
        return json.dumps(info, indent=2)

    def _get_worksheet_charts(self):
        """Get all charts on the active worksheet"""
        if not self.active_sheet:
            raise ValueError("No active sheet")

        worksheet_charts = []

        # Check _charts attribute of worksheet
        if hasattr(self.active_sheet, '_charts') and self.active_sheet._charts:
            for i, chart in enumerate(self.active_sheet._charts):
                # First try to find it in created_objects
                found = False
                for obj_id, obj in self.created_objects.items():
                    if obj is chart:
                        worksheet_charts.append(obj_id)
                        found = True
                        break

                # If not found in created_objects, it's an existing chart
                if not found:
                    chart_class = chart.__class__.__name__.lower().replace('chart', '')
                    chart_id = f"existing_{chart_class}chart_{self.active_sheet.title}_{i}"
                    worksheet_charts.append(chart_id)

        if not worksheet_charts:
            return f"No charts on worksheet '{self.active_sheet.title}'"

        return f"Charts on '{self.active_sheet.title}': {worksheet_charts}"

    def _extract_style_palette(self, formatting_dict):
        """
        Extract unique styles from formatting dict and build palette
        
        Args:
            formatting_dict: {cell_addr: {font: {...}, fill: {...}, ...}}
        
        Returns:
            style_palette: {style_id: style_dict}
            cell_to_style_id: {cell_addr: style_id}
        """
        style_to_id = {}
        palette = {}
        cell_mapping = {}
        counter = 1
        
        for cell_addr, style_dict in formatting_dict.items():
            # Skip empty styles
            if not style_dict:
                continue
            
            # Convert to hashable string for deduplication
            style_hash = json.dumps(style_dict, sort_keys=True)
            
            if style_hash not in style_to_id:
                style_id = f"s{counter}"
                style_to_id[style_hash] = style_id
                palette[style_id] = style_dict
                counter += 1
            
            cell_mapping[cell_addr] = style_to_id[style_hash]
        
        return palette, cell_mapping

    def _consolidate_cell_ranges(self, cells_dict, cell_to_style):
        """
        Collapse consecutive cells with identical data+style into ranges
        
        Args:
            cells_dict: {cell_addr: {value, formula, type, ...}}
            cell_to_style: {cell_addr: style_id}
        
        Returns:
            consolidated: {range_or_cell: {value/formula, style}}
        """
        from openpyxl.utils import coordinate_to_tuple, get_column_letter
        
        # Group cells by row
        rows = {}
        for cell_addr, cell_data in cells_dict.items():
            col, row = coordinate_to_tuple(cell_addr)
            if row not in rows:
                rows[row] = []
            rows[row].append((col, cell_addr, cell_data))
        
        consolidated = {}
        
        for row_num, cells in rows.items():
            # Sort by column
            cells.sort(key=lambda x: x[0])
            
            # Try to find consecutive runs with same data+style
            i = 0
            while i < len(cells):
                col_idx, cell_addr, cell_data = cells[i]
                style_id = cell_to_style.get(cell_addr)
                
                # Look ahead for consecutive cells with same content+style
                j = i + 1
                while j < len(cells):
                    next_col, next_addr, next_data = cells[j]
                    next_style = cell_to_style.get(next_addr)
                    
                    # Check if consecutive and identical
                    if (next_col == col_idx + (j - i) and
                        next_data == cell_data and
                        next_style == style_id):
                        j += 1
                    else:
                        break
                
                # Build entry
                entry = cell_data.copy()
                if style_id:
                    entry["style"] = style_id
                
                # If we found a range (2+ cells), use range notation
                if j - i > 1:
                    start_cell = f"{get_column_letter(col_idx)}{row_num}"
                    end_col = col_idx + (j - i - 1)
                    end_cell = f"{get_column_letter(end_col)}{row_num}"
                    range_addr = f"{start_cell}:{end_cell}"
                    consolidated[range_addr] = entry
                else:
                    consolidated[cell_addr] = entry
                
                i = j
        
        return consolidated

    def _get_sheet_complete(self, sheet=None, include_formatting=True,
                            include_formulas=True, sparse_formatting=True,
                            cell_range=None):
        """Get complete sheet snapshot with compressed style palette"""
        
        # 1. Get sheet
        if sheet:
            if sheet not in self.workbook.sheetnames:
                raise ValueError(f"Sheet '{sheet}' not found")
            ws = self.workbook[sheet]
        else:
            ws = self.active_sheet
            if not ws:
                raise ValueError("No active sheet")
        
        # 2. Determine range
        if cell_range:
            # Parse range like "B24:E50"
            min_col, min_row, max_col, max_row = range_boundaries(cell_range)
        else:
            # Use sheet's used range
            min_row = ws.min_row
            max_row = ws.max_row
            min_col = ws.min_column
            max_col = ws.max_column
        
        # 3. Collect data
        metadata = self._get_sheet_metadata(ws, min_row, max_row, min_col, max_col)
        cells = self._get_all_cells(ws, min_row, max_row, min_col, max_col, include_formulas)
        special_features = self._get_special_features(ws)
        
        # 4. Extract and compress formatting
        if include_formatting:
            formatting = self._get_formatting(ws, min_row, max_row, min_col, max_col, sparse_formatting)
            
            # Build style palette and map cells to style IDs
            style_palette, cell_to_style = self._extract_style_palette(formatting)
            
            # Store palette in executor for later reference
            self.style_palette = style_palette
        else:
            style_palette = {}
            cell_to_style = {}
        
        # 5. Consolidate cells into ranges
        consolidated_cells = self._consolidate_cell_ranges(cells, cell_to_style)
        
        # 6. Build compressed result
        result = {
            "sheet_metadata": metadata,
            "style_palette": style_palette,
            "cells": consolidated_cells,
            "special_features": special_features
        }
        
        return json.dumps(result, indent=2)

    def _get_sheet_metadata(self, sheet, min_row, max_row, min_col, max_col):
        """Collect sheet-level metadata"""
        
        # Column widths
        column_widths = {}
        for col_idx in range(min_col, max_col + 1):
            col_letter = get_column_letter(col_idx)
            col_dim = sheet.column_dimensions[col_letter]
            if col_dim.width:  # Only include if explicitly set
                column_widths[col_letter] = col_dim.width
        
        # Row heights
        row_heights = {}
        for row_idx in range(min_row, max_row + 1):
            row_dim = sheet.row_dimensions[row_idx]
            if row_dim.height:  # Only include if explicitly set
                row_heights[str(row_idx)] = row_dim.height
        
        # Dimensions
        start_cell = f"{get_column_letter(min_col)}{min_row}"
        end_cell = f"{get_column_letter(max_col)}{max_row}"
        
        return {
            "sheet_name": sheet.title,
            "dimensions": f"{start_cell}:{end_cell}",
            "used_range": {
                "min_row": min_row,
                "max_row": max_row,
                "min_col": min_col,
                "max_col": max_col
            },
            "column_widths": column_widths,
            "row_heights": row_heights,
            "default_row_height": sheet.sheet_format.defaultRowHeight,
            "default_column_width": sheet.sheet_format.defaultColWidth
        }

    def _get_all_cells(self, sheet, min_row, max_row, min_col, max_col, include_formulas):
        """Collect all cell values and formulas"""
        cells = {}
        
        for row in sheet.iter_rows(min_row=min_row, max_row=max_row,
                                    min_col=min_col, max_col=max_col):
            for cell in row:
                if cell.value is None:
                    continue  # Skip empty cells
                
                cell_addr = cell.coordinate
                cell_data = {
                    "value": str(cell.value) if cell.value is not None else None,
                    "data_type": cell.data_type
                }
                
                # Add formula if present
                if include_formulas and cell.data_type == 'f':
                    # Handle ArrayFormula objects
                    if hasattr(cell.value, 'text'):
                        formula_text = cell.value.text
                        if not formula_text.startswith('='):
                            formula_text = f"={formula_text}"
                        cell_data["formula"] = formula_text
                    elif isinstance(cell.value, str) and cell.value.startswith('='):
                        cell_data["formula"] = cell.value
                    else:
                        cell_data["formula"] = f"={cell.value}"
                    
                    # Get calculated value if available
                    if hasattr(cell, '_value'):
                        cell_data["calculated_value"] = cell._value
                
                # Determine type
                if cell.data_type == 'f':
                    cell_data["type"] = "formula"
                elif cell.data_type == 'n':
                    cell_data["type"] = "number"
                elif cell.data_type == 's':
                    cell_data["type"] = "string"
                elif cell.data_type == 'b':
                    cell_data["type"] = "boolean"
                elif cell.data_type == 'd':
                    cell_data["type"] = "date"
                else:
                    cell_data["type"] = "other"
                
                cells[cell_addr] = cell_data
        
        return cells

    def _get_formatting(self, sheet, min_row, max_row, min_col, max_col, sparse):
        """Collect cell formatting (sparse mode only includes non-default)"""
        formatting = {}
        
        for row in sheet.iter_rows(min_row=min_row, max_row=max_row,
                                    min_col=min_col, max_col=max_col):
            for cell in row:
                # Skip if sparse mode and cell has default formatting
                if sparse and self._is_default_formatting(cell):
                    continue
                
                cell_addr = cell.coordinate
                cell_format = {}
                
                # Font
                if cell.font:
                    font_data = self._serialize_font(cell.font)
                    if font_data:  # Only add if non-empty
                        cell_format["font"] = font_data
                
                # Fill
                if cell.fill:
                    fill_data = self._serialize_fill(cell.fill)
                    if fill_data:
                        cell_format["fill"] = fill_data
                
                # Border
                if cell.border:
                    border_data = self._serialize_border(cell.border)
                    if border_data:
                        cell_format["border"] = border_data
                
                # Alignment
                if cell.alignment:
                    align_data = self._serialize_alignment(cell.alignment)
                    if align_data:
                        cell_format["alignment"] = align_data
                
                # Number format - use presets when available
                if cell.number_format and cell.number_format != "General":
                    # Check if we have a preset name for this format
                    if cell.number_format in NUMBER_FORMAT_PRESETS:
                        cell_format["number_format"] = NUMBER_FORMAT_PRESETS[cell.number_format]
                    else:
                        cell_format["number_format"] = cell.number_format
                
                # Only add if we collected any formatting
                if cell_format:
                    formatting[cell_addr] = cell_format
        
        return formatting

    def _get_special_features(self, sheet):
        """Collect special features (merged cells, frozen panes, etc.)"""
        features = {}
        
        # Merged cells
        if sheet.merged_cells:
            features["merged_cells"] = [str(cell_range) for cell_range in sheet.merged_cells.ranges]
        
        # Frozen panes
        if sheet.freeze_panes:
            features["frozen_panes"] = {
                "cell": sheet.freeze_panes,
                "type": "freezePane"
            }
        
        # AutoFilter
        if sheet.auto_filter:
            features["auto_filter"] = {
                "range": str(sheet.auto_filter.ref)
            }
        
        # Conditional formatting (full details)
        if hasattr(sheet, 'conditional_formatting') and sheet.conditional_formatting:
            cond_formats = []
            try:
                for cf_range, rules in sheet.conditional_formatting._cf_rules.items():
                    for rule in rules:
                        # Extract the actual range string
                        range_str = str(cf_range.sqref) if hasattr(cf_range, 'sqref') else str(cf_range)
                        
                        # Build rule data
                        rule_data = {
                            "range": range_str,
                            "type": rule.type if hasattr(rule, 'type') else "unknown"
                        }
                        
                        # Extract rule-specific properties for cellIs rules
                        if rule.type == 'cellIs':
                            if hasattr(rule, 'operator') and rule.operator:
                                rule_data["operator"] = rule.operator
                            if hasattr(rule, 'formula') and rule.formula:
                                rule_data["formula"] = rule.formula
                            if hasattr(rule, 'stopIfTrue'):
                                rule_data["stopIfTrue"] = rule.stopIfTrue
                            
                            # Extract styling from dxf (differential formatting)
                            if hasattr(rule, 'dxf') and rule.dxf:
                                # Serialize fill
                                if rule.dxf.fill:
                                    fill_data = self._serialize_fill(rule.dxf.fill)
                                    if fill_data:
                                        rule_data["fill"] = fill_data
                                
                                # Serialize font
                                if rule.dxf.font:
                                    font_data = self._serialize_font(rule.dxf.font)
                                    if font_data:
                                        rule_data["font"] = font_data
                                
                                # Serialize border (if present)
                                if rule.dxf.border:
                                    border_data = self._serialize_border(rule.dxf.border)
                                    if border_data:
                                        rule_data["border"] = border_data
                        
                        # Extract properties for other rule types (color_scale, data_bar, icon_set)
                        elif rule.type == 'colorScale':
                            if hasattr(rule, 'colorScale') and rule.colorScale:
                                # Extract color scale details (simplified)
                                rule_data["color_scale_type"] = "2_color" if len(rule.colorScale.cfvo) == 2 else "3_color"
                        
                        elif rule.type == 'dataBar':
                            if hasattr(rule, 'dataBar') and rule.dataBar:
                                # Extract data bar color
                                if hasattr(rule.dataBar, 'color') and rule.dataBar.color:
                                    color_data = self._serialize_color(rule.dataBar.color)
                                    if color_data:
                                        rule_data["color"] = color_data
                        
                        elif rule.type == 'iconSet':
                            if hasattr(rule, 'iconSet') and rule.iconSet:
                                # Extract icon set style
                                if hasattr(rule.iconSet, 'iconSet'):
                                    rule_data["icon_style"] = rule.iconSet.iconSet
                        
                        cond_formats.append(rule_data)
                
                if cond_formats:
                    features["conditional_formats"] = cond_formats
            except Exception as e:
                # Log error but don't fail
                pass
        
        # Data validations
        if hasattr(sheet, 'data_validations') and sheet.data_validations.dataValidation:
            validations = []
            for dv in sheet.data_validations.dataValidation:
                validations.append({
                    "range": str(dv.sqref),
                    "type": dv.type,
                    "formula1": dv.formula1 if hasattr(dv, 'formula1') else None
                })
            if validations:
                features["data_validations"] = validations
        
        return features

    def _is_default_formatting(self, cell):
        """Check if cell has default formatting (for sparse mode)"""
        
        # Check font - only flag as non-default if something is actually different
        if cell.font:
            # Bold, italic, underline, strike are non-default
            if cell.font.bold or cell.font.italic or cell.font.underline or cell.font.strike:
                return False
            # Color is non-default (but only if it's explicitly set, not theme color)
            if cell.font.color and hasattr(cell.font.color, 'rgb'):
                rgb = cell.font.color.rgb
                if rgb and isinstance(rgb, str) and len(rgb) >= 6 and not rgb.startswith('Values'):
                    return False
            # Size different from 11 is non-default
            if cell.font.size and cell.font.size != 11:
                return False
            # Name different from Calibri is non-default (but don't flag if it's just Calibri)
            if cell.font.name and cell.font.name != 'Calibri':
                return False
        
        # Check fill
        if cell.fill and cell.fill.patternType and cell.fill.patternType != 'none':
            return False
        
        # Check border
        if cell.border:
            if (cell.border.left.style or cell.border.right.style or
                cell.border.top.style or cell.border.bottom.style):
                return False
        
        # Check alignment - only flag if something is actually different
        if cell.alignment:
            # Horizontal alignment different from general is non-default
            if cell.alignment.horizontal and cell.alignment.horizontal != 'general':
                return False
            # Vertical alignment different from bottom is non-default
            if cell.alignment.vertical and cell.alignment.vertical != 'bottom':
                return False
            # Wrap text is non-default
            if cell.alignment.wrap_text:
                return False
            # Indent > 0 is non-default
            if cell.alignment.indent and cell.alignment.indent > 0:
                return False
            # Text rotation is non-default
            if cell.alignment.text_rotation and cell.alignment.text_rotation != 0:
                return False
        
        # Check number format
        if cell.number_format and cell.number_format != "General":
            return False
        
        return True

    def _serialize_font(self, font):
        """Convert Font object to dict"""
        result = {}
        
        if font.name:
            result["name"] = font.name
        if font.size:
            result["size"] = font.size
        if font.bold:
            result["bold"] = font.bold
        if font.italic:
            result["italic"] = font.italic
        if font.underline:
            result["underline"] = font.underline
        if font.strike:
            result["strike"] = font.strike
        
        # Serialize color (supports RGB, theme, and indexed colors)
        if font.color:
            color_data = self._serialize_color(font.color)
            if color_data:
                result["color"] = color_data
        
        return result

    def _serialize_fill(self, fill):
        """Convert Fill object to dict"""
        result = {}
        
        if fill.patternType and fill.patternType != 'none':
            result["pattern_type"] = fill.patternType
            
            # Serialize foreground color
            if fill.fgColor:
                fg_color_data = self._serialize_color(fill.fgColor)
                if fg_color_data:
                    result["fg_color"] = fg_color_data
            
            # Serialize background color
            if fill.bgColor:
                bg_color_data = self._serialize_color(fill.bgColor)
                if bg_color_data:
                    result["bg_color"] = bg_color_data
        
        return result

    def _serialize_border(self, border):
        """Convert Border object to dict"""
        result = {}
        
        for side_name in ['left', 'right', 'top', 'bottom']:
            side = getattr(border, side_name)
            if side and side.style:
                side_data = {"style": side.style}
                # Serialize border color
                if side.color:
                    color_data = self._serialize_color(side.color)
                    if color_data:
                        side_data["color"] = color_data
                result[side_name] = side_data
        
        return result

    def _serialize_alignment(self, alignment):
        """Convert Alignment object to dict"""
        result = {}
        
        if alignment.horizontal:
            result["horizontal"] = alignment.horizontal
        if alignment.vertical:
            result["vertical"] = alignment.vertical
        if alignment.wrap_text:
            result["wrap_text"] = alignment.wrap_text
        if alignment.indent:
            result["indent"] = alignment.indent
        if alignment.text_rotation:
            result["text_rotation"] = alignment.text_rotation
        
        return result

    def _deserialize_color(self, color_dict):
        """
        Convert serialized color dict back to openpyxl Color object
        
        Args:
            color_dict: Dict with type and value (e.g., {"type": "rgb", "value": "#00F"})
        
        Returns:
            String hex color for openpyxl (without #)
        """
        from openpyxl.styles import Color
        
        if not color_dict or not isinstance(color_dict, dict):
            return None
        
        color_type = color_dict.get('type')
        value = color_dict.get('value')
        
        if color_type == 'rgb' and isinstance(value, str):
            # Remove # if present and return hex
            return value.lstrip('#')
        elif color_type == 'theme':
            # Return theme color
            return Color(theme=value, tint=color_dict.get('tint', 0.0))
        elif color_type == 'indexed':
            # Return indexed color
            return Color(indexed=value)
        
        return None

    def _serialize_color(self, color):
        """
        Convert Color object to compressed hex string, handling RGB, theme, and indexed colors
        
        For RGB: returns short hex (e.g., "#00F") or full hex (e.g., "#0000FF")
        For theme/indexed: returns dict with type and value
        """
        if not color:
            return None
        
        # Check color type (openpyxl Color objects have a 'type' attribute)
        color_type = color.type if hasattr(color, 'type') else None
        
        # RGB color - compress to short hex when possible
        if color_type == 'rgb' and hasattr(color, 'rgb'):
            rgb = color.rgb
            # Validate RGB (must be string, at least 6 chars, not an error message)
            if rgb and isinstance(rgb, str) and len(rgb) >= 6 and not rgb.startswith('Values'):
                # Extract RGB from AARRGGBB or RRGGBB format
                if len(rgb) == 8:  # AARRGGBB
                    r, g, b = rgb[2:4], rgb[4:6], rgb[6:8]
                elif len(rgb) == 6:  # RRGGBB
                    r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
                else:
                    return {"type": "rgb", "value": rgb}
                
                # Try 3-char compression if possible (e.g., #00F instead of #0000FF)
                if r[0] == r[1] and g[0] == g[1] and b[0] == b[1]:
                    compressed = f"#{r[0]}{g[0]}{b[0]}".upper()
                    return compressed
                else:
                    full_hex = f"#{r}{g}{b}".upper()
                    return full_hex
        
        # Theme color
        elif color_type == 'theme' and hasattr(color, 'theme'):
            try:
                theme = color.theme
                if theme is not None and isinstance(theme, int):
                    result = {
                        "type": "theme",
                        "value": theme
                    }
                    # Include tint if non-zero
                    if hasattr(color, 'tint') and color.tint and color.tint != 0.0:
                        result["tint"] = color.tint
                    return result
            except:
                pass
        
        # Indexed color
        elif color_type == 'indexed' and hasattr(color, 'indexed'):
            try:
                indexed = color.indexed
                if indexed is not None and isinstance(indexed, int):
                    result = {
                        "type": "indexed",
                        "value": indexed
                    }
                    return result
            except:
                pass
        
        # Fallback: try to extract any valid color info
        # This handles cases where type might not be set correctly
        if hasattr(color, 'rgb'):
            try:
                rgb = color.rgb
                if rgb and isinstance(rgb, str) and len(rgb) >= 6 and not rgb.startswith('Values'):
                    return {"type": "rgb", "value": rgb}
            except:
                pass
        
        return None

    def get_state(self):
        """Get current executor state"""
        return {
            'has_workbook': self.workbook is not None,
            'active_sheet': self.active_sheet.title if self.active_sheet else None,
            'sheets': list(self.workbook.sheetnames) if self.workbook else [],
            'created_objects': list(self.created_objects.keys())
        }


# Test the executor
if __name__ == "__main__":
    print("Testing OpenpyxlToolExecutor...")

    executor = OpenpyxlToolExecutor()

    # Test creating a workbook
    result = executor.execute_tool('openpyxl_create_workbook', {})
    print(f"Create workbook: {result}")

    # Test appending data
    result = executor.execute_tool('openpyxl_worksheet_append',
                                  {'iterable': ['Name', 'Age', 'City']})
    print(f"Append header: {result}")

    result = executor.execute_tool('openpyxl_worksheet_append',
                                  {'iterable': ['John', 25, 'New York']})
    print(f"Append data: {result}")

    # Test saving
    result = executor.execute_tool('openpyxl_workbook_save',
                                  {'filename': 'test_outputs/test_executor.xlsx'})
    print(f"Save: {result}")

    # Show state
    print(f"\nFinal state: {executor.get_state()}")
    print("\n✅ Executor test complete!")