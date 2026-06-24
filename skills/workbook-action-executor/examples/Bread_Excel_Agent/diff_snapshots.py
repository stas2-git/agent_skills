"""
Diff Excel snapshots to detect formatting changes
"""
import openpyxl
from openpyxl.utils import get_column_letter
import json
from pathlib import Path
import sys
from datetime import datetime

def capture_workbook_state(filepath):
    """Capture complete workbook state including all formatting"""
    print(f"  Reading: {filepath.name}")
    
    wb = openpyxl.load_workbook(filepath)
    state = {'sheets': {}}
    
    for sheet in wb.worksheets:
        sheet_state = {
            'cells': {},
            'column_widths': {},
            'row_heights': {},
            'merged_cells': [str(r) for r in sheet.merged_cells.ranges]
        }
        
        # Capture every cell with content or formatting
        for row in sheet.iter_rows():
            for cell in row:
                cell_data = {}
                
                # Value (handle formulas specially)
                if cell.value is not None:
                    # Check if cell contains a formula
                    if cell.data_type == 'f':
                        # For formula cells, get the actual formula string
                        # Handle both regular formulas and array formulas
                        if hasattr(cell.value, 'text'):
                            # ArrayFormula object - .text already includes '='
                            formula_text = cell.value.text
                            if not formula_text.startswith('='):
                                cell_data['value'] = f"={formula_text}"
                            else:
                                cell_data['value'] = formula_text
                        elif isinstance(cell.value, str):
                            # Already a formula string
                            if not cell.value.startswith('='):
                                cell_data['value'] = f"={cell.value}"
                            else:
                                cell_data['value'] = cell.value
                        else:
                            # Fallback: try to get formula from cell directly
                            cell_data['value'] = f"={cell.value}"
                    else:
                        # Regular value (not a formula)
                        cell_data['value'] = str(cell.value)
                
                # Number format (CRITICAL for financial models)
                if cell.number_format and cell.number_format != 'General':
                    cell_data['number_format'] = cell.number_format
                
                # Font
                if cell.font:
                    # Handle font color: only include if it's a direct RGB value, not a theme color
                    font_color = None
                    if cell.font.color and hasattr(cell.font.color, 'rgb'):
                        rgb = cell.font.color.rgb
                        # Only use if it's a valid hex string (not theme color which returns error message)
                        if rgb and isinstance(rgb, str) and len(rgb) >= 6 and not rgb.startswith('Values'):
                            font_color = rgb
                    
                    cell_data['font'] = {
                        'bold': cell.font.bold,
                        'italic': cell.font.italic,
                        'size': cell.font.size,
                        'name': cell.font.name,
                        'color': font_color
                    }
                
                # Fill (background color)
                if cell.fill and cell.fill.patternType:
                    # Handle fill color: only include if it's a direct RGB value, not a theme color
                    fill_color = None
                    if cell.fill.fgColor and hasattr(cell.fill.fgColor, 'rgb'):
                        rgb = cell.fill.fgColor.rgb
                        # Only use if it's a valid hex string (not theme color which returns error message)
                        if rgb and isinstance(rgb, str) and len(rgb) >= 6 and not rgb.startswith('Values'):
                            fill_color = rgb
                    
                    cell_data['fill'] = {
                        'pattern_type': cell.fill.patternType,
                        'fg_color': fill_color
                    }
                
                # Border
                if cell.border:
                    border_data = {}
                    if cell.border.left and cell.border.left.style:
                        border_data['left'] = cell.border.left.style
                    if cell.border.right and cell.border.right.style:
                        border_data['right'] = cell.border.right.style
                    if cell.border.top and cell.border.top.style:
                        border_data['top'] = cell.border.top.style
                    if cell.border.bottom and cell.border.bottom.style:
                        border_data['bottom'] = cell.border.bottom.style
                    
                    if border_data:
                        cell_data['border'] = border_data
                
                # Alignment
                if cell.alignment:
                    cell_data['alignment'] = {
                        'horizontal': cell.alignment.horizontal,
                        'vertical': cell.alignment.vertical,
                        'wrap_text': cell.alignment.wrap_text,
                        'indent': cell.alignment.indent,
                        'text_rotation': cell.alignment.text_rotation
                    }
                
                if cell_data:
                    sheet_state['cells'][cell.coordinate] = cell_data
        
        # Column widths
        for col_letter in sheet.column_dimensions:
            width = sheet.column_dimensions[col_letter].width
            if width is not None:
                sheet_state['column_widths'][col_letter] = round(width, 2)
        
        # Row heights
        for row_num in sheet.row_dimensions:
            height = sheet.row_dimensions[row_num].height
            if height is not None:
                sheet_state['row_heights'][row_num] = round(height, 2)
        
        state['sheets'][sheet.title] = sheet_state
    
    wb.close()
    return state

