-- Chapter 4 SQL layer: Why They Give.
-- Engine: SQLite 3.
-- Import data/processed/sgvp_2023_chapter4_why_they_give_analytical.csv as sgvp_chapter4.

DROP TABLE IF EXISTS sgvp_chapter4;
CREATE TABLE sgvp_chapter4 (
  PUMFID INTEGER, WGHT_PER REAL, analysis_group TEXT, is_charitable_donor INTEGER, is_health_donor INTEGER,
  health_donation_amount REAL, health_donation_count REAL, total_donation_amount REAL, total_donation_count REAL,
  AGEGR10_label TEXT, GENDER2_label TEXT, INCG2_label TEXT, ED4CAT_label TEXT,
  RG_010 INTEGER,
  RG_020 INTEGER,
  RG_030 INTEGER,
  RG_035 INTEGER,
  RG_040 INTEGER,
  RG_050 INTEGER,
  RG_060 INTEGER,
  RG_070 INTEGER
);

DROP VIEW IF EXISTS vw_chapter4_motivation_summary;
CREATE VIEW vw_chapter4_motivation_summary AS
SELECT 'RG_010' AS motivation_variable, 'Personally affected' AS motivation_label, 1 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN RG_010 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN RG_010 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN RG_010 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN RG_010 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN RG_010 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter4
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'RG_020' AS motivation_variable, 'Tax credit' AS motivation_label, 2 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN RG_020 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN RG_020 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN RG_020 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN RG_020 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN RG_020 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter4
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'RG_030' AS motivation_variable, 'Religious reasons' AS motivation_label, 3 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN RG_030 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN RG_030 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN RG_030 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN RG_030 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN RG_030 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter4
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'RG_035' AS motivation_variable, 'Spiritual or other beliefs' AS motivation_label, 4 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN RG_035 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN RG_035 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN RG_035 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN RG_035 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN RG_035 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter4
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'RG_040' AS motivation_variable, 'Belief in the cause' AS motivation_label, 5 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN RG_040 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN RG_040 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN RG_040 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN RG_040 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN RG_040 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter4
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'RG_050' AS motivation_variable, 'Compassion' AS motivation_label, 6 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN RG_050 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN RG_050 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN RG_050 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN RG_050 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN RG_050 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter4
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'RG_060' AS motivation_variable, 'Community contribution' AS motivation_label, 7 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN RG_060 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN RG_060 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN RG_060 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN RG_060 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN RG_060 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter4
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'RG_070' AS motivation_variable, 'Asked by someone you know' AS motivation_label, 8 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN RG_070 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN RG_070 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN RG_070 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN RG_070 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN RG_070 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter4
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group;
