# Backend Routing

Choose the backend for reproducibility and project fit, not for aesthetics alone.

## Python + Matplotlib — default static route

Use by default for new static scientific figures.

Strengths:

- precise physical dimensions and multi-panel layout;
- vector PDF/SVG with selective layer rasterization;
- broad NumPy/Pandas/SciPy/scikit scientific ecosystem;
- easy deterministic QA and provenance scripting.

Prefer Matplotlib's object-oriented API and a scoped style:

```python
from publication_style import publication_style_context, new_figure, save_publication_figure

with publication_style_context(base_font_pt=8):
    fig, ax = new_figure(width_mm=85, height_mm=58)
    # draw
    save_publication_figure(fig, "figure", width_mm=85, height_mm=58)
```

Use `layout="constrained"`/constrained layout for complex grids. Do not call `tight_layout()` afterward. Preserve exact page dimensions by avoiding `bbox_inches="tight"` unless the resulting changed physical size is intentional.

## MATLAB

Route to MATLAB when:

- the user explicitly requests MATLAB;
- the analysis/model is already MATLAB-native;
- `.mat` data and scripts are the reproducibility source;
- the figure depends on MATLAB-specific toolboxes or simulation output.

Rules:

- inspect MAT variables before choosing one;
- keep style and final-size parameters at the top of the script;
- use `exportgraphics` or a modern vector-capable exporter when available;
- set physical size intentionally before export;
- export vector PDF/SVG where the MATLAB version/content permits, plus a preview image;
- if MATLAB CLI is unavailable, provide runnable source and mark rendering `UNVERIFIED`.

Do not migrate a validated MATLAB result to Python merely to change styling unless the user wants that maintenance burden.

## R + ggplot2

Route to R when:

- the user explicitly requests R/ggplot2;
- the statistics/analysis pipeline is R-native;
- ComplexHeatmap, patchwork/cowplot, survival/bioconductor, or another R-native workflow is central.

Rules:

- centralize `theme()` and palette settings;
- use `ggsave()`/appropriate device with physical units and explicit dimensions;
- use `patchwork`/`cowplot` for multi-panel composition rather than stitching exported PNGs;
- prefer facets over excessive categorical colors;
- retain vector text/axes while using rasterized/density layers for huge point clouds when practical;
- verify the exported PDF/SVG rather than assuming device defaults embedded fonts/editable text as intended.

## Origin / OriginPro — explicit user/project route

Use an Origin-oriented workflow only when Origin/OriginPro is already part of the lab/project or the user explicitly requests it.

- Preserve the Origin project/template and the source worksheet/data mapping.
- Record any manual graph edits that change scientific meaning.
- Prefer reproducible Origin Python/LabTalk/COM steps when available in the user's environment.
- Export vector line art where appropriate and raster scientific images at the required final-size resolution.
- Do not claim Origin COM automation or curve fitting ran unless that runtime was actually available and executed.
- Keep a script/procedure note beside the final export so the figure is not an unexplained GUI artifact.

## Cross-backend consistency

Regardless of backend:

- preserve the Figure Contract and data roles;
- preserve category ordering and semantic colors across manuscript figures;
- preserve the uncertainty definition and unit of replication;
- record transformations, exclusions, smoothing, and aggregation;
- render at final physical size;
- inspect the actual exported artifact;
- keep runnable source or a documented reproducible software procedure beside the figure.
