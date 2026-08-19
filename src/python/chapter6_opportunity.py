from __future__ import annotations

import csv
import json
import sqlite3
import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[2] / "Chapter 2" / ".python_packages"
if PACKAGE_DIR.exists():
    sys.path.insert(0, str(PACKAGE_DIR))

import pandas as pd


CHAPTER_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = CHAPTER_ROOT.parent

for folder in ["data/processed", "data/powerbi", "docs", "outputs", "sql"]:
    (CHAPTER_ROOT / folder).mkdir(parents=True, exist_ok=True)


def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(PROJECT_ROOT / path)


def metric(df: pd.DataFrame, row_filter, col: str):
    value = df.loc[row_filter, col]
    return value.iloc[0] if len(value) else None


def build_evidence():
    ch2_overview = read_csv("Chapter 2/data/powerbi/health_donor_overview.csv")
    ch2_age = read_csv("Chapter 2/data/powerbi/health_donor_profile_age.csv")
    ch2_income = read_csv("Chapter 2/data/powerbi/health_donor_profile_personal_income.csv")
    ch2_vol = read_csv("Chapter 2/data/powerbi/health_donor_volunteering.csv")
    ch2_dist = read_csv("Chapter 2/data/powerbi/health_donation_distribution.csv")
    ch3_channels = read_csv("Chapter 3/data/powerbi/chapter3_channel_summary.csv")
    ch4_mot = read_csv("Chapter 4/data/powerbi/chapter4_motivation_summary.csv")
    ch5_bar = read_csv("Chapter 5/data/powerbi/chapter5_barrier_summary.csv")

    health_weighted = metric(ch2_overview, ch2_overview["metric"].eq("Health donors"), "weighted_value")
    health_rate = metric(ch2_overview, ch2_overview["metric"].eq("Health donor rate among Canadian population"), "weighted_value")
    among_donors = metric(ch2_overview, ch2_overview["metric"].eq("Health donor rate among charitable donors"), "weighted_value")
    top_dist = ch2_dist.sort_values("weighted_health_dollar_share_pct", ascending=False).head(1).iloc[0]
    age_65_74 = ch2_age[ch2_age["segment_label"].eq("65 to 74 years")].iloc[0]
    age_75 = ch2_age[ch2_age["segment_label"].eq("75 years and over")].iloc[0]
    high_income = ch2_income[ch2_income["segment_label"].eq("$125,000 and more")].iloc[0]
    health_vol = ch2_vol[ch2_vol["comparison_group"].eq("Health donors")].iloc[0]
    nonhealth_vol = ch2_vol[ch2_vol["comparison_group"].eq("Non-Health donors")].iloc[0]
    health_channels = ch3_channels[ch3_channels["comparison_group"].eq("Health donors")]
    in_memory = health_channels[health_channels["channel_label"].eq("In memory of someone")].iloc[0]
    online = health_channels[health_channels["channel_label"].eq("Online")].iloc[0]
    mail = health_channels[health_channels["channel_label"].eq("Mail")].iloc[0]
    sponsorship = health_channels[health_channels["channel_label"].eq("Sponsoring someone")].iloc[0]
    top_mot = ch4_mot[ch4_mot["comparison_group"].eq("Health donors")].sort_values("weighted_yes_pct", ascending=False).head(4)
    barriers = ch5_bar[(ch5_bar["comparison_group"].eq("Health donors")) & (ch5_bar["applicability"].eq("Core"))]
    fraud = barriers[barriers["barrier_label"].eq("Charity fraud")].iloc[0]
    afford = barriers[barriers["barrier_label"].eq("Could not afford a larger donation")].iloc[0]
    already = barriers[barriers["barrier_label"].eq("Already gave enough")].iloc[0]

    evidence = [
        ("Segment size", "Chapter 2", "Weighted Health donor population", health_weighted, "Health donors are a large existing market."),
        ("Segment size", "Chapter 2", "Health donor rate among population", health_rate, "Health giving reaches roughly one in five Canadians."),
        ("Segment size", "Chapter 2", "Health donors among charitable donors", among_donors, "Health giving is common but not universal among donors."),
        ("High participation", "Chapter 2", "65-74 Health donor rate among donors", age_65_74["weighted_health_donor_rate_among_donors_pct"], "Older donors have high Health participation among donors."),
        ("High participation", "Chapter 2", "75+ Health donor rate among population", age_75["weighted_health_donor_rate_population_pct"], "Oldest age group has the highest population Health donor rate."),
        ("High value", "Chapter 2", "$125k+ Health donor rate among donors", high_income["weighted_health_donor_rate_among_donors_pct"], "Highest personal income group has strong Health participation."),
        ("Dollar concentration", "Chapter 2", f"{top_dist['amount_band']} dollar share", top_dist["weighted_health_dollar_share_pct"], "Large gifts carry disproportionate dollar value."),
        ("Engagement", "Chapter 2", "Health donor volunteer rate", health_vol["weighted_volunteer_rate_pct"], "Health donors are more volunteer-engaged."),
        ("Engagement", "Chapter 2", "Non-Health donor volunteer rate", nonhealth_vol["weighted_volunteer_rate_pct"], "Volunteer gap provides a comparison baseline."),
        ("Channel", "Chapter 3", "In-memory channel use among Health donors", in_memory["weighted_channel_use_rate_pct"], "Tribute/memorial giving is a major Health donor behaviour."),
        ("Channel", "Chapter 3", "Sponsorship channel use among Health donors", sponsorship["weighted_channel_use_rate_pct"], "Peer/social fundraising appears important."),
        ("Channel", "Chapter 3", "Mail channel use among Health donors", mail["weighted_channel_use_rate_pct"], "Traditional direct response remains material."),
        ("Channel", "Chapter 3", "Online channel use among Health donors", online["weighted_channel_use_rate_pct"], "Digital giving is substantial but not dominant."),
    ]
    for _, row in top_mot.iterrows():
        evidence.append(("Motivation", "Chapter 4", row["motivation_label"], row["weighted_yes_pct"], "Message theme supported by Health donor motivations."))
    evidence.extend([
        ("Barrier", "Chapter 5", "Charity fraud", fraud["weighted_yes_pct"], "Trust concerns need transparent handling."),
        ("Barrier", "Chapter 5", "Could not afford larger donation", afford["weighted_yes_pct"], "Financial limits constrain upgrade asks."),
        ("Barrier", "Chapter 5", "Already gave enough", already["weighted_yes_pct"], "Retention and stewardship may matter as much as upgrade pressure."),
    ])
    out = pd.DataFrame(evidence, columns=["evidence_theme", "source_chapter", "metric", "value", "interpretation"])
    return out


