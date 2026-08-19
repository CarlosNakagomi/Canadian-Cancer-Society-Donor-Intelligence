from __future__ import annotations

import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[1] / ".python_packages"
if PACKAGE_DIR.exists():
    sys.path.insert(0, str(PACKAGE_DIR))

import numpy as np
import pandas as pd


CHAPTER_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = CHAPTER_ROOT.parent
SOURCE_ZIP = PROJECT_ROOT / "GVP_DBP_2023.zip"
CH1 = PROJECT_ROOT / "Chapter 1"

for folder in [
    CHAPTER_ROOT / "data" / "processed",
    CHAPTER_ROOT / "data" / "powerbi",
    CHAPTER_ROOT / "docs",
    CHAPTER_ROOT / "outputs",
    CHAPTER_ROOT / "sql",
]:
    folder.mkdir(parents=True, exist_ok=True)


VARIABLES = [
    {
        "name": "PUMFID",
        "start": 1,
        "end": 5,
        "type": "integer",
        "label": "Record identification",
        "values": "Anonymous record identifier.",
        "special": {"99996": "Valid skip", "99997": "Don't know", "99998": "Refusal", "99999": "Not stated"},
        "universe": "All respondents.",
        "role": "Record key / validation",
        "treatment": "Keep for QA only; exclude from aggregate reporting.",
    },
    {
        "name": "WGHT_PER",
        "start": 6,
        "end": 15,
        "type": "decimal",
        "label": "Person weight",
        "values": "Numeric person survey weight.",
        "special": {"99999.9996": "Valid skip", "99999.9997": "Don't know", "99999.9998": "Refusal", "99999.9999": "Not stated"},
        "universe": "All respondents.",
        "role": "Survey weight",
        "treatment": "Use for population-level estimates. Do not use sample percentages as Canadian percentages.",
    },
    {
        "name": "FG1FGIV",
        "start": 875,
        "end": 875,
        "type": "integer",
        "label": "Giving flag",
        "values": {1: "Giver", 2: "Non-giver"},
        "special": {6: "Valid skip", 7: "Don't know", 8: "Refusal", 9: "Not stated"},
        "universe": "All respondents.",
        "role": "All charitable donor flag",
        "treatment": "Map 1 to charitable donor, 2 to non-donor. Treat documented special codes as non-analytic if present.",
        "note": "A giver is defined as a respondent with at least one 'yes' in FG1A_030 to FG1A_170.",
    },
    {
        "name": "GS1DATOT",
        "start": 1061,
        "end": 1072,
        "type": "decimal",
        "label": "Total amount of donations",
        "values": "Dollar amount. Codebook range among amount responses: 000000000.50 to 000138800.00; 000000000.00 = None.",
        "special": {"000000000.00": "None", "999999999.96": "Valid skip", "999999999.97": "Don't know", "999999999.98": "Refusal", "999999999.99": "Not stated"},
        "universe": "FG1FGIV = 1.",
        "role": "Overall charitable giving amount",
        "treatment": "Set analytical total donation amount only for charitable donors with valid non-sentinel values.",
        "note": "All 'other' donations are included in the total amount.",
    },
    {
        "name": "GS1DNTOT",
        "start": 1059,
        "end": 1060,
        "type": "integer",
        "label": "Total number of financial donations",
        "values": "Numeric count of financial donations.",
        "special": {96: "Valid skip", 97: "Don't know", 98: "Refusal", 99: "Not stated"},
        "universe": "FG1FGIV = 1.",
        "role": "Overall charitable giving frequency",
        "treatment": "Set analytical total donation count only for charitable donors with valid non-sentinel values.",
        "note": "Derived count, including up to a maximum of 7 donations for each solicitation method.",
    },
    {
        "name": "GS1DNX05",
        "start": 1249,
        "end": 1250,
        "type": "integer",
        "label": "Number of donations (15) - Health",
        "values": "00 = No donations; 01-10 = Number.",
        "special": {0: "No donations", 96: "Valid skip", 97: "Don't know", 98: "Refusal", 99: "Not stated"},
        "universe": "FG1FGIV = 1.",
        "role": "Health ICNPO donation frequency",
        "treatment": "For donors, keep 0 as a legitimate no-health-donation value and positive values as Health donation counts. Valid skip applies to non-givers.",
        "note": "Derived ICNPO 15-category Health count based on 2-digit ICNPO codes.",
    },
    {
        "name": "GS1DAX05",
        "start": 1319,
        "end": 1330,
        "type": "decimal",
        "label": "Amount of donations (15) - Health",
        "values": "000000000.00 = None; amount responses in codebook: 000000000.50 to 000112500.00.",
        "special": {"000000000.00": "None", "999999999.96": "Valid skip", "999999999.97": "Don't know", "999999999.98": "Refusal", "999999999.99": "Not stated"},
        "universe": "FG1FGIV = 1.",
        "role": "Health ICNPO donation amount",
        "treatment": "For donors, keep 0 as a legitimate no-health-donation value and positive amounts as Health dollars. Valid skip applies to non-givers.",
        "note": "Derived ICNPO 15-category Health amount based on 2-digit ICNPO codes.",
    },
    {
        "name": "GS1DNX06",
        "start": 1251,
        "end": 1252,
        "type": "integer",
        "label": "Number of donations (15) - Hospitals",
        "values": "00 = No donations; 01-09 = Number.",
        "special": {0: "No donations", 96: "Valid skip", 97: "Don't know", 98: "Refusal", 99: "Not stated"},
        "universe": "FG1FGIV = 1.",
        "role": "Hospitals ICNPO donation frequency",
        "treatment": "Analyze separately from Health. Use only in explicitly labelled Hospital or broader health-related derived metrics.",
        "note": "Hospitals is a separate ICNPO category from Health.",
    },
    {
        "name": "GS1DAX06",
        "start": 1331,
        "end": 1342,
        "type": "decimal",
        "label": "Amount of donations (15) - Hospitals",
        "values": "000000000.00 = None; amount responses in codebook: 000000001.00 to 000052000.00.",
        "special": {"000000000.00": "None", "999999999.96": "Valid skip", "999999999.97": "Don't know", "999999999.98": "Refusal", "999999999.99": "Not stated"},
        "universe": "FG1FGIV = 1.",
        "role": "Hospitals ICNPO donation amount",
        "treatment": "Analyze separately from Health. Use only in explicitly labelled Hospital or broader health-related derived metrics.",
        "note": "Hospitals is a separate ICNPO category from Health.",
    },
    {
        "name": "AGEGR10",
        "start": 16,
        "end": 17,
        "type": "integer",
        "label": "Age group of respondent (groups of 10)",
        "values": {1: "15 to 24 years", 2: "25 to 34 years", 3: "35 to 44 years", 4: "45 to 54 years", 5: "55 to 64 years", 6: "65 to 74 years", 7: "75 years and over"},
        "special": {96: "Valid skip", 97: "Don't know", 98: "Refusal", 99: "Not stated"},
        "universe": "All respondents.",
        "role": "Demographic segment",
        "treatment": "Use labelled valid groups; exclude documented special codes from segment denominators if present.",
    },
    {
        "name": "GENDER2",
        "start": 18,
        "end": 18,
        "type": "integer",
        "label": "Gender of respondent after distribution of non-binary persons",
        "values": {1: "Man+", 2: "Woman+"},
        "special": {6: "Valid skip", 7: "Don't know", 8: "Refusal", 9: "Not stated"},
        "universe": "All respondents.",
        "role": "Demographic segment",
        "treatment": "Use labelled valid groups.",
    },
    {
        "name": "PRV",
        "start": 34,
        "end": 35,
        "type": "integer",
        "label": "Province of residence",
        "values": {10: "Newfoundland and Labrador", 11: "Prince Edward Island", 12: "Nova Scotia", 13: "New Brunswick", 24: "Quebec", 35: "Ontario", 46: "Manitoba", 47: "Saskatchewan", 48: "Alberta", 59: "British Columbia"},
        "special": {96: "Valid skip", 97: "Don't know", 98: "Refusal", 99: "Not stated"},
        "universe": "All respondents.",
        "role": "Geographic segment",
        "treatment": "Use sample counts with weighted estimates; label province comparisons descriptive.",
    },
    {
        "name": "INCG2",
        "start": 1612,
        "end": 1613,
        "type": "integer",
        "label": "Income - Personal income group (before tax)",
        "values": {1: "Less than $25,000", 2: "$25,000 to $49,999", 3: "$50,000 to $74,999", 4: "$75,000 to $99,999", 5: "$100,000 to $124,999", 6: "$125,000 and more"},
        "special": {96: "Valid skip", 97: "Don't know", 98: "Refusal", 99: "Not stated"},
        "universe": "All respondents.",
        "role": "Socioeconomic segment",
        "treatment": "Use labelled valid groups.",
    },
    {
        "name": "FAMINCG2",
        "start": 1615,
        "end": 1616,
        "type": "integer",
        "label": "Family income - Family income group (before tax)",
        "values": {1: "Less than $25,000", 2: "$25,000 to $49,999", 3: "$50,000 to $74,999", 4: "$75,000 to $99,999", 5: "$100,000 to $124,999", 6: "$125,000 and more"},
        "special": {96: "Valid skip", 97: "Don't know", 98: "Refusal", 99: "Not stated"},
        "universe": "All respondents.",
        "role": "Socioeconomic segment",
        "treatment": "Use labelled valid groups.",
    },
    {
        "name": "ED4CAT",
        "start": 1528,
        "end": 1528,
        "type": "integer",
        "label": "Education - Highest degree (4 categories)",
        "values": {1: "Less than high school", 2: "Graduated from high school", 3: "Post-secondary diploma", 4: "University diploma"},
        "special": {6: "Valid skip", 7: "Don't know", 8: "Refusal", 9: "Not stated"},
        "universe": "All respondents.",
        "role": "Socioeconomic segment",
        "treatment": "Use labelled valid groups.",
    },
    {
        "name": "MARSTAT",
        "start": 20,
        "end": 21,
        "type": "integer",
        "label": "Marital status of respondent",
        "values": {1: "Married", 2: "Living common law", 3: "Never married (not living common law)", 4: "Separated (not living common law)", 5: "Divorced (not living common law)", 6: "Widowed (not living common law)"},
        "special": {96: "Valid skip", 97: "Don't know", 98: "Refusal", 99: "Not stated"},
        "universe": "All respondents.",
        "role": "Supplementary life-stage segment",
        "treatment": "Use if it adds interpretive value beyond age/income.",
    },
    {
        "name": "HSDSIZEC",
        "start": 22,
        "end": 23,
        "type": "integer",
        "label": "Household size of respondent",
        "values": "01-05 = Number of persons; 06 = 6 or more persons.",
        "special": {96: "Valid skip", 97: "Don't know", 98: "Refusal", 99: "Not stated"},
        "universe": "All respondents.",
        "role": "Supplementary household segment",
        "treatment": "Use labelled household-size groups if analytically useful.",
        "note": "In 2023, respondents were asked directly to provide the number of usual residents staying at the address.",
    },
    {
        "name": "DLFS",
        "start": 1531,
        "end": 1531,
        "type": "integer",
        "label": "Labour force status",
        "values": {1: "Employed", 2: "Unemployed", 3: "Not in labour force", 4: "Unable to determine"},
        "special": {6: "Valid skip", 7: "Don't know", 8: "Refusal", 9: "Not stated"},
        "universe": "All respondents.",
        "role": "Supplementary socioeconomic segment",
        "treatment": "Use descriptively; do not infer causality.",
    },
    {
        "name": "FV1FVOL",
        "start": 51,
        "end": 51,
        "type": "integer",
        "label": "Volunteer flag",
        "values": {1: "Volunteer", 2: "Non-volunteer"},
        "special": {6: "Valid skip", 7: "Don't know", 8: "Refusal", 9: "Not stated"},
        "universe": "All respondents.",
        "role": "Formal volunteering engagement",
        "treatment": "Compare Health donors, non-Health donors, and non-donors.",
        "note": "A volunteer is defined as a respondent with at least one 'yes' in FV_020 to FV_160.",
    },
    {
        "name": "FV_030",
        "start": 37,
        "end": 37,
        "type": "integer",
        "label": "Formal volunteering - Fundraising",
        "values": {1: "Yes", 2: "No"},
        "special": {6: "Valid skip", 7: "Don't know", 8: "Refusal", 9: "Not stated"},
        "universe": "All respondents.",
        "role": "Fundraising volunteering engagement",
        "treatment": "Compare yes rates across donor groups.",
    },
    {
        "name": "FV_100",
        "start": 44,
        "end": 44,
        "type": "integer",
        "label": "Formal volunteering - Health care or support",
        "values": {1: "Yes", 2: "No"},
        "special": {6: "Valid skip", 7: "Don't know", 8: "Refusal", 9: "Not stated"},
        "universe": "All respondents.",
        "role": "Health-related volunteering engagement",
        "treatment": "Compare yes rates across donor groups.",
    },
    {
        "name": "VD1DHRS",
        "start": 86,
        "end": 93,
        "type": "decimal",
        "label": "Formal Volunteering - Total hours - Canadian",
        "values": "Hours; codebook range: 00000.17 to 08602.90.",
        "special": {"99999.96": "Valid skip", "99999.97": "Don't know", "99999.98": "Refusal", "99999.99": "Not stated"},
        "universe": "FV1FVOL = 1.",
        "role": "Formal volunteering intensity",
        "treatment": "Use only for volunteers with valid hours. Valid skip applies to non-volunteers.",
        "note": "Derived total hours volunteered, including mandatory unpaid work, employer supported hours, and amounts of less than one hour.",
    },
]


