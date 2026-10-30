"""Shared normalization and column classification rules for both analyses."""
import re
from datetime import datetime

MISSING = {"", "na", "n/a", "null", "none", "nan", "-", "--"}
DATE_FORMATS = ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%Y/%m/%d",
                "%Y-%m-%d %H:%M:%S", "%m/%d/%Y %H:%M:%S")

def is_missing(value):
    return value is None or str(value).strip().lower() in MISSING

def parse_number(value):
    if is_missing(value):
        return None
    s = str(value).strip()
    neg = s.startswith("(") and s.endswith(")")
    if neg:
        s = s[1:-1]
    s = re.sub(r"[$,%\s,]", "", s)
    if not s or not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", s):
        return None
    try:
        n = float(s)
        return -n if neg else n
    except (ValueError, OverflowError):
        return None

def is_date(value):
    if is_missing(value):
        return False
    s = str(value).strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return True
    return any(_matches_date(s, fmt) for fmt in DATE_FORMATS)

def _matches_date(s, fmt):
    try:
        datetime.strptime(s, fmt)
        return True
    except ValueError:
        return False

def infer_type(values, name=""):
    observed = [str(v).strip() for v in values if not is_missing(v)]
    if not observed:
        return "empty"
    # Avoid treating identifier-like columns as continuous numeric measures.
    if re.search(r"(?:^|[_\s])(id|zip|postal|fips|code)(?:$|[_\s])", name.lower()):
        return "categorical"
    if all(parse_number(v) is not None for v in observed):
        return "numeric"
    if all(is_date(v) for v in observed):
        return "date"
    return "categorical"
