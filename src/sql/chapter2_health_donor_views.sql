-- Chapter 2 SQL layer: Health Donor.
--
-- Engine: SQLite 3.
-- Source table: sgvp_chapter2.
-- Source file:
--   Chapter 2/data/processed/sgvp_2023_chapter2_health_donor_analytical.csv
--
-- Import assumption:
--   1. Run this file once through the CREATE TABLE statement.
--   2. Import the CSV into sgvp_chapter2 using the header row as column names.
--      SQLite CLI example:
--        .mode csv
--        .import --skip 1 "Chapter 2/data/processed/sgvp_2023_chapter2_health_donor_analytical.csv" sgvp_chapter2
--   3. Run the view definitions.
--
-- This SQL recreates the important flags, weighted rate/mean aggregations,
-- segment comparisons, and volunteering valid-denominator calculations.
-- Weighted medians and exact weighted concentration are kept in Python because
-- portable SQL support for these calculations varies by engine.

DROP TABLE IF EXISTS sgvp_chapter2;

CREATE TABLE sgvp_chapter2 (
  "PUMFID" INTEGER,
  "WGHT_PER" REAL NOT NULL,
  "FG1FGIV" INTEGER,
  "donor_group" TEXT,
  "is_charitable_donor" TEXT,
  "is_health_donor" TEXT,
  "is_hospital_donor" TEXT,
  "is_broader_health_related_donor" TEXT,
  "total_donation_amount" REAL,
  "total_donation_count" REAL,
  "health_donation_amount" REAL,
  "health_donation_count" REAL,
  "hospital_donation_amount" REAL,
  "hospital_donation_count" REAL,
  "health_share_of_total_giving_pct" REAL,
  "AGEGR10" INTEGER,
  "AGEGR10_label" TEXT,
  "GENDER2" INTEGER,
  "GENDER2_label" TEXT,
  "PRV" INTEGER,
  "PRV_label" TEXT,
  "INCG2" INTEGER,
  "INCG2_label" TEXT,
  "FAMINCG2" INTEGER,
  "FAMINCG2_label" TEXT,
  "ED4CAT" INTEGER,
  "ED4CAT_label" TEXT,
  "MARSTAT" INTEGER,
  "MARSTAT_label" TEXT,
  "HSDSIZEC" INTEGER,
  "HSDSIZEC_label" TEXT,
  "DLFS" INTEGER,
  "DLFS_label" TEXT,
  "FV1FVOL" INTEGER,
  "FV1FVOL_label" TEXT,
  "FV_030" INTEGER,
  "FV_030_label" TEXT,
  "FV_100" INTEGER,
  "FV_100_label" TEXT,
  "volunteer_hours" REAL,
  "analysis_group" TEXT
);

DROP VIEW IF EXISTS vw_chapter2_flags;
CREATE VIEW vw_chapter2_flags AS
SELECT
  *,
  CASE WHEN "FG1FGIV" = 1 THEN 1 ELSE 0 END AS "sql_is_charitable_donor",
  CASE
    WHEN "FG1FGIV" = 1
     AND (COALESCE("health_donation_amount", 0) > 0 OR COALESCE("health_donation_count", 0) > 0)
    THEN 1 ELSE 0
  END AS "sql_is_health_donor",
  CASE
    WHEN "FG1FGIV" = 1
     AND (COALESCE("hospital_donation_amount", 0) > 0 OR COALESCE("hospital_donation_count", 0) > 0)
    THEN 1 ELSE 0
  END AS "sql_is_hospital_donor"
FROM sgvp_chapter2;

