# Comparison: Standard-library Python vs. Pandas

## Implementations

The pure Python implementation uses `csv.DictReader`, `Counter`, explicit sorting, arithmetic, and a sample standard-deviation formula with denominator `n-1`. The Pandas implementation uses `read_csv`, `Series.describe`, `value_counts`, `nunique`, and Pandas numerical aggregation methods. Both use the same normalization and type-inference definitions from `analysis_common.py`, which makes the two implementations directly comparable while retaining independent statistical calculations.

## Validation result

**PASS:** On the supplied dataset of **246,745 rows and 40 columns**, `compare_results.py` reported **“PASS: Both approaches agree.”** The validator checked overall dimensions, missing-value counts, inferred column types, categorical frequency summaries, and numeric count/mean/min/max/sample standard deviation/median. Numerical values were compared within a floating-point tolerance of `1e-9`; categorical summaries were compared exactly.

## Decisions exposed by pure Python

Implementing the statistics manually forced me to specify what counts as missing, whether standard deviation uses the population or sample formula, what to return for empty or single-observation columns, and how to resolve tied modes. The scripts classify date-like columns separately, and identifier-like fields as categorical even when they resemble numbers. A numeric column is accepted only when all nonmissing values are numeric under the declared parsing rules. These decisions are visible rather than silently delegated to library defaults.

## Lessons from the actual dataset

The most important limitation was not a disagreement between Python and Pandas: it was **data semantics**. The `spend`, `impressions`, and `estimated_audience_size` columns are string-encoded ranges, not simple scalar values. Accordingly, both generic scripts correctly report them as categorical. A separate `political_ads_insights.py` script parses the spending brackets and candidate-mention lists for domain-aware analysis. This separation avoids quietly converting uncertain dollar ranges into false exact totals.

## Tradeoffs and reflection

The standard-library approach makes every operation transparent and needs no third-party package, but it is longer and requires more explicit edge-case handling. Pandas is concise, supports fast summaries, and is easier to extend with grouping by page or month. Sharing parsing rules is a deliberate choice: it isolates statistical differences rather than letting inconsistent cleaning produce false disagreements. The core lesson is that **matching computations do not automatically imply valid interpretation**; column meaning, missingness, and range estimates must still be understood.
