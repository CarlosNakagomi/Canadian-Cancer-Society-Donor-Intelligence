from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
import sys
import zipfile
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[2] / "Chapter 2" / ".python_packages"
if PACKAGE_DIR.exists():
    sys.path.insert(0, str(PACKAGE_DIR))

import numpy as np
import pandas as pd


CHAPTER_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = CHAPTER_ROOT.parent
SOURCE_ZIP = PROJECT_ROOT / "GVP_DBP_2023.zip"
SAS_DIR = PROJECT_ROOT / "Chapter 1" / "data" / "raw" / "GVP_DBP_2023" / "Layout_MisEnPages" / "SAS"

for folder in ["data/processed", "data/powerbi", "docs", "outputs", "sql"]:
    (CHAPTER_ROOT / folder).mkdir(parents=True, exist_ok=True)

MOTIVATIONS = [
    ("RG_010", "Personally affected"),
    ("RG_020", "Tax credit"),
    ("RG_030", "Religious reasons"),
    ("RG_035", "Spiritual or other beliefs"),
    ("RG_040", "Belief in the cause"),
    ("RG_050", "Compassion"),
    ("RG_060", "Community contribution"),
    ("RG_070", "Asked by someone you know"),
]

BASE_VARS = [
    "PUMFID", "WGHT_PER", "FG1FGIV", "GS1DATOT", "GS1DNTOT", "GS1DAX05", "GS1DNX05",
    "AGEGR10", "GENDER2", "INCG2", "ED4CAT",
]
ALL_VARS = BASE_VARS + [v for v, _ in MOTIVATIONS]


def parse_metadata():
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
        start = re.search(r"VALUE\s+(\w+)", line)
        if start:
            current = start.group(1)
            format_values[current] = {}
            continue
        if current and ";" in line:
            current = None
            continue
        if current:
            value = re.search(r"([0-9.]+)\s*=\s*\"(.*)\"", line)
            if value:
                key = value.group(1).lstrip("0") or "0"
                format_values[current][key] = value.group(2).replace("\x92", "'")
    return labels, positions, var_formats, format_values


LABELS, POSITIONS, VAR_FORMATS, FORMAT_VALUES = parse_metadata()


def parse_value(text: str):
    stripped = text.strip()
    return float(stripped) if "." in stripped else int(stripped)


def load_raw():
    with zipfile.ZipFile(SOURCE_ZIP) as z:
        member = [name for name in z.namelist() if name.endswith("GVP_DBP_2023_PUMF_FMGD.txt")][0]
        data = z.read(member)
    rows = []
    for line in data.decode("latin1").splitlines():
        rows.append({var: parse_value(line[POSITIONS[var][0] - 1:POSITIONS[var][1]]) for var in ALL_VARS})
    return pd.DataFrame(rows), hashlib.sha256(data).hexdigest()


def special_amount(series):
    return series.isin([999999999.96, 999999999.97, 999999999.98, 999999999.99])


def special_count(series):
    return series.isin([96, 97, 98, 99])


def wsum(frame, mask=None):
    if mask is None:
        return float(frame["WGHT_PER"].sum())
    return float(frame.loc[mask, "WGHT_PER"].sum())


def pct(num, den):
    return np.nan if den == 0 else 100 * num / den


def weighted_median(frame, col):
    valid = frame[[col, "WGHT_PER"]].dropna().sort_values(col)
    if valid.empty:
        return np.nan
    return float(valid.loc[valid["WGHT_PER"].cumsum() >= valid["WGHT_PER"].sum() / 2, col].iloc[0])


def add_derivations(df):
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
    maps = {
        "AGEGR10": {1: "15 to 24 years", 2: "25 to 34 years", 3: "35 to 44 years", 4: "45 to 54 years", 5: "55 to 64 years", 6: "65 to 74 years", 7: "75 years and over"},
        "GENDER2": {1: "Man+", 2: "Woman+"},
        "INCG2": {1: "Less than $25,000", 2: "$25,000 to $49,999", 3: "$50,000 to $74,999", 4: "$75,000 to $99,999", 5: "$100,000 to $124,999", 6: "$125,000 and more"},
        "ED4CAT": {1: "Less than high school", 2: "Graduated from high school", 3: "Post-secondary diploma", 4: "University diploma"},
    }
    for col, mapping in maps.items():
        df[col + "_label"] = df[col].map(mapping)
    return df


