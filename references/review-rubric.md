# Figure Review Rubric

Review the rendered artifact at intended physical size. Code review alone is insufficient.

## Hard gates

Any failure blocks delivery until fixed or explicitly marked unresolved.

- **Semantic validity** — encoding matches the real data roles and observational structure.
- **Data integrity** — no undisclosed omission, clipping, transformation, smoothing, normalization, binning, aggregation, or image alteration changes the apparent result.
- **Uncertainty/statistical validity** — intervals/tests correspond to the intended estimand and unit of replication.
- **Scale honesty** — baselines, limits, area/radius, color normalization, and shared scales do not manufacture a comparison.
- **Reproducibility** — the figure can be regenerated from source data and runnable code or a documented reproducible software procedure.
- **Artifact verification** — the delivered file exists, is non-empty, and has been inspected rather than assumed correct from the export call.

## Scored dimensions

Score 0-2 after hard gates pass.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Claim support | comparison is obscure/misaligned | readable with effort | intended comparison is immediate |
| Legibility | unreadable at final size | mostly readable | clear at final size |
| Accessibility | depends on fragile color/encoding | partly redundant | robust redundant encoding where practical |
| Visual economy | clutter or decorative emphasis | some redundancy | evidence hierarchy is clear and restrained |
| Cross-panel coherence | inconsistent semantics/scales | minor inconsistency | coherent scales, labels, order, and evidence flow |
| Caption/context readiness | cannot stand alone | minor missing context | units/sample/uncertainty/panels are self-contained |
| Reproducible delivery | source/provenance missing | source present, notes incomplete | source + outputs + contract/report are complete |

A strong final figure normally scores at least 12/14, but score never overrides hard-gate failures.

## Review order

1. Read the Figure Contract.
2. Inspect at intended physical size.
3. Validate semantics and observational structure.
4. Validate missing/excluded data and transformations.
5. Validate uncertainty/statistics.
6. Validate axes, baselines, normalization, and comparison scales.
7. Inspect labels, units, legends, panel ordering/alignment, and accessibility.
8. Inspect export metadata/editability.
9. Record repairs and re-render.

## Finding severity

- **BLOCKING** — changes scientific meaning, makes the evidence misleading, breaks reproducibility, or produces an unusable artifact.
- **RECOMMENDED** — materially improves interpretation, accessibility, caption completeness, or publication robustness.
- **MINOR** — cosmetic consistency/spacing only.
- **AUTHOR VERIFY** — available artifacts cannot establish the answer.

## Repair boundaries

Allowed repairs include typography, spacing, legend placement/order, line/marker weight, redundant encoding, panel ordering, final dimensions, and scientifically defensible scale choices.

Never “repair” by deleting inconvenient observations, redefining groups, moving data points, changing model output, or choosing a transformation solely because it makes the conclusion stronger.

## Review record

Recommended JSON shape:

```json
{
  "selected_candidate": "candidate-02",
  "verdict": "accept|repair|reject|author_verify",
  "hard_gates": {
    "semantic_validity": true,
    "data_integrity": true,
    "statistical_validity": true,
    "scale_honesty": true,
    "reproducibility": true,
    "artifact_verification": true
  },
  "scores": {
    "claim_support": 2,
    "legibility": 2,
    "accessibility": 2,
    "visual_economy": 2,
    "cross_panel_coherence": 2,
    "caption_context_readiness": 2,
    "reproducible_delivery": 2
  },
  "findings": [
    {"severity": "RECOMMENDED", "evidence": "...", "repair": "..."}
  ]
}
```
