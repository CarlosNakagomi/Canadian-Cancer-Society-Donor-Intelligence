# Power BI Build Guide

Build style: executive donor intelligence report. Use a restrained palette, large KPI cards, clear comparisons, and short text callouts. Avoid pie charts, 3D visuals, decorative visuals, and excessive slicers.

Use `Power BI/data/` as the import folder. Most tables are already pre-aggregated in Python; Power BI should present and lightly filter them, not reconstruct survey cleaning logic.

## Page 1 - The Canadian Donor

Business question: Who gives and how much?

Main takeaway: A little over half of the weighted Canadian population are charitable donors, and donation amounts are right-skewed, so medians should be emphasized alongside means.

Source tables:

- `page1_canadian_donor_overall.csv`
- `page1_canadian_donor_segments.csv`
- `page1_donation_amount_bands.csv`
- `page1_donation_frequency.csv`

KPI cards:

- Weighted Canadian population represented
- Weighted donor population
- Weighted donor participation rate
- Weighted median donation among donors
- Weighted median donation frequency

Recommended visuals:

- Segment comparison bar chart: `segment` on Y, `weighted_donor_rate_pct` on X, filtered by `segment_variable`. Use slicer for age, gender, province, income, education.
- Donation amount distribution column chart: `amount_band` on X, `weighted_donor_share_pct` on Y.
- Donation frequency column chart: `donation_count` on X, `weighted_donor_share_pct` on Y.

Sorting:

- Sort amount bands by `sort_order`.
- Sort segment categories by `sort_order`.
- Sort frequency by numeric `donation_count`.

Tooltips:

- Sample count
- Weighted donors
- Weighted mean donation
- Weighted median donation

Do not show:

- Raw sample percentages as Canadian estimates.
- Mean donation without median context.

Suggested callout: "Weighted estimates show 53.7% donor participation; median giving is a better central tendency than the mean because donation amounts are skewed."

## Page 2 - The Health Donor

Business question: What makes Health donors different?

Main takeaway: Health donors are a large donor segment, give more overall than non-Health donors, and show stronger volunteering engagement.

Source tables:

- `page2_health_donor_overview.csv`
- `page2_health_donor_group_comparison.csv`
- `page2_health_profile_age.csv`
- `page2_health_profile_income.csv`
- `page2_health_profile_education.csv`
- `page2_health_profile_province.csv`
- `page2_health_donation_distribution.csv`
- `page2_health_donor_volunteering.csv`

KPI cards:

- Weighted Health donor population
- Weighted Health donor rate among population
- Weighted Health donor rate among charitable donors
- Weighted total Health donation dollars
- Weighted median Health donation
- Weighted median total giving among Health donors

Recommended visuals:

- Group comparison bar chart: `group` on X, `weighted_median_total_donation_among_group_donors` on Y.
- Age participation line/bar chart: `segment_label` on X, `weighted_health_donor_rate_among_donors_pct` on Y.
- Income participation bar chart: `segment_label` on X, `weighted_health_donor_rate_among_donors_pct` on Y.
- Health donation distribution combo chart: `amount_band` on X, donor share and dollar share as two measures.
- Volunteering comparison clustered bar: `comparison_group` on X, volunteer/fundraising/healthcare support rates as values.

Sorting:

- Use `sort_order` for age, income, education, province.

Tooltips:

- Sample Health donor count
- Weighted Health donors
- Weighted mean and median Health donation
- Province reliability note

Do not show:

- Province differences without sample counts and descriptive caveat.
- Hospital donors as Health donors unless explicitly labelled broader Health-or-Hospital.

Suggested callout: "Health donors represent 6.8M weighted Canadians and 38.3% of charitable donors; they also give more overall than non-Health donors."

## Page 3 - How They Give

Business question: Which channels and behaviours matter?

Main takeaway: Health donors are especially distinctive in in-memory, sponsorship, mail, online, and social-prompted giving channels.

Source tables:

- `page3_giving_channel_summary.csv`
- `page3_channel_by_health_value.csv`
- `page3_giving_behaviour_summary.csv`

KPI cards:

- Top Health donor channel by use rate
- Largest Health vs non-Health channel gap
- Weighted channel users for selected channel

Recommended visuals:

- Channel use bar chart: `channel_label` on Y, `weighted_channel_use_rate_pct` on X, filtered to Health donors.
- Health vs non-Health comparison chart: `channel_label` on Y, `weighted_channel_use_rate_pct` on X, `comparison_group` as legend.
- Gap bar chart: `channel_label` on Y, `health_vs_nonhealth_rate_gap_pct_points` on X.
- Channel by Health value heatmap/matrix: `segment_label` rows, `channel_label` columns, `weighted_channel_use_rate_pct` values.

Sorting:

- Use `sort_order` for channel order, or sort by rate/gap for ranking visuals.

Tooltips:

- Sample channel user count
- Weighted channel users
- Valid denominator
- Weighted median channel donation among users

Do not show:

- Channel dollars as Health-specific channel dollars. They are total charitable channel dollars among Health donors.
- Every behaviour variable on the main page; place behaviour details in a drill-through or appendix view.

Suggested callout: "In-memory and sponsorship giving are far more common among Health donors than among non-Health donors, pointing to personal and social giving journeys."

