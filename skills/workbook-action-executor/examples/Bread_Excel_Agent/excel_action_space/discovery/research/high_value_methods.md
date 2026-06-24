# High-Value openpyxl Methods Based on Actual Usage

Based on Stack Overflow questions, tutorials, and real-world usage patterns, these are the most commonly used openpyxl operations:

## 1. File Operations (ESSENTIAL)
- `load_workbook()` - Open existing files (with data_only, read_only params)
- `Workbook()` - Create new workbook
- `save()` - Save file
- `close()` - Close file

## 2. Worksheet Operations (ESSENTIAL)
- `active` - Get active sheet
- `create_sheet()` - Add new sheet
- `remove()` - Delete sheet
- `title` - Get/set sheet name
- `sheetnames` - List all sheets

## 3. Cell Read/Write (ESSENTIAL)
- `ws['A1']` - Cell access by reference
- `ws.cell(row=1, column=1)` - Cell access by indices
- `.value` - Get/set cell value
- `append()` - Add row of data
- `iter_rows()` - Iterate through rows
- `iter_cols()` - Iterate through columns

## 4. Range Information (ESSENTIAL)
- `max_row` - Get last row with data
- `max_column` - Get last column with data
- `min_row` - Get first row with data
- `min_column` - Get first column with data

## 5. Basic Formatting (HIGH USAGE)
- `Font()` - Font styling (bold, size, color)
- `PatternFill()` - Background colors
- `Alignment()` - Text alignment
- `Border()` & `Side()` - Cell borders

## 6. Formulas (HIGH USAGE)
- Writing formulas: `ws['A1'] = '=SUM(B1:B10)'`
- `data_only` parameter in load_workbook

## 7. Row/Column Operations (MEDIUM USAGE)
- `insert_rows()` - Insert rows
- `insert_cols()` - Insert columns
- `delete_rows()` - Delete rows
- `delete_cols()` - Delete columns
- `row_dimensions[x].height` - Row height
- `column_dimensions['A'].width` - Column width

## 8. Merge Operations (MEDIUM USAGE)
- `merge_cells()` - Merge cell range
- `unmerge_cells()` - Unmerge cells

## 9. Common Utility (MEDIUM USAGE)
- `get_column_letter()` - Convert column number to letter
- `column_index_from_string()` - Convert letter to number
- `coordinate_to_tuple()` - Parse cell reference

## 10. Charts (LOWER BUT IMPORTANT)
- `BarChart()` - Bar charts
- `LineChart()` - Line charts
- `PieChart()` - Pie charts
- `add_chart()` - Add chart to sheet

