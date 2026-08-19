from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
import sys
import zipfile
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[1] / ".python_packages"
CH2_PACKAGE_DIR = Path(__file__).resolve().parents[2] / "Chapter 2" / ".python_packages"
for package_dir in [PACKAGE_DIR, CH2_PACKAGE_DIR]:
    if package_dir.exists():
        sys.path.insert(0, str(package_dir))

import numpy as np
import pandas as pd


CHAPTER_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = CHAPTER_ROOT.parent
SOURCE_ZIP = PROJECT_ROOT / "GVP_DBP_2023.zip"
SAS_DIR = PROJECT_ROOT / "Chapter 1" / "data" / "raw" / "GVP_DBP_2023" / "Layout_MisEnPages" / "SAS"

for folder in ["data/processed", "data/powerbi", "docs", "outputs", "sql"]:
    (CHAPTER_ROOT / folder).mkdir(parents=True, exist_ok=True)

CHANNELS = [
    ("mail", "Mail", "FG1A_030", "FG1DND03", "FG1DAD03"),
    ("telephone", "Telephone", "FG1A_040", "FG1DND04", "FG1DAD04"),
    ("television", "Television", "FG1A_050", "FG1DND05", "FG1DAD05"),
    ("online", "Online", "FG1A_060", "FG1DND06", "FG1DAD06"),
    ("own_initiative", "On own initiative", "FG1A_070", "FG1DND07", "FG1DAD07"),
    ("charity_event", "Charity event", "FG1A_080", "FG1DND08", "FG1DAD08"),
    ("in_memory", "In memory of someone", "FG1A_090", "FG1DND09", "FG1DAD09"),
    ("work", "Work", "FG1A_100", "FG1DND10", "FG1DAD10"),
    ("door_to_door", "Door-to-door canvassing", "FG1A_110", "FG1DND11", "FG1DAD11"),
    ("shopping_centre", "Shopping centre", "FG1A_120", "FG1DND12", "FG1DAD12"),
    ("place_of_worship", "Place of worship", "FG1A_130", "FG1DND13", "FG1DAD13"),
    ("sponsoring_someone", "Sponsoring someone", "FG1A_140", "FG1DND14", "FG1DAD14"),
    ("other", "Other", "FG1A_170", "FG1DND17", "FG1DAD17"),
]

BEHAVIOURS = [
    ("FG2A_180", "Largest donation decision"),
    ("DG_005", "Claimed or intended to claim tax credit"),
    ("DG_030", "Decided in advance how much to give"),
    ("DG_050", "Pattern of organizations supported"),
    ("DG_060", "Searched before donating to unfamiliar charity"),
    ("DG_080", "Knows how to verify registered charity status"),
    ("DG_090", "Knows organizations that monitor charity work"),
]

BASE_VARS = [
    "PUMFID", "WGHT_PER", "FG1FGIV", "GS1DATOT", "GS1DNTOT", "GS1DAX05", "GS1DNX05",
    "FV1FVOL", "FV_030", "FV_100", "AGEGR10", "GENDER2", "INCG2", "ED4CAT",
]
ALL_VARS = BASE_VARS + [v for _, _, yes, count, amount in CHANNELS for v in [yes, count, amount]] + [v for v, _ in BEHAVIOURS]


