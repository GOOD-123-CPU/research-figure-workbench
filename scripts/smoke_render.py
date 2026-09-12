#!/usr/bin/env python3
"""Render synthetic publication examples and exercise export + layout QA."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from publication_style import WONG, publication_style_context, save_publication_figure
from visual_qa import audit_layout, render_preview, write_report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="smoke-output")
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    import matplotlib.pyplot as plt

    rng = np.random.default_rng(7)
    x = np.linspace(0, 10, 80)
    mean = np.sin(x / 1.8)
    band = 0.18 + 0.03 * np.cos(x)

    with publication_style_context(base_font_pt=8):
        fig, axes = plt.subplots(1, 2, figsize=(180 / 25.4, 62 / 25.4), layout="constrained")

        ax = axes[0]
        ax.plot(x, mean, color=WONG[6], marker="o", markevery=10, label="Estimate")
        ax.fill_between(
            x,
            mean - band,
            mean + band,
            color=WONG[1],
            alpha=0.28,
            linewidth=0,
            label="95% interval",
        )
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Response (a.u.)")
        ax.grid(True, axis="y")
        ax.legend(frameon=False)

        ax = axes[1]
        a = rng.normal(0.0, 1.0, 70)
        b = 0.65 * a + rng.normal(0.0, 0.7, 70)
        ax.scatter(a, b, s=14, alpha=0.75, color=WONG[2], edgecolors="none", rasterized=True)
        lim = max(abs(a).max(), abs(b).max()) * 1.08
        ax.plot([-lim, lim], [-lim, lim], linestyle="--", linewidth=0.8, color="0.35")
        ax.set_xlim(-lim * 1.12, lim * 1.12)
        ax.set_ylim(-lim * 1.12, lim * 1.12)
        ax.set_xlabel("Measurement A")
        ax.set_ylabel("Measurement B")
        ax.grid(True, alpha=0.2)

        for label, panel_ax in zip(("A", "B"), axes):
            panel_ax.text(-0.16, 1.04, label, transform=panel_ax.transAxes, fontweight="bold", va="bottom")

        report = audit_layout(fig, comparable_groups=[[0, 1]])
        render_preview(fig, out / "smoke_preview.png", dpi=160)
        write_report(report, out / "smoke_layout_report.json")
        save_publication_figure(
            fig,
            out / "smoke_figure",
            width_mm=180,
            height_mm=62,
            formats=("pdf", "svg", "png"),
            raster_dpi=300,
            overwrite=True,
        )
        plt.close(fig)

    for path in (
        out / "smoke_figure.pdf",
        out / "smoke_figure.svg",
        out / "smoke_figure.png",
        out / "smoke_preview.png",
        out / "smoke_layout_report.json",
    ):
        print(path)


if __name__ == "__main__":
    main()