## Methods to SKIP (rarely used or internal):
- Deprecated methods (get_sheet_by_name, get_sheet_names)
- Internal methods (anything with _)
- Advanced chart variants (3D charts, projected charts)
- Complex style methods (individual property setters)
- Protection/security methods (rarely used)
- VBA-related (openpyxl can't execute VBA)

## TOTAL HIGH-VALUE METHODS: ~40-50

This gives us a focused set of tools that cover 95% of real-world usage!

Here's the **comprehensive list covering 95%** of useful openpyxl functionality that you'll actually use in real projects:[1][2][3]

### Core File Operations
- `from openpyxl import Workbook, load_workbook`
- `Workbook()` - Create new workbooks
- `load_workbook(filename, read_only=True/False, data_only=True/False)` - Open files
- `workbook.save(filename)` - Save files
- `workbook.close()` - Close workbooks properly

### Workbook & Worksheet Management
- `workbook.active` - Get active sheet
- `workbook.sheetnames` - List all sheet names
- `workbook["Sheet Name"]` - Access specific sheet
- `workbook.create_sheet(title="Name", index=0)` - Create new sheets
- `workbook.remove(sheet)` - Delete sheets
- `sheet.title = "New Name"` - Rename sheets
- `workbook.copy_worksheet(sheet)` - Duplicate sheets

### Cell Access & Data Operations
- `sheet["A1"] = value` - Write to specific cell
- `sheet["A1"].value` - Read from cell
- `sheet.cell(row=1, column=1, value="data")` - Access by coordinates
- `sheet.append([list, of, values])` - Add entire rows
- `sheet.insert_rows(idx=1, amount=1)` - Insert rows
- `sheet.delete_rows(idx=1, amount=1)` - Delete rows
- `sheet.insert_cols(idx=1, amount=1)` - Insert columns
- `sheet.delete_cols(idx=1, amount=1)` - Delete columns

### Data Iteration & Range Operations
- `sheet.iter_rows(min_row=1, max_row=10, values_only=True)` - Most common iteration
- `sheet.iter_cols(min_col=1, max_col=5, values_only=True)` - Column iteration
- `sheet.rows` and `sheet.columns` - Access all rows/columns
- `sheet.max_row` and `sheet.max_column` - Find data boundaries
- `sheet["A1:C10"]` - Access cell ranges
- `sheet.merge_cells("A1:C1")` and `sheet.unmerge_cells("A1:C1")` - Cell merging

### Formatting & Styles (Essential)
```python
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
```
- `Font(bold=True, italic=True, color="FF0000", size=14)` - Text formatting
- `PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")` - Background colors
- `Border(left=Side(style='thin'), right=Side(style='thin'))` - Cell borders
- `Alignment(horizontal="center", vertical="center", wrap_text=True)` - Text alignment
- `cell.number_format = "$#,##0.00"` - Number formatting (currency, percentage, dates)

### Formulas & Calculations
- `sheet["D1"] = "=SUM(A1:C1)"` - Basic formulas
- `sheet["E1"] = "=VLOOKUP(A1, Table1, 2, FALSE)"` - Advanced formulas
- `workbook.calculation_mode = "automatic"` - Formula calculation control
- `data_only=True` in load_workbook to get formula results instead of formulas

### Charts (Very Useful)
```python
from openpyxl.chart import BarChart, LineChart, PieChart, ScatterChart, Reference
```
- `BarChart()`, `LineChart()`, `PieChart()`, `ScatterChart()` - Chart types
- `Reference(sheet, min_col=1, min_row=1, max_col=3, max_row=10)` - Data references
- `chart.add_data(data, titles_from_data=True)` - Add data to charts
- `chart.set_categories(categories)` - Set chart categories
- `chart.title = "Chart Title"` - Chart titles and axis labels
- `chart.x_axis.title = "X Axis"` and `chart.y_axis.title = "Y Axis"`
- `chart.style = 10` - Chart styling (1-48 styles available)
- `sheet.add_chart(chart, "E5")` - Add chart to worksheet

### Images & Media
```python
from openpyxl.drawing.image import Image
```
- `Image("image.png")` - Load images
- `sheet.add_image(img, "A1")` - Insert images into sheets
- `img.width = 300` and `img.height = 200` - Resize images

### Tables (Professional Look)
```python
from openpyxl.worksheet.table import Table, TableStyleInfo
```
- `Table(displayName="Table1", ref="A1:D10")` - Create Excel tables
- `TableStyleInfo(name="TableStyleMedium9", showRowStripes=True)` - Table styling
- `sheet.add_table(table)` - Add tables to worksheets

### Data Validation
```python
from openpyxl.worksheet.datavalidation import DataValidation
```
- `DataValidation(type="list", formula1='"Option1,Option2,Option3"')` - Dropdown lists
- `DataValidation(type="whole", operator="between", formula1=1, formula2=100)` - Number validation
- `sheet.add_data_validation(validation)` - Apply validation rules

### Conditional Formatting
```python
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule
```
- `ColorScaleRule(start_type='min', start_color='AA0000', end_type='max', end_color='00AA00')` - Color scales
- `CellIsRule(operator='greaterThan', formula=['50'], fill=redFill)` - Conditional rules
- `sheet.conditional_formatting.add("A1:A10", rule)` - Apply conditional formatting

### Advanced Features (When Needed)
- `sheet.freeze_panes = "B2"` - Freeze panes
- `sheet.auto_filter.ref = "A1:D10"` - Add filters
- `sheet.page_setup.orientation = sheet.ORIENTATION_LANDSCAPE` - Page setup
- `sheet.print_area = "A1:F20"` - Print areas
- `sheet.page_breaks` - Page break control
- `sheet.protection.sheet = True` - Sheet protection

### Performance & Memory Management
- `load_workbook(filename, read_only=True)` - Read-only mode for large files
- `load_workbook(filename, data_only=True)` - Get calculated values instead of formulas
- `openpyxl.writer.excel.save_workbook(workbook, filename, as_template=False)` - Advanced saving options

This covers **95% of practical openpyxl usage**. The advanced formatting, charts, tables, and data validation features are what separate professional-looking spreadsheets from basic data dumps. Most real-world projects use a combination of these features rather than just basic cell operations.[2][4][5][3][6][7]

[1](https://openpyxl.readthedocs.io/en/3.1/tutorial.html)
[2](https://realpython.com/openpyxl-excel-spreadsheets-python/)
[3](https://www.youtube.com/watch?v=hZsAvEtg_zI)
[4](https://www.spsanderson.com/steveondata/posts/2025-09-10/)
[5](https://changhsinlee.com/pyderpuffgirls-ep8/)
[6](https://www.geeksforgeeks.org/python/introduction-to-python-openpyxl/)
[7](https://openpyxl.readthedocs.io/en/stable/styles.html)
[8](https://www.reddit.com/r/Python/comments/cwgvvt/a_guide_to_excel_spreadsheets_in_python_with/)
[9](https://openpyxl.readthedocs.io)
[10](https://krython.com/tutorial/python/excel-files-openpyxl-and-pandas/)
[11](https://stackoverflow.com/questions/48657867/manipulate-existing-excel-table-using-openpyxl)
[12](https://www.youtube.com/watch?v=M4Q8ljPyVDQ)
[13](https://www.geeksforgeeks.org/python/creating-the-workbook-and-worksheet-using-openpyxl-in-python/)
[14](https://openpyxl.readthedocs.io/en/stable/charts/introduction.html)
[15](https://stackoverflow.com/questions/46816397/how-do-i-format-all-the-cells-in-an-excel-to-a-single-style-using-openpyxl)
[16](https://www.pythonexcel.com/openpyxl.php)