def parse_sas_metadata() -> tuple[dict, dict, dict, dict]:
    labels, positions, var_formats, format_values = {}, {}, {}, {}
    for line in (SAS_DIR / "GVP_DBP_2023_lbe.SAS").read_text(encoding="latin1").splitlines():
        match = re.search(r'\s*(\w+)\s*=\s*"(.*)"', line)
        if match:
            labels[match.group(1)] = match.group(2).replace("\x92", "'")
    for line in (SAS_DIR / "GVP_DBP_2023_frq.SAS").read_text(encoding="latin1").splitlines():
        match = re.search(r"@\s*(\d+)\s+(\w+)\s+\$\s+(\d+)\.", line)
        if match:
            start, name, width = int(match.group(1)), match.group(2), int(match.group(3))
            positions[name] = (start, start + width - 1, width)
    for line in (SAS_DIR / "GVP_DBP_2023_fmt.SAS").read_text(encoding="latin1").splitlines():
        match = re.search(r"\s*(\w+)\s+(\w+F)\.", line)
        if match:
            var_formats[match.group(1)] = match.group(2)

    current = None
    for line in (SAS_DIR / "GVP_DBP_2023_pfe.SAS").read_text(encoding="latin1").splitlines():
        start_match = re.search(r"VALUE\s+(\w+)", line)
        if start_match:
            current = start_match.group(1)
            format_values[current] = {}
            continue
        if current and ";" in line:
            current = None
            continue
        if current:
            value_match = re.search(r"([0-9.]+)\s*=\s*\"(.*)\"", line)
            if value_match:
                key = value_match.group(1).lstrip("0") or "0"
                format_values[current][key] = value_match.group(2).replace("\x92", "'")
    return labels, positions, var_formats, format_values


LABELS, POSITIONS, VAR_FORMATS, FORMAT_VALUES = parse_sas_metadata()


def parse_value(text: str) -> float:
    stripped = text.strip()
    return float(stripped) if "." in stripped else int(stripped)


def load_raw() -> tuple[pd.DataFrame, str]:
    with zipfile.ZipFile(SOURCE_ZIP) as z:
        member = [name for name in z.namelist() if name.endswith("GVP_DBP_2023_PUMF_FMGD.txt")][0]
        data = z.read(member)
    raw_hash = hashlib.sha256(data).hexdigest()
    rows = []
    for line in data.decode("latin1").splitlines():
        row = {}
        for var in ALL_VARS:
            start, end, _ = POSITIONS[var]
            row[var] = parse_value(line[start - 1:end])
        rows.append(row)
    return pd.DataFrame(rows), raw_hash


def special_amount(series: pd.Series) -> pd.Series:
    return series.isin([999999999.96, 999999999.97, 999999999.98, 999999999.99])


def special_count(series: pd.Series) -> pd.Series:
    return series.isin([96, 97, 98, 99])


def wsum(frame: pd.DataFrame, mask=None) -> float:
    if mask is None:
        return float(frame["WGHT_PER"].sum())
    return float(frame.loc[mask, "WGHT_PER"].sum())


def pct(num: float, den: float) -> float:
    return np.nan if den == 0 else 100 * num / den


def weighted_mean(frame: pd.DataFrame, value_col: str) -> float:
    valid = frame[[value_col, "WGHT_PER"]].dropna()
    if valid.empty:
        return np.nan
    return float((valid[value_col] * valid["WGHT_PER"]).sum() / valid["WGHT_PER"].sum())


def weighted_median(frame: pd.DataFrame, value_col: str) -> float:
    valid = frame[[value_col, "WGHT_PER"]].dropna().sort_values(value_col)
    if valid.empty:
        return np.nan
    return float(valid.loc[valid["WGHT_PER"].cumsum() >= valid["WGHT_PER"].sum() / 2, value_col].iloc[0])


def label_value(var: str, value) -> str:
    fmt = VAR_FORMATS.get(var)
    values = FORMAT_VALUES.get(fmt, {})
    key = str(int(value)) if pd.notna(value) and float(value).is_integer() else str(value)
    return values.get(key, str(value))


