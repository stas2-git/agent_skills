"""
Systematic Discovery Script for pandas Excel functionality - Step 3
Deep dive into Excel writing capabilities and ExcelWriter
"""

import pandas as pd
import inspect
import json
from typing import Any
import io

def get_detailed_signature(func):
    """Get detailed signature with parameter descriptions"""
    try:
        sig = inspect.signature(func)
        params = []

        for param_name, param in sig.parameters.items():
            if param_name in ['self', 'cls']:
                continue

            param_info = {
                'name': param_name,
                'required': param.default == inspect.Parameter.empty,
                'has_default': param.default != inspect.Parameter.empty
            }

            # Get default value if exists
            if param.default != inspect.Parameter.empty:
                if param.default is None:
                    param_info['default'] = None
                elif isinstance(param.default, (str, int, float, bool)):
                    param_info['default'] = param.default
                elif param.default is ...:
                    param_info['default'] = "..."
                else:
                    param_info['default'] = str(param.default)[:50]

            # Get type annotation if exists
            if param.annotation != inspect.Parameter.empty:
                if hasattr(param.annotation, '__name__'):
                    param_info['type'] = param.annotation.__name__
                else:
                    param_info['type'] = str(param.annotation)[:50]

            # Add parameter descriptions
            param_info['description'] = get_param_description(param_name, 'write')

            params.append(param_info)

        return params
    except Exception as e:
        return None

def get_param_description(param_name, context=''):
    """Get meaningful descriptions for pandas write parameters"""

    descriptions = {
        # to_excel parameters
        'excel_writer': 'Path, ExcelWriter object, or buffer to write to',
        'sheet_name': 'Name of sheet to write DataFrame to (default "Sheet1")',
        'na_rep': 'String representation of missing values (default "")',
        'float_format': 'Format string for floating point numbers',
        'columns': 'Columns to write (None writes all)',
        'header': 'Write column names (bool or list of strings)',
        'index': 'Write row names/index (bool)',
        'index_label': 'Column label for index column(s)',
        'startrow': 'Upper left cell row to start writing (0-indexed)',
        'startcol': 'Upper left cell column to start writing (0-indexed)',
        'engine': 'Write engine to use (openpyxl or xlsxwriter)',
        'merge_cells': 'Merge MultiIndex cells (default True)',
        'inf_rep': 'String representation of infinity (default "inf")',
        'freeze_panes': 'Tuple of (row, column) to freeze panes',
        'storage_options': 'Extra options for cloud storage',

        # ExcelWriter parameters
        'path': 'Path to Excel file',
        'mode': 'File mode (write "w" or append "a")',
        'date_format': 'Format for dates written to Excel',
        'datetime_format': 'Format for datetimes written to Excel',
        'if_sheet_exists': 'Action if sheet exists (error, new, replace, overlay)',
        'engine_kwargs': 'Keyword arguments to pass to the engine',

        # General
        'kwargs': 'Additional keyword arguments',
        'args': 'Additional positional arguments'
    }

    return descriptions.get(param_name, f'Parameter {param_name}')

