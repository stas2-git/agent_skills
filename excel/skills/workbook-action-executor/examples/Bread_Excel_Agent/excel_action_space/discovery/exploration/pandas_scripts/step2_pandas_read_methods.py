"""
Systematic Discovery Script for pandas Excel functionality - Step 2
Deep dive into Excel reading capabilities and parameters
"""

import pandas as pd
import inspect
import json
from typing import Any

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
                    param_info['default'] = str(param.default)[:50]  # Truncate long defaults

            # Get type annotation if exists
            if param.annotation != inspect.Parameter.empty:
                if hasattr(param.annotation, '__name__'):
                    param_info['type'] = param.annotation.__name__
                else:
                    param_info['type'] = str(param.annotation)[:50]

            # Add parameter descriptions based on common pandas patterns
            param_info['description'] = get_param_description(param_name, 'read_excel')

            params.append(param_info)

        return params
    except Exception as e:
        return None

def get_param_description(param_name, context=''):
    """Get meaningful descriptions for pandas parameters"""

    descriptions = {
        # read_excel parameters
        'io': 'Path to Excel file, URL, or file-like object',
        'sheet_name': 'Name/index of sheet(s) to read (None for all sheets)',
        'header': 'Row number(s) to use as column names',
        'names': 'List of column names to use',
        'index_col': 'Column(s) to use as row labels',
        'usecols': 'Columns to parse (column names, indices, or callable)',
        'dtype': 'Data type for columns (dict or type)',
        'engine': 'Parser engine to use (openpyxl, xlrd, odf, pyxlsb)',
        'converters': 'Dict of functions for converting column values',
        'true_values': 'Values to consider as True',
        'false_values': 'Values to consider as False',
        'skiprows': 'Rows to skip at the beginning',
        'nrows': 'Number of rows to read',
        'na_values': 'Additional values to treat as NA/NaN',
        'keep_default_na': 'Whether to include default NaN values',
        'na_filter': 'Detect missing values (False can improve performance)',
        'verbose': 'Indicate number of NA values placed in non-numeric columns',
        'parse_dates': 'Parse date columns (bool, list, or dict)',
        'date_parser': 'Function to parse dates (deprecated, use date_format)',
        'date_format': 'Format string for parsing dates',
        'thousands': 'Thousands separator character',
        'decimal': 'Decimal separator character',
        'comment': 'Character indicating remainder of line is a comment',
        'skipfooter': 'Number of rows to skip at end of file',
        'mangle_dupe_cols': 'Rename duplicate columns',
        'storage_options': 'Extra options for remote file storage',
        'dtype_backend': 'Backend data type to use (numpy_nullable or pyarrow)',
        'engine_kwargs': 'Arbitrary keyword arguments passed to engine',

        # ExcelFile parameters
        'path_or_buffer': 'Path to Excel file or file-like object',

        # General parameters
        'kwargs': 'Additional keyword arguments',
        'args': 'Additional positional arguments'
    }

    return descriptions.get(param_name, f'Parameter {param_name}')

