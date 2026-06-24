"""
Systematic Discovery Script for openpyxl - Step 2
Exploring submodules to find where classes actually live
"""

import openpyxl
import inspect
import json

def discover_openpyxl_step2():
    """Step 2: Explore submodules to find classes"""

    print("=" * 60)
    print("STEP 2: Exploring submodules to find classes")
    print("=" * 60)

    # First, let's get the module structure again
    module_contents = dir(openpyxl)
    public_items = [name for name in module_contents if not name.startswith('_')]

    # Classify to find modules
    modules = []
    for name in public_items:
        try:
            obj = getattr(openpyxl, name)
            if inspect.ismodule(obj):
                modules.append(name)
        except:
            pass

    print(f"Found {len(modules)} modules to explore")

    # Key submodules to explore based on Excel's object model
    key_submodules = ['workbook', 'worksheet', 'cell', 'styles', 'chart', 'utils']

    submodule_contents = {}

    for module_name in modules:
        # Focus on key modules first
        if module_name not in key_submodules:
            continue

        print(f"\n📦 Exploring openpyxl.{module_name}...")
        print("-" * 40)

        try:
            submodule = getattr(openpyxl, module_name)
            contents = dir(submodule)
            public_contents = [name for name in contents if not name.startswith('_')]

            classes_in_module = []
            functions_in_module = []
            submodules_in_module = []

            for item_name in public_contents:
                try:
                    item = getattr(submodule, item_name)
                    if inspect.isclass(item):
                        # Get the actual class location
                        module_location = getattr(item, '__module__', 'unknown')
                        classes_in_module.append({
                            'name': item_name,
                            'module': module_location
                        })
                        print(f"  CLASS: {item_name} (from {module_location})")
                    elif inspect.isfunction(item):
                        functions_in_module.append(item_name)
                    elif inspect.ismodule(item):
                        submodules_in_module.append(item_name)
                except Exception as e:
                    pass

            submodule_contents[module_name] = {
                'classes': classes_in_module,
                'functions': functions_in_module,
                'submodules': submodules_in_module,
                'total_public_items': len(public_contents)
            }

            # Print summary
            if classes_in_module:
                print(f"  ✓ Found {len(classes_in_module)} classes")
            if functions_in_module:
                print(f"  ✓ Found {len(functions_in_module)} functions")
            if submodules_in_module:
                print(f"  ✓ Found {len(submodules_in_module)} submodules")

        except Exception as e:
            print(f"  ERROR exploring {module_name}: {e}")

    # Now let's look for the key classes we need
    print("\n" + "=" * 60)
    print("SEARCHING FOR KEY EXCEL CLASSES")
    print("=" * 60)

    # Try to find common classes by exploring deeper
    key_classes = {}

    # Workbook class (we know this exists at top level)
    key_classes['Workbook'] = {
        'location': 'openpyxl.Workbook',
        'accessible': True
    }

    # Try to find Worksheet class
    try:
        from openpyxl.worksheet.worksheet import Worksheet
        key_classes['Worksheet'] = {
            'location': 'openpyxl.worksheet.worksheet.Worksheet',
            'accessible': True
        }
        print("✓ Found Worksheet at openpyxl.worksheet.worksheet.Worksheet")
    except:
        print("✗ Could not find Worksheet")

    # Try to find Cell class
    try:
        from openpyxl.cell.cell import Cell
        key_classes['Cell'] = {
            'location': 'openpyxl.cell.cell.Cell',
            'accessible': True
        }
        print("✓ Found Cell at openpyxl.cell.cell.Cell")
    except:
        print("✗ Could not find Cell")

    # Try to find styles classes
    try:
        from openpyxl.styles import Font, Fill, Border, Alignment
        print("✓ Found style classes: Font, Fill, Border, Alignment")
        key_classes['Font'] = {'location': 'openpyxl.styles.Font', 'accessible': True}
        key_classes['Fill'] = {'location': 'openpyxl.styles.Fill', 'accessible': True}
        key_classes['Border'] = {'location': 'openpyxl.styles.Border', 'accessible': True}
        key_classes['Alignment'] = {'location': 'openpyxl.styles.Alignment', 'accessible': True}
    except:
        print("✗ Could not find style classes")

    # Save Step 2 results
    results = {
        'submodules_explored': submodule_contents,
        'key_classes_found': key_classes,
        'next_step': 'Use these class locations to discover their methods'
    }

    with open('step2_submodules.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Step 2 results saved to step2_submodules.json")

    return key_classes

if __name__ == "__main__":
    discover_openpyxl_step2()