def diff_states(before, after, snapshot_time):
    """Compare two states and generate tool calls for changes"""
    changes = []
    
    for sheet_name in after['sheets']:
        after_sheet = after['sheets'][sheet_name]
        before_sheet = before['sheets'].get(sheet_name, {'cells': {}, 'column_widths': {}, 'row_heights': {}})
        
        # Check each cell for changes
        for cell_addr, after_cell in after_sheet['cells'].items():
            before_cell = before_sheet.get('cells', {}).get(cell_addr, {})
            
            # Value changed (including formulas)
            after_value = after_cell.get('value')
            before_value = before_cell.get('value')
            if after_value != before_value and after_value is not None:
                # Determine if it's a formula or regular value
                if isinstance(after_value, str) and after_value.startswith('='):
                    # Skip formulas with [1] notation - these are external references
                    # captured in shorthand. VBA will capture them with full workbook names.
                    if '[1]' not in after_value and '[2]' not in after_value and '[3]' not in after_value:
                        changes.append({
                            'timestamp': snapshot_time,
                            'action': 'cell_formula',
                            'details': {
                                'cell': cell_addr,
                                'sheet': sheet_name,
                                'formula': after_value
                            },
                            'detected_by': 'diff'
                        })
                else:
                    changes.append({
                        'timestamp': snapshot_time,
                        'action': 'cell_value',
                        'details': {
                            'cell': cell_addr,
                            'sheet': sheet_name,
                            'value': after_value
                        },
                        'detected_by': 'diff'
                    })
            
            # Number format changed
            after_fmt = after_cell.get('number_format')
            before_fmt = before_cell.get('number_format')
            if after_fmt and after_fmt != before_fmt:
                changes.append({
                    'timestamp': snapshot_time,
                    'action': 'format_number',
                    'details': {
                        'cell': cell_addr,
                        'sheet': sheet_name,
                        'format': after_fmt
                    },
                    'detected_by': 'diff'
                })
            
            # Font changes
            after_font = after_cell.get('font', {})
            before_font = before_cell.get('font', {})
            
            font_changed = False
            font_details = {'cell': cell_addr, 'sheet': sheet_name}
            
            if after_font.get('bold') != before_font.get('bold'):
                font_details['bold'] = after_font.get('bold')
                font_changed = True
            
            if after_font.get('italic') != before_font.get('italic'):
                font_details['italic'] = after_font.get('italic')
                font_changed = True
            
            if after_font.get('size') != before_font.get('size') and after_font.get('size'):
                font_details['size'] = after_font.get('size')
                font_changed = True
            
            if after_font.get('color') != before_font.get('color') and after_font.get('color'):
                font_details['color'] = after_font.get('color')
                font_changed = True
            
            if font_changed:
                changes.append({
                    'timestamp': snapshot_time,
                    'action': 'format_font',
                    'details': font_details,
                    'detected_by': 'diff'
                })
            
            # Fill color changed
            after_fill = after_cell.get('fill', {})
            before_fill = before_cell.get('fill', {})
            if after_fill.get('fg_color') != before_fill.get('fg_color') and after_fill.get('fg_color'):
                changes.append({
                    'timestamp': snapshot_time,
                    'action': 'format_fill',
                    'details': {
                        'cell': cell_addr,
                        'sheet': sheet_name,
                        'color': after_fill.get('fg_color')
                    },
                    'detected_by': 'diff'
                })
            
            # Border changed
            after_border = after_cell.get('border', {})
            before_border = before_cell.get('border', {})
            if after_border != before_border and after_border:
                changes.append({
                    'timestamp': snapshot_time,
                    'action': 'format_border',
                    'details': {
                        'cell': cell_addr,
                        'sheet': sheet_name,
                        'borders': after_border
                    },
                    'detected_by': 'diff'
                })
            
            # Alignment changed
            after_align = after_cell.get('alignment', {})
            before_align = before_cell.get('alignment', {})
            if after_align != before_align and after_align:
                changes.append({
                    'timestamp': snapshot_time,
                    'action': 'format_alignment',
                    'details': {
                        'cell': cell_addr,
                        'sheet': sheet_name,
                        'horizontal': after_align.get('horizontal'),
                        'vertical': after_align.get('vertical'),
                        'wrap_text': after_align.get('wrap_text'),
                        'indent': after_align.get('indent'),
                        'text_rotation': after_align.get('text_rotation')
                    },
                    'detected_by': 'diff'
                })
        
        # Check merged cells
        after_merged = set(after_sheet.get('merged_cells', []))
        before_merged = set(before_sheet.get('merged_cells', []))
        new_merges = after_merged - before_merged
        
        for merge_range in new_merges:
            changes.append({
                'timestamp': snapshot_time,
                'action': 'merge_cells',
                'details': {
                    'range': str(merge_range),
                    'sheet': sheet_name
                },
                'detected_by': 'diff'
            })
        
        # Check column widths
        after_widths = after_sheet.get('column_widths', {})
        before_widths = before_sheet.get('column_widths', {})
        for col, width in after_widths.items():
            before_width = before_widths.get(col)
            if width != before_width:
                changes.append({
                    'timestamp': snapshot_time,
                    'action': 'column_width',
                    'details': {
                        'column': col,
                        'sheet': sheet_name,
                        'width': width
                    },
                    'detected_by': 'diff'
                })
        
        # Check row heights
        after_heights = after_sheet.get('row_heights', {})
        before_heights = before_sheet.get('row_heights', {})
        for row, height in after_heights.items():
            before_height = before_heights.get(row)
            if height != before_height:
                changes.append({
                    'timestamp': snapshot_time,
                    'action': 'row_height',
                    'details': {
                        'row': row,
                        'sheet': sheet_name,
                        'height': height
                    },
                    'detected_by': 'diff'
                })
    
    return changes

