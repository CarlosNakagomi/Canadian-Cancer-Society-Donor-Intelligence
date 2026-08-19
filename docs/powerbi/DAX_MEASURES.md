# DAX Measures

Most dashboard metrics are pre-aggregated in Python using validated survey weights and variable-specific denominator rules. Prefer simple display measures over rebuilding SGVP logic in DAX.

Important: CSV percentage columns are stored as percentage-point values, for example `53.7`, not `0.537`. Either format them as decimal numbers with a percent suffix or divide by 100 in explicit DAX measures.

## Global Display Helpers

Use these patterns per table as needed.

```DAX
Selected Weighted Value =
SELECTEDVALUE ( page2_health_donor_overview[weighted_value] )
```

```DAX
Selected Sample Value =
SELECTEDVALUE ( page2_health_donor_overview[sample_value] )
```

## Page 1 - Canadian Donor

```DAX
P1 Weighted Population =
CALCULATE (
    MAX ( page1_canadian_donor_overall[weighted_value_numeric] ),
    page1_canadian_donor_overall[metric] = "Respondents"
)
```

```DAX
P1 Weighted Donors =
CALCULATE (
    MAX ( page1_canadian_donor_overall[weighted_value_numeric] ),
    page1_canadian_donor_overall[metric] = "Donors"
)
```

```DAX
P1 Weighted Donor Rate Pct =
CALCULATE (
    MAX ( page1_canadian_donor_overall[weighted_value_numeric] ),
    page1_canadian_donor_overall[metric] = "Donor participation rate"
)
```

```DAX
P1 Weighted Median Donation =
CALCULATE (
    MAX ( page1_canadian_donor_overall[weighted_value_numeric] ),
    page1_canadian_donor_overall[metric] = "Median donation among donors"
)
```

```DAX
P1 Weighted Median Frequency =
CALCULATE (
    MAX ( page1_canadian_donor_overall[weighted_value_numeric] ),
    page1_canadian_donor_overall[metric] = "Median donation frequency among donors"
)
```

Use pre-aggregated fields directly in visuals:

- `page1_canadian_donor_segments[weighted_donor_rate_pct]`
- `page1_donation_amount_bands[weighted_donor_share_pct]`
- `page1_donation_frequency[weighted_donor_share_pct]`

## Page 2 - Health Donor

```DAX
P2 Weighted Health Donors =
CALCULATE (
    MAX ( page2_health_donor_overview[weighted_value_numeric] ),
    page2_health_donor_overview[metric] = "Health donors"
)
```

```DAX
P2 Health Donor Rate Population Pct =
CALCULATE (
    MAX ( page2_health_donor_overview[weighted_value_numeric] ),
    page2_health_donor_overview[metric] = "Health donor rate among Canadian population"
)
```

```DAX
P2 Health Donor Rate Among Donors Pct =
CALCULATE (
    MAX ( page2_health_donor_overview[weighted_value_numeric] ),
    page2_health_donor_overview[metric] = "Health donor rate among charitable donors"
)
```

```DAX
P2 Weighted Health Donation Dollars =
CALCULATE (
    MAX ( page2_health_donor_overview[weighted_value_numeric] ),
    page2_health_donor_overview[metric] = "Weighted total Health donation dollars"
)
```

```DAX
P2 Weighted Median Health Donation =
CALCULATE (
    MAX ( page2_health_donor_overview[weighted_value_numeric] ),
    page2_health_donor_overview[metric] = "Median Health donation among Health donors"
)
```

```DAX
P2 Health Vs NonHealth Median Total Giving Gap =
VAR HealthMedian =
    CALCULATE (
        MAX ( page2_health_donor_group_comparison[weighted_median_total_donation_among_group_donors] ),
        page2_health_donor_group_comparison[group] = "Health donors"
    )
VAR NonHealthMedian =
    CALCULATE (
        MAX ( page2_health_donor_group_comparison[weighted_median_total_donation_among_group_donors] ),
        page2_health_donor_group_comparison[group] = "Non-Health donors"
    )
RETURN
    HealthMedian - NonHealthMedian
```

Use pre-aggregated fields directly:

- `weighted_health_donor_rate_population_pct`
- `weighted_health_donor_rate_among_donors_pct`
- `weighted_health_donor_composition_pct`
- `weighted_mean_health_donation`
- `weighted_median_health_donation`
- `weighted_total_health_dollars`

