-- Chapter 5 SQL layer: Why They Do Not Give More.
-- Engine: SQLite 3.
-- Import data/processed/sgvp_2023_chapter5_barriers_analytical.csv as sgvp_chapter5.

DROP TABLE IF EXISTS sgvp_chapter5;
CREATE TABLE sgvp_chapter5 (
  PUMFID INTEGER, WGHT_PER REAL, analysis_group TEXT, is_charitable_donor INTEGER, is_health_donor INTEGER,
  health_donation_amount REAL, health_donation_count REAL, total_donation_amount REAL, total_donation_count REAL,
  AGEGR10_label TEXT, INCG2_label TEXT, ED4CAT_label TEXT, health_value_segment TEXT, health_frequency_segment TEXT,
  NG_020 INTEGER,
  NG_030 INTEGER,
  NG_040 INTEGER,
  NG_050 INTEGER,
  NG_060 INTEGER,
  NG_070 INTEGER,
  NG_080 INTEGER,
  NG_090 INTEGER,
  NG_110 INTEGER,
  NG_130 INTEGER,
  NG_150 INTEGER,
  NG_160 INTEGER,
  NG_120A INTEGER,
  NG_120B INTEGER,
  NG_120C INTEGER,
  NG_120D INTEGER,
  NG_140A INTEGER,
  NG_140B INTEGER,
  NG_140C INTEGER,
  NG_140D INTEGER,
  NG_140E INTEGER,
  NG_140F INTEGER
);

DROP VIEW IF EXISTS vw_chapter5_barrier_summary;
CREATE VIEW vw_chapter5_barrier_summary AS
SELECT 'NG_020' AS barrier_variable, 'Already gave enough' AS barrier_label, 'Current giving satisfied' AS barrier_category, 'Core' AS applicability, 1 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_020 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_020 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_020 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_020 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_020 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_030' AS barrier_variable, 'Could not afford a larger donation' AS barrier_label, 'Financial' AS barrier_category, 'Core' AS applicability, 2 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_030 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_030 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_030 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_030 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_030 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_040' AS barrier_variable, 'No one asked' AS barrier_label, 'Solicitation/opportunity' AS barrier_category, 'Core' AS applicability, 3 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_040 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_040 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_040 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_040 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_040 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_050' AS barrier_variable, 'Did not know where to make other donations' AS barrier_label, 'Information/access' AS barrier_category, 'Core' AS applicability, 4 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_050 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_050 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_050 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_050 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_050 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_060' AS barrier_variable, 'Hard to find a cause' AS barrier_label, 'Information/access' AS barrier_category, 'Core' AS applicability, 5 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_060 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_060 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_060 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_060 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_060 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_070' AS barrier_variable, 'Gave time instead' AS barrier_label, 'Alternative contribution' AS barrier_category, 'Core' AS applicability, 6 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_070 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_070 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_070 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_070 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_070 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_080' AS barrier_variable, 'Gave directly to people' AS barrier_label, 'Alternative contribution' AS barrier_category, 'Core' AS applicability, 7 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_080 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_080 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_080 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_080 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_080 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_090' AS barrier_variable, 'Tax credit not enough incentive' AS barrier_label, 'Incentive' AS barrier_category, 'Core' AS applicability, 8 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_090 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_090 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_090 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_090 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_090 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_110' AS barrier_variable, 'Money would not be used efficiently' AS barrier_label, 'Trust/efficiency' AS barrier_category, 'Core' AS applicability, 9 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_110 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_110 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_110 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_110 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_110 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_130' AS barrier_variable, 'Did not like way requests were made' AS barrier_label, 'Solicitation concern' AS barrier_category, 'Core' AS applicability, 10 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_130 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_130 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_130 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_130 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_130 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_150' AS barrier_variable, 'So many organizations' AS barrier_label, 'Choice overload' AS barrier_category, 'Core' AS applicability, 11 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_150 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_150 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_150 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_150 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_150 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_160' AS barrier_variable, 'Charity fraud' AS barrier_label, 'Trust/efficiency' AS barrier_category, 'Core' AS applicability, 12 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_160 IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_160 = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_160 = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_160 = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_160 IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_120A' AS barrier_variable, 'Not efficient - Fundraising' AS barrier_label, 'Trust/efficiency detail' AS barrier_category, 'Follow-up to NG_110' AS applicability, 13 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_120A IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_120A = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_120A = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_120A = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_120A IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_120B' AS barrier_variable, 'Not efficient - Impact' AS barrier_label, 'Trust/efficiency detail' AS barrier_category, 'Follow-up to NG_110' AS applicability, 14 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_120B IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_120B = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_120B = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_120B = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_120B IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_120C' AS barrier_variable, 'Not efficient - Explanation' AS barrier_label, 'Trust/efficiency detail' AS barrier_category, 'Follow-up to NG_110' AS applicability, 15 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_120C IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_120C = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_120C = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_120C = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_120C IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_120D' AS barrier_variable, 'Not efficient - Other' AS barrier_label, 'Trust/efficiency detail' AS barrier_category, 'Follow-up to NG_110' AS applicability, 16 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_120D IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_120D = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_120D = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_120D = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_120D IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_140A' AS barrier_variable, 'Requests - Time of day' AS barrier_label, 'Solicitation detail' AS barrier_category, 'Follow-up to NG_130' AS applicability, 17 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_140A IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_140A = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_140A = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_140A = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_140A IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_140B' AS barrier_variable, 'Requests - Number' AS barrier_label, 'Solicitation detail' AS barrier_category, 'Follow-up to NG_130' AS applicability, 18 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_140B IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_140B = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_140B = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_140B = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_140B IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_140C' AS barrier_variable, 'Requests - Tone' AS barrier_label, 'Solicitation detail' AS barrier_category, 'Follow-up to NG_130' AS applicability, 19 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_140C IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_140C = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_140C = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_140C = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_140C IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_140D' AS barrier_variable, 'Requests - Multiple' AS barrier_label, 'Solicitation detail' AS barrier_category, 'Follow-up to NG_130' AS applicability, 20 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_140D IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_140D = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_140D = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_140D = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_140D IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_140E' AS barrier_variable, 'Requests - Method' AS barrier_label, 'Solicitation detail' AS barrier_category, 'Follow-up to NG_130' AS applicability, 21 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_140E IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_140E = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_140E = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_140E = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_140E IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group
UNION ALL
SELECT 'NG_140F' AS barrier_variable, 'Requests - Other reason' AS barrier_label, 'Solicitation detail' AS barrier_category, 'Follow-up to NG_130' AS applicability, 22 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_group_n,
  SUM(WGHT_PER) AS weighted_group_population,
  SUM(CASE WHEN NG_140F IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN NG_140F = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN NG_140F = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN NG_140F = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN NG_140F IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter5
WHERE analysis_group IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY analysis_group;
