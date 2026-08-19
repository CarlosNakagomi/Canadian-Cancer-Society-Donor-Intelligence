# PowerBI Excel Import Map

Workbook: `data\PowerBI_Data.xlsx`

Source folder: `outputs\powerbi`

Total CSV datasets included: 26
Total worksheets: 27

| CSV filename | Worksheet | Excel table name | Dashboard page | Purpose | Rows | Columns |
|---|---|---|---|---|---:|---:|
| `Generated workbook manifest` | `MANIFEST` | `tbl_MANIFEST` | Documentation | Workbook import map | 26 | 7 |
| `page1_canadian_donor_overall.csv` | `p1_can_dnr_overall` | `tbl_page1_canadian_donor_overall` | Page 1 | Dashboard KPI table; metric rows; normalized numeric KPI columns added for Power BI typing | 7 | 7 |
| `page1_canadian_donor_segments.csv` | `p1_can_dnr_segments` | `tbl_page1_canadian_donor_segments` | Page 1 | Segment-variable by category | 35 | 13 |
| `page1_donation_amount_bands.csv` | `p1_don_amount_bands` | `tbl_page1_donation_amount_bands` | Page 1 | Donation amount band among donors | 7 | 7 |
| `page1_donation_frequency.csv` | `p1_don_freq` | `tbl_page1_donation_frequency` | Page 1 | Donation count among donors | 24 | 4 |
| `page2_health_donation_distribution.csv` | `p2_hlth_don_dist` | `tbl_page2_health_donation_distribution` | Page 2 | Health donation amount band | 7 | 7 |
| `page2_health_donor_group_comparison.csv` | `p2_hlth_dnr_group_comparison` | `tbl_page2_health_donor_group_comparison` | Page 2 | Comparison group summary | 5 | 19 |
| `page2_health_donor_overview.csv` | `p2_hlth_dnr_overview` | `tbl_page2_health_donor_overview` | Page 2 | Dashboard KPI table; metric rows; normalized numeric KPI columns added for Power BI typing | 13 | 7 |
| `page2_health_donor_volunteering.csv` | `p2_hlth_dnr_volunteering` | `tbl_page2_health_donor_volunteering` | Page 2 | Comparison group volunteering summary | 4 | 18 |
| `page2_health_profile_age.csv` | `p2_hlth_prof_age` | `tbl_page2_health_profile_age` | Page 2 | Age category | 7 | 20 |
| `page2_health_profile_education.csv` | `p2_hlth_prof_education` | `tbl_page2_health_profile_education` | Page 2 | Education category | 4 | 20 |
| `page2_health_profile_income.csv` | `p2_hlth_prof_income` | `tbl_page2_health_profile_income` | Page 2 | Personal income category | 6 | 20 |
| `page2_health_profile_province.csv` | `p2_hlth_prof_province` | `tbl_page2_health_profile_province` | Page 2 | Province category | 10 | 21 |
| `page3_channel_by_health_value.csv` | `p3_channel_by_hlth_value` | `tbl_page3_channel_by_health_value` | Page 3 | Health value segment by channel | 65 | 12 |
| `page3_giving_behaviour_summary.csv` | `p3_giv_behaviour_sum` | `tbl_page3_giving_behaviour_summary` | Page 3 | Giving behaviour response distribution | 36 | 10 |
| `page3_giving_channel_summary.csv` | `p3_giv_channel_sum` | `tbl_page3_giving_channel_summary` | Page 3 | Channel by comparison group | 39 | 17 |
| `page4_motivation_by_age.csv` | `p4_motiv_by_age` | `tbl_page4_motivation_by_age` | Page 4 | Health donor age segment by motivation | 56 | 12 |
| `page4_motivation_by_health_value.csv` | `p4_motiv_by_hlth_value` | `tbl_page4_motivation_by_health_value` | Page 4 | Health value segment by motivation | 40 | 12 |
| `page4_motivation_summary.csv` | `p4_motiv_sum` | `tbl_page4_motivation_summary` | Page 4 | Motivation by comparison group | 24 | 12 |
| `page5_barrier_category_summary.csv` | `p5_bar_category_sum` | `tbl_page5_barrier_category_summary` | Page 5 | Barrier category by comparison group | 27 | 5 |
| `page5_barrier_summary.csv` | `p5_bar_sum` | `tbl_page5_barrier_summary` | Page 5 | Barrier by comparison group | 66 | 14 |
| `page5_barriers_by_income.csv` | `p5_bars_by_income` | `tbl_page5_barriers_by_income` | Page 5 | Health donor income segment by barrier | 72 | 13 |
| `page6_evidence_table.csv` | `p6_evidence_table` | `tbl_page6_evidence_table` | Page 6 | Evidence metric rows | 20 | 5 |
| `page6_priority_audiences.csv` | `p6_priority_audiences` | `tbl_page6_priority_audiences` | Page 6 | Priority audience | 5 | 11 |
| `page7_bonus_model_metrics.csv` | `p7_bonus_model_metrics` | `tbl_page7_bonus_model_metrics` | Page 7 | Model metric rows | 1 | 14 |
| `page7_bonus_top_model_coefficients.csv` | `p7_bonus_top_model_coef` | `tbl_page7_bonus_top_model_coefficients` | Page 7 | Model feature coefficient rows | 30 | 4 |
| `powerbi_data_manifest.csv` | `powerbi_data_manifest` | `tbl_powerbi_data_manifest` | Documentation | Import support table | 25 | 7 |