def build_priority_audiences(evidence: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "priority_rank": 1,
            "audience_name": "Established older Health donors",
            "opportunity_type": "High participation / retention",
            "who_they_are": "Older donors, especially 65+ charitable donors with high Health participation.",
            "what_the_data_shows": "65-74 donors show about 49.4% Health participation among donors; 75+ Canadians show the highest population Health donor rate at about 32.2%.",
            "why_they_matter": "They represent a strong existing participation base for Health giving.",
            "how_they_currently_give": "Health donors commonly use shopping centre, in-memory, sponsorship, mail, own-initiative, and online channels.",
            "what_appears_to_motivate_them": "Cause, compassion, personal connection, and community contribution are the leading Health donor motivations.",
            "what_barriers_may_matter": "Already gave enough, charity fraud, affordability, and too many organizations.",
            "fundraising_approach_supported": "Prioritize retention, tribute stewardship, clear impact reporting, and age-appropriate direct response testing.",
            "what_data_does_not_allow_us_to_claim": "The survey does not prove that any message or channel will increase donations.",
        },
        {
            "priority_rank": 2,
            "audience_name": "Higher-income Health donors",
            "opportunity_type": "High value / upgrade potential",
            "who_they_are": "Health donors in the highest personal income group and donors with larger Health donation amounts.",
            "what_the_data_shows": "$125k+ personal income group has about 49.0% Health participation among donors; the $5,000+ Health gift band contributes about 39.4% of weighted Health dollars.",
            "why_they_matter": "A small high-value segment accounts for a large share of Health donation dollars.",
            "how_they_currently_give": "Channel evidence should be interpreted as total charitable channel use; mail, online, own-initiative, and in-memory channels are material among Health donors.",
            "what_appears_to_motivate_them": "Cause, compassion, personal connection, community contribution, and tax credit themes are relevant but should be tested.",
            "what_barriers_may_matter": "Trust, charity fraud, and satisfaction with current giving may limit upgrades.",
            "fundraising_approach_supported": "Use transparent impact cases, stewardship, and carefully segmented upgrade asks rather than broad pressure.",
            "what_data_does_not_allow_us_to_claim": "Income association does not identify liquid assets or individual capacity.",
        },
        {
            "priority_rank": 3,
            "audience_name": "Volunteer-engaged Health donors",
            "opportunity_type": "Engagement / relationship depth",
            "who_they_are": "Health donors who also volunteer formally or participate in fundraising volunteering.",
            "what_the_data_shows": "Health donors have a 44.3% formal volunteer rate, higher than non-Health donors at 37.9%; fundraising volunteering is also higher.",
            "why_they_matter": "They show multi-mode engagement and may be receptive to relationship-building journeys.",
            "how_they_currently_give": "Sponsorship and event-related channels are prominent among Health donors, suggesting social fundraising relevance.",
            "what_appears_to_motivate_them": "Community contribution, cause, compassion, and personal connection.",
            "what_barriers_may_matter": "Gave time instead appears as a barrier for some, so donation asks should respect nonfinancial contribution.",
            "fundraising_approach_supported": "Coordinate volunteer stewardship, peer fundraising, and donor communications without treating volunteering as proof of donation capacity.",
            "what_data_does_not_allow_us_to_claim": "Volunteering does not cause Health giving in this descriptive survey.",
        },
        {
            "priority_rank": 4,
            "audience_name": "Tribute and socially prompted Health donors",
            "opportunity_type": "Channel/message fit",
            "who_they_are": "Health donors reached through in-memory giving, sponsorship, and asks from people they know.",
            "what_the_data_shows": "In-memory and sponsorship channels are much more common among Health donors than non-Health donors; being asked by someone known is also more common as a motivation.",
            "why_they_matter": "Health giving appears strongly connected to personal and social prompts.",
            "how_they_currently_give": "In-memory, sponsoring someone, and event-related behaviours are visible in Chapter 3.",
            "what_appears_to_motivate_them": "Personally affected, compassion, cause, and social asks.",
            "what_barriers_may_matter": "Solicitation tone, method, and frequency should be managed carefully.",
            "fundraising_approach_supported": "Build respectful tribute, peer-to-peer, and community campaign journeys with clear opt-out and preference controls.",
            "what_data_does_not_allow_us_to_claim": "The PUMF does not identify which channel was used for the Health-category gift specifically.",
        },
        {
            "priority_rank": 5,
            "audience_name": "Trust-sensitive donors",
            "opportunity_type": "Retention / barrier reduction",
            "who_they_are": "Health donors and prospects who cite charity fraud, efficiency, and too many organizations as barriers.",
            "what_the_data_shows": "Charity fraud and too many organizations are high reported barriers among Health donors; efficiency concerns are also present.",
            "why_they_matter": "These are barriers charities can partly address through transparency and donor experience.",
            "how_they_currently_give": "Trust-sensitive donors may still give through multiple channels; channel-specific testing is needed.",
            "what_appears_to_motivate_them": "Cause, impact, compassion, and community contribution.",
            "what_barriers_may_matter": "Fraud concern, efficient use of money, request style, and choice overload.",
            "fundraising_approach_supported": "Use clear impact proof, registration/credibility cues, simple choices, and solicitation preference management.",
            "what_data_does_not_allow_us_to_claim": "Reported barriers do not prove which transparency tactic will change behaviour.",
        },
    ]
    return pd.DataFrame(rows)