DROP VIEW IF EXISTS vw_chapter2_overview;
CREATE VIEW vw_chapter2_overview AS
SELECT
  COUNT(*) AS "sample_respondents",
  SUM("WGHT_PER") AS "weighted_population",
  SUM("sql_is_charitable_donor") AS "sample_charitable_donors",
  SUM(CASE WHEN "sql_is_charitable_donor" = 1 THEN "WGHT_PER" ELSE 0 END) AS "weighted_charitable_donors",
  SUM("sql_is_health_donor") AS "sample_health_donors",
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) AS "weighted_health_donors",
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / SUM("WGHT_PER") AS "weighted_health_donor_rate_population_pct",
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END)
    / NULLIF(SUM(CASE WHEN "sql_is_charitable_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_health_donor_rate_among_donors_pct",
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END) AS "weighted_health_donation_dollars",
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END)
    / NULLIF(SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_mean_health_donation",
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "total_donation_amount" * "WGHT_PER" ELSE 0 END)
    / NULLIF(SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_mean_total_giving_health_donors"
FROM vw_chapter2_flags;

DROP VIEW IF EXISTS vw_chapter2_segments;
CREATE VIEW vw_chapter2_segments AS
SELECT 'AGEGR10' AS "segment_variable", "AGEGR10" AS "segment_code", "AGEGR10_label" AS "segment_label",
  COUNT(*) AS "sample_n", SUM("WGHT_PER") AS "weighted_population", SUM("sql_is_health_donor") AS "sample_health_donors",
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) AS "weighted_health_donors",
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / SUM("WGHT_PER") AS "weighted_health_donor_rate_population_pct",
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_charitable_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_health_donor_rate_among_donors_pct",
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END) AS "weighted_health_donation_dollars",
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_mean_health_donation"
FROM vw_chapter2_flags
WHERE "AGEGR10_label" NOT IN ('Valid skip', 'Don''t know', 'Refusal', 'Not stated')
GROUP BY "AGEGR10", "AGEGR10_label"
UNION ALL
SELECT 'GENDER2', "GENDER2", "GENDER2_label", COUNT(*), SUM("WGHT_PER"), SUM("sql_is_health_donor"),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END),
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / SUM("WGHT_PER"),
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_charitable_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0)
FROM vw_chapter2_flags
WHERE "GENDER2_label" NOT IN ('Valid skip', 'Don''t know', 'Refusal', 'Not stated')
GROUP BY "GENDER2", "GENDER2_label"
UNION ALL
SELECT 'PRV', "PRV", "PRV_label", COUNT(*), SUM("WGHT_PER"), SUM("sql_is_health_donor"),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END),
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / SUM("WGHT_PER"),
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_charitable_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0)
FROM vw_chapter2_flags
WHERE "PRV_label" NOT IN ('Valid skip', 'Don''t know', 'Refusal', 'Not stated')
GROUP BY "PRV", "PRV_label"
UNION ALL
SELECT 'INCG2', "INCG2", "INCG2_label", COUNT(*), SUM("WGHT_PER"), SUM("sql_is_health_donor"),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END),
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / SUM("WGHT_PER"),
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_charitable_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0)
FROM vw_chapter2_flags
WHERE "INCG2_label" NOT IN ('Valid skip', 'Don''t know', 'Refusal', 'Not stated')
GROUP BY "INCG2", "INCG2_label"
UNION ALL
SELECT 'FAMINCG2', "FAMINCG2", "FAMINCG2_label", COUNT(*), SUM("WGHT_PER"), SUM("sql_is_health_donor"),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END),
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / SUM("WGHT_PER"),
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_charitable_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0)
FROM vw_chapter2_flags
WHERE "FAMINCG2_label" NOT IN ('Valid skip', 'Don''t know', 'Refusal', 'Not stated')
GROUP BY "FAMINCG2", "FAMINCG2_label"
UNION ALL
SELECT 'ED4CAT', "ED4CAT", "ED4CAT_label", COUNT(*), SUM("WGHT_PER"), SUM("sql_is_health_donor"),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END),
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / SUM("WGHT_PER"),
  100.0 * SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_charitable_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END),
  SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "health_donation_amount" * "WGHT_PER" ELSE 0 END) / NULLIF(SUM(CASE WHEN "sql_is_health_donor" = 1 THEN "WGHT_PER" ELSE 0 END), 0)
FROM vw_chapter2_flags
WHERE "ED4CAT_label" NOT IN ('Valid skip', 'Don''t know', 'Refusal', 'Not stated')
GROUP BY "ED4CAT", "ED4CAT_label";

