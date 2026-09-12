#!/usr/bin/env python3
"""Basic deterministic QA helpers for rendered Matplotlib figures.

These checks screen obvious layout problems. They do not certify scientific meaning,
accessibility, or publisher compliance.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Sequence


def _bbox_dict(bbox) -> dict[str, float]:
    return {
        "x0": float(bbox.x0),
        "y0": float(bbox.y0),
        "x1": float(bbox.x1),
        "y1": float(bbox.y1),
        "width": float(bbox.width),
        "height": float(bbox.height),
    }


def _visible_text_bbox(text, renderer):
    if not text.get_visible() or not str(text.get_text()).strip():
        return None
    try:
        return text.get_window_extent(renderer=renderer)
    except Exception:
        return None


def _overlap_pairs(labels: Iterable, renderer) -> list[tuple[str, str]]:
    boxes: list[tuple[str, Any]] = []
    for label in labels:
        box = _visible_text_bbox(label, renderer)
        if box is not None:
            boxes.append((str(label.get_text()), box))
    pairs: list[tuple[str, str]] = []
    for i, (a_text, a_box) in enumerate(boxes):
        for b_text, b_box in boxes[i + 1 :]:
            if a_box.overlaps(b_box):
                pairs.append((a_text, b_text))
    return pairs


def audit_layout(
    fig,
    *,
    comparable_groups: Sequence[Sequence[int]] | None = None,
    alignment_tolerance_pt: float = 1.5,
) -> dict[str, Any]:
    """Audit clipping, adjacent tick-label overlap, and optional axes alignment."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    fig_box = fig.bbox
    findings: list[dict[str, Any]] = []

    # Inspect text that is actually relevant to the visible axes range. Matplotlib
    # may keep locator-generated tick labels outside the view limits; checking every
    # Text artist would create false clipping alarms.
    visible_texts = list(fig.texts)
    for ax in fig.axes:
        visible_texts.extend([ax.title, ax.xaxis.label, ax.yaxis.label])
        xlo, xhi = sorted(ax.get_xlim())
        ylo, yhi = sorted(ax.get_ylim())
        visible_texts.extend(
            label for tick, label in zip(ax.get_xticks(), ax.get_xticklabels()) if xlo <= tick <= xhi
        )
        visible_texts.extend(
            label for tick, label in zip(ax.get_yticks(), ax.get_yticklabels()) if ylo <= tick <= yhi
        )
        visible_texts.extend(ax.texts)
        legend = ax.get_legend()
        if legend is not None and legend.get_visible():
            visible_texts.extend(legend.get_texts())
            if legend.get_title() is not None:
                visible_texts.append(legend.get_title())

    seen = set()
    for text in visible_texts:
        if id(text) in seen:
            continue
        seen.add(id(text))
        box = _visible_text_bbox(text, renderer)
        if box is None:
            continue
        tol_px = 1.0
        if (
            box.x0 < fig_box.x0 - tol_px
            or box.y0 < fig_box.y0 - tol_px
            or box.x1 > fig_box.x1 + tol_px
            or box.y1 > fig_box.y1 + tol_px
        ):
            findings.append(
                {
                    "severity": "warning",
                    "code": "TEXT_OUTSIDE_CANVAS",
                    "text": str(text.get_text()),
                    "bbox_px": _bbox_dict(box),
                }
            )

    # Tick-label overlaps are a common deterministic failure.
    axes_report: list[dict[str, Any]] = []
    for index, ax in enumerate(fig.axes):
        x_pairs = _overlap_pairs(ax.get_xticklabels(), renderer)
        y_pairs = _overlap_pairs(ax.get_yticklabels(), renderer)
        for a, b in x_pairs:
            findings.append(
                {
                    "severity": "warning",
                    "code": "XTICK_LABEL_OVERLAP",
                    "axes_index": index,
                    "labels": [a, b],
                }
            )
        for a, b in y_pairs:
            findings.append(
                {
                    "severity": "warning",
                    "code": "YTICK_LABEL_OVERLAP",
                    "axes_index": index,
                    "labels": [a, b],
                }
            )

        pos = ax.get_position()
        axes_report.append(
            {
                "index": index,
                "label": ax.get_label(),
                "position_figure_fraction": _bbox_dict(pos),
            }
        )

    # Optional explicit comparable groups avoid guessing colorbars/insets.
    if comparable_groups:
        fig_width_in, fig_height_in = fig.get_size_inches()
        px_per_pt_x = fig.dpi / 72.0
        px_per_pt_y = fig.dpi / 72.0
        tol_x = alignment_tolerance_pt * px_per_pt_x / (fig_width_in * fig.dpi)
        tol_y = alignment_tolerance_pt * px_per_pt_y / (fig_height_in * fig.dpi)

        for group_index, group in enumerate(comparable_groups):
            valid = [i for i in group if 0 <= i < len(fig.axes)]
            if len(valid) < 2:
                continue
            positions = [fig.axes[i].get_position() for i in valid]
            widths = [p.width for p in positions]
            heights = [p.height for p in positions]
            if max(widths) - min(widths) > tol_x:
                findings.append(
                    {
                        "severity": "warning",
                        "code": "PANEL_WIDTH_MISMATCH",
                        "group": group_index,
                        "axes": valid,
                    }
                )
            if max(heights) - min(heights) > tol_y:
                findings.append(
                    {
                        "severity": "warning",
                        "code": "PANEL_HEIGHT_MISMATCH",
                        "group": group_index,
                        "axes": valid,
                    }
                )

    return {
        "figure_size_inches": [float(v) for v in fig.get_size_inches()],
        "dpi": float(fig.dpi),
        "axes": axes_report,
        "findings": findings,
        "passed_screen": not findings,
        "note": "Deterministic layout screening only; visual/scientific review still required.",
    }


def render_preview(fig, path: str | Path, *, dpi: int = 150, grayscale: bool = False) -> Path:
    """Render a PNG preview without changing the publication master."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches=None, facecolor=fig.get_facecolor())
    if grayscale:
        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("Pillow is required for grayscale preview") from exc
        with Image.open(path) as image:
            image.convert("L").save(path)
    return path


def write_report(report: dict[str, Any], path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path
