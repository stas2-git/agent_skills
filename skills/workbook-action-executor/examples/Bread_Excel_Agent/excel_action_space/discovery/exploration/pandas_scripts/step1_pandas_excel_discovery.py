"""
Systematic Discovery Script for pandas Excel functionality - Step 1
Discovering pandas Excel I/O modules and core classes
"""

import pandas as pd
import inspect
import json
import sys

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

def discover_pandas_excel_step1():
    """Step 1: Discover pandas Excel I/O capabilities"""

    print("=" * 60)
    print("STEP 1: Discovering pandas Excel Functionality")
    print("=" * 60)

    results = {}

    # 1. Basic Information
    print(f"\n📊 pandas Version: {pd.__version__}")
    results['version'] = pd.__version__

    # 2. Discover Excel reading capabilities
    print(f"\n📋 Excel Reading Functions:")
    print("-" * 40)

    # Main read function
    if hasattr(pd, 'read_excel'):
        print("✅ pd.read_excel() found")
        results['read_excel'] = {
            'found': True,
            'docstring': inspect.getdoc(pd.read_excel) or '',
            'parameters': get_signature_safe(pd.read_excel)
        }

        # Count parameters
        if results['read_excel']['parameters']:
            print(f"   → {len(results['read_excel']['parameters'])} parameters available")
            print(f"   → Key params: io, sheet_name, header, usecols, dtype, engine")

    # ExcelFile class for reading
    if hasattr(pd, 'ExcelFile'):
        print("✅ pd.ExcelFile class found")
        results['ExcelFile'] = {
            'found': True,
            'docstring': inspect.getdoc(pd.ExcelFile) or '',
            'methods': []
        }

        # Discover ExcelFile methods
        for method_name in dir(pd.ExcelFile):
            if not method_name.startswith('_'):
                try:
                    method = getattr(pd.ExcelFile, method_name)
                    if callable(method):
                        results['ExcelFile']['methods'].append(method_name)
                except:
                    pass

        print(f"   → {len(results['ExcelFile']['methods'])} public methods")

    # 3. Discover Excel writing capabilities
    print(f"\n📋 Excel Writing Functions:")
    print("-" * 40)

    # DataFrame.to_excel method
    if hasattr(pd.DataFrame, 'to_excel'):
        print("✅ DataFrame.to_excel() found")
        results['to_excel'] = {
            'found': True,
            'docstring': inspect.getdoc(pd.DataFrame.to_excel) or '',
            'parameters': get_signature_safe(pd.DataFrame.to_excel)
        }

        if results['to_excel']['parameters']:
            print(f"   → {len(results['to_excel']['parameters'])} parameters available")

    # ExcelWriter class
    if hasattr(pd, 'ExcelWriter'):
        print("✅ pd.ExcelWriter class found")
        results['ExcelWriter'] = {
            'found': True,
            'docstring': inspect.getdoc(pd.ExcelWriter) or '',
            'methods': [],
            'parameters': get_signature_safe(pd.ExcelWriter.__init__)
        }

        # Discover ExcelWriter methods
        for method_name in dir(pd.ExcelWriter):
            if not method_name.startswith('_'):
                try:
                    method = getattr(pd.ExcelWriter, method_name)
                    if callable(method):
                        results['ExcelWriter']['methods'].append(method_name)
                except:
                    pass

        print(f"   → {len(results['ExcelWriter']['methods'])} public methods")
        print(f"   → Methods: {', '.join(results['ExcelWriter']['methods'][:5])}")

    # 4. Check io.excel submodule
    print(f"\n📦 Excel I/O Module Structure:")
    print("-" * 40)

    try:
        import pandas.io.excel as excel_io
        print("✅ pandas.io.excel module accessible")

        results['io_excel'] = {
            'accessible': True,
            'classes': [],
            'functions': [],
            'engines': []
        }

        # Discover what's in io.excel
        for item_name in dir(excel_io):
            if not item_name.startswith('_'):
                item = getattr(excel_io, item_name)
                if inspect.isclass(item):
                    results['io_excel']['classes'].append(item_name)
                elif callable(item):
                    results['io_excel']['functions'].append(item_name)

        print(f"   → {len(results['io_excel']['classes'])} classes found")
        print(f"   → {len(results['io_excel']['functions'])} functions found")

        # Check for engine support
        engine_keywords = ['Openpyxl', 'Xlsxwriter', 'Xlrd', 'Odf']
        for keyword in engine_keywords:
            matching = [c for c in results['io_excel']['classes'] if keyword.lower() in c.lower()]
            if matching:
                results['io_excel']['engines'].append(keyword.lower())
                print(f"   → {keyword} engine support found")

    except ImportError as e:
        print(f"❌ Could not import pandas.io.excel: {e}")
        results['io_excel'] = {'accessible': False, 'error': str(e)}

    # 5. Check for DataFrame manipulation methods relevant to Excel
    print(f"\n📊 DataFrame Methods for Excel-like Operations:")
    print("-" * 40)

    df_methods_to_check = [
        'pivot', 'pivot_table', 'melt', 'stack', 'unstack',
        'merge', 'join', 'concat', 'groupby', 'aggregate',
        'sort_values', 'filter', 'query', 'describe', 'corr'
    ]

    results['dataframe_methods'] = {}
    found_methods = []

    for method_name in df_methods_to_check:
        if hasattr(pd.DataFrame, method_name):
            found_methods.append(method_name)
            results['dataframe_methods'][method_name] = {
                'found': True,
                'docstring': (inspect.getdoc(getattr(pd.DataFrame, method_name)) or '')[:200]
            }

    print(f"✅ Found {len(found_methods)} Excel-like DataFrame methods:")
    print(f"   → {', '.join(found_methods[:10])}")

    # 6. Check for styling capabilities
    print(f"\n🎨 Styling Capabilities:")
    print("-" * 40)

    if hasattr(pd.DataFrame, 'style'):
        print("✅ DataFrame.style property found")

        # Create a sample DataFrame to explore style
        sample_df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        styler = sample_df.style

        style_methods = []
        for method_name in dir(styler):
            if not method_name.startswith('_'):
                try:
                    method = getattr(styler, method_name)
                    if callable(method):
                        style_methods.append(method_name)
                except:
                    pass

        results['style'] = {
            'found': True,
            'class_name': type(styler).__name__,
            'methods': style_methods[:20]  # First 20 methods
        }

        print(f"   → Styler class: {type(styler).__name__}")
        print(f"   → {len(style_methods)} styling methods available")
        print(f"   → Key methods: format, highlight_max, background_gradient")

    # 7. Check for additional Excel-related functions
    print(f"\n🔧 Additional Excel Functions:")
    print("-" * 40)

    additional_functions = ['json_normalize', 'crosstab', 'get_dummies']
    results['additional'] = {}

    for func_name in additional_functions:
        if hasattr(pd, func_name):
            print(f"✅ pd.{func_name}() found")
            results['additional'][func_name] = True

    # Save results
    output_file = 'pandas_scripts/outputs/step1_excel_discovery.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n" + "=" * 60)
    print(f"✅ Discovery complete! Results saved to {output_file}")
    print("=" * 60)

    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"  - Excel reading: {'✅' if results.get('read_excel', {}).get('found') else '❌'}")
    print(f"  - Excel writing: {'✅' if results.get('to_excel', {}).get('found') else '❌'}")
    print(f"  - ExcelWriter: {'✅' if results.get('ExcelWriter', {}).get('found') else '❌'}")
    print(f"  - DataFrame methods: {len(found_methods)} found")
    print(f"  - Styling support: {'✅' if results.get('style', {}).get('found') else '❌'}")

    return results

if __name__ == "__main__":
    discover_pandas_excel_step1()