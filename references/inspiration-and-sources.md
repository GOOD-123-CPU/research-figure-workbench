# Inspiration and Sources

This Workbench is an original synthesis. The following public projects were reviewed for workflow ideas; rules were re-written and filtered for scientific defensibility rather than copied wholesale. Access date for this synthesis: 2026-09-12.

## High-value workflow sources

- **K-Dense-AI/scientific-agent-skills — scientific-visualization**  
  https://github.com/K-Dense-AI/scientific-agent-skills  
  Adopted ideas: scientific-integrity guardrails, missing-data/normalization disclosure, scoped styles, explicit provenance, publisher-stage verification, artifact-level metadata inspection, distinction between accessibility screening and certification.

- **Yuan1z0825/nature-skills — nature-figure**  
  https://github.com/Yuan1z0825/nature-skills  
  Adopted ideas: Figure Contract, panel evidence roles, backend routing, final physical-size QA, strong separation between core workflow and on-demand references. Venue-specific claims are not treated as official unless independently verified.

- **ChenLiu-1996/figures4papers — scientific-figure-making**  
  https://github.com/ChenLiu-1996/figures4papers  
  Adopted ideas: reusable publication patterns, real-code exemplars, compact progressive-loading structure, vector-first Matplotlib production style. Published figure geometry is never traced or copied literally.

- **Haojae/scipilot-figure-skill**  
  https://github.com/Haojae/scipilot-figure-skill  
  Adopted ideas: think before plotting, data profiling, active interception of misleading chart requests, rendered preview + programmatic + perceptual review loop.

- **scdenney/open-science-skills — figures / figure-table-audit**  
  https://github.com/scdenney/open-science-skills  
  Adopted ideas: one-sentence comparison, self-contained captions, legend order matching visual order, end-stage inventory, text-to-evidence audit, `VISUAL READ ONLY — AUTHOR VERIFY` when values cannot be established from source data.

- **anthropics/knowledge-work-plugins — data-visualization**  
  https://github.com/anthropics/knowledge-work-plugins  
  Adopted ideas: broad chart-selection heuristics, visual economy, purposeful color, small multiples, accessibility fallbacks. Generic presentation-oriented title advice is not applied to manuscript figures by default.

- **XiaoMaColtAI/math-modeling-skill — tools/figure**  
  https://github.com/XiaoMaColtAI/math-modeling-skill  
  Adopted ideas: Python/MATLAB routing, data profiling, QA gates, Chinese-language research-figure practicality. Competition-specific fixed figure counts and forced chart diversity were intentionally not adopted.

- **guhou-hvi/elsevier-figure-style**  
  https://github.com/guhou-hvi/elsevier-figure-style  
  Adopted ideas: evidence-classed rules, stage-aware publisher checks, rule provenance, static/metadata/visual QA separation, explicit `UNVERIFIED` handling. The project is unofficial and is not used as a substitute for live Elsevier/journal guidance.

- **TingxiYu/academic-figure-skill**  
  https://github.com/TingxiYu/academic-figure-skill  
  Adopted ideas: question-first workflow, Figure Contract, archetype-aware composition, data-integrity emphasis, runtime-aware backend handling, rendered QA loop. Fixed signal thresholds, forced confirmation gates, and style mimicry were not adopted.

- **youngminsw/Origin-Pro-MCP**  
  https://github.com/youngminsw/Origin-Pro-MCP  
  Adopted idea: treat Origin as a reproducible software backend when it is already the laboratory workflow, rather than converting everything to Python solely for aesthetics.

## Deliberately rejected patterns

- hard-coded sample-size thresholds presented as universal scientific laws;
- refusing to visualize weak, negative, or non-significant results;
- forcing a hero panel because a target journal often uses asymmetric layouts;
- forcing a minimum number/diversity of chart types;
- treating a grayscale preview as complete color-vision accessibility validation;
- claiming publisher compliance from DPI/format checks alone;
- copying published figure layouts or styling so literally that the output becomes derivative;
- adding significance stars without a defensible analysis and unit of replication;
- using generative imagery as quantitative evidence.