## Page 3 - How They Give

```DAX
P3 Selected Channel Use Rate Pct =
MAX ( page3_giving_channel_summary[weighted_channel_use_rate_pct] )
```

```DAX
P3 Selected Channel Weighted Users =
SUM ( page3_giving_channel_summary[weighted_channel_users] )
```

```DAX
P3 Health Vs NonHealth Channel Gap Pct Points =
MAX ( page3_giving_channel_summary[health_vs_nonhealth_rate_gap_pct_points] )
```

```DAX
P3 Selected Channel Median Donation =
MAX ( page3_giving_channel_summary[weighted_median_channel_donation_among_users] )
```

Do not calculate channel rates as raw user count divided by sample count. Use `valid_channel_denominator_weighted` if building a custom measure:

```DAX
P3 Recomputed Weighted Channel Use Rate Pct =
DIVIDE (
    SUM ( page3_giving_channel_summary[weighted_channel_users] ),
    SUM ( page3_giving_channel_summary[valid_channel_denominator_weighted] )
) * 100
```

## Page 4 - Why They Give

```DAX
P4 Motivation Yes Rate Pct =
MAX ( page4_motivation_summary[weighted_yes_pct] )
```

```DAX
P4 Health Vs NonHealth Motivation Gap Pct Points =
MAX ( page4_motivation_summary[health_vs_nonhealth_gap_pct_points] )
```

```DAX
P4 Recomputed Motivation Yes Rate Pct =
DIVIDE (
    SUM ( page4_motivation_summary[weighted_yes] ),
    SUM ( page4_motivation_summary[valid_denominator_weighted] )
) * 100
```

Use the recomputed measure only when the current filter context combines multiple motivation rows. For single-row motivation visuals, the pre-aggregated `weighted_yes_pct` is preferable.

## Page 5 - Why They Do Not Give More

```DAX
P5 Barrier Yes Rate Pct =
MAX ( page5_barrier_summary[weighted_yes_pct] )
```

```DAX
P5 Health Vs NonHealth Barrier Gap Pct Points =
MAX ( page5_barrier_summary[health_vs_nonhealth_gap_pct_points] )
```

```DAX
P5 Recomputed Barrier Yes Rate Pct =
DIVIDE (
    SUM ( page5_barrier_summary[weighted_yes] ),
    SUM ( page5_barrier_summary[valid_denominator_weighted] )
) * 100
```

Use filters:

- `applicability = "Core"` for main barrier visuals.
- Keep conditional follow-up barriers separate.

## Page 6 - Opportunity

```DAX
P6 Priority Audience Count =
COUNTROWS ( page6_priority_audiences )
```

```DAX
P6 Evidence Metric Count =
COUNTROWS ( page6_evidence_table )
```

```DAX
P6 Selected Evidence Value =
SELECTEDVALUE ( page6_evidence_table[value] )
```

Page 6 is mainly a curated evidence/recommendation table. Do not create an artificial opportunity score unless a later methodology is explicitly approved.

## Page 7 - Bonus Model

```DAX
P7 ROC AUC =
MAX ( page7_bonus_model_metrics[roc_auc] )
```

```DAX
P7 Precision =
MAX ( page7_bonus_model_metrics[precision] )
```

```DAX
P7 Recall =
MAX ( page7_bonus_model_metrics[recall] )
```

```DAX
P7 F1 =
MAX ( page7_bonus_model_metrics[f1] )
```

```DAX
P7 Test Sample N =
MAX ( page7_bonus_model_metrics[test_sample_n] )
```

```DAX
P7 False Positives =
MAX ( page7_bonus_model_metrics[false_positive] )
```

```DAX
P7 False Negatives =
MAX ( page7_bonus_model_metrics[false_negative] )
```

Coefficient chart fields:

- Axis: `page7_bonus_top_model_coefficients[feature]`
- Value: `page7_bonus_top_model_coefficients[odds_ratio_per_standardized_unit]`
- Legend/color: `direction`

## Measures To Avoid

- Do not compute weighted medians in Power BI from pre-aggregated tables.
- Do not calculate Canadian population percentages from raw sample counts.
- Do not calculate Health donor flags in Power BI.
- Do not mix core and conditional barrier denominators.
- Do not treat model scores as fundraising recommendations.