DROP VIEW IF EXISTS vw_chapter2_volunteering;
CREATE VIEW vw_chapter2_volunteering AS
SELECT
  "analysis_group" AS "comparison_group",
  COUNT(*) AS "sample_n",
  SUM("WGHT_PER") AS "weighted_population",
  SUM(CASE WHEN "FV1FVOL" = 1 THEN 1 ELSE 0 END) AS "sample_volunteer_n",
  SUM(CASE WHEN "FV1FVOL" = 1 THEN "WGHT_PER" ELSE 0 END) AS "weighted_volunteers",
  SUM(CASE WHEN "FV1FVOL" IN (1, 2) THEN "WGHT_PER" ELSE 0 END) AS "weighted_volunteering_valid_denominator",
  100.0 * SUM(CASE WHEN "FV1FVOL" = 1 THEN "WGHT_PER" ELSE 0 END)
    / NULLIF(SUM(CASE WHEN "FV1FVOL" IN (1, 2) THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_volunteer_rate_pct",
  SUM(CASE WHEN "FV_030" = 1 THEN 1 ELSE 0 END) AS "sample_fundraising_volunteer_n",
  SUM(CASE WHEN "FV_030" = 1 THEN "WGHT_PER" ELSE 0 END) AS "weighted_fundraising_volunteers",
  SUM(CASE WHEN "FV_030" IN (1, 2) THEN "WGHT_PER" ELSE 0 END) AS "weighted_fundraising_valid_denominator",
  100.0 * SUM(CASE WHEN "FV_030" = 1 THEN "WGHT_PER" ELSE 0 END)
    / NULLIF(SUM(CASE WHEN "FV_030" IN (1, 2) THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_fundraising_volunteer_rate_pct",
  SUM(CASE WHEN "FV_100" = 1 THEN 1 ELSE 0 END) AS "sample_healthcare_support_volunteer_n",
  SUM(CASE WHEN "FV_100" = 1 THEN "WGHT_PER" ELSE 0 END) AS "weighted_healthcare_support_volunteers",
  SUM(CASE WHEN "FV_100" IN (1, 2) THEN "WGHT_PER" ELSE 0 END) AS "weighted_healthcare_support_valid_denominator",
  100.0 * SUM(CASE WHEN "FV_100" = 1 THEN "WGHT_PER" ELSE 0 END)
    / NULLIF(SUM(CASE WHEN "FV_100" IN (1, 2) THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_healthcare_support_volunteer_rate_pct",
  SUM(CASE WHEN "FV1FVOL" = 1 THEN "volunteer_hours" * "WGHT_PER" ELSE 0 END)
    / NULLIF(SUM(CASE WHEN "FV1FVOL" = 1 THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_mean_volunteer_hours_among_volunteers"
FROM vw_chapter2_flags
WHERE "analysis_group" IN ('Health donors', 'Non-Health donors', 'Non-donors')
GROUP BY "analysis_group"
UNION ALL
SELECT
  'All charitable donors' AS "comparison_group",
  COUNT(*) AS "sample_n",
  SUM("WGHT_PER") AS "weighted_population",
  SUM(CASE WHEN "FV1FVOL" = 1 THEN 1 ELSE 0 END) AS "sample_volunteer_n",
  SUM(CASE WHEN "FV1FVOL" = 1 THEN "WGHT_PER" ELSE 0 END) AS "weighted_volunteers",
  SUM(CASE WHEN "FV1FVOL" IN (1, 2) THEN "WGHT_PER" ELSE 0 END) AS "weighted_volunteering_valid_denominator",
  100.0 * SUM(CASE WHEN "FV1FVOL" = 1 THEN "WGHT_PER" ELSE 0 END)
    / NULLIF(SUM(CASE WHEN "FV1FVOL" IN (1, 2) THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_volunteer_rate_pct",
  SUM(CASE WHEN "FV_030" = 1 THEN 1 ELSE 0 END) AS "sample_fundraising_volunteer_n",
  SUM(CASE WHEN "FV_030" = 1 THEN "WGHT_PER" ELSE 0 END) AS "weighted_fundraising_volunteers",
  SUM(CASE WHEN "FV_030" IN (1, 2) THEN "WGHT_PER" ELSE 0 END) AS "weighted_fundraising_valid_denominator",
  100.0 * SUM(CASE WHEN "FV_030" = 1 THEN "WGHT_PER" ELSE 0 END)
    / NULLIF(SUM(CASE WHEN "FV_030" IN (1, 2) THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_fundraising_volunteer_rate_pct",
  SUM(CASE WHEN "FV_100" = 1 THEN 1 ELSE 0 END) AS "sample_healthcare_support_volunteer_n",
  SUM(CASE WHEN "FV_100" = 1 THEN "WGHT_PER" ELSE 0 END) AS "weighted_healthcare_support_volunteers",
  SUM(CASE WHEN "FV_100" IN (1, 2) THEN "WGHT_PER" ELSE 0 END) AS "weighted_healthcare_support_valid_denominator",
  100.0 * SUM(CASE WHEN "FV_100" = 1 THEN "WGHT_PER" ELSE 0 END)
    / NULLIF(SUM(CASE WHEN "FV_100" IN (1, 2) THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_healthcare_support_volunteer_rate_pct",
  SUM(CASE WHEN "FV1FVOL" = 1 THEN "volunteer_hours" * "WGHT_PER" ELSE 0 END)
    / NULLIF(SUM(CASE WHEN "FV1FVOL" = 1 THEN "WGHT_PER" ELSE 0 END), 0) AS "weighted_mean_volunteer_hours_among_volunteers"
FROM vw_chapter2_flags
WHERE "sql_is_charitable_donor" = 1;
