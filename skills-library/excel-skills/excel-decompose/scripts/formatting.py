from __future__ import annotations

import json
from typing import Any

from openpyxl.styles import DEFAULT_FONT


def compact_json(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def meaningful_bool(value) -> bool:
    return bool(value) is True


def serialize_color(color) -> dict[str, Any] | None:
    if color is None or color.type is None:
        return None

    if color.type == "rgb":
        rgb = color.rgb
        if not rgb:
            return None
        return {"type": "rgb", "rgb": rgb}
    if color.type == "theme":
        return {"type": "theme", "theme": color.theme, "tint": float(color.tint or 0.0)}
    if color.type == "indexed":
        return {"type": "indexed", "indexed": color.indexed}
    if color.type == "auto":
        return {"type": "auto", "auto": bool(color.auto)}
    return {"type": str(color.type)}


def colors_equal(left, right) -> bool:
    return serialize_color(left) == serialize_color(right)


def serialize_fill(fill) -> dict[str, Any] | None:
    if not fill or fill.fill_type is None:
        return None

    result: dict[str, Any] = {"pattern_type": fill.fill_type}
    fg_color = serialize_color(fill.fgColor)
    bg_color = serialize_color(fill.bgColor)
    if fg_color:
        result["fg_color"] = fg_color
    if bg_color and bg_color != fg_color and bg_color != {"type": "rgb", "rgb": "00000000"}:
        result["bg_color"] = bg_color
    return result


def serialize_side(side) -> dict[str, Any] | None:
    if side is None or side.style is None:
        return None
    result: dict[str, Any] = {"style": side.style}
    color = serialize_color(side.color)
    if color:
        result["color"] = color
    return result


def serialize_border(border) -> dict[str, Any] | None:
    if not border:
        return None
    result = {}
    for side_name in ("left", "right", "top", "bottom"):
        side = serialize_side(getattr(border, side_name))
        if side:
            result[side_name] = side
    return result or None


def serialize_font(font) -> dict[str, Any] | None:
    if not font:
        return None

    result: dict[str, Any] = {}
    if font.name != DEFAULT_FONT.name:
        result["name"] = font.name
    if font.sz != DEFAULT_FONT.sz:
        result["size"] = float(font.sz) if font.sz is not None else None
    if meaningful_bool(font.bold):
        result["bold"] = True
    if meaningful_bool(font.italic):
        result["italic"] = True
    if font.underline:
        result["underline"] = font.underline
    if meaningful_bool(font.strike):
        result["strike"] = True
    if not colors_equal(font.color, DEFAULT_FONT.color):
        color = serialize_color(font.color)
        if color:
            result["color"] = color
    return {key: value for key, value in result.items() if value is not None} or None


def serialize_alignment(alignment) -> dict[str, Any] | None:
    if not alignment:
        return None

    result: dict[str, Any] = {}
    if alignment.horizontal:
        result["horizontal"] = alignment.horizontal
    if alignment.vertical:
        result["vertical"] = alignment.vertical
    if meaningful_bool(alignment.wrap_text):
        result["wrap_text"] = True
    if alignment.text_rotation:
        result["text_rotation"] = alignment.text_rotation
    if meaningful_bool(alignment.shrink_to_fit):
        result["shrink_to_fit"] = True
    if alignment.indent:
        result["indent"] = alignment.indent
    return result or None


def serialize_protection(protection) -> dict[str, Any] | None:
    if not protection:
        return None
    result: dict[str, Any] = {}
    if protection.locked is False:
        result["locked"] = False
    if protection.hidden:
        result["hidden"] = True
    return result or None


def serialize_cell_style(cell) -> dict[str, Any]:
    style: dict[str, Any] = {}

    fill = serialize_fill(cell.fill)
    if fill:
        style["fill"] = fill

    border = serialize_border(cell.border)
    if border:
        style["border"] = border

    if cell.number_format and cell.number_format != "General":
        style["number_format"] = cell.number_format

    font = serialize_font(cell.font)
    if font:
        style["font"] = font

    alignment = serialize_alignment(cell.alignment)
    if alignment:
        style["alignment"] = alignment

    protection = serialize_protection(cell.protection)
    if protection:
        style["protection"] = protection

    return style


def style_has_visible_fill(style: dict[str, Any]) -> bool:
    return bool(style.get("fill"))


def style_has_visible_border(style: dict[str, Any]) -> bool:
    return bool(style.get("border"))


def style_is_unlocked(style: dict[str, Any]) -> bool:
    return (style.get("protection") or {}).get("locked") is False


def blank_style_has_strong_signal(style: dict[str, Any]) -> bool:
    return (
        style_has_visible_fill(style)
        or style_has_visible_border(style)
        or style_is_unlocked(style)
    )
