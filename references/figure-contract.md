# Figure Contract

Complete this before publication-facing plotting. Keep it short enough to review before every major revision.

## Required fields

```text
Figure ID:
Scientific question / one-sentence claim:
Reader comparison to notice first:
Observational unit:
Structure: independent | paired | repeated | nested | spatial | temporal | aggregated | other
Data source(s):
Data exclusions / missing / censored handling:
Transformations already applied:

x:
y:
group/color:
shape/linetype:
facet/panel:
uncertainty:
reference/zero/baseline:

Figure archetype: quantitative-grid | schematic-led | image-plus-quant | asymmetric-mixed
Panel evidence roles:
  A:
  B:
  C:

Target medium:
Target venue/article type/submission phase:
Final physical size:
Backend:
Required outputs:

Primary scientific risk:
Primary reviewer-misreading risk:
Unverified assumptions:
```

## Rules

- The claim may be exploratory ("show the distribution") or confirmatory; do not force a positive result.
- Write the observational unit before computing uncertainty. Subjects, technical replicates, pixels, wells, repeated time points, and model seeds are not interchangeable.
- State missing/censored/excluded handling before plotting. Missing is not zero.
- Declare transformations before evaluating visual impact. Do not choose log/normalization/smoothing after seeing which version looks stronger unless the exploratory comparison is explicitly disclosed.
- For multi-panel figures, each panel needs an evidence role. Delete or move a panel if it adds no distinct evidence.
- Do not force an asymmetric hero layout. Use it only when one panel has genuinely greater evidentiary centrality or information density.
- If the target journal is unknown, set publisher fields to `UNVERIFIED` and use general defaults.

## Machine-readable companion

Use `scripts/figure_contract.py --init <path.json>` to create a JSON version. Keep it beside the plotting script or under `.research-figure/contracts/`.
