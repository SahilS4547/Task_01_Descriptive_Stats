"""Check that the two independently computed outputs agree."""
import json
import math
from pathlib import Path

pure = json.loads(Path("outputs/pure_python_results.json").read_text())
pandas = json.loads(Path("outputs/pandas_results.json").read_text())
issues = []
for field in ("rows", "columns"):
    if pure[field] != pandas[field]:
        issues.append(f"{field}: {pure[field]} vs {pandas[field]}")
if set(pure["by_column"]) != set(pandas["by_column"]):
    issues.append("Column names differ")
for name in pure["by_column"]:
    if name not in pandas["by_column"]:
        continue
    a, b = pure["by_column"][name], pandas["by_column"][name]
    for field in ("inferred_type", "missing"):
        if a[field] != b[field]:
            issues.append(f"{name}.{field}: {a[field]} vs {b[field]}")
    for key, v in a["stats"].items():
        w = b["stats"].get(key)
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if w is None or not math.isclose(v, w, rel_tol=1e-9, abs_tol=1e-9):
                issues.append(f"{name}.{key}: {v} vs {w}")
        elif v != w:
            issues.append(f"{name}.{key}: {v} vs {w}")
print("PASS: Both approaches agree." if not issues else "FAIL:\n" + "\n".join(issues))
if issues:
    raise SystemExit(1)
