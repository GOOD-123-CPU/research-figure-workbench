# Research Figure Workbench

Research Figure Workbench is a Codex skill for building, revising, auditing, and exporting research-paper figures with scientific integrity as the default.

It is designed for data figures, multi-panel manuscript figures, method diagrams, thesis figures, journal-ready exports, and pre-submission figure QA. The skill favors reproducible scripts, source-data traceability, explicit uncertainty, final-size rendering checks, and editable vector outputs over cosmetic-only polishing.

## Why This Exists

Scientific figures are easy to make attractive and surprisingly easy to make misleading. This workbench gives an AI coding agent a disciplined figure-production workflow:

- clarify the scientific claim before choosing a chart;
- inspect the data before plotting;
- preserve observational units, pairing, missingness, transformations, exclusions, and uncertainty definitions;
- route to Python, MATLAB, R, Origin-oriented workflows, or editable diagrams based on the project context;
- export manuscript-friendly PDF/SVG/PNG deliverables;
- run metadata and layout preflight checks;
- separate verified publisher requirements from unverified style assumptions.

The goal is not to imitate a journal aesthetic. The goal is to help produce figures that are honest, readable, reproducible, and ready for serious review.

## What It Handles

- CSV, Excel, MAT, NPY, and NPZ data inspection workflows
- Python/Matplotlib publication-style plotting
- multi-panel evidence layout planning
- method and conceptual diagram workflows
- graphical abstract and schematic routing guidance
- caption and manuscript-figure audits
- final-size legibility checks
- PDF, SVG, and PNG export preflight
- journal/conference figure-rule verification discipline
- explicit project style memory for stated user preferences

## What It Will Not Do

- invent or hide data to make a figure look stronger;
- add significance stars without a defensible analysis;
- treat remembered journal rules as current official policy;
- use generative images as quantitative scientific evidence;
- claim publisher compliance from file format alone;
- silently change scales, normalization, exclusions, or uncertainty definitions.

## Repository Layout

```text
.
|-- SKILL.md
|-- README.md
|-- LICENSE
|-- agents/
|   `-- openai.yaml
|-- assets/
|   `-- icon.svg
|-- references/
|   |-- backend-routing.md
|   |-- chart-selection.md
|   |-- diagram-workflow.md
|   |-- evidence-architecture.md
|   |-- figure-contract.md
|   |-- figure-report-template.md
|   |-- inspiration-and-sources.md
|   |-- journal-source-policy.md
|   |-- manuscript-figure-audit.md
|   |-- publication-style.md
|   |-- review-rubric.md
|   |-- taste-memory.md
|   `-- visual-qa.md
`-- scripts/
    |-- figure_contract.py
    |-- inspect_data.py
    |-- install_skill.sh
    |-- preflight_figure.py
    |-- publication_style.py
    |-- smoke_render.py
    |-- style_profile.py
    `-- visual_qa.py
```

## Requirements

Python 3.10+ is recommended.

Most scripts use the Python standard library. The full helper-tool workflow can also use:

- `matplotlib`
- `numpy`
- `openpyxl`
- `pandas`
- `Pillow`
- `pypdf`
- `scipy`

Install them with:

```bash
python -m pip install -r requirements.txt
```

## Quick Start

Clone the repository:

```bash
git clone https://github.com/GOOD-123-CPU/research-figure-workbench.git
cd research-figure-workbench
```

Install the skill into Codex:

```bash
bash scripts/install_skill.sh --target codex
```

The installer copies this folder into the target skills directory. If a skill folder with the same name already exists there, it is replaced.

Supported install targets:

- `codex`
- `claude-code`
- `cursor`
- `dir --path /path/to/skills`

## Verify The Toolchain

Run the synthetic smoke render:

```bash
python scripts/smoke_render.py --out /tmp/research-figure-workbench-smoke
```

Preflight the generated outputs:

```bash
python scripts/preflight_figure.py /tmp/research-figure-workbench-smoke/smoke_figure.pdf --strict
python scripts/preflight_figure.py /tmp/research-figure-workbench-smoke/smoke_figure.svg --strict
python scripts/preflight_figure.py /tmp/research-figure-workbench-smoke/smoke_figure.png --strict --min-dpi 300
```

On Windows PowerShell:

```powershell
$out = Join-Path $env:TEMP "research-figure-workbench-smoke"
python scripts\smoke_render.py --out $out
python scripts\preflight_figure.py "$out\smoke_figure.pdf" --strict
python scripts\preflight_figure.py "$out\smoke_figure.svg" --strict
python scripts\preflight_figure.py "$out\smoke_figure.png" --strict --min-dpi 300
```

## Useful Scripts

Create or validate a machine-readable figure contract:

```bash
python scripts/figure_contract.py --init figure-contract.json
python scripts/figure_contract.py --validate figure-contract.json
```

Inspect a data file before plotting:

```bash
python scripts/inspect_data.py data.csv --json data-profile.json
```

Preflight an exported figure:

```bash
python scripts/preflight_figure.py figure.pdf --strict
python scripts/preflight_figure.py figure.svg --strict
python scripts/preflight_figure.py figure.png --strict --min-dpi 300
```

## Workflow Summary

Research Figure Workbench routes figure requests through a compact but strict sequence:

1. Define the figure contract: claim, comparison, unit of observation, visual roles, backend, target medium, and deliverables.
2. Inspect the data before plotting.
3. Choose a chart based on the scientific comparison rather than decoration.
4. Use consistent evidence roles for multi-panel figures.
5. Verify journal or conference requirements from current official sources when compliance matters.
6. Render at final physical size.
7. Export PDF/SVG/PNG plus source code and a concise report.
8. Run file-level and layout QA.
9. Inspect the final rendered artifact before calling it publication-ready.

## Design Principles

- Scientific truth first.
- Reproducibility over manual edits.
- Explicit uncertainty over visual implication.
- Editable vector outputs when possible.
- Accessibility by design, not as a last-minute filter.
- Publisher rules must be sourced, current, and clearly distinguished from best practice.

## Acknowledgements

This workbench is an original synthesis. Public projects and skill repositories that informed its workflow are listed in `references/inspiration-and-sources.md`.

## License

Released under the MIT License. See `LICENSE` for details.
