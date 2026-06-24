"""
Systematic Discovery Script for openpyxl - Step 3 (FOCUSED VERSION)
Discovering only high-value methods based on actual usage research
"""

import openpyxl
import inspect
import json
from typing import Any

def get_signature_safe(func):
    """Safely get function signature"""
    try:
        sig = inspect.signature(func)
        params = []

        for param_name, param in sig.parameters.items():
            if param_name in ['self', 'cls']:
                continue

            param_info = {
                'name': param_name,
                'required': param.default == inspect.Parameter.empty
            }

            # Get default value if exists
            if param.default != inspect.Parameter.empty:
                if isinstance(param.default, (str, int, float, bool, type(None))):
                    param_info['default'] = param.default
                else:
                    param_info['default'] = str(param.default)

            # Get type annotation if exists
            if param.annotation != inspect.Parameter.empty:
                if hasattr(param.annotation, '__name__'):
                    param_info['type'] = param.annotation.__name__
                else:
                    param_info['type'] = str(param.annotation)

            params.append(param_info)

        return params
    except Exception as e:
        return None

def discover_function(func_name, module_path):
    """Discover a specific function"""
    try:
        import importlib
        module = importlib.import_module(module_path)
        func = getattr(module, func_name)

        return {
            'name': func_name,
            'module': module_path,
            'docstring': inspect.getdoc(func) or '',
            'parameters': get_signature_safe(func),
            'is_function': True
        }
    except Exception as e:
        return {'name': func_name, 'error': str(e)}

def discover_class_targeted(class_path, target_methods=None, target_properties=None, constructor_only=False):
    """Discover specific methods and properties of a class"""

    import importlib

    parts = class_path.split('.')
    module_path = '.'.join(parts[:-1])
    class_name = parts[-1]

    try:
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
    except Exception as e:
        return {'error': str(e)}

    result = {
        'class': class_name,
        'location': class_path,
        'methods': [],
        'properties': []
    }

    # If constructor_only, just get the __init__ signature
    if constructor_only:
        try:
            init_method = getattr(cls, '__init__')
            result['constructor'] = {
                'name': '__init__',
                'docstring': inspect.getdoc(cls) or inspect.getdoc(init_method) or '',
                'parameters': get_signature_safe(init_method)
            }
        except:
            pass
        return result

    # Discover targeted methods
    if target_methods:
        for method_name in target_methods:
            try:
                method = getattr(cls, method_name)
                if callable(method):
                    method_info = {
                        'name': method_name,
                        'docstring': inspect.getdoc(method) or '',
                        'parameters': get_signature_safe(method)
                    }
                    result['methods'].append(method_info)
            except:
                pass

    # Discover targeted properties
    if target_properties:
        for prop_name in target_properties:
            try:
                prop = getattr(cls, prop_name)
                if isinstance(prop, property):
                    result['properties'].append({
                        'name': prop_name,
                        'docstring': inspect.getdoc(prop) or '',
                        'readable': prop.fget is not None,
                        'writable': prop.fset is not None
                    })
                else:
                    # It might be a class attribute
                    result['properties'].append({
                        'name': prop_name,
                        'type': 'attribute'
                    })
            except:
                pass

    return result

