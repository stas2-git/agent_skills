class openpyxl.workbook.workbook.Workbook(write_only=False, iso_dates=False)[source]
Bases: object

Workbook is the container for all other parts of the document.

property active
Get the currently active sheet or None

Type:
openpyxl.worksheet.worksheet.Worksheet

add_named_style(style)[source]
Add a named style

property chartsheets
A list of Chartsheets in this workbook

Type:
list of openpyxl.chartsheet.chartsheet.Chartsheet

close()[source]
Close workbook file if open. Only affects read-only and write-only modes.

copy_worksheet(from_worksheet)[source]
Copy an existing worksheet in the current workbook

Warning This function cannot copy worksheets between workbooks. worksheets can only be copied within the workbook that they belong
Parameters:
from_worksheet – the worksheet to be copied from

Returns:
copy of the initial worksheet

create_chartsheet(title=None, index=None)[source]
create_named_range(name, worksheet=None, value=None, scope=None)[source]
Create a new named_range on a worksheet

Note Deprecated: Assign scoped named ranges directly to worksheets or global ones to the workbook. Deprecated in 3.1
create_sheet(title=None, index=None)[source]
Create a worksheet (at an optional index).

Parameters:
title (str) – optional title of the sheet

index (int) – optional position at which the sheet will be inserted

property data_only
property epoch
property excel_base_date
get_index(worksheet)[source]
Return the index of the worksheet.

Note Deprecated: Use wb.index(worksheet)
get_sheet_by_name(name)[source]
Returns a worksheet by its name.

param name:
the name of the worksheet to look for

type name:
string

Note Deprecated: Use wb[sheetname]
get_sheet_names()[source]
Note Deprecated: Use wb.sheetnames
index(worksheet)[source]
Return the index of a worksheet.

property mime_type
The mime type is determined by whether a workbook is a template or not and whether it contains macros or not. Excel requires the file extension to match but openpyxl does not enforce this.

move_sheet(sheet, offset=0)[source]
Move a sheet or sheetname

property named_styles
List available named styles

path = '/xl/workbook.xml'
property read_only
remove(worksheet)[source]
Remove worksheet from this workbook.

remove_sheet(worksheet)[source]
Remove worksheet from this workbook.

Note Deprecated: Use wb.remove(worksheet) or del wb[sheetname]
save(filename)[source]
Save the current workbook under the given filename. Use this function instead of using an ExcelWriter.

Warning When creating your workbook using write_only set to True, you will only be able to call this function once. Subsequent attempts to modify or save the file will raise an openpyxl.shared.exc.WorkbookAlreadySaved exception.
property sheetnames
Returns the list of the names of worksheets in this workbook.

Names are returned in the worksheets order.

Type:
list of strings

property style_names
List of named styles

template = False
property worksheets
A list of sheets in this workbook

Type:
list of openpyxl.worksheet.worksheet.Worksheet

property write_only


Worksheet is the 2nd-level container in Excel.

class openpyxl.worksheet.worksheet.Worksheet(parent, title=None)[source]
Bases: _WorkbookChild

Represents a worksheet.

Do not create worksheets yourself, use openpyxl.workbook.Workbook.create_sheet() instead

BREAK_COLUMN = 2
BREAK_NONE = 0
BREAK_ROW = 1
ORIENTATION_LANDSCAPE = 'landscape'
ORIENTATION_PORTRAIT = 'portrait'
PAPERSIZE_A3 = '8'
PAPERSIZE_A4 = '9'
PAPERSIZE_A4_SMALL = '10'
PAPERSIZE_A5 = '11'
PAPERSIZE_EXECUTIVE = '7'
PAPERSIZE_LEDGER = '4'
PAPERSIZE_LEGAL = '5'
PAPERSIZE_LETTER = '1'
PAPERSIZE_LETTER_SMALL = '2'
PAPERSIZE_STATEMENT = '6'
PAPERSIZE_TABLOID = '3'
SHEETSTATE_HIDDEN = 'hidden'
SHEETSTATE_VERYHIDDEN = 'veryHidden'
SHEETSTATE_VISIBLE = 'visible'
property active_cell
add_chart(chart, anchor=None)[source]
Add a chart to the sheet Optionally provide a cell for the top-left anchor

add_data_validation(data_validation)[source]
Add a data-validation object to the sheet. The data-validation object defines the type of data-validation to be applied and the cell or range of cells it should apply to.

add_image(img, anchor=None)[source]
Add an image to the sheet. Optionally provide a cell for the top-left anchor

add_pivot(pivot)[source]
add_table(table)[source]
Check for duplicate name in definedNames and other worksheet tables before adding table.

append(iterable)[source]
Appends a group of values at the bottom of the current sheet.

If it’s a list: all values are added in order, starting from the first column

If it’s a dict: values are assigned to the columns indicated by the keys (numbers or letters)

Parameters:
iterable (list|tuple|range|generator or dict) – list, range or generator, or dict containing values to append

Usage:

append([‘This is A1’, ‘This is B1’, ‘This is C1’])

or append({‘A’ : ‘This is A1’, ‘C’ : ‘This is C1’})

or append({1 : ‘This is A1’, 3 : ‘This is C1’})

Raise:
TypeError when iterable is neither a list/tuple nor a dict

property array_formulae
Returns a dictionary of cells with array formulae and the cells in array

calculate_dimension()[source]
Return the minimum bounding range for all cells containing data (ex. ‘A1:M24’)

Return type:
string

cell(row, column, value=None)[source]
Returns a cell object based on the given coordinates.

