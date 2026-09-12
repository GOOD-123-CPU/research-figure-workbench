#!/usr/bin/env python3
"""Inspect PDF/SVG/PNG figure outputs and screen common publication-delivery risks."""

from __future__ import annotations

import argparse
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

MM_PER_INCH = 25.4
PT_PER_INCH = 72.0
PX_PER_INCH = 96.0  # CSS/SVG px convention used only for physical-size estimation.


def _length_to_mm(value: str | None) -> float | None:
    if not value:
        return None
    match = re.fullmatch(r"\s*([-+]?\d*\.?\d+)\s*([a-zA-Z%]*)\s*", value)
    if not match:
        return None
    number = float(match.group(1))
    unit = match.group(2).lower()
    if unit in {"", "px"}:
        return number / PX_PER_INCH * MM_PER_INCH
    if unit == "mm":
        return number
    if unit == "cm":
        return number * 10.0
    if unit == "in":
        return number * MM_PER_INCH
    if unit == "pt":
        return number / PT_PER_INCH * MM_PER_INCH
    return None


def inspect_svg(path: Path) -> dict[str, Any]:
    root = ET.parse(path).getroot()
    width_raw = root.attrib.get("width")
    height_raw = root.attrib.get("height")
    viewbox = root.attrib.get("viewBox")
    text_nodes = sum(1 for elem in root.iter() if elem.tag.endswith("text"))
    image_nodes = sum(1 for elem in root.iter() if elem.tag.endswith("image"))
    path_nodes = sum(1 for elem in root.iter() if elem.tag.endswith("path"))
    return {
        "type": "svg",
        "width": width_raw,
        "height": height_raw,
        "width_mm_estimate": _length_to_mm(width_raw),
        "height_mm_estimate": _length_to_mm(height_raw),
        "viewBox": viewbox,
        "text_nodes": text_nodes,
        "image_nodes": image_nodes,
        "path_nodes": path_nodes,
    }


def inspect_png(path: Path) -> dict[str, Any]:
    try:
        from PIL import Image
    except ImportError as exc:
        return {"type": "png", "dependency_warning": f"Pillow not installed: {exc}"}
    with Image.open(path) as image:
        dpi = image.info.get("dpi")
        dpi_values = [float(v) for v in dpi] if dpi else None
        width_mm = None
        height_mm = None
        if dpi_values and min(dpi_values) > 0:
            width_mm = image.size[0] / dpi_values[0] * MM_PER_INCH
            height_mm = image.size[1] / dpi_values[1] * MM_PER_INCH
        return {
            "type": "png",
            "pixels": list(image.size),
            "dpi": dpi_values,
            "width_mm_estimate": width_mm,
            "height_mm_estimate": height_mm,
            "mode": image.mode,
            "has_alpha": "A" in image.getbands(),
            "icc_profile_present": bool(image.info.get("icc_profile")),
        }


def _pdf_font_summary(page) -> dict[str, Any]:
    summary: dict[str, Any] = {"font_resources": [], "font_count": 0}
    try:
        resources = page.get("/Resources") or {}
        fonts = resources.get("/Font") or {}
        if hasattr(fonts, "get_object"):
            fonts = fonts.get_object()
        entries = []
        for name, ref in fonts.items():
            obj = ref.get_object() if hasattr(ref, "get_object") else ref
            entries.append(
                {
                    "resource": str(name),
                    "subtype": str(obj.get("/Subtype")) if hasattr(obj, "get") else None,
                    "basefont": str(obj.get("/BaseFont")) if hasattr(obj, "get") else None,
                }
            )
        summary["font_resources"] = entries
        summary["font_count"] = len(entries)
    except Exception as exc:
        summary["font_warning"] = str(exc)
    return summary


def inspect_pdf(path: Path) -> dict[str, Any]:
    reader = None
    errors = []
    for module_name in ("pypdf", "PyPDF2"):
        try:
            module = __import__(module_name)
            reader = module.PdfReader(str(path))
            break
        except Exception as exc:
            errors.append(f"{module_name}: {exc}")
    if reader is None:
        return {"type": "pdf", "dependency_warning": "PDF metadata library unavailable", "details": errors}
    if not reader.pages:
        return {"type": "pdf", "pages": 0}
    page = reader.pages[0]
    box = page.mediabox
    width_pt = float(box.width)
    height_pt = float(box.height)
    payload = {
        "type": "pdf",
        "pages": len(reader.pages),
        "width_mm": width_pt / PT_PER_INCH * MM_PER_INCH,
        "height_mm": height_pt / PT_PER_INCH * MM_PER_INCH,
    }
    payload.update(_pdf_font_summary(page))
    return payload