SORT_ORDERS = {
    "AGEGR10": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7},
    "GENDER2": {1: 1, 2: 2},
    "PRV": {10: 1, 11: 2, 12: 3, 13: 4, 24: 5, 35: 6, 46: 7, 47: 8, 48: 9, 59: 10},
    "INCG2": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6},
    "FAMINCG2": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6},
    "ED4CAT": {1: 1, 2: 2, 3: 3, 4: 4},
    "MARSTAT": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6},
    "HSDSIZEC": {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6},
    "DLFS": {1: 1, 2: 2, 3: 3, 4: 4},
}


def find_zip_member(zf: zipfile.ZipFile, suffix: str) -> str:
    for name in zf.namelist():
        if name.replace("\\", "/").endswith(suffix):
            return name
    raise FileNotFoundError(f"Could not find {suffix} in {SOURCE_ZIP}")


def read_raw_dataframe() -> tuple[pd.DataFrame, str]:
    colspecs = [(v["start"] - 1, v["end"]) for v in VARIABLES]
    names = [v["name"] for v in VARIABLES]
    with zipfile.ZipFile(SOURCE_ZIP) as zf:
        member = find_zip_member(zf, "GVP_DBP_2023_PUMF_FMGD.txt")
        raw_bytes = zf.read(member)
    raw_hash = hashlib.sha256(raw_bytes).hexdigest()
    text = raw_bytes.decode("ascii")
    df = pd.read_fwf(io.StringIO(text), colspecs=colspecs, names=names, dtype=str)
    for v in VARIABLES:
        df[v["name"] + "_raw"] = df[v["name"]].astype("string").str.strip()
        df[v["name"]] = pd.to_numeric(df[v["name"] + "_raw"], errors="coerce")
    return df, raw_hash


