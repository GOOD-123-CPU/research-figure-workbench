# Chart Selection for Research Figures

Choose the visual encoding from the scientific comparison, observational structure, and uncertainty—not from aesthetics or the available template gallery.

## Fast decision table

| Scientific task | Strong defaults | Use with care | Hard reject when |
|---|---|---|---|
| Trend over ordered x/time | line + points; line + interval band; small multiples | smoothed trend | x is nominal/unordered but connecting lines imply continuity |
| Compare independent groups | raw points + interval; box+jitter; violin+jitter; dot/interval | grouped bar | distribution/individual variation is central but hidden |
| Compare paired/repeated groups | paired points/lines; slopegraph; repeated-measures small multiples; model estimates | unpaired box/violin | pairing is discarded while within-unit change is the claim |
| Estimate/effect comparison | point + CI/credible interval; forest/coefficient plot | bar + error | interval meaning/denominator is undefined |
| Relationship between two numeric variables | scatter; regression scatter; hex/density | fitted curve | fit is shown without assumptions/raw support |
| Agreement of measurements | parity scatter + y=x; Bland-Altman | correlation alone | agreement is claimed only from correlation |
| Distribution | ECDF; histogram; box+jitter; violin+jitter; density | standalone violin/density | sample size or multimodality is concealed |
| Matrix/grid values | heatmap; clustered heatmap when clustering is scientifically justified | annotated heatmap | scale/normalization hides sign or meaningful zero |
| Many series | small multiples; highlighted focal series; direct labels | spaghetti plot | color-only distinction becomes unreadable |
| Ranking | dot/lollipop; sorted bar | radar | angle/area makes ranking hard to compare |
| Composition | stacked bar/area when total matters | pie/donut | precise category comparison is required |
| Spatial field | map/contour with perceptual scale | choropleth | polygon area is mistaken for observation weight |
| Spectrum/frequency | line; log axes when meaningful | filled area | smoothing hides narrow peaks without disclosure |
| Convergence/residual | line; semilog y for multiplicative decay | snapshots | iteration/order information is lost |
| Classification/model performance | ROC/PR where justified; calibration; confusion matrix; estimate intervals | single scalar bar | class balance/threshold behavior is hidden when it matters |
| Survival/time-to-event | Kaplan-Meier + at-risk table; model estimates | simple proportion bars | censoring/time information is discarded |

## Semantic checks before rendering

1. What is the observational unit?
2. Are observations independent, paired, repeated, nested, clustered, spatial, or temporal?
3. Which quantity is encoded by position, length, area, color, shape, opacity, and panel?
4. What zero/reference value is scientifically meaningful?
5. What exactly does uncertainty represent and what is the unit of replication?
6. What transformations were applied before plotting?
7. Are missing, censored, and excluded observations distinguishable?
8. Can all data be shown directly, or is density/binning/rasterization needed?

## Active interception

Do not blindly execute a requested chart when its geometry would mislead. Explain the issue and offer a valid alternative while respecting the user's final scientific decision.

Examples:

- mean bar hides a small or heterogeneous sample -> show raw observations + interval/summary;
- dual y-axis creates apparent correlation -> use aligned panels/shared x;
- nominal categories connected by lines -> use point/interval/bar as appropriate;
- radius used to encode magnitude -> encode area correctly or use position/length;
- rainbow map for continuous data -> use perceptually ordered sequential/diverging map;
- per-panel normalization destroys an intended cross-panel comparison -> use common normalization or clearly separate the claims.

Avoid universal thresholds such as “n < X means chart Y is forbidden.” The problem is whether the chosen summary hides scientifically relevant structure, not a magic sample-size cutoff.

## Candidate strategy

When several encodings are valid, render 2-4 candidates that make genuinely different scientific comparisons easy.

Example for repeated measurements:

- paired trajectories -> individual change;
- estimation interval -> group-level effect and uncertainty;
- subject-faceted trends -> heterogeneity over time.

Do not present three palettes of the same chart as meaningful candidates.
