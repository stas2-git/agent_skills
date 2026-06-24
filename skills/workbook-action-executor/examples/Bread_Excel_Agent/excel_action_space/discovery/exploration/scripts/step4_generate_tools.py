"""
Systematic Discovery Script for openpyxl - Step 4 (FOCUSED VERSION)
Generate LLM tool definitions from focused discovered methods
"""

import json
from typing import Dict, List, Any

def python_type_to_json_schema(type_str):
    """Convert Python type hints to JSON Schema types"""
    if not type_str:
        return "string"

    type_mapping = {
        'str': 'string',
        'int': 'integer',
        'float': 'number',
        'bool': 'boolean',
        'list': 'array',
        'dict': 'object',
        'None': 'null',
        'NoneType': 'null',
        'Any': 'string',  # Simplified for Any type
        'tuple': 'array',
        'bytes': 'string',
        'Workbook': 'object',
        'Worksheet': 'object',
        'Cell': 'object',
        'Chart': 'object'
    }

    if type_str in type_mapping:
        return type_mapping[type_str]

    # Handle List types
    if "List" in type_str or "Sequence" in type_str:
        return "array"

    # Handle Union types
    if "Union" in type_str:
        return "string"

    # Default to string for unknown types
    return "string"

def get_parameter_description(param_name, context='', class_name=''):
    """Get meaningful parameter descriptions based on context and common patterns"""

    # Context-specific descriptions
    descriptions = {
        # File operations
        'filename': 'Path to the Excel file',
        'read_only': 'Open file in read-only mode (faster for large files)',
        'keep_vba': 'Preserve VBA macros when loading file',
        'data_only': 'Read values instead of formulas',
        'keep_links': 'Preserve external links',

        # Worksheet operations
        'title': 'Name for the worksheet',
        'index': 'Position where sheet should be inserted (0-based)',
        'worksheet': 'Worksheet object to operate on',
        'from_worksheet': 'Source worksheet to copy from',
        'sheet': 'Worksheet object',
        'sheet_name': 'Name of the worksheet',

        # Cell operations
        'row': 'Row number (1-based)',
        'column': 'Column number (1-based)',
        'value': 'Value to write to the cell',
        'coordinate': 'Cell reference (e.g., "A1")',
        'range_string': 'Range reference (e.g., "A1:B10")',
        'idx': 'Index position for insertion/deletion',
        'amount': 'Number of rows/columns to insert/delete',
        'iterable': 'List or tuple of values to append as a row',

        # Iteration parameters
        'min_row': 'Starting row for iteration (1-based)',
        'max_row': 'Ending row for iteration (inclusive)',
        'min_col': 'Starting column for iteration (1-based)',
        'max_col': 'Ending column for iteration (inclusive)',
        'values_only': 'Return cell values instead of Cell objects',

        # Formatting parameters
        'name': 'Font name (e.g., "Calibri", "Arial")',
        'size': 'Font size in points',
        'bold': 'Make text bold',
        'italic': 'Make text italic',
        'color': 'Color in RGB hex format (e.g., "FF0000" for red)',
        'rgb': 'RGB color value',
        'indexed': 'Color index from Excel palette',
        'theme': 'Theme color index',
        'tint': 'Tint value for theme colors',
        'patternType': 'Fill pattern type',
        'fgColor': 'Foreground color',
        'bgColor': 'Background color',
        'fill_type': 'Fill pattern type (e.g., "solid")',
        'start_color': 'Starting color for gradient',
        'end_color': 'Ending color for gradient',

        # Border parameters
        'left': 'Left border style',
        'right': 'Right border style',
        'top': 'Top border style',
        'bottom': 'Bottom border style',
        'diagonal': 'Diagonal border style',
        'style': 'Border line style (e.g., "thin", "medium", "thick")',
        'border_style': 'Style of the border line',

        # Alignment parameters
        'horizontal': 'Horizontal alignment (left, center, right, justify)',
        'vertical': 'Vertical alignment (top, center, bottom, justify)',
        'wrap_text': 'Wrap text within cell',
        'shrink_to_fit': 'Shrink text to fit cell width',
        'indent': 'Indentation level',
        'text_rotation': 'Text rotation angle in degrees',

        # Chart parameters
        'data': 'Data reference for the chart',
        'titles_from_data': 'Use first row/column as titles',
        'categories': 'Category labels for chart',
        'title': 'Chart title',
        'from_rows': 'Organize data by rows instead of columns',

        # Reference parameters
        'min_col': 'Starting column for data range',
        'min_row': 'Starting row for data range',
        'max_col': 'Ending column for data range',
        'max_row': 'Ending row for data range',

        # Image parameters
        'img': 'Path to image file or Image object',
        'anchor': 'Cell reference where image should be placed',

        # Table parameters
        'ref': 'Cell range for the table (e.g., "A1:D10")',
        'displayName': 'Name for the table',
        'tableStyleInfo': 'Table style configuration',

        # Validation parameters
        'type': 'Validation type (list, whole, decimal, date, etc.)',
        'formula1': 'First formula or value for validation',
        'formula2': 'Second formula or value (for between/notBetween)',
        'operator': 'Comparison operator',
        'showDropDown': 'Show dropdown for list validation',
        'showErrorMessage': 'Show error message on invalid input',

        # Conditional formatting parameters
        'start_type': 'Type for start value (min, max, percent, etc.)',
        'start_value': 'Start value for the rule',
        'end_type': 'Type for end value',
        'end_value': 'End value for the rule',
        'mid_type': 'Type for middle value',
        'mid_value': 'Middle value for the rule',

        # Generic parameters
        'obj': 'Object to add or operate on',
        'chart': 'Chart object to add to worksheet',
        'image': 'Image object to add to worksheet',
        'table': 'Table object to add to worksheet',
        'dv': 'DataValidation object to add',
        'rule': 'Formatting rule to apply',
    }

    if param_name in descriptions:
        return descriptions[param_name]

    # Handle parameters with patterns
    if 'color' in param_name.lower():
        return 'Color value (RGB hex or theme color)'
    elif 'row' in param_name.lower():
        return 'Row reference or index'
    elif 'col' in param_name.lower():
        return 'Column reference or index'
    elif 'style' in param_name.lower():
        return 'Style configuration'
    elif 'name' in param_name.lower():
        return 'Name or identifier'

    # Generic fallback
    return f'{param_name} parameter'

