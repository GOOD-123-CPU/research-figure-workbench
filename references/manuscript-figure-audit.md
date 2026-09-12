# Manuscript Figure Audit

Use this near submission or when reviewing a stable figure set.

## 1. Build an inventory first

For each figure/panel record:

- figure ID/number;
- exported file path;
- producing script or documented manual source;
- data source;
- caption location;
- first in-text callout;
- supplement/extended-data location if applicable;
- current QA status.

Do not list findings before establishing what actually exists.

## 2. Cross-reference checks

Verify:

- every in-text figure reference resolves;
- every delivered figure is called out in the manuscript;
- numbering and panel labels are unique and gap-free as required by the manuscript system;
- main-text and supplementary identifiers do not collide;
- panel references in prose match the correct panel.

## 3. Text-to-evidence consistency

For each substantive claim supported by a figure:

- identify the exact panel/series/quantity;
- verify direction and qualitative magnitude from source data when available;
- verify subgroup/denominator and uncertainty;
- check the prose does not overstate an imprecise/null estimate;
- confirm the plot and text use the same transformation, population, and model version.

Do not infer exact numerical values from an unlabeled image. If source data are unavailable, write:

`VISUAL READ ONLY — AUTHOR VERIFY`

## 4. Caption completeness

A caption should usually state enough to interpret the evidence without searching the body text:

- what is plotted;
- observational/sample unit and relevant N;
- units;
- panel meanings;
- uncertainty type;
- key transformation/normalization;
- relevant model/test and multiplicity correction when significance is shown;
- exclusions/subgroup restrictions that materially affect interpretation;
- abbreviation definitions.

Default manuscript data figures should not carry redundant descriptive titles inside the plotting area unless the venue specifically asks for them.

## 5. Reproducibility and source linkage

Check that each main result figure can be traced to:

- a script or documented reproducible software procedure;
- input/source data or a documented access restriction;
- environment/version information sufficient for replay;
- the final export dimensions and formats.

Manual Illustrator/Inkscape/Origin edits are not automatically forbidden, but every scientifically meaningful manual edit must be documented.

## 6. Output report

Use severity:

- **BLOCKING** — wrong/missing figure, contradicted claim, denominator/panel mismatch, unresolved reference, undisclosed scientifically meaningful manual change, non-reproducible main result.
- **RECOMMENDED** — incomplete caption, missing units/source link, accessibility issue, ambiguous uncertainty/statistics.
- **MINOR** — spacing, typography, non-substantive consistency.
- **AUTHOR VERIFY** — cannot establish from available source data/artifacts.

Suggested table:

```text
| Location | Figure/panel | Severity | Finding | Evidence | Repair |
```