def write_dictionary():
    rows = []
    for var in ALL_VARS:
        fmt = VAR_FORMATS.get(var, "")
        values = FORMAT_VALUES.get(fmt, {})
        rows.append({
            "variable_name": var,
            "official_label_description": LABELS.get(var, ""),
            "position": f"{POSITIONS[var][0]}-{POSITIONS[var][1]}",
            "format": fmt,
            "valid_values_categories": "; ".join(f"{k}={v}" for k, v in values.items()) if values else "Numeric value",
            "universe_applicability": "Reasons for giving variables apply to charitable donors; documented valid skips and nonresponse codes are excluded from valid denominators.",
            "analytical_role": "Motivation measure" if var.startswith("RG_") else "Baseline, weight, donor definition, or segment control",
            "proposed_treatment": "Use 1=Yes and 2=No valid denominator for motivation rates; exclude valid skip, don't know, refusal, and not stated.",
            "source_reference": "Official SGVP 2023 English codebook and SAS layout files: lbe, frq, fmt, pfe.",
        })
    pd.DataFrame(rows).to_csv(CHAPTER_ROOT / "docs" / "chapter4_variable_dictionary.csv", index=False)


def motivation_summary(df):
    rows = []
    groups = {"Health donors": df["is_health_donor"], "Non-Health donors": df["is_charitable_donor"] & ~df["is_health_donor"], "All charitable donors": df["is_charitable_donor"]}
    for sort_order, (var, label) in enumerate(MOTIVATIONS, start=1):
        for group, mask in groups.items():
            g = df[mask]
            valid = g[var].isin([1, 2])
            yes = g[var].eq(1)
            rows.append({
                "chapter": "Chapter 4",
                "comparison_group": group,
                "motivation_variable": var,
                "motivation_label": label,
                "sort_order": sort_order,
                "sample_donor_n": len(g),
                "weighted_donors": round(wsum(g)),
                "valid_denominator_weighted": round(wsum(g, valid)),
                "sample_yes_n": int(yes.sum()),
                "weighted_yes": round(wsum(g, yes)),
                "weighted_yes_pct": round(pct(wsum(g, yes), wsum(g, valid)), 1),
            })
    out = pd.DataFrame(rows)
    health = out[out.comparison_group.eq("Health donors")][["motivation_variable", "weighted_yes_pct"]].rename(columns={"weighted_yes_pct": "health_pct"})
    non = out[out.comparison_group.eq("Non-Health donors")][["motivation_variable", "weighted_yes_pct"]].rename(columns={"weighted_yes_pct": "nonhealth_pct"})
    diff = health.merge(non, on="motivation_variable")
    diff["health_vs_nonhealth_gap_pct_points"] = diff["health_pct"] - diff["nonhealth_pct"]
    out = out.merge(diff[["motivation_variable", "health_vs_nonhealth_gap_pct_points"]], on="motivation_variable", how="left")
    out.to_csv(CHAPTER_ROOT / "outputs" / "chapter4_motivation_summary.csv", index=False)
    out.to_csv(CHAPTER_ROOT / "data" / "powerbi" / "chapter4_motivation_summary.csv", index=False)
    return out


def segment_summary(df, segment_col, output_name):
    health = df[df["is_health_donor"] & df[segment_col].notna()].copy()
    rows = []
    for segment, g in health.groupby(segment_col, observed=False):
        for sort_order, (var, label) in enumerate(MOTIVATIONS, start=1):
            valid = g[var].isin([1, 2])
            yes = g[var].eq(1)
            rows.append({
                "chapter": "Chapter 4",
                "segment_variable": segment_col,
                "segment_label": str(segment),
                "motivation_variable": var,
                "motivation_label": label,
                "sort_order": sort_order,
                "sample_health_donor_n": len(g),
                "weighted_health_donors": round(wsum(g)),
                "valid_denominator_weighted": round(wsum(g, valid)),
                "sample_yes_n": int(yes.sum()),
                "weighted_yes": round(wsum(g, yes)),
                "weighted_yes_pct": round(pct(wsum(g, yes), wsum(g, valid)), 1),
            })
    out = pd.DataFrame(rows)
    out.to_csv(CHAPTER_ROOT / "outputs" / f"{output_name}.csv", index=False)
    out.to_csv(CHAPTER_ROOT / "data" / "powerbi" / f"{output_name}.csv", index=False)
    return out


