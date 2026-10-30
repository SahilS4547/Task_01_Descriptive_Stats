"""Task 1: Pandas replication using the same explicit parsing rules."""
import argparse
import json
import math
from pathlib import Path
import pandas as pd
from analysis_common import is_missing, parse_number, infer_type

def analyze(path):
    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    if not df.columns.is_unique:
        raise ValueError("Duplicate column names: please fix the CSV header.")
    print("Dataset shape:", df.shape)
    print("\nOriginal text dtypes:\n", df.dtypes.to_string())
    print("\nDataFrame.info():")
    df.info()
    result = {"rows": int(len(df)), "columns": int(len(df.columns)), "by_column": {}}
    for name in df.columns:
        values = df[name].tolist()
        kind = infer_type(values, name)
        missing = sum(is_missing(v) for v in values)
        if kind == "numeric":
            s = pd.Series([parse_number(v) for v in values], dtype="float64").dropna()
            s = s[s.map(math.isfinite)]
            desc = s.describe()
            stats = {"count": int(s.count()),
                     "mean": float(s.mean()) if len(s) else None,
                     "min": float(s.min()) if len(s) else None,
                     "max": float(s.max()) if len(s) else None,
                     "std": float(s.std(ddof=1)) if len(s) > 1 else None,
                     "median": float(s.median()) if len(s) else None}
            print(f"\n{name} (numeric):\n{desc}")
        else:
            s = pd.Series([str(v).strip() for v in values if not is_missing(v)], dtype="string")
            counts = s.value_counts(dropna=True)
            ranked = sorted(((str(k), int(v)) for k, v in counts.items()),
                            key=lambda pair: (-pair[1], pair[0]))
            stats = {"count": int(s.count()), "unique": int(s.nunique()),
                     "mode": ranked[0][0] if ranked else None,
                     "mode_frequency": ranked[0][1] if ranked else 0,
                     "top_5": [{"value": v, "frequency": n} for v, n in ranked[:5]]}
            if len(s):
                print(f"\n{name} (categorical/date):\n{s.describe()}")
                print("Top 5:\n", counts.head(5))
        result["by_column"][name] = {
            "inferred_type": kind, "missing": missing,
            "missing_percent": round(missing * 100 / len(df), 4) if len(df) else 0,
            "stats": stats
        }
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", nargs="?", default="data/facebook_ads_2024.csv")
    parser.add_argument("--output", default="outputs/pandas_results.json")
    args = parser.parse_args()
    result = analyze(args.csv_path)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"\nSaved {out}")

if __name__ == "__main__":
    main()
