#!/usr/bin/env python3
"""Maintain project-local publication figure taste memory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_PROFILE: dict[str, Any] = {
    "version": 1,
    "defaults": {
        "single_column_width_mm": 85,
        "double_column_width_mm": 180,
        "base_font_pt": 8,
        "qualitative_palette": "wong",
        "continuous_colormap": "viridis",
        "outputs": ["pdf", "svg", "png"],
    },
    "liked_traits": [],
    "rejected_traits": [],
    "notes": [],
}


def load_profile(path: Path) -> dict[str, Any]:
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_PROFILE))
    return json.loads(path.read_text(encoding="utf-8"))


def save_profile(path: Path, profile: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def add_unique(profile: dict[str, Any], field: str, value: str) -> None:
    items = profile.setdefault(field, [])
    if value not in items:
        items.append(value)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", default=".research-figure/style-profile.json")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--init", action="store_true")
    group.add_argument("--show", action="store_true")
    group.add_argument("--like")
    group.add_argument("--reject")
    group.add_argument("--note")
    args = parser.parse_args()

    path = Path(args.profile)
    profile = load_profile(path)
    if args.init:
        save_profile(path, profile)
    elif args.like:
        add_unique(profile, "liked_traits", args.like)
        save_profile(path, profile)
    elif args.reject:
        add_unique(profile, "rejected_traits", args.reject)
        save_profile(path, profile)
    elif args.note:
        add_unique(profile, "notes", args.note)
        save_profile(path, profile)

    print(json.dumps(profile, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
