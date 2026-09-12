#!/usr/bin/env python3
"""Create and validate a machine-readable scientific Figure Contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

TEMPLATE: dict[str, Any] = {
    "version": 1,
    "figure_id": "",
    "scientific_question_or_claim": "",
    "reader_comparison": "",
    "observational_unit": "",
    "dependence_structure": "independent",
    "data_sources": [],
    "missing_censored_excluded_handling": "",
    "transformations": [],
    "roles": {
        "x": "",
        "y": "",
        "group_color": "",
        "shape_linetype": "",
        "facet_panel": "",
        "uncertainty": "",
        "reference_baseline": "",
    },
    "archetype": "quantitative-grid",
    "panel_evidence_roles": {},
    "destination": {
        "medium": "manuscript",
        "venue": "UNVERIFIED",
        "article_type": "UNVERIFIED",
        "submission_phase": "UNVERIFIED",
        "final_width_mm": None,
        "final_height_mm": None,
    },
    "backend": "python-matplotlib",
    "required_outputs": ["pdf", "svg", "png", "source", "report"],
    "scientific_risks": [],
    "reviewer_misreading_risks": [],
    "unverified_assumptions": [],
}

REQUIRED_NONEMPTY = (
    "scientific_question_or_claim",
    "reader_comparison",
    "observational_unit",
)

ALLOWED_STRUCTURES = {
    "independent",
    "paired",
    "repeated",
    "nested",
    "clustered",
    "spatial",
    "temporal",
    "aggregated",
    "other",
}

ALLOWED_ARCHETYPES = {
    "quantitative-grid",
    "schematic-led",
    "image-plus-quant",
    "asymmetric-mixed",
}


def validate(contract: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    for key in REQUIRED_NONEMPTY:
        if not str(contract.get(key, "")).strip():
            problems.append(f"missing required field: {key}")

    structure = str(contract.get("dependence_structure", ""))
    if structure not in ALLOWED_STRUCTURES:
        problems.append(
            "dependence_structure must be one of: " + ", ".join(sorted(ALLOWED_STRUCTURES))
        )

    archetype = str(contract.get("archetype", ""))
    if archetype not in ALLOWED_ARCHETYPES:
        problems.append("archetype must be one of: " + ", ".join(sorted(ALLOWED_ARCHETYPES)))

    roles = contract.get("roles")
    if not isinstance(roles, dict):
        problems.append("roles must be an object")
    elif not str(roles.get("y", "")).strip():
        problems.append("roles.y is empty; record the primary measured/derived quantity")

    destination = contract.get("destination")
    if not isinstance(destination, dict):
        problems.append("destination must be an object")

    outputs = contract.get("required_outputs")
    if not isinstance(outputs, list) or not outputs:
        problems.append("required_outputs must be a non-empty list")

    return problems


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--init", metavar="PATH")
    mode.add_argument("--validate", metavar="PATH")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.init:
        path = Path(args.init)
        if path.exists() and not args.force:
            raise SystemExit(f"Refusing to overwrite existing file: {path} (use --force)")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(TEMPLATE, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(path)
        return

    path = Path(args.validate)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    problems = validate(payload)
    result = {"path": str(path), "valid": not problems, "problems": problems}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if problems:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
