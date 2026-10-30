# Research Task 1 — Descriptive Statistics With and Without Pandas

## Purpose
Analyze the **2024 Facebook Political Ads** dataset using independent standard-library Python and Pandas implementations, then validate agreement. This project reports descriptive patterns only; it does not infer voter intent or causal effects.

## Dataset
**Source:** The Google Drive dataset titled *2024 Facebook Political Ads*, supplied in the course assignment. The assignment does not contain a direct download URL; insert the authorized dataset link here after obtaining it: **Course-provided Google Drive file: `fb_ads_president_scored_anon.zip` (add the instructor-provided share URL if available)**.

**Do not commit the dataset.** Download the source CSV and save it locally at `data/facebook_ads_2024.csv`. If your download is Excel, export the worksheet as UTF-8 CSV first.

## Requirements
- Python 3.9 or newer
- Pandas (see `requirements.txt`)

## Run
```bash
python -m pip install -r requirements.txt
python pure_python_stats.py
python pandas_stats.py
python compare_results.py
```
Optional: pass a custom CSV path as the first argument to either statistics script.

The first two commands create JSON files in `outputs/` (ignored by Git). The third checks numeric values within a small floating-point tolerance and exact categorical values.

## Methods and assumptions
- Missing values: blank, `NA`, `N/A`, `NULL`, `None`, `NaN`, `-`, `--` (case-insensitive).
- Numeric strings can contain commas, currency signs, percent signs and accounting parentheses. Percent values are treated as their displayed number, not divided by 100.
- A column is numeric only if **every non-missing entry** can be parsed as a number; otherwise it is treated as categorical (or date if all non-missing values match supported date formats).
- Identifier-like names containing `id`, `zip`, `postal`, `fips`, or `code` are categorical.
- Standard deviation is the **sample** standard deviation (`n-1`); for fewer than two numeric observations it is undefined (`null`).
- Ties for categorical mode are broken alphabetically for reproducibility.
- Date columns receive categorical frequency summaries; this task does not automatically compute time-series aggregations.
- All-missing columns are reported as `empty`.
- The Pandas script intentionally reads values as strings and applies the **same explicit cleaning and inference** as pure Python so comparison is meaningful. It still uses Pandas `describe`, `value_counts`, `nunique`, and numeric summary methods.

## Deliverables
- `pure_python_stats.py`: standard-library statistics.
- `pandas_stats.py`: Pandas replication.
- `analysis_common.py`: shared data parsing/type rules.
- `compare_results.py`: checks agreement.
- `political_ads_insights.py`: domain-aware spending-bracket and candidate-mention analysis.
- `FINDINGS.md`: completed research narrative based on the supplied dataset.
- `COMPARISON.md`: methodological reflection and validated agreement.

## Results and interpretation
**Completed analysis:** 246,745 rows and 40 source columns. The two scripts passed the automated comparison on the supplied CSV. See [FINDINGS.md](FINDINGS.md) for empirical results and [COMPARISON.md](COMPARISON.md) for validation and methodological reflection. Run `python political_ads_insights.py` for domain-aware summaries of spend brackets, dates, and candidate-mention lists.

## Research integrity
This repository includes analysis code and documentation, not the source dataset. Empirical findings are based on the course-supplied CSV and locally executed scripts. The data itself is excluded from GitHub.
