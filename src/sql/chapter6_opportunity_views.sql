-- Chapter 6 SQL layer: Opportunity synthesis.
-- Engine: SQLite 3.
-- Import data/processed/chapter6_priority_audiences.csv as chapter6_priority_audiences
-- and data/processed/chapter6_evidence_table.csv as chapter6_evidence_table.

DROP TABLE IF EXISTS chapter6_priority_audiences;
CREATE TABLE chapter6_priority_audiences (
  priority_rank INTEGER,
  audience_name TEXT,
  opportunity_type TEXT,
  who_they_are TEXT,
  what_the_data_shows TEXT,
  why_they_matter TEXT,
  how_they_currently_give TEXT,
  what_appears_to_motivate_them TEXT,
  what_barriers_may_matter TEXT,
  fundraising_approach_supported TEXT,
  what_data_does_not_allow_us_to_claim TEXT
);

DROP TABLE IF EXISTS chapter6_evidence_table;
CREATE TABLE chapter6_evidence_table (
  evidence_theme TEXT,
  source_chapter TEXT,
  metric TEXT,
  value TEXT,
  interpretation TEXT
);

DROP VIEW IF EXISTS vw_chapter6_priority_evidence_counts;
CREATE VIEW vw_chapter6_priority_evidence_counts AS
SELECT
  p.priority_rank,
  p.audience_name,
  p.opportunity_type,
  COUNT(e.metric) AS available_evidence_metrics
FROM chapter6_priority_audiences p
CROSS JOIN chapter6_evidence_table e
GROUP BY p.priority_rank, p.audience_name, p.opportunity_type;
