#!/usr/bin/env python3
"""Reusable, scoped Matplotlib defaults for publication-oriented scientific figures."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator

MM_PER_INCH = 25.4

# Okabe-Ito / Wong-style qualitative sequence. Yellow should be used carefully on white.
WONG = [
    "#E69F00",
    "#56B4E9",
    "#009E73",
    "#CC79A7",
    "#D55E00",
    "#F0E442",
    "#0072B2",
    "#000000",
]
OKABE_ITO = WONG


def mm_to_inch(value_mm: float) -> float:
    return float(value_mm) / MM_PER_INCH


def _style_dict(base_font_pt: float = 8.0, font_family: str = "DejaVu Sans") -> dict[str, object]:
    return {
        "font.family": font_family,
        "font.size": base_font_pt,
        "axes.labelsize": base_font_pt,
        "axes.titlesize": base_font_pt,
        "xtick.labelsize": base_font_pt,
        "ytick.labelsize": base_font_pt,
        "legend.fontsize": base_font_pt,
        "legend.title_fontsize": base_font_pt,
        "axes.linewidth": 0.6,
        "lines.linewidth": 1.2,
        "lines.markersize": 4.0,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.minor.width": 0.4,
        "ytick.minor.width": 0.4,
        "grid.linewidth": 0.4,
        "grid.alpha": 0.25,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "savefig.transparent": False,
    }


@contextmanager
def publication_style_context(
    base_font_pt: float = 8.0,
    font_family: str = "DejaVu Sans",
) -> Iterator[None]:
    """Apply publication defaults only inside this context."""
    import matplotlib as mpl

    with mpl.rc_context(_style_dict(base_font_pt=base_font_pt, font_family=font_family)):
        yield


def apply_publication_style(base_font_pt: float = 8.0, font_family: str = "DejaVu Sans") -> None:
    """Compatibility helper that applies defaults globally to the current process.

    Prefer publication_style_context() for new code so unrelated figures are not affected.
    """
    import matplotlib as mpl

    mpl.rcParams.update(_style_dict(base_font_pt=base_font_pt, font_family=font_family))


def new_figure(width_mm: float = 85.0, height_mm: float = 58.0, **kwargs):
    import matplotlib.pyplot as plt

    kwargs.setdefault("layout", "constrained")
    return plt.subplots(
        figsize=(mm_to_inch(width_mm), mm_to_inch(height_mm)),
        **kwargs,
    )


def save_publication_figure(
    fig,
    stem: str | Path,
    *,
    width_mm: float = 85.0,
    height_mm: float = 58.0,
    formats: Iterable[str] = ("pdf", "svg", "png"),
    raster_dpi: int = 300,
    transparent: bool = False,
    overwrite: bool = False,
) -> list[Path]:
    """Save an exact-size figure to vector outputs plus a raster preview.

    The page size is preserved intentionally: bbox_inches='tight' is not used.
    """
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.set_size_inches(mm_to_inch(width_mm), mm_to_inch(height_mm), forward=True)

    outputs: list[Path] = []
    for fmt in formats:
        fmt = fmt.lower().lstrip(".")
        if fmt not in {"pdf", "svg", "png", "tif", "tiff"}:
            raise ValueError(f"Unsupported format: {fmt}")
        path = stem.with_suffix(f".{fmt}")
        if path.exists() and not overwrite:
            raise FileExistsError(f"Refusing to overwrite existing output: {path}")

        save_kwargs: dict[str, object] = {
            "transparent": transparent,
            "bbox_inches": None,
        }
        if fmt in {"png", "tif", "tiff"}:
            save_kwargs["dpi"] = int(raster_dpi)
        fig.savefig(path, **save_kwargs)
        outputs.append(path)
    return outputs
