from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
from openpyxl.worksheet.datavalidation import DataValidation


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "decompose_excel.py"
spec = importlib.util.spec_from_file_location("decompose_excel", SCRIPT_PATH)
decompose_excel = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(decompose_excel)


def build_signal_workbook(path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Signals"

    ws["B2"] = "Peach input"
    ws["C2"].fill = PatternFill(fill_type="solid", fgColor="FFFFE0CC")

    ws["B3"] = "Gray input"
    ws["C3"].fill = PatternFill(fill_type="solid", fgColor="FFD9D9D9")

    ws["B4"] = "Boxed input"
    border_side = Side(style="thin", color="FF808080")
    ws["C4"].border = Border(left=border_side, right=border_side, top=border_side, bottom=border_side)

    ws["B5"] = "Bottom border input"
    ws["C5"].border = Border(bottom=Side(style="medium", color="FF1F4E78"))

    ws["B6"] = "Dropdown"
    dropdown = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True)
    ws.add_data_validation(dropdown)
    dropdown.add(ws["C6"])

    ws["B7"] = "Unlocked"
    ws["C7"].protection = Protection(locked=False)

    ws["B8"] = "Font only"
    ws["C8"].font = Font(name="Arial", size=10)

    ws["B9"] = "Bold underline only"
    ws["C9"].font = Font(bold=True, underline="single")

    ws["B10"] = "Alignment only"
    ws["C10"].alignment = Alignment(horizontal="center")

    ws["B11"] = "Number format only"
    ws["C11"].number_format = "0.0000%"

    ws["B12"] = "Fill and number format"
    ws["C12"].fill = PatternFill(fill_type="solid", fgColor="FFFFFF00")
    ws["C12"].number_format = "0.0000%"

    ws["B13"] = "Premium"
    ws["C13"] = 12500
    ws["C13"].number_format = '$#,##0.00;[Red]($#,##0.00);"-"'

    ws["B14"] = "Total Premium"
    ws["C14"] = "=C13*1.1"
    ws["C14"].font = Font(bold=True, color="FF1F4E78")
    ws["C14"].alignment = Alignment(horizontal="right", wrap_text=True)
    ws["C14"].number_format = "$#,##0.00"

    ws["B15"] = "Minimum premium"
    ws["B16"] = "Maximum premium"
    decimal_rule = DataValidation(type="decimal", operator="between", formula1=0, formula2=1000000, allow_blank=True)
    ws.add_data_validation(decimal_rule)
    decimal_rule.add("C15:C16")

    wb.save(path)


def render(path: Path) -> str:
    wb_formula = load_workbook(path, data_only=False)
    wb_values = load_workbook(path, data_only=True)
    try:
        return decompose_excel.render_output(path, wb_formula, wb_values)
    finally:
        wb_formula.close()
        wb_values.close()


def parse_styles(text: str) -> dict[str, dict]:
    styles: dict[str, dict] = {}
    in_styles = False
    for line in text.splitlines():
        if line == "STYLES":
            in_styles = True
            continue
        if in_styles and line == "":
            break
        if in_styles and line.startswith("  s"):
            style_id, payload = line.strip().split(": ", 1)
            styles[style_id] = json.loads(payload)
    return styles


def style_for_cell(text: str, styles: dict[str, dict], ref: str) -> dict:
    for line in text.splitlines():
        if line.startswith(f"  - {ref}:"):
            for part in line.split(" | "):
                if part.startswith("style="):
                    return styles[part[len("style="):]]
    raise AssertionError(f"No style found for {ref}")


def test_blank_cells_require_strong_ui_signal(tmp_path: Path) -> None:
    workbook_path = tmp_path / "signals.xlsx"
    build_signal_workbook(workbook_path)

    text = render(workbook_path)
    styles = parse_styles(text)

    assert "- C2: blank | style=" in text
    assert "- C3: blank | style=" in text
    assert "- C4: blank | style=" in text
    assert "- C5: blank | style=" in text
    assert "- C6: blank | validation=true" in text
    assert "- C15: blank | validation=true" in text
    assert "- C16: blank | validation=true" in text
    assert "- C7: blank | style=" in text
    assert "- C8:" not in text
    assert "- C9:" not in text
    assert "- C10:" not in text
    assert "- C11:" not in text
    assert "- C12: blank | style=" in text
    assert "- D20:" not in text

    assert style_for_cell(text, styles, "C2").get("fill", {}).get("fg_color") == {
        "type": "rgb",
        "rgb": "FFFFE0CC",
    }
    assert style_for_cell(text, styles, "C3").get("fill", {}).get("fg_color") == {
        "type": "rgb",
        "rgb": "FFD9D9D9",
    }
    assert all(side in style_for_cell(text, styles, "C4").get("border", {}) for side in ("left", "right", "top", "bottom"))
    assert "bottom" in style_for_cell(text, styles, "C5").get("border", {})
    assert style_for_cell(text, styles, "C7").get("protection") == {"locked": False}
    assert style_for_cell(text, styles, "C12").get("fill", {}).get("fg_color") == {
        "type": "rgb",
        "rgb": "FFFFFF00",
    }
    assert style_for_cell(text, styles, "C12").get("number_format") == "0.0000%"

    assert text.count('"range":"C6"') == 1
    assert text.count('"range":"C15:C16"') == 1
    assert '"type":"list"' in text
    assert '"type":"decimal"' in text
    assert '"formula1":"\\"Yes,No\\""' in text


def test_nonblank_cells_still_preserve_formatting(tmp_path: Path) -> None:
    workbook_path = tmp_path / "signals.xlsx"
    build_signal_workbook(workbook_path)

    text = render(workbook_path)
    styles = parse_styles(text)

    assert "- C13: value=12500 | style=" in text
    assert style_for_cell(text, styles, "C13").get("number_format") == '$#,##0.00;[Red]($#,##0.00);"-"'
    assert "- C14: formula=C13*1.1 | style=" in text
    c14_style = style_for_cell(text, styles, "C14")
    assert c14_style.get("font", {}).get("bold") is True
    assert c14_style.get("alignment", {}).get("horizontal") == "right"
    assert c14_style.get("number_format") == "$#,##0.00"


def test_style_ids_are_deterministic(tmp_path: Path) -> None:
    workbook_path = tmp_path / "signals.xlsx"
    build_signal_workbook(workbook_path)

    first = parse_styles(render(workbook_path))
    second = parse_styles(render(workbook_path))

    assert first == second
    assert list(first) == [f"s{idx}" for idx in range(1, len(first) + 1)]


def test_formula_cached_value_output_is_preserved(tmp_path: Path) -> None:
    workbook_path = tmp_path / "signals.xlsx"
    build_signal_workbook(workbook_path)

    wb_formula = load_workbook(workbook_path, data_only=False)
    wb_values = load_workbook(workbook_path, data_only=True)
    try:
        wb_values["Signals"]["C14"] = 13750
        text = decompose_excel.render_output(workbook_path, wb_formula, wb_values)
    finally:
        wb_formula.close()
        wb_values.close()

    assert "- C14: formula=C13*1.1 | value=13750 | style=" in text