Usage: cell(row=15, column=1, value=5)

Calling cell creates cells in memory when they are first accessed.

Parameters:
row (int) – row index of the cell (e.g. 4)

column (int) – column index of the cell (e.g. 3)

value (numeric or time or string or bool or none) – value of the cell (e.g. 5)

Return type:
openpyxl.cell.cell.Cell

property column_groups
Return a list of column ranges where more than one column

property columns
Produces all cells in the worksheet, by column (see iter_cols())

delete_cols(idx, amount=1)[source]
Delete column or columns from col==idx

delete_rows(idx, amount=1)[source]
Delete row or rows from row==idx

property dimensions
Returns the result of calculate_dimension()

property freeze_panes
insert_cols(idx, amount=1)[source]
Insert column or columns before col==idx

insert_rows(idx, amount=1)[source]
Insert row or rows before row==idx

iter_cols(min_col=None, max_col=None, min_row=None, max_row=None, values_only=False)[source]
Produces cells from the worksheet, by column. Specify the iteration range using indices of rows and columns.

If no indices are specified the range starts at A1.

If no cells are in the worksheet an empty tuple will be returned.

Parameters:
min_col (int) – smallest column index (1-based index)

min_row (int) – smallest row index (1-based index)

max_col (int) – largest column index (1-based index)

max_row (int) – largest row index (1-based index)

values_only (bool) – whether only cell values should be returned

Return type:
generator

iter_rows(min_row=None, max_row=None, min_col=None, max_col=None, values_only=False)[source]
Produces cells from the worksheet, by row. Specify the iteration range using indices of rows and columns.

If no indices are specified the range starts at A1.

If no cells are in the worksheet an empty tuple will be returned.

Parameters:
min_col (int) – smallest column index (1-based index)

min_row (int) – smallest row index (1-based index)

max_col (int) – largest column index (1-based index)

max_row (int) – largest row index (1-based index)

values_only (bool) – whether only cell values should be returned

Return type:
generator

property max_column
The maximum column index containing data (1-based)

Type:
int

property max_row
The maximum row index containing data (1-based)

Type:
int

merge_cells(range_string=None, start_row=None, start_column=None, end_row=None, end_column=None)[source]
Set merge on a cell range. Range is a cell range (e.g. A1:E1)

property merged_cell_ranges
Return a copy of cell ranges

Note Deprecated: Use ws.merged_cells.ranges
mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml'
property min_column
The minimum column index containing data (1-based)

Type:
int

property min_row
The minimum row index containing data (1-based)

Type:
int

move_range(cell_range, rows=0, cols=0, translate=False)[source]
Move a cell range by the number of rows and/or columns: down if rows > 0 and up if rows < 0 right if cols > 0 and left if cols < 0 Existing cells will be overwritten. Formulae and references will not be updated.

property print_area
The print area for the worksheet, or None if not set. To set, supply a range like ‘A1:D4’ or a list of ranges.

property print_title_cols
Columns to be printed at the left side of every page (ex: ‘A:C’)

property print_title_rows
Rows to be printed at the top of every page (ex: ‘1:3’)

property print_titles
property rows
Produces all cells in the worksheet, by row (see iter_rows())

Type:
generator

property selected_cell
set_printer_settings(paper_size, orientation)[source]
Set printer settings

property sheet_view
property show_gridlines
property tables
unmerge_cells(range_string=None, start_row=None, start_column=None, end_row=None, end_column=None)[source]
Remove merge on a cell range. Range is a cell range (e.g. A1:E1)

property values
Produces all cell values in the worksheet, by row

Type:
generator

openpyxl.worksheet.worksheet.isgenerator(obj)


Manage individual cells in a spreadsheet.

The Cell class is required to know its value and type, display options, and any other features of an Excel cell. Utilities for referencing cells using Excel’s ‘A1’ column/row nomenclature are also provided.

class openpyxl.cell.cell.Cell(worksheet, row=None, column=None, value=None, style_array=None)[source]
Bases: StyleableObject

Describes cell associated properties.

Properties of interest include style, type, value, and address.

property base_date
check_error(value)[source]
Tries to convert Error” else N/A

check_string(value)[source]
Check string coding, length, and line break character

property col_idx
The numerical index of the column

column
Column number of this cell (1-based)

property column_letter
property comment
Returns the comment associated with this cell

Type:
openpyxl.comments.Comment

property coordinate
This cell’s coordinate (ex. ‘A5’)

data_type
property encoding
property hyperlink
Return the hyperlink target or an empty string

property internal_value
Always returns the value for excel.

property is_date
True if the value is formatted as a date

Type:
bool

offset(row=0, column=0)[source]
Returns a cell location relative to this cell.

Parameters:
row (int) – number of rows to offset

column (int) – number of columns to offset

Return type:
openpyxl.cell.Cell

parent
row
Row number of this cell (1-based)

property value
Get or set the value held in the cell.

Type:
depends on the value (string, float, int or datetime.datetime)

class openpyxl.cell.cell.MergedCell(worksheet, row=None, column=None)[source]
Bases: StyleableObject

Describes the properties of a cell in a merged cell and helps to display the borders of the merged cell.

The value of a MergedCell is always None.

column
comment = None
property coordinate
This cell’s coordinate (ex. ‘A5’)

data_type = 'n'
hyperlink = None
row
value = None
openpyxl.cell.cell.WriteOnlyCell(ws=None, value=None)[source]
openpyxl.cell.cell.get_time_format(t)[source]
openpyxl.cell.cell.get_type(t, value)[source]