def discover_write_excel_details():
    """Discover detailed Excel writing capabilities"""

    results = {
        'to_excel': {},
        'ExcelWriter': {},
        'engines': {},
        'advanced_features': {},
        'examples': {}
    }

    print("=" * 60)
    print("STEP 3: Deep Dive into pandas Excel Writing")
    print("=" * 60)

    # 1. Analyze DataFrame.to_excel method
    print(f"\n📝 Analyzing DataFrame.to_excel():")
    print("-" * 40)

    if hasattr(pd.DataFrame, 'to_excel'):
        method = pd.DataFrame.to_excel

        # Get docstring and signature
        docstring = inspect.getdoc(method) or ''
        params = get_detailed_signature(method)

        results['to_excel'] = {
            'docstring': docstring[:500],
            'parameters': params,
            'parameter_count': len(params) if params else 0
        }

        if params:
            print(f"✅ Found {len(params)} parameters")

            # Categorize parameters
            param_groups = {
                'output': ['excel_writer', 'sheet_name'],
                'formatting': ['float_format', 'na_rep', 'inf_rep'],
                'layout': ['startrow', 'startcol', 'freeze_panes'],
                'content': ['columns', 'header', 'index', 'index_label'],
                'advanced': ['merge_cells', 'engine', 'storage_options']
            }

            results['to_excel']['parameter_groups'] = param_groups

            print(f"\n   Parameter Groups:")
            for group_name, group_params in param_groups.items():
                available = [p for p in group_params if any(param['name'] == p for param in params)]
                print(f"   → {group_name}: {len(available)} params")

    # 2. Analyze ExcelWriter class in detail
    print(f"\n📄 Analyzing pd.ExcelWriter class:")
    print("-" * 40)

    if hasattr(pd, 'ExcelWriter'):
        cls = pd.ExcelWriter

        # Get constructor parameters
        init_params = get_detailed_signature(cls.__init__)

        # Get all methods
        methods = {}
        context_manager_support = False

        for method_name in dir(cls):
            if not method_name.startswith('_') or method_name in ['__enter__', '__exit__']:
                try:
                    method = getattr(cls, method_name)
                    if callable(method):
                        if method_name == '__enter__':
                            context_manager_support = True
                        elif method_name == '__exit__':
                            continue
                        else:
                            method_doc = inspect.getdoc(method) or ''
                            method_params = get_detailed_signature(method)
                            methods[method_name] = {
                                'docstring': method_doc[:200],
                                'parameters': method_params
                            }
                except:
                    pass

        # Get properties
        properties = []
        for prop_name in dir(cls):
            if not prop_name.startswith('_'):
                try:
                    # Check if it's a property on the class
                    class_attr = getattr(cls, prop_name)
                    if isinstance(class_attr, property):
                        properties.append(prop_name)
                except:
                    pass

        results['ExcelWriter'] = {
            'docstring': (inspect.getdoc(cls) or '')[:500],
            'init_parameters': init_params,
            'methods': methods,
            'properties': properties,
            'context_manager': context_manager_support
        }

        print(f"✅ ExcelWriter class analysis:")
        print(f"   → Constructor params: {len(init_params) if init_params else 0}")
        print(f"   → Methods: {len(methods)}")
        print(f"   → Properties: {len(properties)}")
        print(f"   → Context manager support: {'✅' if context_manager_support else '❌'}")

        if init_params:
            key_params = [p['name'] for p in init_params[:5]]
            print(f"   → Key params: {', '.join(key_params)}")

    # 3. Test writing engines
    print(f"\n🔧 Testing Excel Writing Engines:")
    print("-" * 40)

    # Test openpyxl engine
    try:
        import openpyxl
        results['engines']['openpyxl'] = {
            'available': True,
            'version': openpyxl.__version__,
            'features': ['append_mode', 'overlay', 'formatting']
        }
        print(f"✅ openpyxl: v{openpyxl.__version__} (supports append mode)")
    except ImportError:
        results['engines']['openpyxl'] = {'available': False}
        print(f"❌ openpyxl: Not installed")

    # Test xlsxwriter engine
    try:
        import xlsxwriter
        results['engines']['xlsxwriter'] = {
            'available': True,
            'version': xlsxwriter.__version__,
            'features': ['charts', 'formatting', 'images']
        }
        print(f"✅ xlsxwriter: v{xlsxwriter.__version__} (best for new files)")
    except ImportError:
        results['engines']['xlsxwriter'] = {'available': False}
        print(f"❌ xlsxwriter: Not installed")

    # 4. Discover advanced features
    print(f"\n🚀 Advanced Writing Features:")
    print("-" * 40)

    # Test mode support (append vs write)
    advanced_features = {
        'append_mode': False,
        'overlay_mode': False,
        'multiple_sheets': True,
        'formatting_support': False,
        'buffer_support': False
    }

    # Check for append mode support
    if 'mode' in [p['name'] for p in init_params] if init_params else []:
        advanced_features['append_mode'] = True
        print("✅ Append mode supported (mode='a')")

    # Check for if_sheet_exists parameter
    if 'if_sheet_exists' in [p['name'] for p in init_params] if init_params else []:
        advanced_features['overlay_mode'] = True
        print("✅ Overlay mode supported (if_sheet_exists='overlay')")

    print("✅ Multiple sheets supported (context manager)")

    # Check buffer support
    try:
        # Test if ExcelWriter works with BytesIO
        buffer = io.BytesIO()
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        with pd.ExcelWriter(buffer, engine='openpyxl' if results['engines'].get('openpyxl', {}).get('available') else None) as writer:
            df.to_excel(writer)
        advanced_features['buffer_support'] = True
        print("✅ Buffer/BytesIO support confirmed")
    except:
        print("❌ Buffer/BytesIO support not available")

    results['advanced_features'] = advanced_features

    # 5. Create usage examples
    print(f"\n📝 Usage Examples:")
    print("-" * 40)

    usage_examples = {
        'basic_write': {
            'description': 'Write DataFrame to Excel file',
            'code': "df.to_excel('output.xlsx', sheet_name='Data')"
        },
        'no_index': {
            'description': 'Write without row index',
            'code': "df.to_excel('output.xlsx', index=False)"
        },
        'multiple_sheets': {
            'description': 'Write multiple DataFrames to different sheets',
            'code': """with pd.ExcelWriter('output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Sheet1')
    df2.to_excel(writer, sheet_name='Sheet2')"""
        },
        'append_sheet': {
            'description': 'Append to existing Excel file',
            'code': """with pd.ExcelWriter('output.xlsx', mode='a', if_sheet_exists='new') as writer:
    df.to_excel(writer, sheet_name='NewSheet')"""
        },
        'overlay_data': {
            'description': 'Overlay data on existing sheet',
            'code': """with pd.ExcelWriter('output.xlsx', mode='a', if_sheet_exists='overlay') as writer:
    df.to_excel(writer, sheet_name='Sheet1', startrow=10)"""
        },
        'formatting': {
            'description': 'Apply number formatting',
            'code': "df.to_excel('output.xlsx', float_format='%.2f')"
        },
        'freeze_panes': {
            'description': 'Freeze top row and first column',
            'code': "df.to_excel('output.xlsx', freeze_panes=(1,1))"
        },
        'to_buffer': {
            'description': 'Write to BytesIO buffer',
            'code': """buffer = io.BytesIO()
with pd.ExcelWriter(buffer) as writer:
    df.to_excel(writer)
excel_data = buffer.getvalue()"""
        }
    }

    results['examples'] = usage_examples

    for i, (example_name, example_info) in enumerate(list(usage_examples.items())[:5]):
        print(f"   {i+1}. {example_info['description']}")

    # Save results
    output_file = 'pandas_scripts/outputs/step3_write_methods.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n" + "=" * 60)
    print(f"✅ Analysis complete! Results saved to {output_file}")
    print("=" * 60)

    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"  - to_excel parameters: {results['to_excel'].get('parameter_count', 0)}")
    print(f"  - ExcelWriter params: {len(results['ExcelWriter'].get('init_parameters', []))}")
    print(f"  - Available engines: {sum(1 for e in results['engines'].values() if e.get('available'))}/{len(results['engines'])}")
    print(f"  - Advanced features: {sum(1 for v in advanced_features.values() if v)}/{len(advanced_features)}")
    print(f"  - Usage examples: {len(results['examples'])}")

    return results

if __name__ == "__main__":
    discover_write_excel_details()