## Page 4 - Why They Give

Business question: What motivates Health donors?

Main takeaway: Cause, compassion, personal connection, and community contribution dominate Health donor motivations.

Source tables:

- `page4_motivation_summary.csv`
- `page4_motivation_by_age.csv`
- `page4_motivation_by_health_value.csv`

KPI cards:

- Top Health donor motivation
- Personally affected rate among Health donors
- Largest Health vs non-Health motivation gap

Recommended visuals:

- Motivation rank bar chart: `motivation_label` on Y, `weighted_yes_pct` on X, filtered to Health donors.
- Motivation comparison clustered bar: `motivation_label` on Y, `weighted_yes_pct` on X, `comparison_group` as legend.
- Gap bar chart: `motivation_label` on Y, `health_vs_nonhealth_gap_pct_points` on X.
- Small matrix for selected motivations by age or Health value: segment rows, motivation columns, `weighted_yes_pct` values.

Sorting:

- Sort top chart by `weighted_yes_pct` descending.
- Use `sort_order` for official motivation order where needed.

Tooltips:

- Sample yes count
- Weighted yes
- Valid denominator

Do not show:

- Motivation differences as causal messaging proof.
- Segment cuts with very small sample counts as strong conclusions.

Suggested callout: "Health donors stand out most on personal connection and being asked by someone they know."

## Page 5 - Why They Don't Give More

Business question: What are the barriers?

Main takeaway: Health donors report a mix of financial limits, satisfaction with current giving, trust concerns, and choice overload.

Source tables:

- `page5_barrier_summary.csv`
- `page5_barrier_category_summary.csv`
- `page5_barriers_by_income.csv`

KPI cards:

- Top Health donor barrier
- Financial barrier rate
- Charity fraud concern rate
- Already gave enough rate

Recommended visuals:

- Core barrier rank bar chart: `barrier_label` on Y, `weighted_yes_pct` on X, filtered to Health donors and `applicability = Core`.
- Barrier category bar chart: `barrier_category` on Y, `max_weighted_yes_pct` or `mean_weighted_yes_pct` on X.
- Health vs non-Health gap chart for core barriers: `barrier_label` on Y, `health_vs_nonhealth_gap_pct_points` on X.
- Income matrix: `segment_label` rows, selected barrier labels columns, `weighted_yes_pct` values.

Sorting:

- Sort core barrier rank by `weighted_yes_pct` descending.
- Keep conditional follow-up barriers separate from core barriers.

Tooltips:

- Valid denominator
- Sample yes count
- Applicability
- Barrier category

Do not show:

- Conditional follow-up barriers next to core barriers without an applicability note.
- Non-donor rows where the denominator is zero or not applicable.

Suggested callout: "Some barriers are addressable through donor experience and trust-building; affordability and already-gave responses require more careful ask strategy."

## Page 6 - The Opportunity

Business question: Which audiences and fundraising approaches should a Health charity prioritize?

Main takeaway: The strongest opportunities are retention, high-value stewardship, volunteer engagement, tribute/social giving, and trust-sensitive donor experience.

Source tables:

- `page6_priority_audiences.csv`
- `page6_evidence_table.csv`

KPI cards:

- Number of priority audiences
- Evidence metrics used
- Top opportunity type

Recommended visuals:

- Priority audience table: columns `priority_rank`, `audience_name`, `opportunity_type`, `what_the_data_shows`, `fundraising_approach_supported`.
- Evidence table by theme: `evidence_theme`, `source_chapter`, `metric`, `value`, `interpretation`.
- Optional matrix: `audience_name` rows and fields for data finding, recommendation, limitation.

Sorting:

- Sort priority audiences by `priority_rank`.
- Sort evidence by source chapter and theme.

Tooltips:

- What the data does not allow us to claim
- Source chapter

Do not show:

- Recommendations without the linked data finding.
- A synthetic opportunity score unless it is explicitly developed later.

Suggested callout: "The opportunity framework is evidence-linked and descriptive; recommendations should be tested before campaign scaling."

## Page 7 - Bonus: Health Donor Propensity

Business question: Can interpretable respondent characteristics help distinguish Health donors?

Main takeaway: A small weighted logistic regression shows moderate discrimination, but it is secondary to the descriptive donor intelligence.

Source tables:

- `page7_bonus_model_metrics.csv`
- `page7_bonus_top_model_coefficients.csv`

KPI cards:

- ROC-AUC
- Precision
- Recall
- F1
- Test sample size

Recommended visuals:

- Metric card row for ROC-AUC, precision, recall, F1.
- Coefficient bar chart: `feature` on Y, `odds_ratio_per_standardized_unit` on X, `direction` as color.
- Confusion matrix table: true positive, false positive, true negative, false negative from model metrics.

Sorting:

- Sort coefficient chart by absolute coefficient or odds ratio distance from 1.

Tooltips:

- Coefficient
- Direction
- Leakage note

Do not show:

- Respondent-level scores as deployable fundraising targets.
- Accuracy as the main metric.
- Model output as the basis for Chapter 6 recommendations.

Suggested callout: "The model is an interpretable technical extension; leakage-prone Health donation and behaviour variables were excluded."