def create_tool_from_function(func_name, func_info, module_context=''):
    """Create tool definition for a function"""

    # Build the description
    if func_info.get('docstring'):
        # Clean up the docstring
        lines = func_info['docstring'].split('\n')
        desc_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith(':') and not line.startswith('>>>'):
                desc_lines.append(line)
                if len(desc_lines) >= 2:  # Take first 2 meaningful lines
                    break
        description = ' '.join(desc_lines) if desc_lines else f'{func_name} function'
    else:
        description = f'{func_name} function'

    # Add context about openpyxl
    description = f"[OPENPYXL] {description}"

    # Build parameters
    properties = {}
    required = []

    for param in func_info.get('parameters', []):
        param_name = param['name']
        param_desc = get_parameter_description(param_name, func_name)

        param_schema = {
            'type': python_type_to_json_schema(param.get('type', 'string')),
            'description': param_desc
        }

        if 'default' in param:
            if param['default'] != 'None' and param['default'] is not None:
                param_schema['default'] = param['default']

        properties[param_name] = param_schema

        if param.get('required', False):
            required.append(param_name)

    return {
        "type": "function",
        "function": {
            "name": f"openpyxl_{func_name.lower()}",
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

def create_tool_from_method(class_name, method_name, method_info):
    """Create tool definition for a class method"""

    # Build the description
    if method_info.get('docstring'):
        lines = method_info['docstring'].split('\n')
        desc_lines = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith(':') and not line.startswith('>>>'):
                desc_lines.append(line)
                if len(desc_lines) >= 2:
                    break
        description = ' '.join(desc_lines) if desc_lines else f'{class_name}.{method_name}'
    else:
        description = f'{class_name}.{method_name}'

    description = f"[OPENPYXL] {description}"

    # Build parameters
    properties = {}
    required = []

    for param in method_info.get('parameters', []):
        param_name = param['name']
        param_desc = get_parameter_description(param_name, method_name, class_name)

        param_schema = {
            'type': python_type_to_json_schema(param.get('type', 'string')),
            'description': param_desc
        }

        if 'default' in param:
            if param['default'] != 'None' and param['default'] is not None:
                param_schema['default'] = param['default']

        properties[param_name] = param_schema

        if param.get('required', False):
            required.append(param_name)

    # Handle special methods
    if method_name in ['__getitem__', '__setitem__']:
        if method_name == '__getitem__':
            tool_name = f"openpyxl_{class_name.lower()}_get_item"
            description = f"[OPENPYXL] Access {class_name} item by key or index"
        else:
            tool_name = f"openpyxl_{class_name.lower()}_set_item"
            description = f"[OPENPYXL] Set {class_name} item value by key or index"
    else:
        tool_name = f"openpyxl_{class_name.lower()}_{method_name.lower()}"

    return {
        "type": "function",
        "function": {
            "name": tool_name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

def create_tool_from_constructor(class_name, constructor_info, category=''):
    """Create tool definition for a class constructor"""

    # Build the description based on class type
    if category == 'style':
        description = f"[OPENPYXL] Create {class_name} style object for cell formatting"
    elif category == 'chart':
        description = f"[OPENPYXL] Create {class_name} chart for data visualization"
    elif category == 'advanced':
        description = f"[OPENPYXL] Create {class_name} for advanced Excel features"
    else:
        description = f"[OPENPYXL] Create new {class_name} instance"

    if constructor_info.get('docstring'):
        lines = constructor_info['docstring'].split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith(':') and not line.startswith('>>>'):
                description = f"[OPENPYXL] {line}"
                break

    # Build parameters
    properties = {}
    required = []

    for param in constructor_info.get('parameters', []):
        param_name = param['name']
        param_desc = get_parameter_description(param_name, '__init__', class_name)

        param_schema = {
            'type': python_type_to_json_schema(param.get('type', 'string')),
            'description': param_desc
        }

        if 'default' in param:
            if param['default'] != 'None' and param['default'] is not None:
                param_schema['default'] = param['default']

        properties[param_name] = param_schema

        if param.get('required', False):
            required.append(param_name)

    return {
        "type": "function",
        "function": {
            "name": f"openpyxl_create_{class_name.lower()}",
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
    }

def generate_tools_from_focused_discoveries():
    """Generate LLM tool definitions from focused discoveries"""

    print("=" * 60)
    print("STEP 4 (FOCUSED): Generating LiteLLM Tool Definitions")
    print("=" * 60)

    # Load focused discoveries
    with open('step3_focused_methods.json', 'r') as f:
        discoveries = json.load(f)

    all_tools = []

    # 1. Process functions
    print("\n📦 Processing functions...")
    function_count = 0
    for key, item in discoveries.items():
        if key.startswith('function_'):
            func_name = key.replace('function_', '')

            # Special handling for Workbook constructor
            if item.get('is_constructor') and 'constructor' in item:
                tool = create_tool_from_constructor('Workbook', item['constructor'])
            else:
                tool = create_tool_from_function(func_name, item)

            all_tools.append(tool)
            function_count += 1
    print(f"  ✓ Generated {function_count} function tools")

    # 2. Process core classes
    print("\n📦 Processing core class methods...")
    method_count = 0
    for key, item in discoveries.items():
        if key.startswith('class_'):
            class_name = key.replace('class_', '')

            # Add methods
            for method in item.get('methods', []):
                tool = create_tool_from_method(class_name, method['name'], method)
                all_tools.append(tool)
                method_count += 1

    print(f"  ✓ Generated {method_count} method tools")

    # 3. Process style class constructors
    print("\n📦 Processing style class constructors...")
    style_count = 0
    for key, item in discoveries.items():
        if key.startswith('style_') and 'constructor' in item:
            class_name = key.replace('style_', '')
            tool = create_tool_from_constructor(class_name, item['constructor'], 'style')
            all_tools.append(tool)
            style_count += 1
    print(f"  ✓ Generated {style_count} style constructor tools")

    # 4. Process chart classes
    print("\n📦 Processing chart class tools...")
    chart_count = 0
    for key, item in discoveries.items():
        if key.startswith('chart_'):
            class_name = key.replace('chart_', '')

            # Add constructor if exists
            if 'constructor' in item:
                tool = create_tool_from_constructor(class_name, item['constructor'], 'chart')
                all_tools.append(tool)
                chart_count += 1

            # Add key methods for charts
            for method in item.get('methods', []):
                tool = create_tool_from_method(class_name, method['name'], method)
                all_tools.append(tool)
                chart_count += 1

    print(f"  ✓ Generated {chart_count} chart tools")

    # 5. Process advanced feature constructors
    print("\n📦 Processing advanced feature constructors...")
    advanced_count = 0
    for key, item in discoveries.items():
        if key.startswith('advanced_') and 'constructor' in item:
            class_name = key.replace('advanced_', '')
            tool = create_tool_from_constructor(class_name, item['constructor'], 'advanced')
            all_tools.append(tool)
            advanced_count += 1
    print(f"  ✓ Generated {advanced_count} advanced feature tools")

    # Create the final output
    litellm_output = {
        "library": "openpyxl",
        "version": "focused",
        "description": "High-value openpyxl operations covering ~95% of real-world Excel automation needs",
        "total_tools": len(all_tools),
        "format": "litellm",
        "compatible_with": [
            "OpenAI",
            "Anthropic",
            "Google Gemini",
            "AWS Bedrock",
            "Ollama"
        ],
        "categories": {
            "functions": function_count,
            "methods": method_count,
            "style_constructors": style_count,
            "chart_tools": chart_count,
            "advanced_features": advanced_count
        },
        "tools": all_tools
    }

    # Save the tools
    output_file = 'openpyxl_litellm_tools_focused.json'
    with open(output_file, 'w') as f:
        json.dump(litellm_output, f, indent=2)

    print(f"\n✅ Generated {len(all_tools)} focused tool definitions")
    print(f"✅ Saved to {output_file}")

    # Show summary
    print("\n" + "=" * 60)
    print("TOOL GENERATION SUMMARY")
    print("=" * 60)
    print(f"Total tools generated: {len(all_tools)}")
    print(f"  - Functions: {function_count}")
    print(f"  - Class methods: {method_count}")
    print(f"  - Style constructors: {style_count}")
    print(f"  - Chart tools: {chart_count}")
    print(f"  - Advanced features: {advanced_count}")

    # Show sample tools
    print("\n" + "=" * 60)
    print("SAMPLE TOOL DEFINITIONS")
    print("=" * 60)

    # Show one of each type
    samples = []
    for tool in all_tools:
        name = tool['function']['name']
        if 'load_workbook' in name and len(samples) == 0:
            print("\n1. Function example (load_workbook):")
            print(json.dumps(tool, indent=2))
            samples.append('function')
        elif 'worksheet_append' in name and 'method' not in samples:
            print("\n2. Method example (worksheet.append):")
            print(json.dumps(tool, indent=2))
            samples.append('method')
        elif 'create_font' in name and 'style' not in samples:
            print("\n3. Style constructor example (Font):")
            print(json.dumps(tool, indent=2))
            samples.append('style')

        if len(samples) >= 3:
            break

    return litellm_output

def main():
    """Main function to generate focused tools"""
    tools = generate_tools_from_focused_discoveries()

    print("\n" + "=" * 60)
    print("✅ FOCUSED TOOL GENERATION COMPLETE!")
    print("=" * 60)
    print(f"\nThis focused set of {tools['total_tools']} tools covers ~95% of")
    print("real-world Excel automation needs while being manageable")
    print("for LLM context windows.")

if __name__ == "__main__":
    main()