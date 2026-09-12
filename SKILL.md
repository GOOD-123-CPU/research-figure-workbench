---
name: research-figure-workbench
description: End-to-end research-paper figure workflow for selecting, generating, revising, auditing, and exporting publication-ready scientific figures and method diagrams. Use for CSV/Excel/MAT/NPY/NPZ data, manuscript figures, thesis figures, multi-panel evidence layouts, uncertainty visualization, journal/conference figure compliance, vector PDF/SVG export, Python/Matplotlib, MATLAB, R/ggplot2, Origin-oriented workflows, graphical-method diagrams, figure captions, and pre-submission figure QA. Route to Python/Matplotlib by default, MATLAB or R when explicitly requested or project-native, and Mermaid-to-draw.io for editable conceptual diagrams. Preserve scientific truth, reproducibility, source-data traceability, and final-size visual QA above aesthetic polish.
---

# Research Figure Workbench

## Operating contract

Treat scientific truth as the first constraint, communication clarity as the second, and visual polish as the third.

- Never invent, hide, selectively omit, smooth, rescale, transform, clip, or relabel data merely to make a stronger-looking result.
- Preserve source data, exclusions, missing-value handling, transformations, aggregation, normalization, smoothing, binning, random seeds, and image-processing steps.
- Make the claim-to-encoding relationship explicit before styling.
- Prefer reproducible scripts and editable/vector outputs over manual image edits.
- Render and inspect the actual final artifact whenever an execution environment is available.
- Do not claim a figure is publication-ready until the rendered output has passed semantic, statistical, visual, and production review.
- Separate publisher policy from community best practice. Never present remembered or third-party style advice as an official journal requirement.
- Do not use a generative-image model for quantitative evidence. For graphical abstracts or conceptual artwork, verify the target venue's current AI-image policy first and treat unverified output as a draft.

## Task routing

Classify the request before doing figure work.

1. **Data figure** — numeric/statistical evidence, plots, heatmaps, images with quantitative overlays. Follow the data-figure workflow.
2. **Conceptual/method diagram** — architecture, experiment pipeline, signal chain, algorithm flow, graphical method overview. Read `references/diagram-workflow.md`.
3. **Composite manuscript figure** — mixes plots, scientific images, and/or diagrams. Build and review each panel independently, then compose using `references/evidence-architecture.md`.
4. **Figure audit** — finished or near-finished figure/caption/manuscript checks. Read `references/manuscript-figure-audit.md` and do not redraw unless revision is requested.
5. **Cosmetic revision only** — preserve data, statistics, scales, and semantics unless the user explicitly requests a substantive change.

## Data-figure workflow

### 1. Freeze the Figure Contract

Before choosing a chart, read `references/figure-contract.md` and record at least:

- one-sentence scientific claim or question;
- comparison the reader must notice first;
- observational unit and independence/paired/repeated/nested structure;
- x, y, group, facet, color, shape, and uncertainty roles;
- transformations and exclusions already applied or planned;
- target medium, journal/conference if known, article type, submission phase, and final physical size;
- backend and required deliverables;
- for multi-panel figures, the evidence role of every panel.

If the user's scientific goal is already inferable from the manuscript context, state the assumption and proceed. Ask only when a missing semantic choice would materially change the scientific meaning.

### 2. Inspect the data before plotting

For supported data files run:

```bash
python scripts/inspect_data.py <file> --json <report.json>
```

Check missingness, numeric ranges, robust summaries, category counts, duplicated keys, likely identifiers/time/order fields, imbalance, and plausible paired/grouped structures.

- Do not silently choose among multiple plausible MAT/NPZ arrays.
- Do not downsample merely to make rendering easier. Prefer density/binning or rasterized dense layers and disclose them.
- Do not infer a statistical test solely from the desired annotation style.

### 3. Choose the encoding from the scientific comparison

Read `references/chart-selection.md`.

- Prefer position on a common scale and encodings whose geometry matches the comparison.
- Preserve pairing/repeated measures when scientifically important.
- Show raw observations when feasible and informative.
- Define uncertainty explicitly: SD, SEM, CI, credible interval, percentile range, bootstrap interval, etc.
- Distinguish missing, zero, censored, and excluded observations.
- Reject misleading baselines, normalization, color scales, area/radius mappings, dual-axis constructions, or category-connecting lines.

When multiple encodings are scientifically valid, render 2-4 meaningfully different candidates and compare them with `references/review-rubric.md`. Do not generate cosmetic variants as fake alternatives.