def validation(df, raw_hash, summary):
    checks = [
        ("raw_zip_exists", SOURCE_ZIP.exists(), "pass" if SOURCE_ZIP.exists() else "fail"),
        ("raw_data_sha256_inside_zip", raw_hash, "recorded"),
        ("row_count", len(df), "pass" if len(df) == 26678 else "fail"),
        ("health_donor_sample_n", int(df["is_health_donor"].sum()), "pass" if int(df["is_health_donor"].sum()) == 6399 else "fail"),
        ("motivation_summary_rows", len(summary), "pass" if len(summary) == len(MOTIVATIONS) * 3 else "fail"),
        ("motivation_codes_yes_no_or_special", int(df[[v for v, _ in MOTIVATIONS]].isin([1, 2, 6, 7, 8, 9]).all().all()), "pass"),
        ("weighted_health_donor_total", round(wsum(df, df["is_health_donor"]), 4), "pass" if abs(wsum(df, df["is_health_donor"]) - 6797271.8867) < 1 else "fail"),
    ]
    pd.DataFrame(checks, columns=["check", "result", "status"]).to_csv(CHAPTER_ROOT / "outputs" / "chapter4_validation_results.csv", index=False)


def write_outputs(df):
    cols = ["PUMFID", "WGHT_PER", "analysis_group", "is_charitable_donor", "is_health_donor", "health_donation_amount", "health_donation_count", "total_donation_amount", "total_donation_count", "AGEGR10_label", "GENDER2_label", "INCG2_label", "ED4CAT_label"] + [v for v, _ in MOTIVATIONS]
    out = df[cols].copy()
    for col in ["is_charitable_donor", "is_health_donor"]:
        out[col] = out[col].astype(int)
    out.to_csv(CHAPTER_ROOT / "data" / "processed" / "sgvp_2023_chapter4_why_they_give_analytical.csv", index=False)


def write_sql():
    sql = """-- Chapter 4 SQL layer: Why They Give.
-- Engine: SQLite 3.
-- Import data/processed/sgvp_2023_chapter4_why_they_give_analytical.csv as sgvp_chapter4.

DROP TABLE IF EXISTS sgvp_chapter4;
CREATE TABLE sgvp_chapter4 (
  PUMFID INTEGER, WGHT_PER REAL, analysis_group TEXT, is_charitable_donor INTEGER, is_health_donor INTEGER,
  health_donation_amount REAL, health_donation_count REAL, total_donation_amount REAL, total_donation_count REAL,
  AGEGR10_label TEXT, GENDER2_label TEXT, INCG2_label TEXT, ED4CAT_label TEXT,
"""
    for var, _ in MOTIVATIONS:
        sql += f"  {var} INTEGER,\n"
    sql = sql.rstrip(",\n") + "\n);\n\nDROP VIEW IF EXISTS vw_chapter4_motivation_summary;\nCREATE VIEW vw_chapter4_motivation_summary AS\n"
    unions = []
    for order, (var, label) in enumerate(MOTIVATIONS, start=1):
        unions.append(f"""SELECT '{var}' AS motivation_variable, '{label}' AS motivation_label, {order} AS sort_order,
  analysis_group AS comparison_group,
  COUNT(*) AS sample_donor_n,
  SUM(WGHT_PER) AS weighted_donors,
  SUM(CASE WHEN {var} IN (1, 2) THEN WGHT_PER ELSE 0 END) AS valid_denominator_weighted,
  SUM(CASE WHEN {var} = 1 THEN 1 ELSE 0 END) AS sample_yes_n,
  SUM(CASE WHEN {var} = 1 THEN WGHT_PER ELSE 0 END) AS weighted_yes,
  100.0 * SUM(CASE WHEN {var} = 1 THEN WGHT_PER ELSE 0 END) / NULLIF(SUM(CASE WHEN {var} IN (1, 2) THEN WGHT_PER ELSE 0 END), 0) AS weighted_yes_pct
FROM sgvp_chapter4
WHERE analysis_group IN ('Health donors', 'Non-Health donors')
GROUP BY analysis_group""")
    sql += "\nUNION ALL\n".join(unions) + ";\n"
    (CHAPTER_ROOT / "sql" / "chapter4_why_they_give_views.sql").write_text(sql, encoding="utf-8")


