"""
Translate recorded events to Excel tool calls (v2.0 - Consolidated Tools)
Uses new openpyxl_cell_set_style and universal chart tools
"""
import json
import sys
from pathlib import Path
from collections import defaultdict

def translate_cell_value(details):
    """Translate typing a value into a cell"""
    return {
        "tool": "openpyxl_worksheet_set_item",
        "params": {
            "key": details["cell"].replace("$", ""),
            "value": details["value"]
        }
    }

def translate_cell_formula(details):
    """Translate entering a formula"""
    return {
        "tool": "openpyxl_worksheet_set_item",
        "params": {
            "key": details["cell"].replace("$", ""),
            "value": details["formula"]
        }
    }

def translate_merge_cells(details):
    """Translate merging cells"""
    return {
        "tool": "openpyxl_worksheet_merge_cells",
        "params": {
            "range_string": details["range"]
        }
    }

def translate_column_width(details):
    """Translate column width change"""
    return {
        "tool": "openpyxl_worksheet_set_column_width",
        "params": {
            "column": details["column"],
            "width": str(details["width"])
        }
    }

def translate_row_height(details):
    """Translate row height change"""
    return {
        "tool": "openpyxl_worksheet_set_row_height",
        "params": {
            "row": str(details["row"]),
            "height": str(details["height"])
        }
    }

def translate_sheet_create(details):
    """Translate creating new sheet"""
    return {
        "tool": "openpyxl_workbook_create_sheet",
        "params": {
            "title": details["sheet_name"]
        }
    }

def translate_sheet_activate(details):
    """Translate switching sheets"""
    return {
        "tool": "openpyxl_workbook_get_item",
        "params": {
            "key": details["sheet_name"]
        }
    }

def translate_workbook_save(details):
    """Translate saving workbook"""
    return {
        "tool": "openpyxl_workbook_save",
        "params": {
            "filename": details.get("filename", "workbook.xlsx")
        }
    }

# Formatting consolidation helpers
def consolidate_cell_formatting(cell_formats):
    """
    Consolidate multiple formatting changes for same cell into single openpyxl_cell_set_style call
    cell_formats: dict of {cell_addr: [list of format events]}
    """
    consolidated = []
    
    for cell_addr, formats in cell_formats.items():
        # Collect all formatting properties for this cell
        # Normalize cell reference by stripping $ characters (absolute → relative)
        style_params = {"cell_reference": cell_addr.replace("$", "")}
        
        for fmt in formats:
            action = fmt['action']
            details = fmt['details']
            
            if action == 'format_number':
                style_params['number_format'] = details['format']
            
            elif action in ['format_font', 'format_bold', 'format_italic']:
                if 'font' not in style_params:
                    style_params['font'] = {}
                
                # Build inline font JSON
                # Handle explicit bold/italic actions (VBA captures these without details)
                if action == 'format_bold':
                    style_params['font']['bold'] = True
                elif action == 'format_italic':
                    style_params['font']['italic'] = True
                
                # Handle detailed font properties
                if 'bold' in details:
                    style_params['font']['bold'] = details['bold']
                if 'italic' in details:
                    style_params['font']['italic'] = details['italic']
                if 'size' in details:
                    style_params['font']['size'] = details['size']
                if 'color' in details:
                    style_params['font']['color'] = details['color']
            
            elif action == 'format_fill':
                # Inline fill JSON
                style_params['fill'] = json.dumps({
                    "color": details['color']
                })
            
            elif action == 'format_border':
                # Inline border JSON
                style_params['border'] = json.dumps({
                    "style": "thin",
                    "sides": list(details['borders'].keys())
                })
            
            elif action == 'format_alignment':
                # Inline alignment JSON
                align = {}
                if details.get('horizontal'):
                    align['horizontal'] = details['horizontal']
                if details.get('vertical'):
                    align['vertical'] = details['vertical']
                if details.get('wrap_text'):
                    align['wrap_text'] = details['wrap_text']
                if details.get('indent') is not None:
                    align['indent'] = details['indent']
                if details.get('text_rotation') is not None:
                    align['text_rotation'] = details['text_rotation']
                
                if align:
                    style_params['alignment'] = json.dumps(align)
        
        # Convert font dict to JSON string if exists
        if 'font' in style_params and isinstance(style_params['font'], dict):
            style_params['font'] = json.dumps(style_params['font'])
        
        # Create consolidated tool call
        consolidated.append({
            "tool": "openpyxl_cell_set_style",
            "params": style_params,
            "timestamp": formats[0]['timestamp'],  # Use first format's timestamp
            "original_actions": [f['action'] for f in formats],
            "source": "diff_consolidated"
        })
    
    return consolidated

# Main translation mapping for non-formatting events
EVENT_TRANSLATORS = {
    "cell_value": translate_cell_value,
    "cell_formula": translate_cell_formula,
    "merge_cells": translate_merge_cells,
    "column_width": translate_column_width,
    "row_height": translate_row_height,
    "sheet_create": translate_sheet_create,
    "sheet_activate": translate_sheet_activate,
    "workbook_save": translate_workbook_save,
}

# Formatting events that get consolidated
FORMATTING_EVENTS = {
    'format_number', 'format_font', 'format_fill', 
    'format_border', 'format_alignment',
    'format_bold', 'format_italic'
}