def discover_read_excel_details():
    """Discover detailed read_excel capabilities"""

    results = {
        'read_excel': {},
        'ExcelFile': {},
        'engines': {},
        'examples': {}
    }

    print("=" * 60)
    print("STEP 2: Deep Dive into pandas Excel Reading")
    print("=" * 60)

    # 1. Detailed analysis of pd.read_excel
    print(f"\n📖 Analyzing pd.read_excel():")
    print("-" * 40)

    if hasattr(pd, 'read_excel'):
        func = pd.read_excel

        # Get full docstring
        docstring = inspect.getdoc(func) or ''

        # Get signature
        params = get_detailed_signature(func)

        results['read_excel'] = {
            'docstring': docstring[:500],  # First 500 chars
            'parameters': params,
            'parameter_count': len(params) if params else 0
        }

        if params:
            print(f"✅ Found {len(params)} parameters")

            # Categorize parameters
            required_params = [p for p in params if p.get('required', False)]
            optional_params = [p for p in params if not p.get('required', False)]

            print(f"   → Required: {len(required_params)}")
            print(f"   → Optional: {len(optional_params)}")

            # Group parameters by functionality
            param_groups = {
                'file_handling': ['io', 'sheet_name', 'engine', 'storage_options'],
                'data_selection': ['header', 'names', 'index_col', 'usecols', 'skiprows', 'nrows'],
                'type_conversion': ['dtype', 'converters', 'true_values', 'false_values', 'parse_dates'],
                'missing_data': ['na_values', 'keep_default_na', 'na_filter'],
                'formatting': ['thousands', 'decimal', 'comment']
            }

            results['read_excel']['parameter_groups'] = param_groups

            print(f"\n   Parameter Groups:")
            for group_name, group_params in param_groups.items():
                available = [p for p in group_params if any(param['name'] == p for param in params)]
                print(f"   → {group_name}: {len(available)} params")

    # 2. Analyze ExcelFile class
    print(f"\n📁 Analyzing pd.ExcelFile class:")
    print("-" * 40)

    if hasattr(pd, 'ExcelFile'):
        cls = pd.ExcelFile

        # Get constructor parameters
        init_params = get_detailed_signature(cls.__init__)

        # Get methods
        methods = {}
        for method_name in dir(cls):
            if not method_name.startswith('_'):
                try:
                    method = getattr(cls, method_name)
                    if callable(method) and method_name != '__class__':
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
                    prop = getattr(cls, prop_name)
                    if isinstance(prop, property):
                        properties.append(prop_name)
                except:
                    pass

        results['ExcelFile'] = {
            'docstring': (inspect.getdoc(cls) or '')[:500],
            'init_parameters': init_params,
            'methods': methods,
            'properties': properties
        }

        print(f"✅ ExcelFile class analysis:")
        print(f"   → Constructor params: {len(init_params) if init_params else 0}")
        print(f"   → Methods: {len(methods)}")
        print(f"   → Properties: {len(properties)}")

        if methods:
            print(f"   → Key methods: {', '.join(list(methods.keys())[:5])}")

    # 3. Test engine availability
    print(f"\n🔧 Testing Excel Engine Availability:")
    print("-" * 40)

    engines_to_test = ['openpyxl', 'xlrd', 'odf', 'pyxlsb']

    for engine_name in engines_to_test:
        try:
            # Try importing the engine
            if engine_name == 'openpyxl':
                import openpyxl
                version = openpyxl.__version__
                results['engines'][engine_name] = {'available': True, 'version': version}
                print(f"✅ {engine_name}: Available (v{version})")
            elif engine_name == 'xlrd':
                import xlrd
                version = xlrd.__version__
                results['engines'][engine_name] = {'available': True, 'version': version}
                print(f"✅ {engine_name}: Available (v{version})")
            elif engine_name == 'odf':
                import odfpy
                results['engines'][engine_name] = {'available': True}
                print(f"✅ {engine_name}: Available")
            elif engine_name == 'pyxlsb':
                import pyxlsb
                results['engines'][engine_name] = {'available': True}
                print(f"✅ {engine_name}: Available")
        except ImportError:
            results['engines'][engine_name] = {'available': False}
            print(f"❌ {engine_name}: Not installed")

    # 4. Create example usage patterns
    print(f"\n📝 Common Usage Patterns:")
    print("-" * 40)

    usage_examples = {
        'basic_read': {
            'description': 'Read first sheet of Excel file',
            'code': "df = pd.read_excel('file.xlsx')"
        },
        'specific_sheet': {
            'description': 'Read specific sheet by name or index',
            'code': "df = pd.read_excel('file.xlsx', sheet_name='Sheet2')"
        },
        'multiple_sheets': {
            'description': 'Read all sheets into dictionary',
            'code': "dfs = pd.read_excel('file.xlsx', sheet_name=None)"
        },
        'select_columns': {
            'description': 'Read only specific columns',
            'code': "df = pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])"
        },
        'skip_rows': {
            'description': 'Skip header rows',
            'code': "df = pd.read_excel('file.xlsx', skiprows=2)"
        },
        'parse_dates': {
            'description': 'Parse date columns',
            'code': "df = pd.read_excel('file.xlsx', parse_dates=['Date'])"
        },
        'with_dtypes': {
            'description': 'Specify column data types',
            'code': "df = pd.read_excel('file.xlsx', dtype={'ID': str, 'Amount': float})"
        },
        'excel_file_object': {
            'description': 'Use ExcelFile for multiple operations',
            'code': "with pd.ExcelFile('file.xlsx') as xls:\n    df1 = pd.read_excel(xls, 'Sheet1')\n    df2 = pd.read_excel(xls, 'Sheet2')"
        }
    }

    results['examples'] = usage_examples

    for example_name, example_info in list(usage_examples.items())[:5]:
        print(f"   → {example_info['description']}")

    # Save results
    output_file = 'pandas_scripts/outputs/step2_read_methods.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n" + "=" * 60)
    print(f"✅ Analysis complete! Results saved to {output_file}")
    print("=" * 60)

    # Summary statistics
    print(f"\n📊 SUMMARY:")
    print(f"  - read_excel parameters: {results['read_excel'].get('parameter_count', 0)}")
    print(f"  - ExcelFile methods: {len(results['ExcelFile'].get('methods', {}))}")
    print(f"  - Available engines: {sum(1 for e in results['engines'].values() if e.get('available'))}/{len(results['engines'])}")
    print(f"  - Usage examples: {len(results['examples'])}")

    return results

if __name__ == "__main__":
    discover_read_excel_details()