def _finding(severity: str, code: str, message: str) -> dict[str, str]:
    return {"severity": severity, "code": code, "message": message}


def evaluate(
    path: Path,
    info: dict[str, Any],
    *,
    min_dpi: float | None = None,
    expected_width_mm: float | None = None,
    expected_height_mm: float | None = None,
    tolerance_mm: float = 1.0,
    require_editable_text: bool = False,
) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if path.stat().st_size == 0:
        findings.append(_finding("blocking", "EMPTY_FILE", "file is empty"))

    if info.get("dependency_warning"):
        findings.append(_finding("warning", "DEPENDENCY", str(info["dependency_warning"])))

    ftype = info.get("type")
    if ftype == "png":
        dpi = info.get("dpi")
        if min_dpi is not None:
            if not dpi:
                findings.append(_finding("warning", "DPI_MISSING", "raster file does not expose DPI metadata"))
            elif min(dpi) + 0.5 < min_dpi:
                findings.append(
                    _finding("warning", "DPI_LOW", f"raster DPI {min(dpi):.1f} is below requested {min_dpi:.1f}")
                )

    if ftype == "pdf" and info.get("pages", 1) != 1:
        findings.append(_finding("warning", "PDF_PAGES", "manuscript figure PDF normally should contain one page"))

    if ftype == "svg" and require_editable_text and info.get("text_nodes", 0) == 0:
        findings.append(
            _finding("warning", "SVG_NO_TEXT", "SVG contains no <text> nodes; labels may have been converted to paths")
        )

    width = info.get("width_mm")
    height = info.get("height_mm")
    if width is None:
        width = info.get("width_mm_estimate")
    if height is None:
        height = info.get("height_mm_estimate")

    if expected_width_mm is not None:
        if width is None:
            findings.append(_finding("warning", "WIDTH_UNKNOWN", "could not determine physical width"))
        elif abs(float(width) - expected_width_mm) > tolerance_mm:
            findings.append(
                _finding(
                    "warning",
                    "WIDTH_MISMATCH",
                    f"width {float(width):.2f} mm differs from expected {expected_width_mm:.2f} mm",
                )
            )
    if expected_height_mm is not None:
        if height is None:
            findings.append(_finding("warning", "HEIGHT_UNKNOWN", "could not determine physical height"))
        elif abs(float(height) - expected_height_mm) > tolerance_mm:
            findings.append(
                _finding(
                    "warning",
                    "HEIGHT_MISMATCH",
                    f"height {float(height):.2f} mm differs from expected {expected_height_mm:.2f} mm",
                )
            )

    if isinstance(width, (int, float)) and width > 220:
        findings.append(_finding("warning", "VERY_WIDE", "figure width exceeds 220 mm; verify target layout"))

    return findings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--strict", action="store_true", help="exit 1 on warnings as well as blocking findings")
    parser.add_argument("--min-dpi", type=float)
    parser.add_argument("--expected-width-mm", type=float)
    parser.add_argument("--expected-height-mm", type=float)
    parser.add_argument("--tolerance-mm", type=float, default=1.0)
    parser.add_argument("--require-editable-text", action="store_true")
    parser.add_argument("--json-out")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".svg":
        info = inspect_svg(path)
    elif suffix == ".png":
        info = inspect_png(path)
    elif suffix == ".pdf":
        info = inspect_pdf(path)
    else:
        raise SystemExit("Supported: .pdf, .svg, .png")

    findings = evaluate(
        path,
        info,
        min_dpi=args.min_dpi,
        expected_width_mm=args.expected_width_mm,
        expected_height_mm=args.expected_height_mm,
        tolerance_mm=args.tolerance_mm,
        require_editable_text=args.require_editable_text,
    )
    result = {
        "path": str(path),
        "bytes": path.stat().st_size,
        "info": info,
        "findings": findings,
        "status": "PASS" if not findings else "REVIEW",
        "note": "Metadata/preflight screening only; not a scientific, accessibility, or publisher-compliance certification.",
    }
    text = json.dumps(result, indent=2, ensure_ascii=False)
    print(text)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")

    blocking = any(f["severity"] == "blocking" for f in findings)
    warnings = bool(findings)
    if blocking or (args.strict and warnings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