def write_docs(df, summary):
    top = summary[summary.comparison_group.eq("Health donors")].sort_values("weighted_yes_pct", ascending=False).head(5)
    gaps = summary[summary.comparison_group.eq("Health donors")].sort_values("health_vs_nonhealth_gap_pct_points", ascending=False).head(5)
    (CHAPTER_ROOT / "outputs" / "chapter4_findings.md").write_text(
        "# Chapter 4 Findings - Why They Give\n\n"
        "## Most Common Health Donor Motivations\n\n"
        + "\n".join(f"- {r.motivation_label}: {r.weighted_yes_pct:.1f}%." for r in top.itertuples())
        + "\n\n## Motivations More Common Among Health Donors Than Non-Health Donors\n\n"
        + "\n".join(f"- {r.motivation_label}: {r.health_vs_nonhealth_gap_pct_points:.1f} percentage-point gap." for r in gaps.itertuples())
        + "\n\n## Interpretation\n\n"
        "- Motivation rates are weighted descriptive estimates among charitable donors with valid yes/no responses.\n"
        "- Results support message testing themes but do not prove which message would cause additional giving.\n"
        "- Chapter 5 should compare these motivations with reported barriers to giving more.\n",
        encoding="utf-8",
    )
    (CHAPTER_ROOT / "docs" / "chapter4_methodology.md").write_text(
        "# Chapter 4 Methodology\n\n"
        "Business question: What motivates Health donors?\n\n"
        "The chapter uses official SGVP `RG_*` reasons-for-giving variables verified against the English codebook/SAS layout. "
        "Rates use 1=Yes over valid 1/2 yes/no denominators among charitable donors. Valid skip, don't know, refusal, and not stated values are excluded from valid denominators. "
        "Health donors use the validated Chapter 2 definition.\n",
        encoding="utf-8",
    )
    (CHAPTER_ROOT / "README.md").write_text(
        "# Chapter 4 - Why They Give\n\n"
        "This chapter analyzes documented reasons for charitable giving among Health donors and compares them with non-Health charitable donors.\n\n"
        "Run from the project root using the Chapter 2 Python environment:\n\n"
        "```powershell\n& \"Chapter 2\\.venv\\Scripts\\python.exe\" \"Chapter 4\\scripts\\chapter4_why_they_give.py\"\n```\n\n"
        "Outputs are organized into `docs/`, `outputs/`, `data/processed/`, `data/powerbi/`, and `sql/`.\n",
        encoding="utf-8",
    )


def audit_sql_vs_python():
    sql_path = CHAPTER_ROOT / "sql" / "chapter4_why_they_give_views.sql"
    sql = sql_path.read_text(encoding="utf-8")
    create_part = sql.split("DROP VIEW IF EXISTS vw_chapter4_motivation_summary;")[0]
    view_part = "DROP VIEW IF EXISTS vw_chapter4_motivation_summary;" + sql.split("DROP VIEW IF EXISTS vw_chapter4_motivation_summary;")[1]
    con = sqlite3.connect(":memory:")
    con.executescript(create_part)
    with open(CHAPTER_ROOT / "data" / "processed" / "sgvp_2023_chapter4_why_they_give_analytical.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        con.executemany(f"INSERT INTO sgvp_chapter4 VALUES ({','.join(['?'] * len(header))})", reader)
    con.executescript(view_part)
    sql_df = pd.read_sql_query("SELECT * FROM vw_chapter4_motivation_summary", con)
    py = pd.read_csv(CHAPTER_ROOT / "data" / "powerbi" / "chapter4_motivation_summary.csv")
    py = py[py["comparison_group"].isin(["Health donors", "Non-Health donors"])]
    merged = sql_df.merge(py, on=["motivation_variable", "comparison_group"], suffixes=("_sql", "_py"))
    ok = bool((merged["weighted_yes_pct_sql"].round(1) == merged["weighted_yes_pct_py"].round(1)).all())
    pd.DataFrame([{"check": "sql_motivation_rates_match_python_powerbi", "result": ok, "status": "pass" if ok else "fail"}]).to_csv(CHAPTER_ROOT / "outputs" / "chapter4_sql_audit.csv", index=False)


def main():
    df, raw_hash = load_raw()
    df = add_derivations(df)
    write_dictionary()
    write_outputs(df)
    summary = motivation_summary(df)
    for col, name in [
        ("AGEGR10_label", "chapter4_motivation_by_age"),
        ("INCG2_label", "chapter4_motivation_by_personal_income"),
        ("ED4CAT_label", "chapter4_motivation_by_education"),
        ("GENDER2_label", "chapter4_motivation_by_gender"),
        ("health_value_segment", "chapter4_motivation_by_health_value"),
        ("health_frequency_segment", "chapter4_motivation_by_health_frequency"),
    ]:
        segment_summary(df, col, name)
    validation(df, raw_hash, summary)
    write_sql()
    write_docs(df, summary)
    audit_sql_vs_python()
    print(json.dumps({"rows": len(df), "health_donor_sample_n": int(df["is_health_donor"].sum()), "chapter": "Chapter 4"}, indent=2))


if __name__ == "__main__":
    main()