## Shortened Worksheet Names

- `page1_canadian_donor_overall` -> `p1_can_dnr_overall`
- `page1_canadian_donor_segments` -> `p1_can_dnr_segments`
- `page1_donation_amount_bands` -> `p1_don_amount_bands`
- `page1_donation_frequency` -> `p1_don_freq`
- `page2_health_donation_distribution` -> `p2_hlth_don_dist`
- `page2_health_donor_group_comparison` -> `p2_hlth_dnr_group_comparison`
- `page2_health_donor_overview` -> `p2_hlth_dnr_overview`
- `page2_health_donor_volunteering` -> `p2_hlth_dnr_volunteering`
- `page2_health_profile_age` -> `p2_hlth_prof_age`
- `page2_health_profile_education` -> `p2_hlth_prof_education`
- `page2_health_profile_income` -> `p2_hlth_prof_income`
- `page2_health_profile_province` -> `p2_hlth_prof_province`
- `page3_channel_by_health_value` -> `p3_channel_by_hlth_value`
- `page3_giving_behaviour_summary` -> `p3_giv_behaviour_sum`
- `page3_giving_channel_summary` -> `p3_giv_channel_sum`
- `page4_motivation_by_age` -> `p4_motiv_by_age`
- `page4_motivation_by_health_value` -> `p4_motiv_by_hlth_value`
- `page4_motivation_summary` -> `p4_motiv_sum`
- `page5_barrier_category_summary` -> `p5_bar_category_sum`
- `page5_barrier_summary` -> `p5_bar_sum`
- `page5_barriers_by_income` -> `p5_bars_by_income`
- `page6_evidence_table` -> `p6_evidence_table`
- `page6_priority_audiences` -> `p6_priority_audiences`
- `page7_bonus_model_metrics` -> `p7_bonus_model_metrics`
- `page7_bonus_top_model_coefficients` -> `p7_bonus_top_model_coef`

## Validation

Validation details: `docs\powerbi\POWERBI_EXCEL_VALIDATION.csv`

- Every source CSV is represented exactly once as a data worksheet.
- The first worksheet is `MANIFEST`.
- Each worksheet has a matching Excel table.
- No source CSV files were modified.
- Numeric columns inferred from the CSV content were written as numeric worksheet cells where feasible.