"""Task 1: standard-library-only descriptive statistics."""
import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from analysis_common import is_missing, parse_number, infer_type

def numeric_stats(values):
    nums = [parse_number(v) for v in values]
    nums = sorted(v for v in nums if v is not None and math.isfinite(v))
    n = len(nums)
    if not n:
        return {"count": 0, "mean": None, "min": None, "max": None,
                "std": None, "median": None}
    mean = sum(nums) / n
    variance = sum((v - mean)**2 for v in nums) / (n - 1) if n > 1 else None
    median = nums[n // 2] if n % 2 else (nums[n//2 - 1] + nums[n//2]) / 2
    return {"count": n, "mean": mean, "min": nums[0], "max": nums[-1],
            "std": math.sqrt(variance) if variance is not None else None,
            "median": median}

def categorical_stats(values):
    observed = [str(v).strip() for v in values if not is_missing(v)]
    counts = Counter(observed)
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return {"count": len(observed), "unique": len(counts),
            "mode": ranked[0][0] if ranked else None,
            "mode_frequency": ranked[0][1] if ranked else 0,
            "top_5": [{"value": v, "frequency": n} for v, n in ranked[:5]]}

def analyze(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        if len(set(columns)) != len(columns):
            raise ValueError("Duplicate column names: please fix the CSV header.")
        rows = list(reader)
    result = {"rows": len(rows), "columns": len(columns), "by_column": {}}
    for name in columns:
        values = [row.get(name) for row in rows]
        kind = infer_type(values, name)
        result["by_column"][name] = {
            "inferred_type": kind,
            "missing": sum(is_missing(v) for v in values),
            "stats": numeric_stats(values) if kind == "numeric" else categorical_stats(values)
        }
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", nargs="?", default="data/facebook_ads_2024.csv")
    parser.add_argument("--output", default="outputs/pure_python_results.json")
    args = parser.parse_args()
    result = analyze(args.csv_path)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nSaved {out}")

if __name__ == "__main__":
    main()
