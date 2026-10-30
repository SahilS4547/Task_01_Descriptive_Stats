"""Optional domain-aware report: estimates from Facebook ad spend brackets."""
import ast
from collections import Counter
from pathlib import Path
import pandas as pd

DATA = Path('data/facebook_ads_2024.csv')
df = pd.read_csv(DATA, dtype=str, keep_default_na=False, encoding='utf-8-sig')
def bracket(value):
    try:
        d = ast.literal_eval(value)
        lo = float(d['lower_bound'])
        hi = float(d['upper_bound']) if 'upper_bound' in d else None
        return lo, hi
    except (ValueError, SyntaxError, KeyError, TypeError):
        return None, None
bounds = df['spend'].map(bracket)
df['spend_lower'] = [x[0] for x in bounds]
df['spend_upper'] = [x[1] for x in bounds]
print('Records:', len(df), 'Columns:', len(df.columns)-2)
print('Spending lower-bound total:', df.spend_lower.sum())
print('Spending upper-bound total (only when present):', df.spend_upper.sum(min_count=1))
print('Open-ended brackets:', df.spend_upper.isna().sum())
print('\nTop pages by lower-bound spending:')
print(df.groupby('page_name').agg(ads=('page_name','size'), lower=('spend_lower','sum'), upper=('spend_upper','sum')).sort_values('lower',ascending=False).head(10))
print('\nMonthly ad starts:')
print(df.groupby(df.ad_delivery_start_time.str[:7]).size().sort_index())
mentions = Counter()
for item in df['illuminating_mentions']:
    try:
        for name in ast.literal_eval(item):
            mentions[name] += 1
    except (ValueError, SyntaxError, TypeError):
        pass
print('\nTop literal candidate mention labels:', mentions.most_common(15))
