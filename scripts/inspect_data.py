#!/usr/bin/env python3
"""Inspect common research data files and emit a compact, figure-oriented schema report."""

from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import Counter
from pathlib import Path
from typing import Any

TIME_NAME_TOKENS = {"time", "date", "day", "week", "month", "year", "hour", "minute", "second", "epoch"}
ID_NAME_TOKENS = {"id", "subject", "participant", "sample", "specimen", "patient", "animal", "trial", "run", "seed"}
GROUP_NAME_TOKENS = {"group", "condition", "treatment", "arm", "cohort", "class", "category", "sex", "gender"}


def _safe_number(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        try:
            out = float(value)
            return out if math.isfinite(out) else None
        except Exception:
            return None
    text = str(value).strip()
    if not text:
        return None
    try:
        out = float(text)
        return out if math.isfinite(out) else None
    except Exception:
        return None


def _percentile(sorted_values: list[float], q: float) -> float:
    if not sorted_values:
        return math.nan
    if len(sorted_values) == 1:
        return sorted_values[0]
    pos = (len(sorted_values) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return sorted_values[lo]
    frac = pos - lo
    return sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac


def _skew(values: list[float]) -> float | None:
    n = len(values)
    if n < 3:
        return None
    mean = statistics.fmean(values)
    m2 = statistics.fmean([(x - mean) ** 2 for x in values])
    if m2 <= 0:
        return 0.0
    m3 = statistics.fmean([(x - mean) ** 3 for x in values])
    return m3 / (m2 ** 1.5)


def _name_tokens(name: str) -> set[str]:
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in name)
    return set(cleaned.split())


def _summarize_rows(columns: list[str], rows: list[list[Any]]) -> dict[str, Any]:
    n_rows = len(rows)
    result: dict[str, Any] = {
        "rows": n_rows,
        "columns": len(columns),
        "duplicate_rows": 0,
        "fields": [],
        "warnings": [],
    }

    row_keys = [tuple("" if v is None else str(v) for v in row) for row in rows]
    if row_keys:
        counts = Counter(row_keys)
        result["duplicate_rows"] = sum(count - 1 for count in counts.values() if count > 1)

    for idx, name in enumerate(columns):
        values = [row[idx] if idx < len(row) else None for row in rows]
        nonmissing = [v for v in values if v is not None and str(v).strip() != ""]
        missing = n_rows - len(nonmissing)
        numeric = [_safe_number(v) for v in nonmissing]
        finite = [v for v in numeric if v is not None]
        numeric_fraction = len(finite) / max(1, len(nonmissing))
        unique_values = {str(v) for v in nonmissing}
        unique = len(unique_values)
        unique_fraction = unique / max(1, len(nonmissing))
        tokens = _name_tokens(str(name))

        field: dict[str, Any] = {
            "name": str(name),
            "missing": missing,
            "missing_fraction": round(missing / max(1, n_rows), 4),
            "unique": unique,
            "unique_fraction": round(unique_fraction, 4),
            "numeric_fraction": round(numeric_fraction, 4),
            "hints": [],
        }

        if finite and numeric_fraction >= 0.9:
            ordered = sorted(finite)
            q1 = _percentile(ordered, 0.25)
            median = _percentile(ordered, 0.50)
            q3 = _percentile(ordered, 0.75)
            iqr = q3 - q1
            lo = q1 - 1.5 * iqr
            hi = q3 + 1.5 * iqr
            outliers = sum(1 for x in finite if x < lo or x > hi) if iqr > 0 else 0
            field.update(
                {
                    "kind": "numeric",
                    "n_finite": len(finite),
                    "min": min(finite),
                    "q1": q1,
                    "median": median,
                    "q3": q3,
                    "max": max(finite),
                    "mean": statistics.fmean(finite),
                    "std": statistics.stdev(finite) if len(finite) > 1 else 0.0,
                    "skew_moment": _skew(finite),
                    "iqr_outlier_count": outliers,
                    "constant": min(finite) == max(finite),
                }
            )
        else:
            field["kind"] = "categorical_or_text"
            counts = Counter(str(v) for v in nonmissing)
            field["top_values"] = [
                {"value": value, "count": count} for value, count in counts.most_common(8)
            ]
            field["sample"] = [str(v) for v in nonmissing[:5]]

        if tokens & TIME_NAME_TOKENS:
            field["hints"].append("time_or_order_candidate")
        if tokens & ID_NAME_TOKENS or (unique_fraction > 0.95 and len(nonmissing) >= 10):
            field["hints"].append("identifier_or_observational_unit_candidate")
        if tokens & GROUP_NAME_TOKENS or (
            field["kind"] != "numeric"
            and 1 < unique <= 12
            and not (tokens & ID_NAME_TOKENS)
        ):
            field["hints"].append("grouping_candidate")
        if (
            field["kind"] == "numeric"
            and unique <= 12
            and len(nonmissing) > unique * 2
            and not (tokens & TIME_NAME_TOKENS)
            and not (tokens & ID_NAME_TOKENS)
        ):
            field["hints"].append("numeric_coded_category_candidate")

        result["fields"].append(field)

    if result["duplicate_rows"]:
        result["warnings"].append(f"{result['duplicate_rows']} duplicate row(s) detected")
    if any(f.get("missing_fraction", 0) > 0.2 for f in result["fields"]):
        result["warnings"].append("at least one field has >20% missing values; inspect missing-data semantics")
    if any(f.get("kind") == "numeric" and f.get("constant") for f in result["fields"]):
        result["warnings"].append("one or more numeric fields are constant")

    return result


def _read_delimited(path: Path, delimiter: str) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle, delimiter=delimiter))
    if not rows:
        return {"rows": 0, "columns": 0, "duplicate_rows": 0, "fields": [], "warnings": []}
    return _summarize_rows([str(c) for c in rows[0]], rows[1:])