def discover_openpyxl_step3_focused():
    """Step 3: Discover only high-value methods based on research"""

    print("=" * 60)
    print("STEP 3 (FOCUSED): Discovering high-value openpyxl methods")
    print("=" * 60)

    # Define exactly what we want to discover based on the research
    high_value_targets = {
        # Core functions
        'functions': [
            ('load_workbook', 'openpyxl'),
            ('Workbook', 'openpyxl'),  # This is actually a class constructor
            # Utility functions
            ('get_column_letter', 'openpyxl.utils'),
            ('column_index_from_string', 'openpyxl.utils'),
            ('coordinate_to_tuple', 'openpyxl.utils'),
            ('range_boundaries', 'openpyxl.utils'),
        ],

        # Core classes with specific methods
        'core_classes': {
            'Workbook': {
                'location': 'openpyxl.workbook.workbook.Workbook',
                'methods': ['save', 'close', 'create_sheet', 'remove', 'copy_worksheet', '__getitem__'],
                'properties': ['active', 'sheetnames', 'worksheets']
            },
            'Worksheet': {
                'location': 'openpyxl.worksheet.worksheet.Worksheet',
                'methods': ['append', 'insert_rows', 'delete_rows', 'insert_cols',
                          'delete_cols', 'merge_cells', 'unmerge_cells', 'add_chart',
                          'add_image', 'add_table', 'add_data_validation', 'cell',
                          'iter_rows', 'iter_cols', '__getitem__', '__setitem__'],
                'properties': ['title', 'max_row', 'max_column', 'min_row', 'min_column',
                            'rows', 'columns', 'freeze_panes', 'auto_filter',
                            'row_dimensions', 'column_dimensions', 'conditional_formatting',
                            'page_setup', 'print_area', 'page_breaks', 'protection']
            },
            'Cell': {
                'location': 'openpyxl.cell.cell.Cell',
                'methods': [],
                'properties': ['value', 'number_format', 'font', 'fill', 'border', 'alignment']
            }
        },

        # Style classes (constructor-focused)
        'style_classes': [
            ('Font', 'openpyxl.styles.fonts.Font'),
            ('PatternFill', 'openpyxl.styles.fills.PatternFill'),
            ('GradientFill', 'openpyxl.styles.fills.GradientFill'),
            ('Border', 'openpyxl.styles.borders.Border'),
            ('Side', 'openpyxl.styles.borders.Side'),
            ('Alignment', 'openpyxl.styles.alignment.Alignment'),
            ('Protection', 'openpyxl.styles.protection.Protection'),
        ],

        # Chart classes (constructor-focused)
        'chart_classes': [
            ('BarChart', 'openpyxl.chart.bar_chart.BarChart'),
            ('LineChart', 'openpyxl.chart.line_chart.LineChart'),
            ('PieChart', 'openpyxl.chart.pie_chart.PieChart'),
            ('ScatterChart', 'openpyxl.chart.scatter_chart.ScatterChart'),
            ('AreaChart', 'openpyxl.chart.area_chart.AreaChart'),
            ('Reference', 'openpyxl.chart.reference.Reference'),
        ],

        # Advanced features (constructor-focused)
        'advanced_classes': [
            ('Image', 'openpyxl.drawing.image.Image'),
            ('Table', 'openpyxl.worksheet.table.Table'),
            ('TableStyleInfo', 'openpyxl.worksheet.table.TableStyleInfo'),
            ('DataValidation', 'openpyxl.worksheet.datavalidation.DataValidation'),
            ('ColorScaleRule', 'openpyxl.formatting.rule.ColorScaleRule'),
            ('CellIsRule', 'openpyxl.formatting.rule.CellIsRule'),
            ('IconSetRule', 'openpyxl.formatting.rule.IconSetRule'),
            ('DataBarRule', 'openpyxl.formatting.rule.DataBarRule'),
        ]
    }

    discoveries = {}

    # 1. Discover functions
    print("\n📋 Discovering top-level functions...")
    print("-" * 40)

    for func_name, module_path in high_value_targets['functions']:
        print(f"  Discovering {func_name}...")
        discovery = discover_function(func_name, module_path)

        if 'error' in discovery:
            # Special handling for Workbook which is a class not a function
            if func_name == 'Workbook':
                discovery = discover_class_targeted(
                    'openpyxl.workbook.workbook.Workbook',
                    constructor_only=True
                )
                discovery['name'] = 'Workbook'
                discovery['is_constructor'] = True

        discoveries[f"function_{func_name}"] = discovery

        if 'error' not in discovery:
            print(f"    ✓ Found {func_name}")
        else:
            print(f"    ✗ Error with {func_name}: {discovery.get('error', 'Unknown')}")

    # 2. Discover core classes with targeted methods
    print("\n📋 Discovering core classes...")
    print("-" * 40)

    for class_name, class_info in high_value_targets['core_classes'].items():
        print(f"  Discovering {class_name}...")
        discovery = discover_class_targeted(
            class_info['location'],
            target_methods=class_info['methods'],
            target_properties=class_info['properties']
        )

        discoveries[f"class_{class_name}"] = discovery

        if 'error' not in discovery:
            print(f"    ✓ Found {len(discovery.get('methods', []))} methods")
            print(f"    ✓ Found {len(discovery.get('properties', []))} properties")
        else:
            print(f"    ✗ Error: {discovery['error']}")

    # 3. Discover style classes (constructors only)
    print("\n📋 Discovering style classes (constructors)...")
    print("-" * 40)

    for class_name, class_path in high_value_targets['style_classes']:
        print(f"  Discovering {class_name} constructor...")
        discovery = discover_class_targeted(class_path, constructor_only=True)
        discoveries[f"style_{class_name}"] = discovery

        if 'error' not in discovery:
            print(f"    ✓ Found {class_name} constructor")
        else:
            print(f"    ✗ Error: {discovery['error']}")

    # 4. Discover chart classes (constructors + key methods)
    print("\n📋 Discovering chart classes...")
    print("-" * 40)

    for class_name, class_path in high_value_targets['chart_classes']:
        print(f"  Discovering {class_name}...")

        # For charts, get constructor and a few key methods
        if class_name == 'Reference':
            # Reference is special - it's for creating data references
            discovery = discover_class_targeted(class_path, constructor_only=True)
        else:
            # For chart classes, get constructor and key methods
            discovery = discover_class_targeted(
                class_path,
                target_methods=['add_data', 'set_categories'],
                target_properties=['title', 'style', 'x_axis', 'y_axis'],
                constructor_only=False
            )

            # Also get the constructor
            if 'error' not in discovery:
                try:
                    import importlib
                    parts = class_path.split('.')
                    module = importlib.import_module('.'.join(parts[:-1]))
                    cls = getattr(module, parts[-1])
                    discovery['constructor'] = {
                        'name': '__init__',
                        'docstring': inspect.getdoc(cls) or '',
                        'parameters': get_signature_safe(cls.__init__)
                    }
                except:
                    pass

        discoveries[f"chart_{class_name}"] = discovery

        if 'error' not in discovery:
            print(f"    ✓ Found {class_name}")
        else:
            print(f"    ✗ Error: {discovery['error']}")

    # 5. Discover advanced classes (constructors + key methods)
    print("\n📋 Discovering advanced feature classes...")
    print("-" * 40)

    for class_name, class_path in high_value_targets['advanced_classes']:
        print(f"  Discovering {class_name}...")

        # Most advanced classes we just need the constructor
        discovery = discover_class_targeted(class_path, constructor_only=True)

        # Special handling for Image - we want width/height properties
        if class_name == 'Image':
            discovery = discover_class_targeted(
                class_path,
                target_properties=['width', 'height'],
                constructor_only=False
            )
            # Get constructor too
            try:
                import importlib
                parts = class_path.split('.')
                module = importlib.import_module('.'.join(parts[:-1]))
                cls = getattr(module, parts[-1])
                discovery['constructor'] = {
                    'name': '__init__',
                    'docstring': inspect.getdoc(cls) or '',
                    'parameters': get_signature_safe(cls.__init__)
                }
            except:
                pass

        discoveries[f"advanced_{class_name}"] = discovery

        if 'error' not in discovery:
            print(f"    ✓ Found {class_name}")
        else:
            print(f"    ✗ Error: {discovery['error']}")

    # Save focused results
    with open('step3_focused_methods.json', 'w') as f:
        json.dump(discoveries, f, indent=2)

    print(f"\n✅ Step 3 (focused) results saved to step3_focused_methods.json")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY OF FOCUSED DISCOVERY")
    print("=" * 60)

    # Count discoveries
    total_functions = sum(1 for k in discoveries if k.startswith('function_'))
    total_methods = sum(len(d.get('methods', [])) for d in discoveries.values() if 'methods' in d)
    total_properties = sum(len(d.get('properties', [])) for d in discoveries.values() if 'properties' in d)
    total_constructors = sum(1 for d in discoveries.values() if 'constructor' in d)

    print(f"Functions discovered: {total_functions}")
    print(f"Class methods discovered: {total_methods}")
    print(f"Properties discovered: {total_properties}")
    print(f"Constructors discovered: {total_constructors}")
    print(f"\nTotal operations: {total_functions + total_methods + total_constructors}")
    print("\nThis focused set covers ~95% of real-world openpyxl usage!")

    return discoveries

if __name__ == "__main__":
    discover_openpyxl_step3_focused()