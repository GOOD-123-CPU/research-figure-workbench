# Multi-panel Evidence Architecture

A multi-panel figure is a scientific argument, not a collage.

## Start from one Results-level question

Prefer one main question per figure. If panels support unrelated claims, split the figure unless the manuscript structure or venue strongly favors combination.

Map panels to distinct roles such as:

- **Context / overview** — what system, population, space, or trajectory is being examined?
- **Primary evidence** — which panel directly supports the main claim?
- **Distribution / heterogeneity** — how variable are observations or subgroups?
- **Mechanism / relationship** — what association, dependency, or process supports interpretation?
- **Robustness / sensitivity** — does the result persist under defensible alternatives?
- **Validation / agreement** — does a method agree with ground truth, benchmark, or independent measurement?
- **Failure / boundary case** — where does the claim stop applying?

Do not repeat the same numerical result as a bar, boxplot, and violin simply to fill panels.

## Layout archetypes

### Quantitative grid
Use when panels have comparable weight and similar geometry.

- Equal or intentionally related plot-area sizes.
- Shared axes/scales where the comparison requires them.
- Regular reading order.

### Schematic-led composite
Use when a method/system diagram provides necessary orientation and quantitative panels validate it.

- Schematic may be larger, but should not visually overwhelm the evidence.
- Match typography and panel labeling between schematic and plots.

### Image + quantification
Use for microscopy, imaging, spatial fields, specimen photographs, or similar evidence.

- Preserve original image data and processing provenance.
- Show scale bars and acquisition/processing information as required by the field/venue.
- Place quantitative validation near the image evidence it explains.

### Asymmetric mixed-modality
Use when one panel is genuinely denser or more central (e.g., overview heatmap or primary outcome) and supporting panels answer narrower questions.

Do not use asymmetry just to imitate a journal's visual style.

## Reading order

Arrange A -> B -> C in the same sequence as the manuscript's reasoning. A common pattern is:

1. orient;
2. show primary effect;
3. expose distribution/heterogeneity;
4. validate mechanism or agreement;
5. show robustness/boundaries.

This is a pattern, not a mandatory template.

## Cross-panel consistency

Keep consistent when semantics match:

- category order;
- colors, markers, and line styles;
- units and transformations;
- uncertainty definitions;
- diverging center/reference values;
- panel label position and typography.

Use a common color scale only when readers are expected to compare absolute color-mapped magnitudes across panels. Independent scales are acceptable when the comparison is within-panel; disclose that clearly.

## Alignment QA

At final size, inspect plot-area rectangles rather than only outer axes boxes.

- Comparable panels should align baselines and plotting regions.
- Repeated equal-grid panels should have visibly equal plot widths/heights unless the difference is intentional.
- Colorbars, legends, and insets should not create accidental misalignment of the data regions.
- Record intentional unequal spans in the Figure Contract rather than weakening all alignment checks.

Use `scripts/visual_qa.py` for basic geometry reporting, then visually inspect the rendered figure.