def label_for(value, spec):
    if pd.isna(value):
        return pd.NA
    if isinstance(spec["values"], dict) and int(value) in spec["values"]:
        return spec["values"][int(value)]
    if int(value) in spec.get("special", {}):
        return spec["special"][int(value)]
    if spec["name"] == "HSDSIZEC" and 1 <= int(value) <= 5:
        return f"{int(value)} person" if int(value) == 1 else f"{int(value)} persons"
    if spec["name"] == "HSDSIZEC" and int(value) == 6:
        return "6 or more persons"
    return pd.NA


def is_special_amount(series: pd.Series) -> pd.Series:
    return series.isin([999999999.96, 999999999.97, 999999999.98, 999999999.99])


def is_special_count(series: pd.Series) -> pd.Series:
    return series.isin([96, 97, 98, 99])


def wsum(df: pd.DataFrame, mask=None) -> float:
    if mask is None:
        return float(df["WGHT_PER"].sum())
    return float(df.loc[mask, "WGHT_PER"].sum())


def weighted_mean(frame: pd.DataFrame, value_col: str) -> float:
    valid = frame[[value_col, "WGHT_PER"]].dropna()
    if valid.empty or valid["WGHT_PER"].sum() == 0:
        return np.nan
    return float((valid[value_col] * valid["WGHT_PER"]).sum() / valid["WGHT_PER"].sum())


def weighted_median(frame: pd.DataFrame, value_col: str) -> float:
    valid = frame[[value_col, "WGHT_PER"]].dropna().sort_values(value_col)
    if valid.empty:
        return np.nan
    cutoff = valid["WGHT_PER"].sum() / 2
    return float(valid.loc[valid["WGHT_PER"].cumsum() >= cutoff, value_col].iloc[0])


def weighted_percentile(frame: pd.DataFrame, value_col: str, percentile: float) -> float:
    valid = frame[[value_col, "WGHT_PER"]].dropna().sort_values(value_col)
    if valid.empty:
        return np.nan
    cutoff = valid["WGHT_PER"].sum() * percentile
    return float(valid.loc[valid["WGHT_PER"].cumsum() >= cutoff, value_col].iloc[0])


def weighted_top_share(frame: pd.DataFrame, value_col: str, top_weight_share: float) -> dict:
    valid = frame[[value_col, "WGHT_PER"]].dropna().sort_values(value_col, ascending=False).copy()
    if valid.empty:
        return {
            "sample_n_touched": 0,
            "full_sample_n_included": 0,
            "weighted_donors_included": 0.0,
            "weighted_dollars_included": 0.0,
            "weighted_dollar_share_pct": np.nan,
            "boundary_fraction_used": np.nan,
        }

    target_weight = valid["WGHT_PER"].sum() * top_weight_share
    total_dollars = float((valid[value_col] * valid["WGHT_PER"]).sum())
    valid["cum_weight_before"] = valid["WGHT_PER"].cumsum() - valid["WGHT_PER"]
    valid["take_weight"] = np.minimum(valid["WGHT_PER"], np.maximum(0, target_weight - valid["cum_weight_before"]))
    used = valid[valid["take_weight"] > 0].copy()
    used_dollars = float((used[value_col] * used["take_weight"]).sum())
    full_rows = used[used["take_weight"] >= used["WGHT_PER"] - 1e-9]
    boundary_fraction = np.nan
    if not used.empty and used["take_weight"].iloc[-1] < used["WGHT_PER"].iloc[-1] - 1e-9:
        boundary_fraction = float(used["take_weight"].iloc[-1] / used["WGHT_PER"].iloc[-1])
    return {
        "sample_n_touched": len(used),
        "full_sample_n_included": len(full_rows),
        "weighted_donors_included": float(used["take_weight"].sum()),
        "weighted_dollars_included": used_dollars,
        "weighted_dollar_share_pct": pct(used_dollars, total_dollars),
        "boundary_fraction_used": boundary_fraction,
    }


def pct(num: float, den: float) -> float:
    return np.nan if den == 0 else 100 * num / den


def fmt_money(x: float) -> str:
    if pd.isna(x):
        return ""
    return f"{x:.2f}"


