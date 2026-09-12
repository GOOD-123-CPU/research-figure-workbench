# Publication Style Defaults

Use exact venue instructions first. These are neutral scientific-manuscript defaults, not compliance guarantees.

## Physical dimensions

- Start around 85-90 mm for single-column figures.
- Start around 175-185 mm for double-column figures.
- Choose height from evidence density; do not force every figure into the same aspect ratio.
- Preserve equal aspect when x and y represent the same quantity or spatial scale.
- Design at final physical size; downstream scaling should not be required to make text readable.

When a target venue is known, verify its exact live requirements using `journal-source-policy.md`.

## Typography

- Use one restrained type family or a compatible manuscript/journal family.
- About 8 pt is a useful neutral base at final size; venue guidance and content density override this.
- Keep tick labels, axis labels, legends, annotations, and panel labels readable after final-size rendering.
- Put the descriptive figure title in the manuscript caption by default. Panel tags A/B/C belong in the composite figure.
- Use correct mathematical notation, SI/field units, superscripts/subscripts, and Greek letters.
- Do not use tiny annotations to compensate for overcrowding; redesign the layout instead.

## Color semantics

### Qualitative groups

Default small-set Okabe-Ito/Wong sequence:

1. `#E69F00`
2. `#56B4E9`
3. `#009E73`
4. `#CC79A7`
5. `#D55E00`
6. `#F0E442`
7. `#0072B2`
8. `#000000`

Keep category-color mappings stable across related panels and manuscript figures. For many groups, use facets, direct labels, line styles, markers, grouping, or selective emphasis instead of an ever-longer color legend.

### Continuous values

Use a map whose perceptual structure matches meaning:

- sequential: viridis/cividis or equivalent perceptually ordered maps;
- diverging: only with a scientifically meaningful midpoint/reference;
- cyclic: for periodic variables;
- log/symlog normalization: only when ratio/signed-order-of-magnitude meaning justifies it.

Quantile/rank mappings are transformations; use only when ranks/balanced occupancy are the intended message and disclose them.

Avoid rainbow/jet for quantitative magnitude unless reproducing a required field convention and the accessibility tradeoff is explicit.

## Visual hierarchy

- Data marks should be stronger than grids and decorative frames.
- Model fits should not dominate the observations needed to judge them.
- One accent color may guide attention, but do not gray out evidence in a way that hides relevant groups.
- Remove chartjunk rather than removing scientific context.

## Legends and direct labels

- Match legend order to the visual/category order, not alphabetical order when a natural order exists.
- Prefer direct line-end/bar-end labels for a few series when it reduces lookup effort.
- Never let a legend cover important data.
- Share a legend across panels only when semantics truly match.

## Axes and scales

- Bars and filled magnitude areas normally need a meaningful zero baseline.
- Points/lines may use nonzero limits when scientifically appropriate; provide enough context to avoid exaggeration.
- Label log or transformed scales explicitly and state how zero/negative values were handled.
- Use shared scales across comparable panels when absolute comparison is part of the claim.
- Do not silently normalize each panel independently when cross-panel magnitude comparison matters.

## Uncertainty and statistics

- Name the interval: SD, SEM, CI, credible interval, percentile/bootstrap range, etc.
- State sample size and unit of replication when material.
- Preserve paired/repeated structure when it carries information.
- Do not use significance stars as the only statistical communication when effect size and interval information are available.
- Do not add inferential annotations without a defensible analysis.

## Dense data

For dense scatter/images:

- use alpha, density, hex/binning, aggregation, or layer rasterization;
- disclose any aggregation/binning/subsampling;
- do not delete rare/outlying observations simply to reduce clutter or file size;
- keep labels/axes/vector line art vector where practical.

## Multi-panel composition

- Use consistent panel labels and anchors.
- Align comparable plot regions, not only outer boxes.
- Keep color/category semantics stable.
- Reuse axes/legends only when doing so reduces redundancy without hiding meaning.
- Use asymmetry only when evidence roles justify it.

## Export

Default bundle:

- PDF — primary vector manuscript output;
- SVG — editable/interchange output;
- PNG — review/compatibility preview.

For raster-native content, use the target venue's required effective DPI at final physical size. Upsampling does not create new scientific detail.

For editable fonts:

- PDF/PS Type 42 generally preserves TrueType text better than Type 3 defaults in some workflows;
- SVG text can remain editable (`svg.fonttype="none"`) but depends on font availability;
- converting text to paths preserves appearance but loses searchable/editable text.

Use an explicit background unless transparency is required and reviewed in the intended manuscript background.