def _read_excel(path: Path) -> dict[str, Any]:
    import pandas as pd

    df = pd.read_excel(path)
    columns = [str(c) for c in df.columns]
    rows = df.where(df.notna(), None).values.tolist()
    report = _summarize_rows(columns, rows)
    report["sheet"] = "first/default sheet"
    return report


def _array_summary(arr) -> dict[str, Any]:
    import numpy as np

    payload: dict[str, Any] = {
        "shape": list(arr.shape),
        "dtype": str(arr.dtype),
        "size": int(arr.size),
    }
    if np.issubdtype(arr.dtype, np.number) and arr.size:
        finite = arr[np.isfinite(arr)]
        payload["finite_count"] = int(finite.size)
        payload["missing_or_nonfinite"] = int(arr.size - finite.size)
        if finite.size:
            payload["min"] = float(np.min(finite))
            payload["max"] = float(np.max(finite))
            payload["mean"] = float(np.mean(finite))
            payload["median"] = float(np.median(finite))
    return payload


def _read_numpy(path: Path) -> dict[str, Any]:
    import numpy as np

    data = np.load(path, allow_pickle=False)
    if isinstance(data, np.lib.npyio.NpzFile):
        return {"arrays": {key: _array_summary(data[key]) for key in data.files}}
    return _array_summary(data)


def _read_mat(path: Path) -> dict[str, Any]:
    from scipy.io import whosmat

    variables = []
    for name, shape, cls in whosmat(path):
        if name.startswith("__"):
            continue
        variables.append({"name": name, "shape": list(shape), "class": cls})
    return {
        "variables": variables,
        "warning": "MAT inspection lists candidates only; select variables from scientific context rather than guessing.",
    }


def _figure_hints(report: dict[str, Any]) -> list[str]:
    fields = report.get("fields", [])
    numeric = [f for f in fields if f.get("kind") == "numeric"]
    grouping = [f for f in fields if "grouping_candidate" in f.get("hints", [])]
    time_like = [f for f in fields if "time_or_order_candidate" in f.get("hints", [])]
    id_like = [f for f in fields if "identifier_or_observational_unit_candidate" in f.get("hints", [])]
    hints: list[str] = []
    if len(numeric) == 1 and grouping:
        hints.append("group distribution/comparison candidate; preserve raw observations when informative")
    if len(numeric) >= 2:
        hints.append("numeric relationship candidate; check whether columns share the same observational unit")
    if numeric and time_like:
        hints.append("ordered/time trend candidate; verify repeated-measures structure before connecting points")
    if id_like and grouping and numeric:
        hints.append("paired/repeated/nested structure may be present; inspect identifiers before group summaries")
    if len(numeric) >= 3:
        hints.append("multivariate/heatmap/small-multiple candidate; choose from the scientific question, not column count alone")
    return hints or ["manual semantic review required before chart selection"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--json", dest="json_path")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")

    suffix = path.suffix.lower()
    report: dict[str, Any] = {"path": str(path), "suffix": suffix}
    try:
        if suffix == ".csv":
            payload = _read_delimited(path, ",")
        elif suffix == ".tsv":
            payload = _read_delimited(path, "\t")
        elif suffix in {".xlsx", ".xls"}:
            payload = _read_excel(path)
        elif suffix in {".npy", ".npz"}:
            payload = _read_numpy(path)
        elif suffix == ".mat":
            payload = _read_mat(path)
        else:
            raise SystemExit("Supported: .csv, .tsv, .xlsx, .xls, .npy, .npz, .mat")
    except ImportError as exc:
        raise SystemExit(f"Optional dependency missing for {suffix}: {exc}") from exc

    report.update(payload)
    if "fields" in report:
        report["figure_task_hints"] = _figure_hints(report)

    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.json_path:
        out = Path(args.json_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