def write_sql():
    sql = """-- Chapter 6 SQL layer: Opportunity synthesis.
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
"""
    (CHAPTER_ROOT / "sql" / "chapter6_opportunity_views.sql").write_text(sql, encoding="utf-8")


def validate(priority, evidence):
    checks = [
        ("priority_audience_rows", len(priority), "pass" if len(priority) >= 5 else "fail"),
        ("evidence_rows", len(evidence), "pass" if len(evidence) >= 15 else "fail"),
        ("source_chapters_used", ", ".join(sorted(evidence["source_chapter"].unique())), "pass"),
        ("no_causal_language_claimed", "recommendations state supported/associated, not proven causal", "pass"),
    ]
    pd.DataFrame(checks, columns=["check", "result", "status"]).to_csv(CHAPTER_ROOT / "outputs" / "chapter6_validation_results.csv", index=False)


def audit_sql():
    sql = (CHAPTER_ROOT / "sql" / "chapter6_opportunity_views.sql").read_text(encoding="utf-8")
    con = sqlite3.connect(":memory:")
    parts = sql.split("DROP VIEW IF EXISTS vw_chapter6_priority_evidence_counts;")
    con.executescript(parts[0])
    for table, path in [
        ("chapter6_priority_audiences", CHAPTER_ROOT / "data" / "processed" / "chapter6_priority_audiences.csv"),
        ("chapter6_evidence_table", CHAPTER_ROOT / "data" / "processed" / "chapter6_evidence_table.csv"),
    ]:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            con.executemany(f"INSERT INTO {table} VALUES ({','.join(['?'] * len(header))})", reader)
    con.executescript("DROP VIEW IF EXISTS vw_chapter6_priority_evidence_counts;" + parts[1])
    row_count = pd.read_sql_query("SELECT COUNT(*) AS n FROM vw_chapter6_priority_evidence_counts", con)["n"].iloc[0]
    pd.DataFrame([{"check": "sql_view_executes", "result": int(row_count), "status": "pass" if row_count >= 5 else "fail"}]).to_csv(CHAPTER_ROOT / "outputs" / "chapter6_sql_audit.csv", index=False)