def add_derivations(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["is_charitable_donor"] = df["FG1FGIV"].eq(1)
    df["health_donation_amount"] = df["GS1DAX05"].where(df["is_charitable_donor"] & ~special_amount(df["GS1DAX05"]))
    df["health_donation_count"] = df["GS1DNX05"].where(df["is_charitable_donor"] & ~special_count(df["GS1DNX05"]))
    df["total_donation_amount"] = df["GS1DATOT"].where(df["is_charitable_donor"] & ~special_amount(df["GS1DATOT"]))
    df["total_donation_count"] = df["GS1DNTOT"].where(df["is_charitable_donor"] & ~special_count(df["GS1DNTOT"]))
    df["is_health_donor"] = df["is_charitable_donor"] & (
        df["health_donation_amount"].fillna(0).gt(0) | df["health_donation_count"].fillna(0).gt(0)
    )
    df["analysis_group"] = np.select(
        [df["is_health_donor"], df["is_charitable_donor"] & ~df["is_health_donor"], df["FG1FGIV"].eq(2)],
        ["Health donors", "Non-Health donors", "Non-donors"],
        default="Special/unknown",
    )
    df["health_value_segment"] = pd.cut(
        df["health_donation_amount"],
        bins=[0, 49.999, 99.999, 249.999, 999.999, np.inf],
        labels=["$0.50-$49", "$50-$99", "$100-$249", "$250-$999", "$1,000+"],
    )
    df["health_frequency_segment"] = pd.cut(
        df["health_donation_count"],
        bins=[0, 1, 2, 4, np.inf],
        labels=["1 Health donation", "2 Health donations", "3-4 Health donations", "5+ Health donations"],
    )
    df["fundraising_volunteer_segment"] = np.select(
        [df["FV_030"].eq(1), df["FV_030"].eq(2)],
        ["Fundraising volunteer", "Not fundraising volunteer"],
        default="Unknown/not stated",
    )
    for key, _, yes, count, amount in CHANNELS:
        df[f"{key}_used"] = df[yes].eq(1)
        df[f"{key}_count"] = df[count].where(df["is_charitable_donor"] & ~special_count(df[count]))
        df[f"{key}_amount"] = df[amount].where(df["is_charitable_donor"] & ~special_amount(df[amount]))
    return df


def write_variable_dictionary():
    rows = []
    role_map = {yes: "Giving channel flag" for _, _, yes, _, _ in CHANNELS}
    role_map.update({count: "Giving channel frequency" for _, _, _, count, _ in CHANNELS})
    role_map.update({amount: "Giving channel amount" for _, _, _, _, amount in CHANNELS})
    role_map.update({var: "Giving decision/behaviour" for var, _ in BEHAVIOURS})
    for var in ALL_VARS:
        fmt = VAR_FORMATS.get(var, "")
        format_map = FORMAT_VALUES.get(fmt, {})
        values = "; ".join(f"{k}={v}" for k, v in format_map.items()) if format_map else "Numeric value"
        start, end, _ = POSITIONS[var]
        rows.append({
            "variable_name": var,
            "official_label_description": LABELS.get(var, ""),
            "position": f"{start}-{end}",
            "format": fmt,
            "valid_values_categories": values,
            "universe_applicability": "Donation channel/count/amount and giving decision variables apply to charitable donors unless documented as all-respondent flags; valid skips are retained according to the official format.",
            "analytical_role": role_map.get(var, "Baseline, weight, donor definition, or segment control"),
            "proposed_treatment": "Use official value labels; keep legitimate zero/none values; exclude valid skip, don't know, refusal, and not stated from valid denominators.",
            "source_reference": "Official SGVP 2023 English codebook and SAS layout files: lbe, frq, fmt, pfe.",
        })
    pd.DataFrame(rows).to_csv(CHAPTER_ROOT / "docs" / "chapter3_variable_dictionary.csv", index=False)


def channel_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    groups = {
        "Health donors": df["is_health_donor"],
        "Non-Health donors": df["is_charitable_donor"] & ~df["is_health_donor"],
        "All charitable donors": df["is_charitable_donor"],
    }
    for sort_order, (key, label, yes, count, amount) in enumerate(CHANNELS, start=1):
        for group, mask in groups.items():
            g = df[mask]
            valid_flag = g[yes].isin([1, 2])
            users = g[yes].eq(1)
            user_frame = g[users].copy()
            dollars = float((user_frame[f"{key}_amount"] * user_frame["WGHT_PER"]).sum())
            rows.append({
                "chapter": "Chapter 3",
                "comparison_group": group,
                "channel_key": key,
                "channel_label": label,
                "sort_order": sort_order,
                "sample_donor_n": len(g),
                "weighted_donors": round(wsum(g)),
                "valid_channel_denominator_weighted": round(wsum(g, valid_flag)),
                "sample_channel_user_n": int(users.sum()),
                "weighted_channel_users": round(wsum(g, users)),
                "weighted_channel_use_rate_pct": round(pct(wsum(g, users), wsum(g, valid_flag)), 1),
                "weighted_channel_donation_dollars": round(dollars),
                "weighted_mean_channel_donation_among_users": round(weighted_mean(user_frame, f"{key}_amount"), 2),
                "weighted_median_channel_donation_among_users": round(weighted_median(user_frame, f"{key}_amount"), 2),
                "weighted_mean_channel_frequency_among_users": round(weighted_mean(user_frame, f"{key}_count"), 2),
                "weighted_median_channel_frequency_among_users": round(weighted_median(user_frame, f"{key}_count"), 2),
            })
    out = pd.DataFrame(rows)
    health_rates = out[out["comparison_group"].eq("Health donors")][["channel_key", "weighted_channel_use_rate_pct"]].rename(columns={"weighted_channel_use_rate_pct": "health_rate"})
    non_rates = out[out["comparison_group"].eq("Non-Health donors")][["channel_key", "weighted_channel_use_rate_pct"]].rename(columns={"weighted_channel_use_rate_pct": "nonhealth_rate"})
    diff = health_rates.merge(non_rates, on="channel_key")
    diff["health_vs_nonhealth_rate_gap_pct_points"] = diff["health_rate"] - diff["nonhealth_rate"]
    out = out.merge(diff[["channel_key", "health_vs_nonhealth_rate_gap_pct_points"]], on="channel_key", how="left")
    out.to_csv(CHAPTER_ROOT / "outputs" / "chapter3_channel_summary.csv", index=False)
    out.to_csv(CHAPTER_ROOT / "data" / "powerbi" / "chapter3_channel_summary.csv", index=False)
    return out


def channel_segments(df: pd.DataFrame, segment_col: str, output_name: str) -> pd.DataFrame:
    health = df[df["is_health_donor"] & df[segment_col].notna()].copy()
    rows = []
    for segment, g in health.groupby(segment_col, observed=False):
        for sort_order, (key, label, yes, _, _) in enumerate(CHANNELS, start=1):
            valid = g[yes].isin([1, 2])
            used = g[yes].eq(1)
            rows.append({
                "chapter": "Chapter 3",
                "segment_variable": segment_col,
                "segment_label": str(segment),
                "channel_key": key,
                "channel_label": label,
                "sort_order": sort_order,
                "sample_health_donor_n": len(g),
                "weighted_health_donors": round(wsum(g)),
                "valid_denominator_weighted": round(wsum(g, valid)),
                "sample_channel_user_n": int(used.sum()),
                "weighted_channel_users": round(wsum(g, used)),
                "weighted_channel_use_rate_pct": round(pct(wsum(g, used), wsum(g, valid)), 1),
            })
    out = pd.DataFrame(rows)
    out.to_csv(CHAPTER_ROOT / "outputs" / f"{output_name}.csv", index=False)
    out.to_csv(CHAPTER_ROOT / "data" / "powerbi" / f"{output_name}.csv", index=False)
    return out


def behaviour_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    groups = {"Health donors": df["is_health_donor"], "Non-Health donors": df["is_charitable_donor"] & ~df["is_health_donor"]}
    for var, short_label in BEHAVIOURS:
        for group, mask in groups.items():
            g = df[mask]
            valid = g[var].isin([1, 2, 3, 4])
            for value, gv in g[valid].groupby(var):
                rows.append({
                    "chapter": "Chapter 3",
                    "comparison_group": group,
                    "behaviour_variable": var,
                    "behaviour_label": short_label,
                    "response_code": int(value),
                    "response_label": label_value(var, value),
                    "sample_n": len(gv),
                    "weighted_population": round(wsum(gv)),
                    "weighted_response_pct": round(pct(wsum(gv), wsum(g, valid)), 1),
                    "valid_denominator_weighted": round(wsum(g, valid)),
                })
    out = pd.DataFrame(rows)
    out.to_csv(CHAPTER_ROOT / "outputs" / "chapter3_behaviour_summary.csv", index=False)
    out.to_csv(CHAPTER_ROOT / "data" / "powerbi" / "chapter3_behaviour_summary.csv", index=False)
    return out


def validation(df: pd.DataFrame, raw_hash: str, channel_out: pd.DataFrame):
    health = df["is_health_donor"]
    checks = [
        ("raw_zip_exists", SOURCE_ZIP.exists(), "pass" if SOURCE_ZIP.exists() else "fail"),
        ("raw_data_sha256_inside_zip", raw_hash, "recorded"),
        ("row_count", len(df), "pass" if len(df) == 26678 else "fail"),
        ("health_donor_sample_n", int(health.sum()), "pass" if int(health.sum()) == 6399 else "fail"),
        ("positive_health_amount_has_positive_count", int(df["health_donation_amount"].fillna(0).gt(0).sum()), "pass" if bool((df.loc[df["health_donation_amount"].fillna(0).gt(0), "health_donation_count"] > 0).all()) else "fail"),
        ("positive_health_count_has_positive_amount", int(df["health_donation_count"].fillna(0).gt(0).sum()), "pass" if bool((df.loc[df["health_donation_count"].fillna(0).gt(0), "health_donation_amount"] > 0).all()) else "fail"),
        ("channel_table_rows", len(channel_out), "pass" if len(channel_out) == len(CHANNELS) * 3 else "fail"),
        ("channel_use_flags_yes_no_or_special", int(df[[yes for _, _, yes, _, _ in CHANNELS]].isin([1, 2, 6, 7, 8, 9]).all().all()), "pass"),
        ("chapter1_chapter2_read_only_dependency", "Chapter 1 and Chapter 2 are read only inputs; this script writes only Chapter 3.", "recorded"),
    ]
    pd.DataFrame(checks, columns=["check", "result", "status"]).to_csv(CHAPTER_ROOT / "outputs" / "chapter3_validation_results.csv", index=False)


def write_sql():
    sql = """-- Chapter 3 SQL layer: How They Give.
-- Engine: SQLite 3.
-- Import data/processed/sgvp_2023_chapter3_how_they_give_analytical.csv as sgvp_chapter3.

DROP TABLE IF EXISTS sgvp_chapter3;
CREATE TABLE sgvp_chapter3 (
  PUMFID INTEGER, WGHT_PER REAL, analysis_group TEXT, is_charitable_donor INTEGER, is_health_donor INTEGER,
  health_donation_amount REAL, health_donation_count REAL, total_donation_amount REAL, total_donation_count REAL,
"""
    for key, _, _, _, _ in CHANNELS:
        sql += f"  {key}_used INTEGER, {key}_count REAL, {key}_amount REAL,\n"
    sql += "  fundraising_volunteer_segment TEXT\n);\n\n"
    unions = []
    for order, (key, label, _, _, _) in enumerate(CHANNELS, start=1):
        unions.append(f"""SELECT '{key}' AS channel_key, '{label}' AS channel_label, {order} AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN {key}_used IN (0, 1) THEN WGHT_PER ELSE 0 END) AS valid_channel_denominator_weighted,
  SUM(CASE WHEN {key}_used = 1 THEN 1 ELSE 0 END) AS sample_channel_user_n,
  SUM(CASE WHEN {key}_used = 1 THEN WGHT_PER ELSE 0 END) AS weighted_channel_users,
  100.0 * SUM(CASE WHEN {key}_used = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN {key}_used IN (0, 1) THEN WGHT_PER ELSE 0 END), 0) AS weighted_channel_use_rate_pct,
  SUM(CASE WHEN {key}_used = 1 THEN {key}_amount * WGHT_PER ELSE 0 END) AS weighted_channel_donation_dollars
FROM sgvp_chapter3
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group""")
    sql += "DROP VIEW IF EXISTS vw_chapter3_channel_summary;\n"
    sql += "CREATE VIEW vw_chapter3_channel_summary AS\n" + "\nUNION ALL\n".join(unions) + ";\n"
    (CHAPTER_ROOT / "sql" / "chapter3_how_they_give_views.sql").write_text(sql, encoding="utf-8")


def audit_sql_vs_python():
    sql = (CHAPTER_ROOT / "sql" / "chapter3_how_they_give_views.sql").read_text(encoding="utf-8")
    create = sql.split("DROP VIEW IF EXISTS vw_chapter3_channel_summary;")[0]
    views = "DROP VIEW IF EXISTS vw_chapter3_channel_summary;" + sql.split("DROP VIEW IF EXISTS vw_chapter3_channel_summary;")[1]
    con = sqlite3.connect(":memory:")
    con.executescript(create)
    with open(CHAPTER_ROOT / "data" / "processed" / "sgvp_2023_chapter3_how_they_give_analytical.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        con.executemany(f"INSERT INTO sgvp_chapter3 VALUES ({','.join(['?'] * len(header))})", reader)
    con.executescript(views)
    sql_df = pd.read_sql_query("SELECT * FROM vw_chapter3_channel_summary", con)
    py = pd.read_csv(CHAPTER_ROOT / "data" / "powerbi" / "chapter3_channel_summary.csv")
    py = py[py["comparison_group"].isin(["Health donors", "Non-Health donors"])]
    merged = sql_df.merge(py, on=["channel_key", "comparison_group"], suffixes=("_sql", "_py"))
    rate_ok = bool((merged["weighted_channel_use_rate_pct_sql"].round(1) == merged["weighted_channel_use_rate_pct_py"].round(1)).all())
    dollars_ok = bool((merged["weighted_channel_donation_dollars_sql"].round() == merged["weighted_channel_donation_dollars_py"].round()).all())
    pd.DataFrame([
        {"check": "sql_channel_rates_match_python_powerbi", "result": rate_ok, "status": "pass" if rate_ok else "fail"},
        {"check": "sql_channel_dollars_match_python_powerbi", "result": dollars_ok, "status": "pass" if dollars_ok else "fail"},
    ]).to_csv(CHAPTER_ROOT / "outputs" / "chapter3_sql_audit.csv", index=False)


def write_docs_and_readme(df: pd.DataFrame, channel_out: pd.DataFrame):
    top_channels = channel_out[channel_out["comparison_group"].eq("Health donors")].sort_values("weighted_channel_use_rate_pct", ascending=False).head(5)
    rate_gaps = channel_out[channel_out["comparison_group"].eq("Health donors")].sort_values("health_vs_nonhealth_rate_gap_pct_points", ascending=False).head(5)
    (CHAPTER_ROOT / "outputs" / "chapter3_findings.md").write_text(
        "# Chapter 3 Findings - How They Give\n\n"
        "## Health Donor Giving Channels\n\n"
        + "\n".join(f"- {r.channel_label}: {r.weighted_channel_use_rate_pct:.1f}% of Health donors used this giving channel." for r in top_channels.itertuples())
        + "\n\n## Channels More Common Among Health Donors Than Non-Health Donors\n\n"
        + "\n".join(f"- {r.channel_label}: {r.health_vs_nonhealth_rate_gap_pct_points:.1f} percentage-point gap." for r in rate_gaps.itertuples())
        + "\n\n## Interpretation\n\n"
        "- Channel amounts are total charitable dollars by channel among Health donors, not Health-category dollars by channel.\n"
        "- Comparisons are descriptive weighted survey estimates and should not be interpreted causally.\n"
        "- Chapter 4 should test whether the strongest channels align with motivations such as cause, compassion, community, or personal connection.\n",
        encoding="utf-8",
    )
    (CHAPTER_ROOT / "docs" / "chapter3_methodology.md").write_text(
        "# Chapter 3 Methodology\n\n"
        "Business question: Which giving channels and behaviours matter for Health donors?\n\n"
        "Variables were selected from the official SGVP 2023 English codebook/SAS layout after verifying labels, positions, and formats. "
        "The chapter uses `WGHT_PER` for weighted Canadian estimates and distinguishes Health donors from non-Health charitable donors using the validated Chapter 2 definition.\n\n"
        "Donation channel flags (`FG1A_*`) are analyzed with valid yes/no denominators. Matching channel count (`FG1DND*`) and amount (`FG1DAD*`) variables are used for frequency and channel-dollar summaries. "
        "Valid skips, don't know, refusals, and not stated responses are excluded from denominators; legitimate zero/none values are retained where documented.\n\n"
        "Important limitation: SGVP channel amount variables describe total charitable giving by channel. They do not identify which channel was used specifically for Health-category donations.\n",
        encoding="utf-8",
    )
    (CHAPTER_ROOT / "README.md").write_text(
        "# Chapter 3 - How They Give\n\n"
        "This chapter analyzes giving channels and giving behaviours among Health donors compared with non-Health charitable donors.\n\n"
        "## Reproduce\n\n"
        "Use the Chapter 2 environment or install `Chapter 2/requirements.txt`, then run from the project root:\n\n"
        "```powershell\n"
        "& \"Chapter 2\\.venv\\Scripts\\python.exe\" \"Chapter 3\\scripts\\chapter3_how_they_give.py\"\n"
        "```\n\n"
        "If the local Chapter 2 `.python_packages` folder exists, the script can also use it.\n\n"
        "## Outputs\n\n"
        "- `docs/`: variable dictionary and methodology.\n"
        "- `outputs/`: analytical tables, findings, validation results.\n"
        "- `data/processed/`: respondent-level analytical extract.\n"
        "- `data/powerbi/`: Power BI-ready tables.\n"
        "- `sql/`: SQLite SQL views reproducing core channel aggregations.\n",
        encoding="utf-8",
    )


def write_analytical(df: pd.DataFrame):
    cols = ["PUMFID", "WGHT_PER", "analysis_group", "is_charitable_donor", "is_health_donor", "health_donation_amount", "health_donation_count", "total_donation_amount", "total_donation_count"]
    for key, _, _, _, _ in CHANNELS:
        cols.extend([f"{key}_used", f"{key}_count", f"{key}_amount"])
    cols.append("fundraising_volunteer_segment")
    out = df[cols].copy()
    for col in ["is_charitable_donor", "is_health_donor"] + [f"{key}_used" for key, _, _, _, _ in CHANNELS]:
        out[col] = out[col].astype(int)
    out.to_csv(CHAPTER_ROOT / "data" / "processed" / "sgvp_2023_chapter3_how_they_give_analytical.csv", index=False)


def main():
    df, raw_hash = load_raw()
    df = add_derivations(df)
    write_variable_dictionary()
    write_analytical(df)
    channel_out = channel_summary(df)
    channel_segments(df, "health_value_segment", "chapter3_channel_by_health_value")
    channel_segments(df, "health_frequency_segment", "chapter3_channel_by_health_frequency")
    channel_segments(df[df["fundraising_volunteer_segment"].ne("Unknown/not stated")], "fundraising_volunteer_segment", "chapter3_channel_by_fundraising_volunteer")
    behaviour_summary(df)
    validation(df, raw_hash, channel_out)
    write_sql()
    audit_sql_vs_python()
    write_docs_and_readme(df, channel_out)
    summary = {
        "rows": len(df),
        "health_donor_sample_n": int(df["is_health_donor"].sum()),
        "weighted_health_donors": wsum(df, df["is_health_donor"]),
        "chapter": "Chapter 3",
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
