# Power Query Import All CSVs As Separate Tables

Power BI Desktop's Text/CSV connector imports one file at a time. Do not use the Folder connector for this package unless you intentionally want to combine files, which this project does not require.

Goal: import every CSV in `Power BI/data` as a separate query/table, preserving the table name from the filename.

Data folder:

`outputs\powerbi`

## Recommended Method: Blank Query Per Table

1. Open Power BI Desktop.
2. Select **Transform data** to open Power Query Editor.
3. Select **New Source > Blank Query**.
4. In the Queries pane, rename the query to the target table name, for example `page1_canadian_donor_overall`.
5. Open **Advanced Editor**.
6. Copy the matching M script block from `POWER_QUERY_M_SCRIPTS.md`.
7. Paste it into Advanced Editor and select **Done**.
8. Confirm headers, column types, and row count.
9. Repeat for each CSV/table.
10. Select **Close & Apply** after all queries are created.

## Important Rules

- Create one query per CSV.
- Do not append or combine the CSV files.
- Use filenames without `.csv` as query names.
- The query scripts use `Csv.Document`, `File.Contents`, `Table.PromoteHeaders`, and `Table.TransformColumnTypes`.
- If Power BI prompts for privacy settings, use the same local file privacy level for all files.
- `powerbi_data_manifest` is optional but useful as documentation inside the model.

## Tables To Create

- `page1_canadian_donor_overall` from `page1_canadian_donor_overall.csv` (7 rows, 7 columns)
- `page1_canadian_donor_segments` from `page1_canadian_donor_segments.csv` (35 rows, 13 columns)
- `page1_donation_amount_bands` from `page1_donation_amount_bands.csv` (7 rows, 7 columns)
- `page1_donation_frequency` from `page1_donation_frequency.csv` (24 rows, 4 columns)
- `page2_health_donation_distribution` from `page2_health_donation_distribution.csv` (7 rows, 7 columns)
- `page2_health_donor_group_comparison` from `page2_health_donor_group_comparison.csv` (5 rows, 19 columns)
- `page2_health_donor_overview` from `page2_health_donor_overview.csv` (13 rows, 7 columns)
- `page2_health_donor_volunteering` from `page2_health_donor_volunteering.csv` (4 rows, 18 columns)
- `page2_health_profile_age` from `page2_health_profile_age.csv` (7 rows, 20 columns)
- `page2_health_profile_education` from `page2_health_profile_education.csv` (4 rows, 20 columns)
- `page2_health_profile_income` from `page2_health_profile_income.csv` (6 rows, 20 columns)
- `page2_health_profile_province` from `page2_health_profile_province.csv` (10 rows, 21 columns)
- `page3_channel_by_health_value` from `page3_channel_by_health_value.csv` (65 rows, 12 columns)
- `page3_giving_behaviour_summary` from `page3_giving_behaviour_summary.csv` (36 rows, 10 columns)
- `page3_giving_channel_summary` from `page3_giving_channel_summary.csv` (39 rows, 17 columns)
- `page4_motivation_by_age` from `page4_motivation_by_age.csv` (56 rows, 12 columns)
- `page4_motivation_by_health_value` from `page4_motivation_by_health_value.csv` (40 rows, 12 columns)
- `page4_motivation_summary` from `page4_motivation_summary.csv` (24 rows, 12 columns)
- `page5_barrier_category_summary` from `page5_barrier_category_summary.csv` (27 rows, 5 columns)
- `page5_barrier_summary` from `page5_barrier_summary.csv` (66 rows, 14 columns)
- `page5_barriers_by_income` from `page5_barriers_by_income.csv` (72 rows, 13 columns)
- `page6_evidence_table` from `page6_evidence_table.csv` (20 rows, 5 columns)
- `page6_priority_audiences` from `page6_priority_audiences.csv` (5 rows, 11 columns)
- `page7_bonus_model_metrics` from `page7_bonus_model_metrics.csv` (1 rows, 14 columns)
- `page7_bonus_top_model_coefficients` from `page7_bonus_top_model_coefficients.csv` (30 rows, 4 columns)
- `powerbi_data_manifest` from `powerbi_data_manifest.csv` (25 rows, 7 columns)

## After Import

- Follow `POWER_BI_DATA_MODEL.md` for relationships. Most tables should remain disconnected because they are pre-aggregated at different grains.
- Follow `DAX_MEASURES.md` for KPI measures.
- Use `sort_order` columns where documented.
- Use numeric KPI fields such as `weighted_value_numeric` for Page 1 and Page 2 cards.
