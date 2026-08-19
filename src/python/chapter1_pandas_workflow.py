from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_TXT = ROOT / "data/raw/GVP_DBP_2023/Data_Donnees/GVP_DBP_2023_PUMF_FMGD.txt"
if not RAW_TXT.exists():
    RAW_TXT = ROOT / "data/raw/GVP_DBP_2023/Data_Données/GVP_DBP_2023_PUMF_FMGD.txt"

COLUMNS = [
    ("WGHT_PER", 5, 15),
    ("AGEGR10", 15, 17),
    ("GENDER2", 17, 18),
    ("PRV", 33, 35),
    ("FG1FGIV", 874, 875),
    ("GS1DNTOT", 1058, 1060),
    ("GS1DATOT", 1060, 1072),
    ("ED4CAT", 1527, 1528),
    ("INCG2", 1611, 1613),
    ("FAMINCG2", 1614, 1616),
]

LABELS = {
    "FG1FGIV": {1: "Giver", 2: "Non-giver"},
    "AGEGR10": {1: "15 to 24 years", 2: "25 to 34 years", 3: "35 to 44 years", 4: "45 to 54 years", 5: "55 to 64 years", 6: "65 to 74 years", 7: "75 years and over"},
    "GENDER2": {1: "Man+", 2: "Woman+"},
    "PRV": {10: "Newfoundland and Labrador", 11: "Prince Edward Island", 12: "Nova Scotia", 13: "New Brunswick", 24: "Quebec", 35: "Ontario", 46: "Manitoba", 47: "Saskatchewan", 48: "Alberta", 59: "British Columbia"},
    "INCG2": {1: "Less than $25,000", 2: "$25,000 to $49,999", 3: "$50,000 to $74,999", 4: "$75,000 to $99,999", 5: "$100,000 to $124,999", 6: "$125,000 and more"},
    "FAMINCG2": {1: "Less than $25,000", 2: "$25,000 to $49,999", 3: "$50,000 to $74,999", 4: "$75,000 to $99,999", 5: "$100,000 to $124,999", 6: "$125,000 and more"},
    "ED4CAT": {1: "Less than high school", 2: "Graduated from high school", 3: "Post-secondary diploma", 4: "University diploma"},
}


def weighted_mean(frame, value):
    valid = frame[[value, "WGHT_PER"]].dropna()
    return (valid[value] * valid["WGHT_PER"]).sum() / valid["WGHT_PER"].sum()


def weighted_median(frame, value):
    valid = frame[[value, "WGHT_PER"]].dropna().sort_values(value)
    cutoff = valid["WGHT_PER"].sum() / 2
    return valid.loc[valid["WGHT_PER"].cumsum() >= cutoff, value].iloc[0]


df = pd.read_fwf(
    RAW_TXT,
    colspecs=[(start, end) for _, start, end in COLUMNS],
    names=[name for name, _, _ in COLUMNS],
)

df["is_donor"] = df["FG1FGIV"].eq(1)
df["donation_amount"] = df["GS1DATOT"].where(df["is_donor"] & df["GS1DATOT"].lt(999999999))
df["donation_count"] = df["GS1DNTOT"].where(df["is_donor"] & df["GS1DNTOT"].lt(96))

for col, labels in LABELS.items():
    df[f"{col}_label"] = df[col].map(labels)

out = ROOT / "data/processed"
out.mkdir(parents=True, exist_ok=True)
df.to_csv(out / "sgvp_2023_chapter1_analytical_from_pandas.csv", index=False)

donors = df[df["is_donor"]]
summary = pd.DataFrame(
    [
        {"metric": "weighted_donor_rate_pct", "value": 100 * donors["WGHT_PER"].sum() / df["WGHT_PER"].sum()},
        {"metric": "weighted_mean_donation", "value": weighted_mean(donors, "donation_amount")},
        {"metric": "weighted_median_donation", "value": weighted_median(donors, "donation_amount")},
        {"metric": "weighted_mean_frequency", "value": weighted_mean(donors, "donation_count")},
        {"metric": "weighted_median_frequency", "value": weighted_median(donors, "donation_count")},
    ]
)
summary.to_csv(ROOT / "outputs/chapter1/chapter1_pandas_summary.csv", index=False)