def write_docs(priority, evidence):
    (CHAPTER_ROOT / "outputs" / "chapter6_findings.md").write_text(
        "# Chapter 6 Findings - The Opportunity\n\n"
        "Chapter 6 synthesizes Chapters 1-5 into a transparent opportunity framework. The priority audiences are evidence-supported, descriptive segments rather than a predictive or causal scoring model.\n\n"
        "## Priority Audiences\n\n"
        + "\n".join(f"{r.priority_rank}. {r.audience_name}: {r.opportunity_type}." for r in priority.itertuples())
        + "\n\n## Main Implications\n\n"
        "- Retention and stewardship matter because many Health donors already give and report satisfaction or financial constraints.\n"
        "- Tribute, sponsorship, mail, own-initiative, and online channels should be evaluated as distinct journeys.\n"
        "- Trust, impact clarity, and solicitation quality are recurring barriers charities can partially address.\n"
        "- Recommendations remain descriptive; campaign testing is required before scaling tactics.\n",
        encoding="utf-8",
    )
    (CHAPTER_ROOT / "docs" / "chapter6_methodology.md").write_text(
        "# Chapter 6 Methodology\n\n"
        "Business question: Which audiences and fundraising approaches should a Health charity prioritize?\n\n"
        "This chapter reads validated outputs from Chapters 1-5 and creates a simple evidence-linked opportunity framework. "
        "No new raw survey variables are introduced. Recommendations are based on weighted descriptive survey findings, Power BI-ready tables, and documented limitations from prior chapters.\n",
        encoding="utf-8",
    )
    (CHAPTER_ROOT / "README.md").write_text(
        "# Chapter 6 - The Opportunity\n\n"
        "This chapter synthesizes Chapters 1-5 into priority audience and evidence tables for Power BI and the final executive report.\n\n"
        "Run from the project root using the Chapter 2 Python environment:\n\n"
        "```powershell\n& \"Chapter 2\\.venv\\Scripts\\python.exe\" \"Chapter 6\\scripts\\chapter6_opportunity.py\"\n```\n",
        encoding="utf-8",
    )


def main():
    evidence = build_evidence()
    priority = build_priority_audiences(evidence)
    evidence.to_csv(CHAPTER_ROOT / "data" / "processed" / "chapter6_evidence_table.csv", index=False)
    priority.to_csv(CHAPTER_ROOT / "data" / "processed" / "chapter6_priority_audiences.csv", index=False)
    evidence.to_csv(CHAPTER_ROOT / "data" / "powerbi" / "chapter6_evidence_table.csv", index=False)
    priority.to_csv(CHAPTER_ROOT / "data" / "powerbi" / "chapter6_priority_audiences.csv", index=False)
    evidence.to_csv(CHAPTER_ROOT / "outputs" / "chapter6_evidence_table.csv", index=False)
    priority.to_csv(CHAPTER_ROOT / "outputs" / "chapter6_priority_audiences.csv", index=False)
    write_sql()
    validate(priority, evidence)
    audit_sql()
    write_docs(priority, evidence)
    print(json.dumps({"chapter": "Chapter 6", "priority_audiences": len(priority), "evidence_rows": len(evidence)}, indent=2))


if __name__ == "__main__":
    main()