### 4. Design multi-panel evidence architecture

For two or more panels, read `references/evidence-architecture.md`.

- Make the whole figure answer one Results-level question when possible.
- Give panels distinct inferential roles rather than repeating the same result in different chart types.
- Use a symmetric grid when panels have equal scientific weight; use an asymmetric/hero layout only when one panel genuinely carries the central evidence or information density.
- Order panels in the same sequence as the scientific argument.
- Keep shared units, scales, category order, color meaning, and uncertainty definitions consistent.

### 5. Resolve publisher requirements with evidence discipline

Read `references/journal-source-policy.md` whenever a target venue is named or submission compliance matters.

- Identify exact journal/conference, article type, figure type, and submission phase.
- Prefer live official author/production guidance when web access is available.
- Record source URL/title, access date, rule, evidence class, and applicability in the figure report or journal profile.
- Treat bundled dimensions and style defaults only as provisional starting points.
- If live verification is unavailable, clearly mark publisher-specific choices as **UNVERIFIED** rather than guessing.

### 6. Route the renderer

Read `references/backend-routing.md` when the backend is not obvious.

- Default: **Python + Matplotlib** for static scientific figures.
- Use **MATLAB** when explicitly requested or the analysis is MATLAB-centric.
- Use **R + ggplot2** when explicitly requested or the project is R-native.
- Use an **Origin-oriented workflow** only when the user explicitly works in Origin/OriginPro and preserve a reproducible project/export path; do not claim COM automation ran if the runtime is unavailable.

Do not switch backends only because a different library would look prettier. Preserve the project-native analysis path when reproducibility matters more.

### 7. Implement at final physical size

Keep figure width, height, font size, line width, marker size, palette, output formats, and raster DPI in one parameter block.

For Python, prefer `scripts/publication_style.py` and its scoped `publication_style_context()` rather than mutating global style permanently.

- Use one restrained type system.
- Use color to encode meaning, not decoration.
- Add line style, marker, hatching, direct labels, or faceting so color is not the only cue.
- Keep manuscript figure titles in the caption by default; panel labels such as A/B are fine.
- Match legend order to visual/category order; prefer direct labels for a few series when they improve decoding.
- Use explicit units in axis labels.

### 8. Render publication outputs

Default deliverables for data figures:

- **PDF** — primary vector manuscript output;
- **SVG** — editable/vector interchange output;
- **PNG** — review/compatibility preview;
- runnable plotting source;
- Figure Contract + concise provenance/report.

Rasterize only scientifically dense raster-like layers when needed; keep text, axes, line art, and annotations vector where practical.

### 9. Run machine QA before visual QA

For Matplotlib figures, use `scripts/visual_qa.py` after the final draw to screen obvious clipping, tick-label overlap, and panel geometry issues. Save a preview and layout report when practical.

Run file-level preflight on every final output:

```bash
python scripts/preflight_figure.py figure.pdf --strict
python scripts/preflight_figure.py figure.svg --strict
python scripts/preflight_figure.py figure.png --strict --min-dpi 300
```

Automated checks are screening tools, not scientific or publisher certification.

### 10. Inspect the rendered figure at final size

Read `references/visual-qa.md` and `references/review-rubric.md`.

Review in this order:

1. semantic validity and observational structure;
2. data integrity and transformation disclosure;
3. uncertainty/statistical meaning;
4. scale/baseline/color-normalization honesty;
5. final-size legibility, clipping, overlaps, panel alignment;
6. accessibility and redundant encoding;
7. visual economy and evidence hierarchy;
8. export dimensions, editability, fonts, raster quality, and transparency.

After any material repair, re-render and repeat the relevant checks.

### 11. Audit caption and manuscript linkage when applicable

For submission-facing work, read `references/manuscript-figure-audit.md`.

Check that the caption stands alone and states the plotted quantity, units, sample/replication, uncertainty, panel meanings, relevant transformations, and statistical model/test details where needed.

When checking claims against a rendered image, never invent exact values by eyeballing unlabeled graphics. Prefer source data; otherwise mark the finding **VISUAL READ ONLY — AUTHOR VERIFY**.

### 12. Deliver a reproducible bundle

Read `references/figure-report-template.md`. Deliver, as applicable:

- source plotting/diagram code;
- final PDF/SVG and preview image;
- figure contract;
- provenance/report including transformations and uncertainty definition;
- QA findings and any unresolved warnings;
- editable diagram source for conceptual panels;
- project-local style profile only when based on explicit user preferences.

## Scientific defaults