def add_derivations(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for spec in VARIABLES:
        if isinstance(spec["values"], dict) or spec["name"] == "HSDSIZEC":
            df[spec["name"] + "_label"] = df[spec["name"]].apply(lambda v, s=spec: label_for(v, s))

    df["is_charitable_donor"] = df["FG1FGIV"].eq(1)
    df["donor_group"] = np.select(
        [df["FG1FGIV"].eq(1), df["FG1FGIV"].eq(2)],
        ["Charitable donor", "Non-donor"],
        default="Special/unknown donor status",
    )

    df["total_donation_amount"] = df["GS1DATOT"].where(df["is_charitable_donor"] & ~is_special_amount(df["GS1DATOT"]))
    df["total_donation_count"] = df["GS1DNTOT"].where(df["is_charitable_donor"] & ~is_special_count(df["GS1DNTOT"]))
    df["health_donation_amount"] = df["GS1DAX05"].where(df["is_charitable_donor"] & ~is_special_amount(df["GS1DAX05"]))
    df["health_donation_count"] = df["GS1DNX05"].where(df["is_charitable_donor"] & ~is_special_count(df["GS1DNX05"]))
    df["hospital_donation_amount"] = df["GS1DAX06"].where(df["is_charitable_donor"] & ~is_special_amount(df["GS1DAX06"]))
    df["hospital_donation_count"] = df["GS1DNX06"].where(df["is_charitable_donor"] & ~is_special_count(df["GS1DNX06"]))

    df["is_health_donor"] = df["is_charitable_donor"] & (
        df["health_donation_amount"].fillna(0).gt(0) | df["health_donation_count"].fillna(0).gt(0)
    )
    df["is_hospital_donor"] = df["is_charitable_donor"] & (
        df["hospital_donation_amount"].fillna(0).gt(0) | df["hospital_donation_count"].fillna(0).gt(0)
    )
    df["is_broader_health_related_donor"] = df["is_health_donor"] | df["is_hospital_donor"]
    df["health_share_of_total_giving_pct"] = np.where(
        df["is_health_donor"] & df["total_donation_amount"].gt(0),
        100 * df["health_donation_amount"] / df["total_donation_amount"],
        np.nan,
    )
    df["volunteer_hours"] = df["VD1DHRS"].where(df["FV1FVOL"].eq(1) & ~df["VD1DHRS"].isin([99999.96, 99999.97, 99999.98, 99999.99]))
    df["analysis_group"] = np.select(
        [df["is_health_donor"], df["is_charitable_donor"] & ~df["is_health_donor"], df["FG1FGIV"].eq(2)],
        ["Health donors", "Non-Health donors", "Non-donors"],
        default="Special/unknown",
    )
    return df


def write_variable_dictionary():
    rows = []
    for spec in VARIABLES:
        values = spec["values"]
        if isinstance(values, dict):
            values_text = "; ".join(f"{k}={v}" for k, v in values.items())
        else:
            values_text = values
        special = spec["special"]
        special_text = "; ".join(f"{k}={v}" for k, v in special.items())
        rows.append(
            {
                "variable_name": spec["name"],
                "official_label_description": spec["label"],
                "position": f"{spec['start']}-{spec['end']}",
                "valid_values_categories": values_text,
                "special_codes": special_text,
                "valid_skip": "; ".join(str(k) for k, v in special.items() if v == "Valid skip"),
                "dont_know": "; ".join(str(k) for k, v in special.items() if v == "Don't know"),
                "refusal": "; ".join(str(k) for k, v in special.items() if v == "Refusal"),
                "not_stated": "; ".join(str(k) for k, v in special.items() if v == "Not stated"),
                "universe_applicability": spec["universe"],
                "analytical_role": spec["role"],
                "proposed_treatment": spec["treatment"],
                "official_note": spec.get("note", ""),
                "source": "Statistics Canada SGVP 2023 PUMF English data dictionary/codebook and English SAS layout files",
                "source_reference": "Chapter 1/data/raw/GVP_DBP_2023/Codebook_Dictionaire de données/GVP_2023_PUMF_EN.pdf; Layout_MisEnPages/SAS/GVP_DBP_2023_lbe.SAS; GVP_DBP_2023_frq.SAS; GVP_DBP_2023_fmt.SAS; GVP_DBP_2023_pfe.SAS",
            }
        )
    pd.DataFrame(rows).to_csv(CHAPTER_ROOT / "docs" / "chapter2_variable_dictionary.csv", index=False)


def data_quality_profile(df: pd.DataFrame):
    rows = []
    total_w = wsum(df)
    for spec in VARIABLES:
        raw_col = spec["name"] + "_raw"
        counts = df.groupby(raw_col, dropna=False).agg(sample_n=(raw_col, "size"), weighted_population=("WGHT_PER", "sum")).reset_index()
        for _, row in counts.sort_values("sample_n", ascending=False).iterrows():
            raw_value = row[raw_col]
            numeric = pd.to_numeric(pd.Series([raw_value]), errors="coerce").iloc[0]
            issue = "Valid observed value"
            for code, meaning in spec["special"].items():
                if str(raw_value) == str(code) or (pd.notna(numeric) and str(numeric) == str(float(code))):
                    issue = meaning
                    break
            rows.append(
                {
                    "variable_name": spec["name"],
                    "raw_value": raw_value,
                    "sample_n": int(row["sample_n"]),
                    "sample_pct": round(100 * row["sample_n"] / len(df), 2),
                    "weighted_population": round(row["weighted_population"]),
                    "weighted_pct": round(100 * row["weighted_population"] / total_w, 2),
                    "issue_type": issue,
                }
            )
    pd.DataFrame(rows).to_csv(CHAPTER_ROOT / "outputs" / "chapter2_data_quality_profile.csv", index=False)


def summarize_group(df: pd.DataFrame, label: str, mask) -> dict:
    g = df.loc[mask].copy()
    group_donors = g.loc[g["is_charitable_donor"]]
    health = g.loc[g["is_health_donor"]]
    return {
        "group": label,
        "sample_n": len(g),
        "weighted_population": round(wsum(g)),
        "sample_charitable_donor_n": int(g["is_charitable_donor"].sum()),
        "weighted_charitable_donors": round(wsum(g, g["is_charitable_donor"])),
        "weighted_charitable_donor_rate_pct": round(pct(wsum(g, g["is_charitable_donor"]), wsum(g)), 1),
        "sample_health_donor_n": int(g["is_health_donor"].sum()),
        "weighted_health_donors": round(wsum(g, g["is_health_donor"])),
        "weighted_health_donor_rate_population_pct": round(pct(wsum(g, g["is_health_donor"]), wsum(g)), 1),
        "weighted_health_donor_rate_among_donors_pct": round(pct(wsum(g, g["is_health_donor"]), wsum(group_donors)), 1) if len(group_donors) else np.nan,
        "weighted_mean_total_donation_among_group_donors": round(weighted_mean(group_donors, "total_donation_amount"), 2),
        "weighted_median_total_donation_among_group_donors": round(weighted_median(group_donors, "total_donation_amount"), 2),
        "weighted_mean_total_frequency_among_group_donors": round(weighted_mean(group_donors, "total_donation_count"), 2),
        "weighted_median_total_frequency_among_group_donors": round(weighted_median(group_donors, "total_donation_count"), 2),
        "weighted_total_health_dollars": round(float((health["health_donation_amount"] * health["WGHT_PER"]).sum())),
        "weighted_mean_health_donation": round(weighted_mean(health, "health_donation_amount"), 2),
        "weighted_median_health_donation": round(weighted_median(health, "health_donation_amount"), 2),
        "weighted_mean_health_frequency": round(weighted_mean(health, "health_donation_count"), 2),
        "weighted_median_health_frequency": round(weighted_median(health, "health_donation_count"), 2),
    }


def make_overview(df: pd.DataFrame):
    all_donors = df["is_charitable_donor"]
    health = df["is_health_donor"]
    hospitals = df["is_hospital_donor"]
    broader = df["is_broader_health_related_donor"]
    ch1_summary = pd.read_csv(CH1 / "outputs" / "chapter1" / "chapter1_overall_summary.csv")
    ch1_map = dict(zip(ch1_summary["metric"], ch1_summary["weighted_value"]))
    rows = [
        {"metric": "Weighted Canadian population represented", "sample_value": len(df), "weighted_value": round(wsum(df)), "note": "All respondents"},
        {"metric": "All charitable donors - Chapter 1 baseline", "sample_value": int(all_donors.sum()), "weighted_value": round(wsum(df, all_donors)), "note": f"Chapter 1 weighted donor rate: {ch1_map.get('Donor participation rate')}"},
        {"metric": "Health donors", "sample_value": int(health.sum()), "weighted_value": round(wsum(df, health)), "note": "Primary Chapter 2 definition: positive valid Health amount or count"},
        {"metric": "Health donor rate among Canadian population", "sample_value": f"{100 * health.mean():.1f}%", "weighted_value": f"{pct(wsum(df, health), wsum(df)):.1f}%", "note": "Denominator: all respondents / weighted Canadian population"},
        {"metric": "Health donor rate among charitable donors", "sample_value": f"{100 * health.sum() / all_donors.sum():.1f}%", "weighted_value": f"{pct(wsum(df, health), wsum(df, all_donors)):.1f}%", "note": "Denominator: charitable donors only"},
        {"metric": "Weighted total Health donation dollars", "sample_value": "", "weighted_value": round(float((df.loc[health, "health_donation_amount"] * df.loc[health, "WGHT_PER"]).sum())), "note": "Health ICNPO category only"},
        {"metric": "Mean Health donation among Health donors", "sample_value": round(df.loc[health, "health_donation_amount"].mean(), 2), "weighted_value": round(weighted_mean(df.loc[health], "health_donation_amount"), 2), "note": "Use with median because donations are right-skewed"},
        {"metric": "Median Health donation among Health donors", "sample_value": round(df.loc[health, "health_donation_amount"].median(), 2), "weighted_value": round(weighted_median(df.loc[health], "health_donation_amount"), 2), "note": "Preferred central tendency metric"},
        {"metric": "Mean total charitable giving among Health donors", "sample_value": round(df.loc[health, "total_donation_amount"].mean(), 2), "weighted_value": round(weighted_mean(df.loc[health], "total_donation_amount"), 2), "note": "All charity giving by Health donors"},
        {"metric": "Median total charitable giving among Health donors", "sample_value": round(df.loc[health, "total_donation_amount"].median(), 2), "weighted_value": round(weighted_median(df.loc[health], "total_donation_amount"), 2), "note": "All charity giving by Health donors"},
        {"metric": "Median Health share of total giving among Health donors", "sample_value": round(df.loc[health, "health_share_of_total_giving_pct"].median(), 1), "weighted_value": round(weighted_median(df.loc[health], "health_share_of_total_giving_pct"), 1), "note": "Health dollars / total charitable dollars"},
        {"metric": "Hospital donors", "sample_value": int(hospitals.sum()), "weighted_value": round(wsum(df, hospitals)), "note": "Separate ICNPO Hospitals category, not combined into primary Health donor definition"},
        {"metric": "Broader health-related donors", "sample_value": int(broader.sum()), "weighted_value": round(wsum(df, broader)), "note": "Secondary derived metric: Health OR Hospitals"},
    ]
    overview = pd.DataFrame(rows)
    overview.to_csv(CHAPTER_ROOT / "outputs" / "chapter2_health_donor_overview.csv", index=False)
    overview.to_csv(CHAPTER_ROOT / "data" / "powerbi" / "health_donor_overview.csv", index=False)


def segment_table(df: pd.DataFrame, var: str, label_col: str, file_stem: str):
    excluded_labels = {"Valid skip", "Don't know", "Refusal", "Not stated"}
    valid = df[df[label_col].notna() & ~df[label_col].isin(excluded_labels)].copy()
    rows = []
    total_health_w = wsum(df, df["is_health_donor"])
    for key, g in valid.groupby(var, dropna=False):
        donors = g[g["is_charitable_donor"]]
        health = g[g["is_health_donor"]]
        nonhealth_donors = g[g["is_charitable_donor"] & ~g["is_health_donor"]]
        rows.append(
            {
                "segment_variable": var,
                "segment_code": int(key) if pd.notna(key) else "",
                "segment_label": g[label_col].iloc[0],
                "sort_order": SORT_ORDERS.get(var, {}).get(int(key), int(key) if pd.notna(key) else 999),
                "sample_n": len(g),
                "weighted_population": round(wsum(g)),
                "sample_charitable_donor_n": int(g["is_charitable_donor"].sum()),
                "weighted_charitable_donors": round(wsum(g, g["is_charitable_donor"])),
                "weighted_charitable_donor_rate_pct": round(pct(wsum(g, g["is_charitable_donor"]), wsum(g)), 1),
                "sample_health_donor_n": int(g["is_health_donor"].sum()),
                "weighted_health_donors": round(wsum(g, g["is_health_donor"])),
                "weighted_health_donor_rate_population_pct": round(pct(wsum(g, g["is_health_donor"]), wsum(g)), 1),
                "weighted_health_donor_rate_among_donors_pct": round(pct(wsum(g, g["is_health_donor"]), wsum(donors)), 1) if len(donors) else np.nan,
                "weighted_health_donor_composition_pct": round(pct(wsum(g, g["is_health_donor"]), total_health_w), 1),
                "weighted_mean_health_donation": round(weighted_mean(health, "health_donation_amount"), 2),
                "weighted_median_health_donation": round(weighted_median(health, "health_donation_amount"), 2),
                "weighted_mean_total_giving_health_donors": round(weighted_mean(health, "total_donation_amount"), 2),
                "weighted_median_total_giving_health_donors": round(weighted_median(health, "total_donation_amount"), 2),
                "weighted_mean_total_giving_nonhealth_donors": round(weighted_mean(nonhealth_donors, "total_donation_amount"), 2),
                "weighted_median_total_giving_nonhealth_donors": round(weighted_median(nonhealth_donors, "total_donation_amount"), 2),
            }
        )
    out = pd.DataFrame(rows).sort_values("sort_order")
    if var == "PRV":
        out["reliability_note"] = "Descriptive province estimate; sample counts are shown, and no bootstrap confidence intervals are applied in Chapter 2."
    out.to_csv(CHAPTER_ROOT / "outputs" / f"{file_stem}.csv", index=False)
    out.to_csv(CHAPTER_ROOT / "data" / "powerbi" / f"{file_stem}.csv", index=False)
    return out


def make_comparison_and_segments(df: pd.DataFrame):
    comparison = pd.DataFrame(
        [
            summarize_group(df, "Canadian population", df.index == df.index),
            summarize_group(df, "All charitable donors", df["is_charitable_donor"]),
            summarize_group(df, "Health donors", df["is_health_donor"]),
            summarize_group(df, "Non-Health donors", df["is_charitable_donor"] & ~df["is_health_donor"]),
            summarize_group(df, "Non-donors", df["FG1FGIV"].eq(2)),
        ]
    )
    comparison.to_csv(CHAPTER_ROOT / "outputs" / "chapter2_donor_group_comparison.csv", index=False)
    comparison.to_csv(CHAPTER_ROOT / "data" / "powerbi" / "health_donor_group_comparison.csv", index=False)

    segment_table(df, "AGEGR10", "AGEGR10_label", "health_donor_profile_age")
    segment_table(df, "INCG2", "INCG2_label", "health_donor_profile_personal_income")
    segment_table(df, "FAMINCG2", "FAMINCG2_label", "health_donor_profile_family_income")
    segment_table(df, "ED4CAT", "ED4CAT_label", "health_donor_profile_education")
    segment_table(df, "GENDER2", "GENDER2_label", "health_donor_profile_gender")
    segment_table(df, "PRV", "PRV_label", "health_donor_profile_province")
    segment_table(df, "MARSTAT", "MARSTAT_label", "health_donor_profile_marital_status")
    segment_table(df, "HSDSIZEC", "HSDSIZEC_label", "health_donor_profile_household_size")
    segment_table(df, "DLFS", "DLFS_label", "health_donor_profile_labour_force")


def make_distribution(df: pd.DataFrame):
    health = df[df["is_health_donor"]].copy()
    bands = [
        ("$0.50 to $49", 1, 0.5, 49.999),
        ("$50 to $99", 2, 50, 99.999),
        ("$100 to $249", 3, 100, 249.999),
        ("$250 to $499", 4, 250, 499.999),
        ("$500 to $999", 5, 500, 999.999),
        ("$1,000 to $4,999", 6, 1000, 4999.999),
        ("$5,000 and over", 7, 5000, np.inf),
    ]
    total_health_w = wsum(health)
    total_health_dollars = float((health["health_donation_amount"] * health["WGHT_PER"]).sum())
    rows = []
    for label, sort_order, lo, hi in bands:
        g = health[health["health_donation_amount"].between(lo, hi)]
        dollars = float((g["health_donation_amount"] * g["WGHT_PER"]).sum())
        rows.append(
            {
                "amount_band": label,
                "sort_order": sort_order,
                "sample_health_donor_n": len(g),
                "weighted_health_donors": round(wsum(g)),
                "weighted_health_donor_share_pct": round(pct(wsum(g), total_health_w), 1),
                "weighted_health_donation_dollars": round(dollars),
                "weighted_health_dollar_share_pct": round(pct(dollars, total_health_dollars), 1),
            }
        )
    dist = pd.DataFrame(rows)
    dist.to_csv(CHAPTER_ROOT / "outputs" / "chapter2_health_donation_distribution.csv", index=False)
    dist.to_csv(CHAPTER_ROOT / "data" / "powerbi" / "health_donation_distribution.csv", index=False)

    freq = (
        health.groupby("health_donation_count")
        .agg(sample_health_donor_n=("PUMFID", "size"), weighted_health_donors=("WGHT_PER", "sum"))
        .reset_index()
        .sort_values("health_donation_count")
    )
    freq["weighted_health_donor_share_pct"] = 100 * freq["weighted_health_donors"] / total_health_w
    freq.to_csv(CHAPTER_ROOT / "outputs" / "chapter2_health_donation_frequency.csv", index=False)
    freq.to_csv(CHAPTER_ROOT / "data" / "powerbi" / "health_donation_frequency.csv", index=False)

    concentration = []
    for share in [0.01, 0.05, 0.10, 0.25, 0.50]:
        result = weighted_top_share(health, "health_donation_amount", share)
        concentration.append(
            {
                "top_weighted_health_donor_share": f"Top {int(share*100)}%",
                "method": "Exact weighted top-share using fractional boundary weight at the percentile cutoff",
                "sample_n_touched": result["sample_n_touched"],
                "full_sample_n_included": result["full_sample_n_included"],
                "weighted_health_donors_included": round(result["weighted_donors_included"]),
                "weighted_health_donation_dollars": round(result["weighted_dollars_included"]),
                "weighted_health_dollar_share_pct": round(result["weighted_dollar_share_pct"], 1),
                "boundary_fraction_used": round(result["boundary_fraction_used"], 6) if pd.notna(result["boundary_fraction_used"]) else "",
            }
        )
    pd.DataFrame(concentration).to_csv(CHAPTER_ROOT / "outputs" / "chapter2_health_donor_concentration.csv", index=False)


def make_volunteering(df: pd.DataFrame):
    def valid_rate(group: pd.DataFrame, col: str) -> tuple[int, float, float, float]:
        valid = group[group[col].isin([1, 2])]
        yes = group[col].eq(1)
        return int(yes.sum()), wsum(valid), round(pct(wsum(group, yes), wsum(valid)), 1), round(wsum(group, yes))

    rows = []
    for label, mask in {
        "Health donors": df["is_health_donor"],
        "Non-Health donors": df["is_charitable_donor"] & ~df["is_health_donor"],
        "Non-donors": df["FG1FGIV"].eq(2),
        "All charitable donors": df["is_charitable_donor"],
    }.items():
        g = df[mask]
        volunteers = g[g["FV1FVOL"].eq(1)]
        volunteer_n, volunteer_valid_w, volunteer_rate, weighted_volunteers = valid_rate(g, "FV1FVOL")
        fundraising_n, fundraising_valid_w, fundraising_rate, weighted_fundraising = valid_rate(g, "FV_030")
        healthcare_n, healthcare_valid_w, healthcare_rate, weighted_healthcare = valid_rate(g, "FV_100")
        rows.append(
            {
                "comparison_group": label,
                "sample_n": len(g),
                "weighted_population": round(wsum(g)),
                "sample_volunteer_n": volunteer_n,
                "weighted_volunteers": weighted_volunteers,
                "weighted_volunteering_valid_denominator": round(volunteer_valid_w),
                "weighted_volunteer_rate_pct": volunteer_rate,
                "sample_fundraising_volunteer_n": fundraising_n,
                "weighted_fundraising_volunteers": weighted_fundraising,
                "weighted_fundraising_valid_denominator": round(fundraising_valid_w),
                "weighted_fundraising_volunteer_rate_pct": fundraising_rate,
                "sample_healthcare_support_volunteer_n": healthcare_n,
                "weighted_healthcare_support_volunteers": weighted_healthcare,
                "weighted_healthcare_support_valid_denominator": round(healthcare_valid_w),
                "weighted_healthcare_support_volunteer_rate_pct": healthcare_rate,
                "volunteer_sample_n_with_hours": len(volunteers),
                "weighted_mean_volunteer_hours_among_volunteers": round(weighted_mean(volunteers, "volunteer_hours"), 2),
                "weighted_median_volunteer_hours_among_volunteers": round(weighted_median(volunteers, "volunteer_hours"), 2),
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(CHAPTER_ROOT / "outputs" / "chapter2_health_donor_volunteering.csv", index=False)
    out.to_csv(CHAPTER_ROOT / "data" / "powerbi" / "health_donor_volunteering.csv", index=False)


def validation(df: pd.DataFrame, raw_hash: str):
    health = df["is_health_donor"]
    hosp = df["is_hospital_donor"]
    broader = df["is_broader_health_related_donor"]
    checks = [
        {"check": "raw_zip_exists", "result": str(SOURCE_ZIP.exists()), "status": "pass" if SOURCE_ZIP.exists() else "fail"},
        {"check": "raw_data_sha256_inside_zip", "result": raw_hash, "status": "recorded"},
        {"check": "row_count", "result": len(df), "status": "pass" if len(df) == 26678 else "fail"},
        {"check": "charitable_donor_sample_n", "result": int(df["is_charitable_donor"].sum()), "status": "pass" if int(df["is_charitable_donor"].sum()) == 15934 else "fail"},
        {"check": "health_donor_flag_positive_amount_or_count", "result": int(health.sum()), "status": "pass" if bool((df.loc[health, "health_donation_amount"].gt(0) | df.loc[health, "health_donation_count"].gt(0)).all()) else "fail"},
        {"check": "positive_health_amount_has_positive_count", "result": int(df["health_donation_amount"].gt(0).sum()), "status": "pass" if bool((df.loc[df["health_donation_amount"].gt(0), "health_donation_count"] > 0).all()) else "fail"},
        {"check": "positive_health_count_has_positive_amount", "result": int(df["health_donation_count"].gt(0).sum()), "status": "pass" if bool((df.loc[df["health_donation_count"].gt(0), "health_donation_amount"] > 0).all()) else "fail"},
        {"check": "non_givers_health_amount_valid_skip", "result": int((df.loc[df["FG1FGIV"].eq(2), "GS1DAX05"] == 999999999.96).sum()), "status": "pass" if bool((df.loc[df["FG1FGIV"].eq(2), "GS1DAX05"] == 999999999.96).all()) else "fail"},
        {"check": "non_givers_health_count_valid_skip", "result": int((df.loc[df["FG1FGIV"].eq(2), "GS1DNX05"] == 96).sum()), "status": "pass" if bool((df.loc[df["FG1FGIV"].eq(2), "GS1DNX05"] == 96).all()) else "fail"},
        {"check": "health_and_hospital_categories_kept_separate", "result": f"health={int(health.sum())}; hospital={int(hosp.sum())}; broader={int(broader.sum())}", "status": "pass"},
        {"check": "weighted_population_total", "result": round(wsum(df), 4), "status": "pass" if abs(wsum(df) - 33038673.0041) < 1 else "review"},
        {"check": "health_amount_not_greater_than_total_amount", "result": int((df.loc[health, "health_donation_amount"] <= df.loc[health, "total_donation_amount"]).sum()), "status": "pass" if bool((df.loc[health, "health_donation_amount"] <= df.loc[health, "total_donation_amount"]).all()) else "fail"},
    ]
    pd.DataFrame(checks).to_csv(CHAPTER_ROOT / "outputs" / "chapter2_validation_results.csv", index=False)


def write_analytical_dataset(df: pd.DataFrame):
    columns = [
        "PUMFID", "WGHT_PER", "FG1FGIV", "donor_group", "is_charitable_donor",
        "is_health_donor", "is_hospital_donor", "is_broader_health_related_donor",
        "total_donation_amount", "total_donation_count", "health_donation_amount", "health_donation_count",
        "hospital_donation_amount", "hospital_donation_count", "health_share_of_total_giving_pct",
        "AGEGR10", "AGEGR10_label", "GENDER2", "GENDER2_label", "PRV", "PRV_label",
        "INCG2", "INCG2_label", "FAMINCG2", "FAMINCG2_label", "ED4CAT", "ED4CAT_label",
        "MARSTAT", "MARSTAT_label", "HSDSIZEC", "HSDSIZEC_label", "DLFS", "DLFS_label",
        "FV1FVOL", "FV1FVOL_label", "FV_030", "FV_030_label", "FV_100", "FV_100_label",
        "volunteer_hours", "analysis_group",
    ]
    df[columns].to_csv(CHAPTER_ROOT / "data" / "processed" / "sgvp_2023_chapter2_health_donor_analytical.csv", index=False)


def write_docs(df: pd.DataFrame):
    health = df[df["is_health_donor"]]
    nonhealth = df[df["is_charitable_donor"] & ~df["is_health_donor"]]
    non_donors = df[df["FG1FGIV"].eq(2)]
    hospital = df[df["is_hospital_donor"]]
    broader = df[df["is_broader_health_related_donor"]]
    total_health_dollars = float((health["health_donation_amount"] * health["WGHT_PER"]).sum())
    total_hospital_dollars = float((hospital["hospital_donation_amount"] * hospital["WGHT_PER"]).sum())
    total_charity_dollars_by_health_donors = float((health["total_donation_amount"] * health["WGHT_PER"]).sum())
    docs = CHAPTER_ROOT / "docs"
    outputs = CHAPTER_ROOT / "outputs"

    (docs / "health_donor_definition.md").write_text(
        f"""# Health Donor Definition

Primary Chapter 2 definition:

`Health donor = charitable donor (FG1FGIV = 1) with a positive valid value in either GS1DAX05 or GS1DNX05.`

This definition is traceable to the official SGVP 2023 English codebook:

- `GS1DAX05`: Amount of donations (15) - Health; universe `FG1FGIV = 1`.
- `GS1DNX05`: Number of donations (15) - Health; universe `FG1FGIV = 1`.
- `GS1DAX05 = 000000000.00` means None.
- `GS1DNX05 = 00` means No donations.
- `999999999.96` and `96` are Valid skip for non-givers.

Hospitals are not combined into the primary Health donor definition because the codebook documents them as separate ICNPO categories:

- `GS1DAX06`: Amount of donations (15) - Hospitals.
- `GS1DNX06`: Number of donations (15) - Hospitals.

A secondary derived metric, `broader_health_related_donor`, is included only for context and equals Health donor OR Hospital donor. It should be labelled clearly if used.

Validated Health donor sample count: {len(health):,}.
Validated weighted Health donor population estimate: {wsum(health):,.0f}.
""",
        encoding="utf-8",
    )

    (docs / "cleaning_and_derivation_rules.md").write_text(
        """# Cleaning And Derivation Rules

Raw data source: `../GVP_DBP_2023.zip`.

The Chapter 2 workflow reads the fixed-width PUMF text file directly from the root ZIP. It does not duplicate or overwrite the raw ZIP and does not modify Chapter 1.

## Rules

- Use `WGHT_PER` for all population-level estimates.
- Use `FG1FGIV = 1` as the charitable donor universe for donation amount/count variables.
- Preserve `GS1DAX05 = 000000000.00` and `GS1DNX05 = 00` as legitimate zero/no Health donation values among charitable donors.
- Convert Health donation amount/count to analytical null only for valid skips or other documented special codes.
- Keep Health and Hospitals separate because they are separate ICNPO 15-category activity groups.
- Create `is_health_donor` from positive valid Health amount or count.
- Create `is_hospital_donor` separately from positive valid Hospital amount or count.
- Create `is_broader_health_related_donor` only as a secondary derived metric: Health OR Hospitals.
- Use median, distribution, and concentration metrics alongside means because donation amounts are right-skewed.
- Health donor concentration uses an exact weighted top-share method: respondents are sorted by Health donation amount and the boundary respondent's survey weight is fractionally allocated where needed to hit the requested weighted population share.
- Treat province comparisons as descriptive unless bootstrap confidence intervals are added.
""",
        encoding="utf-8",
    )

    (outputs / "chapter2_data_quality_assessment.md").write_text(
        f"""# Chapter 2 Data Quality Assessment

Source of truth: official Statistics Canada SGVP 2023 English data dictionary/codebook and English layout files.

## Key Data Quality Findings

- Raw row count: {len(df):,}.
- Weighted represented population: {wsum(df):,.0f}.
- Charitable donor sample count: {int(df['is_charitable_donor'].sum()):,}.
- Health donor sample count: {len(health):,}.
- `GS1DAX05 = 999999999.96` and `GS1DNX05 = 96` occur for all non-givers and are documented Valid skip values.
- `GS1DAX05 = 000000000.00` and `GS1DNX05 = 00` are legitimate no-Health-donation values among charitable donors.
- Health amount and count are internally consistent in this PUMF: every positive Health amount has a positive Health count, and every positive Health count has a positive Health amount.
- Health donation amounts among Health donors range from ${health['health_donation_amount'].min():,.2f} to ${health['health_donation_amount'].max():,.2f}; the codebook documents amount responses for `GS1DAX05` from `000000000.50` to `000112500.00`.
- Hospital donation variables are valid and analytically useful, but kept separate from Health for the primary definition.
- Volunteer hours (`VD1DHRS`) apply to `FV1FVOL = 1`; valid skips are expected for non-volunteers.

No generic missing-value rule is used. Each special-code rule is variable-specific and traceable to the codebook.
""",
        encoding="utf-8",
    )

    findings = f"""# Chapter 2 Findings - The Health Donor

## Segment Size

- Weighted Canadian Health donor rate: {pct(wsum(df, df['is_health_donor']), wsum(df)):.1f}%.
- Weighted Health donor rate among charitable donors: {pct(wsum(df, df['is_health_donor']), wsum(df, df['is_charitable_donor'])):.1f}%.
- Estimated weighted Health donor population: {wsum(health):,.0f}.
- Sample Health donors: {len(health):,}.

## Financial Importance

- Weighted Health donation dollars: ${total_health_dollars:,.0f}.
- Weighted median Health donation among Health donors: ${weighted_median(health, 'health_donation_amount'):,.2f}.
- Weighted mean Health donation among Health donors: ${weighted_mean(health, 'health_donation_amount'):,.2f}.
- Weighted median total charitable giving among Health donors: ${weighted_median(health, 'total_donation_amount'):,.2f}.
- Weighted median total charitable giving among non-Health donors: ${weighted_median(nonhealth, 'total_donation_amount'):,.2f}.
- Median Health share of total giving among Health donors: {weighted_median(health, 'health_share_of_total_giving_pct'):.1f}%.

## Health Versus Hospitals

- Hospital donor weighted population estimate: {wsum(hospital):,.0f}.
- Weighted Hospital donation dollars: ${total_hospital_dollars:,.0f}.
- Broader Health-or-Hospital donor weighted population estimate: {wsum(broader):,.0f}.
- Health and Hospitals are separate ICNPO categories and should not be merged unless the dashboard explicitly labels the derived broader measure.

## What Differentiates Health Donors

- Health donors are a large subset of charitable donors, but not all donors give to Health.
- Health donors have much higher overall charitable giving than non-Health donors by both mean and median.
- Older age groups, higher personal income, and higher education levels tend to show higher Health donor rates.
- Health donors show stronger volunteering engagement than non-Health donors and non-donors across formal volunteering, fundraising volunteering, and health care/support volunteering.
- Province-level differences are descriptive only; sample counts should remain visible in Power BI.
- The Health donor concentration table uses exact weighted top-share calculations, including fractional allocation at the cutoff boundary.

## Do Not Overinterpret

- These are descriptive survey associations, not causal effects.
- Large donation values are valid documented responses, not automatically outliers.
- Province comparisons should not become strong strategic recommendations without design-based uncertainty estimates.
- Weighted concentration results describe the distribution of weighted Health donation dollars by reported Health donation amount; they are not a donor-level predictive model.

## Questions For Chapter 3

- Do Health donors use different fundraising channels than other donors?
- Are Health donors more likely to respond to events, online requests, or personal networks?
- Do volunteering-engaged Health donors give through different channels than Health donors who do not volunteer?
- Are high-value Health donors concentrated in particular channels or giving behaviours?
"""
    (outputs / "chapter2_findings.md").write_text(findings, encoding="utf-8")


def write_readme():
    (CHAPTER_ROOT / "README.md").write_text(
        """# Chapter 2 - The Health Donor

This chapter answers: What makes Health donors different?

It builds on the Chapter 1 Canadian donor baseline and focuses on donors who financially support the ICNPO Health category in the Statistics Canada 2023 Survey on Giving, Volunteering and Participating PUMF.

## Reproduce

Use Python 3.10 or newer. From the project root, create a local virtual environment for Chapter 2 and install dependencies:

```powershell
py -3 -m venv "Chapter 2\\.venv"
& "Chapter 2\\.venv\\Scripts\\python.exe" -m pip install --upgrade pip
& "Chapter 2\\.venv\\Scripts\\python.exe" -m pip install -r "Chapter 2\\requirements.txt"
```

Then run the workflow from the project root:

```powershell
& "Chapter 2\\.venv\\Scripts\\python.exe" "Chapter 2\\scripts\\chapter2_health_donor_analysis.py"
```

For this local working copy only, the script also supports the existing `Chapter 2\\.python_packages` folder if present. A fresh GitHub portfolio clone should use the virtual environment workflow above.

## Folder Structure

- `data/processed/`: analytical respondent-level Chapter 2 dataset.
- `data/powerbi/`: clean Power BI-ready tables.
- `docs/`: variable dictionary, Health donor definition, derivation rules.
- `outputs/`: DQA, validation, analytical tables, findings.
- `scripts/`: Python/pandas workflow.
- `sql/`: SQL transformation and aggregation layer.

## Method Notes

- Raw data is read directly from `..\\GVP_DBP_2023.zip`.
- Chapter 1 is read only for baseline context.
- Health and Hospitals are separate ICNPO categories. Health donor is based on Health only; a broader Health-or-Hospital metric is secondary and explicitly derived.
- Weighted estimates use `WGHT_PER`.
- Donation means are reported, but medians and distributions are emphasized because donation amounts are right-skewed.
- Health donor concentration uses an exact weighted top-share method with fractional boundary-weight allocation.
- Province-level tables include sample counts and a reliability note. They are descriptive because Chapter 2 does not implement bootstrap confidence intervals.

## SQL Layer

The SQL file is written for SQLite 3 and documents the exact import schema for `data/processed/sgvp_2023_chapter2_health_donor_analytical.csv`. It recreates the main flags, overview metrics, segment aggregations, and volunteering rates with the same valid yes/no denominators used by Python. Weighted medians remain in Python because generic SQL median support is inconsistent across engines.

## Output Copies

`outputs/` stores analysis/audit artifacts for review. `data/powerbi/` stores dashboard-ready copies of selected tables with presentation-oriented filenames. The duplicated CSV content is intentional: Power BI should connect to `data/powerbi/`, while `outputs/` remains the analytical audit trail.
""",
        encoding="utf-8",
    )


def main():
    df, raw_hash = read_raw_dataframe()
    df = add_derivations(df)

    write_variable_dictionary()
    data_quality_profile(df)
    write_analytical_dataset(df)
    make_overview(df)
    make_comparison_and_segments(df)
    make_distribution(df)
    make_volunteering(df)
    validation(df, raw_hash)
    write_docs(df)
    write_readme()

    summary = {
        "rows": len(df),
        "weighted_population": wsum(df),
        "charitable_donors_sample": int(df["is_charitable_donor"].sum()),
        "health_donors_sample": int(df["is_health_donor"].sum()),
        "health_donors_weighted": wsum(df, df["is_health_donor"]),
        "health_donor_rate_population_weighted_pct": pct(wsum(df, df["is_health_donor"]), wsum(df)),
        "health_donor_rate_among_donors_weighted_pct": pct(wsum(df, df["is_health_donor"]), wsum(df, df["is_charitable_donor"])),
        "outputs": [
            "docs/chapter2_variable_dictionary.csv",
            "docs/health_donor_definition.md",
            "docs/cleaning_and_derivation_rules.md",
            "outputs/chapter2_data_quality_assessment.md",
            "outputs/chapter2_data_quality_profile.csv",
            "outputs/chapter2_validation_results.csv",
            "outputs/chapter2_findings.md",
            "data/processed/sgvp_2023_chapter2_health_donor_analytical.csv",
            "data/powerbi/*.csv",
        ],
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