def process_snapshots(snapshot_dir):
    """Process all snapshots and generate diff events"""
    snapshot_path = Path(snapshot_dir)
    
    if not snapshot_path.exists():
        print(f"❌ Snapshot directory not found: {snapshot_dir}")
        return []
    
    # Find all snapshots
    snapshots = sorted(snapshot_path.glob("snapshot_*.xlsx"))
    
    if len(snapshots) < 2:
        print(f"⚠️  Need at least 2 snapshots to diff. Found: {len(snapshots)}")
        return []
    
    print(f"\n📸 Processing {len(snapshots)} snapshots...")
    
    all_changes = []
    prev_state = None
    
    for i, snapshot in enumerate(snapshots):
        print(f"\nSnapshot {i+1}/{len(snapshots)}")
        
        # Extract timestamp from filename
        # Format: snapshot_001_hhmmss.xlsx
        parts = snapshot.stem.split('_')
        time_str = parts[-1] if len(parts) >= 3 else "000000"
        snapshot_time = f"2025-10-06 {time_str[:2]}:{time_str[2:4]}:{time_str[4:6]}"
        
        # Capture state
        try:
            current_state = capture_workbook_state(snapshot)
        except Exception as e:
            print(f"  ❌ Error reading snapshot: {e}")
            continue
        
        if prev_state:
            # Diff against previous
            changes = diff_states(prev_state, current_state, snapshot_time)
            all_changes.extend(changes)
            print(f"  ✅ Found {len(changes)} formatting changes")
        
        prev_state = current_state
    
    print(f"\n✅ Total formatting changes detected: {len(all_changes)}")
    return all_changes

def merge_vba_and_diff_logs(vba_log_file, snapshot_dir):
    """Merge VBA events with diff-detected changes"""
    
    print("=" * 60)
    print("MERGING VBA EVENTS + DIFF CHANGES")
    print("=" * 60)
    
    # Load VBA log
    with open(vba_log_file) as f:
        vba_events = json.load(f)
    
    print(f"\n📝 VBA Events: {len(vba_events)}")
    
    # Process snapshots
    diff_changes = process_snapshots(snapshot_dir)
    print(f"🎨 Diff Changes: {len(diff_changes)}")
    
    # Merge and sort by timestamp
    combined = vba_events + diff_changes
    combined.sort(key=lambda x: x.get('timestamp', ''))
    
    print(f"\n📊 TOTAL EVENTS: {len(combined)}")
    print(f"   - Cell operations (VBA): {len([e for e in vba_events if 'cell' in e.get('action', '')])}")
    print(f"   - Formatting (Diff): {len([e for e in diff_changes if 'format' in e.get('action', '')])}")
    print(f"   - Structural (Diff): {len([e for e in diff_changes if e.get('action') in ['merge_cells', 'column_width', 'row_height']])}")
    
    return combined

def main():
    if len(sys.argv) < 2:
        print("Usage: python diff_snapshots.py <vba_log.json>")
        print("\nExample:")
        print("  python diff_snapshots.py excel_recordings/recording_20251006_184254.json")
        sys.exit(1)
    
    vba_log = Path(sys.argv[1])
    
    if not vba_log.exists():
        print(f"❌ VBA log file not found: {vba_log}")
        sys.exit(1)
    
    # Infer snapshot directory from log filename
    # recording_20251006_184254.json → recording_20251006_184254_snapshots/
    snapshot_dir = vba_log.parent / f"{vba_log.stem}_snapshots"
    
    print(f"VBA Log: {vba_log}")
    print(f"Snapshots: {snapshot_dir}")
    
    # Merge logs
    combined = merge_vba_and_diff_logs(vba_log, snapshot_dir)
    
    # Save merged log
    output_file = vba_log.parent / f"{vba_log.stem}_complete.json"
    with open(output_file, 'w') as f:
        json.dump(combined, f, indent=2)
    
    print(f"\n✅ Saved complete log to: {output_file}")
    print("\nNext step: Translate to tool calls")
    print(f"  python translate_recording.py {output_file}")

if __name__ == "__main__":
    main()