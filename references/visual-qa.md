# Rendered Figure QA

Review the exported artifact, not only the plotting code.

## Pass 1 — Scientific semantics

Check:

- axes and encodings correspond to the intended variables;
- pairing/repeated/nested structure is preserved;
- missing/censored/excluded observations are represented or disclosed correctly;
- uncertainty has the intended definition and unit of replication;
- model fits or smooths are not mistaken for observations;
- transformations/normalization are visible or documented.

A semantic failure blocks delivery regardless of visual quality.

## Pass 2 — Scale and statistical honesty

Check:

- bar/area baselines are meaningful;
- nonzero limits on points/lines do not exaggerate a conclusion;
- log/symlog/normalized axes are labeled and scientifically meaningful;
- diverging color maps have a meaningful center;
- compared panels do not use incompatible hidden normalization;
- p-values/significance markers match the actual analysis and correction;
- negative/null/weak findings are not visually suppressed.

## Pass 3 — Final-size visual inspection

Inspect at the intended physical size, ideally in the manuscript context.

Look for:

- clipped text, panel labels, legends, annotations, or colorbars;
- tick-label collisions or unreadable rotation;
- line/marker weights too weak at print size;
- legends covering data;
- inconsistent panel-label anchors;
- misaligned comparable plot regions;
- excessive white space or crowding;
- over-dominant grids, fits, or annotations relative to the data;
- labels too vague to stand without surrounding prose.

Use `scripts/visual_qa.py` as a deterministic screen, not as a substitute for inspection.

## Pass 4 — Accessibility

Check that the comparison survives when color information is weakened.

- Use redundant line style, marker, hatch, direct label, or panel separation.
- Avoid red/green-only distinctions.
- Use perceptually appropriate sequential/diverging/cyclic maps.
- A grayscale preview is useful screening but does not certify color-vision accessibility.
- For web/accessibility workflows, provide alt text and a data/table alternative where appropriate.

## Pass 5 — Production artifact

Check the exported file itself:

- physical page/figure dimensions;
- raster pixel dimensions and effective DPI at final size;
- vector text/editability expectations;
- font resources/embedding where inspectable;
- transparency/background assumptions;
- file not empty/corrupt;
- dense layers rasterized only when intended.

Run `scripts/preflight_figure.py` for supported formats.

## Repair loop

For each finding, record:

```text
Severity: BLOCKING | RECOMMENDED | MINOR | AUTHOR VERIFY
Evidence:
Repair:
Scientific meaning changed? yes/no
Re-render required? yes/no
```

After any material repair to data geometry, scales, labels, fonts, legend, annotations, panel size, or layout, re-render and repeat the relevant passes.
