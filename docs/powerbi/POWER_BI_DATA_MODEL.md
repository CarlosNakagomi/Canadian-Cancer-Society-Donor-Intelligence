# Power BI Data Model

This handoff uses pre-aggregated, validated CSVs. The safest model is a lightweight reporting model with mostly disconnected fact-like tables. Avoid forced many-to-many relationships across tables with different grains.

## Import Folder

Import CSV files from:

`Power BI/data/`

Also import:

`powerbi_data_manifest.csv`

Use the manifest for documentation, not dashboard visuals.

## Recommended Model Pattern

Use each page's tables independently unless a relationship is explicitly listed below. Most metrics were already calculated in Python using validated survey weights and denominator logic. Power BI should not rebuild special-code handling.

## Tables

| Table | Grain | Page | Relationship Guidance |
|---|---|---|---|
| `page1_canadian_donor_overall` | One row per KPI metric | Page 1 | Disconnected |
| `page1_canadian_donor_segments` | Segment variable x category | Page 1 | Disconnected |
| `page1_donation_amount_bands` | Donation amount band | Page 1 | Disconnected |
| `page1_donation_frequency` | Donation count | Page 1 | Disconnected |
| `page2_health_donor_overview` | One row per KPI metric | Page 2 | Disconnected |
| `page2_health_donor_group_comparison` | Comparison group | Page 2 | May relate to disconnected comparison group dimension if desired |
| `page2_health_profile_age` | Age category | Page 2 | Disconnected or related to `dim_age` |
| `page2_health_profile_income` | Personal income category | Page 2 | Disconnected or related to `dim_income` |
| `page2_health_profile_education` | Education category | Page 2 | Disconnected or related to `dim_education` |
| `page2_health_profile_province` | Province category | Page 2 | Disconnected or related to `dim_province` |
| `page2_health_donation_distribution` | Health donation amount band | Page 2 | Disconnected |
| `page2_health_donor_volunteering` | Comparison group | Page 2 | May relate to disconnected comparison group dimension if desired |
| `page3_giving_channel_summary` | Channel x comparison group | Page 3 | Optional many-to-one to `dim_channel` |
| `page3_channel_by_health_value` | Health value segment x channel | Page 3 | Optional many-to-one to `dim_channel` |
| `page3_giving_behaviour_summary` | Behaviour x response x comparison group | Page 3 | Disconnected |
| `page4_motivation_summary` | Motivation x comparison group | Page 4 | Optional many-to-one to `dim_motivation` |
| `page4_motivation_by_age` | Health donor age segment x motivation | Page 4 | Optional many-to-one to `dim_motivation` |
| `page4_motivation_by_health_value` | Health value segment x motivation | Page 4 | Optional many-to-one to `dim_motivation` |
| `page5_barrier_summary` | Barrier x comparison group | Page 5 | Optional many-to-one to `dim_barrier` |
| `page5_barrier_category_summary` | Barrier category x comparison group | Page 5 | Disconnected |
| `page5_barriers_by_income` | Health donor income segment x barrier | Page 5 | Optional many-to-one to `dim_barrier` |
| `page6_priority_audiences` | Priority audience | Page 6 | Disconnected |
| `page6_evidence_table` | Evidence metric row | Page 6 | Disconnected |
| `page7_bonus_model_metrics` | One model metric row | Page 7 | Disconnected |
| `page7_bonus_top_model_coefficients` | Model feature coefficient | Page 7 | Disconnected |

## Optional Dimensions

Optional dimensions can be created in Power Query using reference tables from the imported facts:

| Dimension | Source | Key | Related Tables | Cardinality | Filter Direction |
|---|---|---|---|---|---|
| `dim_channel` | Distinct `channel_key`, `channel_label`, `sort_order` from `page3_giving_channel_summary` | `channel_key` | `page3_giving_channel_summary`, `page3_channel_by_health_value` | One-to-many | Single |
| `dim_motivation` | Distinct `motivation_variable`, `motivation_label`, `sort_order` from `page4_motivation_summary` | `motivation_variable` | Chapter 4 motivation tables | One-to-many | Single |
| `dim_barrier` | Distinct `barrier_variable`, `barrier_label`, `barrier_category`, `applicability`, `sort_order` from `page5_barrier_summary` | `barrier_variable` | Chapter 5 barrier tables | One-to-many | Single |

Do not create a single universal segment dimension unless you intentionally standardize segment keys across chapters. Age, income, education, province, Health value segment, and barrier/motivation segment tables have different grains and should not be forced together.

## Relationships To Avoid

- Do not join Page 1 segment tables to Page 2 profile tables directly. They represent related concepts but different measures and chapter definitions.
- Do not join overview KPI metric tables to segment tables.
- Do not join Chapter 3 channel tables to Chapter 4 motivation tables unless creating an explicit bridge and accepting that it is not respondent-level.
- Do not join Bonus model coefficients to respondent-level scores; respondent-level scored data is not included in this handoff because the Bonus page should stay summary-level.

## Sort Columns

Use these sort requirements:

- `sort_order` sorts age, income, education, province, channel, motivation, and barrier rows where present.
- `priority_rank` sorts Page 6 audiences.
- `donation_count` sorts Page 1 frequency.
- Amount bands without sort columns should be manually sorted in the order shown in the source CSV.

## Data Types

Set these types:

- Counts and sample sizes: whole number
- Weighted populations and weighted dollars: decimal number or whole number after rounding
- KPI overview tables include both original display columns (`sample_value`, `weighted_value`) and normalized numeric columns (`sample_value_numeric`, `weighted_value_numeric`) for reliable Power BI measures.
- Percentages: decimal number, formatted as percentage only if divided by 100. These CSV percentages are already stored as percentage-point values, such as `53.7`, so use numeric format with `%` suffix or divide by 100 in explicit DAX measures.
- Sort columns and ranks: whole number
- Labels and notes: text

## Survey Weighting

The weighted fields are already computed with `WGHT_PER` in Python. Use the pre-aggregated weighted columns for dashboard visuals. Do not use raw row counts as population estimates.
