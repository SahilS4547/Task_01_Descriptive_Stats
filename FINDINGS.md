# Findings: 2024 Facebook Political Ads

## Scope and method

I analyzed **246,745 ad-purchase records and 40 source columns** from the course-provided `fb_ads_president_scored_anon.csv` dataset. Although the file is described as a 2024 presidential-election advertising dataset, the `ad_delivery_start_time` field includes dates as early as **July 6, 2021**, and as late as **November 5, 2024**. It would therefore be misleading to describe every row as an ad first delivered during 2024. My analysis treats the supplied file as the study population, rather than claiming it represents all Facebook political advertising.

The file contains advertising-page identifiers and names, ad identifiers, dates, bylines, currency, estimated audience-size and impression ranges, spend ranges, platform lists, candidate-mention lists, and a set of scored message/topic flags. I used standard-library Python and Pandas to compute per-column descriptive statistics, then compared their outputs. To interpret the nested spend and candidate-mention fields, I performed a separate domain-aware aggregation, reproducible using `political_ads_insights.py`.

## Spending: concentration and measurement uncertainty

The `spend` field contains **bracket dictionaries**, such as `{'lower_bound': '200', 'upper_bound': '299'}`, rather than exact spending figures. Summing bracket lower bounds across all records yields **$227,487,000**, and summing upper bounds yields **$296,496,455**. These are *bounds on summed reported ad-level brackets*, **not an exact observed total**. The range does not account for any limitations of the original platform estimates or sampling.

The page named **Kamala Harris** had **55,503 records**, with a combined reported-spend bracket of **$72,902,800–$92,743,997**. The page named **Joe Biden** had **14,822 records**, with **$23,357,200–$29,393,578**; **Donald J. Trump** had **23,988 records**, with **$16,795,100–$22,447,612**. These are *page names*, not a comprehensive accounting of each campaign's spending across associated organizations. The `page_name` grouping should not be confused with verified ownership, sponsorship, or total candidate support. Nevertheless, the observed page-level distribution suggests that a small set of high-volume pages accounted for a substantial share of the records and bracketed spending in this file.

A different ranking appears when considering ad counts rather than spending. After Kamala Harris and Donald J. Trump, the page **Joe Biden** had 14,822 ads and **The Daily Scroll** had 10,461. This illustrates why ad count and dollar volume are different metrics: many small ads can produce a large number of records without implying the largest aggregate spend.

## Timing: a strong late-campaign increase

Grouping by the month in `ad_delivery_start_time` reveals **17,673** records starting in July 2024, **33,777** in August, **35,893** in September, and **85,172** in October. October had more than twice as many ad starts as September. October's sum of spend brackets was **$74,387,300–$97,377,228**, compared with **$38,715,100–$50,041,407** in September. These patterns are consistent with increased advertising activity near the November election, but descriptive data alone cannot attribute the change to any single debate, news event, or campaign decision.

## Candidate mentions: labels need careful interpretation

The `illuminating_mentions` field contains lists of name labels, not a single candidate per row. The most frequent literal labels were **Donald Trump (78,324)**, **Kamala Harris (53,239)**, **Joe Biden (24,247)**, **President Trump (22,153)**, and **President Biden (16,517)**. These figures are **counts of rows containing each literal label**; they are not unique counts of ads about each person, because a record may contain multiple labels and alternate names for the same person. In particular, I did not automatically merge “Donald Trump” with “President Trump,” or “Joe Biden” with “President Biden.” The labels also do not establish whether the message supports or opposes the mentioned candidate.

## Data quality and limitations

The `bylines` column has **1,009 blank entries**, and `ad_delivery_stop_time` has **2,159 blanks**. The spending, impressions, and estimated-audience fields use structured string ranges, so they should not be interpreted as exact scalar measurements. Some columns are binary scored flags, where the mean represents the fraction of nonmissing records with a value of one, assuming the scores are coded consistently. The dataset has no obvious dedicated state or ZIP field, so a credible geographic comparison cannot be made solely from the displayed columns.

The analysis does not establish whether ads were effective, whether exposure changed voter behavior, or whether an ad was misleading. It documents recorded purchases, metadata, and scored labels. Distinguishing **observed records** from **inferred intent** is essential in interpreting political-advertising data.

## Conclusion

The clearest empirical pattern is the concentration of recorded advertising in the final pre-election months, particularly October 2024, alongside high page-level activity for several prominent political pages. A second lesson is methodological: correct analysis requires recognizing that spending is stored as **ranges** and candidate mentions as **lists**. Treating either as ordinary numeric or single-category values would produce misleading conclusions. The agreement of the two general-purpose statistics scripts provides a reproducible baseline; the domain-aware script makes the most substantively relevant fields interpretable without inventing exact values.