Use these only when no stronger project or venue requirement exists.

- Start around 85-90 mm for single-column and 175-185 mm for double-column manuscript figures; verify the exact venue before submission.
- Use about 8 pt as a neutral final-size base text starting point; never infer compliance from that number alone.
- Use an Okabe-Ito/Wong-style colorblind-safe qualitative palette for small group counts, with redundant encoding.
- Use perceptually uniform sequential maps such as viridis/cividis; use diverging normalization only around a meaningful reference value.
- Bars and filled magnitude areas normally require a meaningful zero baseline; points/lines may use nonzero limits when scientifically defensible and clearly contextualized.
- Prefer raw points + intervals, paired displays, estimation plots, box/jitter, violin+jitter, ECDFs, or model-estimate intervals when distributions or repeated observations matter.
- Avoid decorative 3D, rainbow/jet maps, unexplained smoothing, undisclosed independent per-panel normalization, and arbitrary dual y-axes.
- For dense point clouds use alpha, density/binning, or disclosed layer rasterization rather than deleting inconvenient observations.
- For comparable multi-panel plots align plotting regions and use common scales where the comparison requires them.

## Statistical restraint

A figure is not a license to invent inference.

- Do not add p-values or significance stars merely because the user asks for a “publication look.”
- Use the user's existing analysis/test when available.
- If a new test is required, make the assumptions and unit of replication explicit before computing it.
- Prefer effect sizes and interval estimates where they answer the scientific question.
- Never treat non-significance, weak effects, or negative results as reasons to hide data or refuse to plot them.

## Diagram route

For conceptual or method figures:

1. Draft logic in Mermaid while the structure is still changing.
2. Move to draw.io/diagrams.net when precise alignment, grouped containers, or editable publication source is needed.
3. Keep text concise and technical; make arrow semantics consistent.
4. Export SVG/PDF and keep editable source.
5. Match typography and panel labels to quantitative panels in composites.
6. Verify current venue rules before using any generative-image output as submission artwork.

Read `references/diagram-workflow.md` before final delivery.

## Project taste memory

If `.research-figure/style-profile.json` exists, read it before styling. Update it only from explicit user feedback such as “prefer,” “reuse,” “like,” or “avoid.” Do not infer durable aesthetic preferences from silence, and never store unpublished numerical results or private reviewer text in the profile.

Use `scripts/style_profile.py` to initialize or update it.

## Verification rules

- Do not claim code ran unless it actually ran.
- Do not claim a figure was visually reviewed unless the rendered artifact was actually inspected.
- Do not claim a journal requirement is official unless it was verified from an authoritative current source.
- Do not claim a file is editable/vector solely from its extension; inspect the exported artifact.
- Do not claim a statistical interpretation that the plot alone cannot establish.
- If a required backend is unavailable, provide runnable source and mark execution as unverified.

## Bundled resources

Core references:

- `references/figure-contract.md` — Figure Contract and data-integrity fields.
- `references/chart-selection.md` — semantic chart choice and hard rejects.
- `references/evidence-architecture.md` — multi-panel scientific argument and layout roles.
- `references/journal-source-policy.md` — source hierarchy and stage-specific publisher verification.
- `references/publication-style.md` — neutral typography/color/export defaults.
- `references/backend-routing.md` — Python/MATLAB/R/Origin-oriented routing.
- `references/visual-qa.md` — rendered-artifact review loop.
- `references/review-rubric.md` — hard gates + scored comparison.
- `references/manuscript-figure-audit.md` — captions, callouts, text-to-evidence, source linkage.
- `references/diagram-workflow.md` — editable conceptual figures.
- `references/figure-report-template.md` — reproducibility/report template.
- `references/taste-memory.md` — explicit project style memory.
- `references/inspiration-and-sources.md` — external Skills/projects whose best practices informed this workbench.

Scripts:

- `scripts/inspect_data.py` — inspect common scientific data files.
- `scripts/publication_style.py` — scoped Matplotlib publication defaults and exporters.
- `scripts/visual_qa.py` — basic rendered-layout and preview QA for Matplotlib.
- `scripts/preflight_figure.py` — inspect PDF/SVG/PNG metadata and delivery risks.
- `scripts/figure_contract.py` — initialize/validate a machine-readable Figure Contract.
- `scripts/smoke_render.py` — render synthetic examples and exercise QA/export path.
- `scripts/style_profile.py` — maintain project-local explicit style preferences.
- `scripts/install_skill.sh` — install into Codex, Claude Code, Cursor-compatible, or generic skill directories.
