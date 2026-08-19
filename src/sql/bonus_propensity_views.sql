-- Bonus SQL layer: Health donor propensity analytical base.
-- Engine: SQLite 3.
-- Import data/processed/bonus_health_donor_propensity_scored.csv as bonus_propensity_scored.

DROP TABLE IF EXISTS bonus_propensity_scored;
CREATE TABLE bonus_propensity_scored (
  PUMFID INTEGER,
  WGHT_PER REAL,
  is_health_donor INTEGER,
  split TEXT,
  predicted_probability REAL,
  predicted_class INTEGER
);

DROP VIEW IF EXISTS vw_bonus_score_summary;
CREATE VIEW vw_bonus_score_summary AS
SELECT
  split,
  COUNT(*) AS sample_n,
  SUM(WGHT_PER) AS weighted_population,
  AVG(is_health_donor) AS sample_health_donor_rate,
  AVG(predicted_probability) AS mean_predicted_probability
FROM bonus_propensity_scored
GROUP BY split;
