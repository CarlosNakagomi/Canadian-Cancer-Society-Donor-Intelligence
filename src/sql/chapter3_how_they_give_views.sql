-- Chapter 3 SQL layer: How They Give.
-- Engine: SQLite 3.
-- Import data/processed/sgvp_2023_chapter3_how_they_give_analytical.csv as sgvp_chapter3.

DROP TABLE IF EXISTS sgvp_chapter3;
CREATE TABLE sgvp_chapter3 (
  PUMFID INTEGER, WGHT_PER REAL, analysis_group TEXT, is_charitable_donor INTEGER, is_health_donor INTEGER,
  health_donation_amount REAL, health_donation_count REAL, total_donation_amount REAL, total_donation_count REAL,
  mail_used INTEGER, mail_count REAL, mail_amount REAL,
  telephone_used INTEGER, telephone_count REAL, telephone_amount REAL,
  television_used INTEGER, television_count REAL, television_amount REAL,
  online_used INTEGER, online_count REAL, online_amount REAL,
  own_initiative_used INTEGER, own_initiative_count REAL, own_initiative_amount REAL,
  charity_event_used INTEGER, charity_event_count REAL, charity_event_amount REAL,
  in_memory_used INTEGER, in_memory_count REAL, in_memory_amount REAL,
  work_used INTEGER, work_count REAL, work_amount REAL,
  door_to_door_used INTEGER, door_to_door_count REAL, door_to_door_amount REAL,
  shopping_centre_used INTEGER, shopping_centre_count REAL, shopping_centre_amount REAL,
  place_of_worship_used INTEGER, place_of_worship_count REAL, place_of_worship_amount REAL,
  sponsoring_someone_used INTEGER, sponsoring_someone_count REAL, sponsoring_someone_amount REAL,
  other_used INTEGER, other_count REAL, other_amount REAL,
  fundraising_volunteer_segment TEXT
);

DROP VIEW IF EXISTS vw_chapter3_channel_summary;
CREATE VIEW vw_chapter3_channel_summary AS
SELECT 'mail' AS channel_key, 'Mail' AS channel_label, 1 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN mail_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN mail_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN mail_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN mail_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN mail_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN mail_used = 1 THEN mail_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'telephone' AS channel_key, 'Telephone' AS channel_label, 2 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN telephone_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN telephone_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN telephone_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN telephone_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN telephone_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN telephone_used = 1 THEN telephone_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'television' AS channel_key, 'Television' AS channel_label, 3 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN television_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN television_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN television_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN television_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN television_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN television_used = 1 THEN television_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'online' AS channel_key, 'Online' AS channel_label, 4 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN online_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN online_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN online_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN online_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN online_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN online_used = 1 THEN online_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'own_initiative' AS channel_key, 'On own initiative' AS channel_label, 5 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN own_initiative_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN own_initiative_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN own_initiative_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN own_initiative_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN own_initiative_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN own_initiative_used = 1 THEN own_initiative_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'charity_event' AS channel_key, 'Charity event' AS channel_label, 6 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN charity_event_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN charity_event_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN charity_event_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN charity_event_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN charity_event_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN charity_event_used = 1 THEN charity_event_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'in_memory' AS channel_key, 'In memory of someone' AS channel_label, 7 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN in_memory_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN in_memory_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN in_memory_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN in_memory_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN in_memory_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN in_memory_used = 1 THEN in_memory_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'work' AS channel_key, 'Work' AS channel_label, 8 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN work_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN work_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN work_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN work_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN work_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN work_used = 1 THEN work_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'door_to_door' AS channel_key, 'Door-to-door canvassing' AS channel_label, 9 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN door_to_door_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN door_to_door_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN door_to_door_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN door_to_door_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN door_to_door_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN door_to_door_used = 1 THEN door_to_door_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'shopping_centre' AS channel_key, 'Shopping centre' AS channel_label, 10 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN shopping_centre_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN shopping_centre_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN shopping_centre_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN shopping_centre_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN shopping_centre_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN shopping_centre_used = 1 THEN shopping_centre_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'place_of_worship' AS channel_key, 'Place of worship' AS channel_label, 11 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN place_of_worship_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN place_of_worship_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN place_of_worship_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN place_of_worship_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN place_of_worship_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN place_of_worship_used = 1 THEN place_of_worship_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'sponsoring_someone' AS channel_key, 'Sponsoring someone' AS channel_label, 12 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN sponsoring_someone_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN sponsoring_someone_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN sponsoring_someone_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN sponsoring_someone_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN sponsoring_someone_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN sponsoring_someone_used = 1 THEN sponsoring_someone_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group
UNION ALL
SELECT 'other' AS channel_key, 'Other' AS channel_label, 13 AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN other_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN other_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN other_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN other_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN other_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN other_used = 1 THEN other_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group;