def translate_recording(json_file):
    """Translate recorded events to tool calls with formatting consolidation"""
    
    with open(json_file, 'r') as f:
        events = json.load(f)
    
    print(f"Loaded {len(events)} events from {json_file.name}")
    
    # Separate formatting events from other events
    formatting_events = []
    other_events = []
    skipped_events = ["snapshot_taken"]
    
    for event in events:
        action = event.get("action")
        
        if action in skipped_events:
            continue
        elif action in FORMATTING_EVENTS:
            formatting_events.append(event)
        else:
            other_events.append(event)
    
    print(f"  - Cell operations: {len(other_events)}")
    print(f"  - Formatting events: {len(formatting_events)}")
    
    # Group formatting events by cell and timestamp window
    # Events within 2 seconds for same cell get consolidated
    cell_format_groups = defaultdict(list)
    
    for event in formatting_events:
        cell = event['details'].get('cell')
        if cell:
            cell_format_groups[cell].append(event)
    
    # Consolidate formatting for each cell
    print(f"\nConsolidating formatting for {len(cell_format_groups)} cells...")
    consolidated_formatting = consolidate_cell_formatting(cell_format_groups)
    print(f"  - Reduced to {len(consolidated_formatting)} consolidated style calls")
    
    # Translate other events
    tool_sequence = []
    unmapped_events = []
    
    for event in other_events:
        action = event.get("action")
        details = event.get("details", {})
        timestamp = event.get("timestamp")
        
        if action in EVENT_TRANSLATORS:
            tool_call = EVENT_TRANSLATORS[action](details)
            tool_call["timestamp"] = timestamp
            tool_call["original_action"] = action
            tool_call["source"] = event.get("detected_by", "vba")
            tool_sequence.append(tool_call)
        else:
            unmapped_events.append({
                "action": action,
                "timestamp": timestamp,
                "details": details
            })
            print(f"⚠️  Unmapped action: {action}")
    
    # Add consolidated formatting
    tool_sequence.extend(consolidated_formatting)
    
    # Sort by timestamp
    tool_sequence.sort(key=lambda x: x.get('timestamp', ''))
    
    # DEDUPLICATION: Remove duplicate tool calls (same tool + params)
    # Happens when both diff and VBA capture the same operation
    seen_signatures = set()
    deduplicated_sequence = []
    duplicates_removed = 0
    
    for tool in tool_sequence:
        # Create signature from tool name and params
        tool_name = tool['tool']
        params = tool.get('params', {})
        param_str = json.dumps(params, sort_keys=True)
        signature = (tool_name, param_str)
        
        if signature not in seen_signatures:
            seen_signatures.add(signature)
            deduplicated_sequence.append(tool)
        else:
            duplicates_removed += 1
    
    tool_sequence = deduplicated_sequence
    
    print(f"\n✅ Translated {len(tool_sequence)} tool calls")
    print(f"   - Cell operations: {len([t for t in tool_sequence if t['source'] == 'vba'])}")
    print(f"   - Consolidated styles: {len(consolidated_formatting)}")
    if duplicates_removed > 0:
        print(f"   - Duplicates removed: {duplicates_removed}")
    
    if unmapped_events:
        print(f"⚠️  Unmapped: {len(unmapped_events)} events")
    
    return tool_sequence, unmapped_events

def save_tool_sequence(tool_sequence, output_file):
    """Save the translated tool sequence"""
    output = {
        "source": "hybrid_vba_plus_diff_v2",
        "tool_format": "consolidated_109_tools",
        "total_steps": len(tool_sequence),
        "tool_sequence": tool_sequence
    }
    
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n✅ Saved tool sequence to: {output_file}")

def print_summary_stats(tool_sequence):
    """Print helpful summary statistics"""
    from collections import Counter
    
    tool_counts = Counter(t['tool'] for t in tool_sequence)
    
    print("\n" + "=" * 60)
    print("TOOL USAGE SUMMARY")
    print("=" * 60)
    
    print("\nMost used tools:")
    for tool, count in tool_counts.most_common(10):
        print(f"  {tool}: {count}")
    
    # Count consolidated formatting
    style_calls = [t for t in tool_sequence if t['tool'] == 'openpyxl_cell_set_style']
    if style_calls:
        print(f"\n📊 Formatting efficiency:")
        total_formats = sum(len(t.get('original_actions', [])) for t in style_calls)
        print(f"  {total_formats} formatting events → {len(style_calls)} style calls")
        print(f"  Reduction: {100 - (len(style_calls)/max(total_formats, 1)*100):.1f}%")

def main():
    if len(sys.argv) < 2:
        print("Usage: python translate_recording.py <complete_log.json>")
        print("\nExample:")
        print("  python translate_recording.py excel_recordings/recording_20251006_184254_complete.json")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"❌ File not found: {input_file}")
        sys.exit(1)
    
    output_file = input_file.parent / f"{input_file.stem}_tools.json"
    
    print("=" * 60)
    print("TRANSLATING TO CONSOLIDATED TOOL CALLS (v2.0)")
    print("=" * 60)
    print(f"Input: {input_file.name}\n")
    
    # Translate
    tool_sequence, unmapped = translate_recording(input_file)
    
    # Save
    save_tool_sequence(tool_sequence, output_file)
    
    # Summary
    print_summary_stats(tool_sequence)
    
    print("\n" + "=" * 60)
    print("TRANSLATION COMPLETE")
    print("=" * 60)
    print(f"Output: {output_file}")
    print(f"Total tool calls: {len(tool_sequence)}")
    print("\n✅ Ready for model training!")

if __name__ == "__main__":
    main()