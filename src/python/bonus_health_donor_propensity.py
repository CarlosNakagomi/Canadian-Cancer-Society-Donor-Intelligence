from __future__ import annotations

import csv
import json
import sqlite3
import sys
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parents[2] / "Chapter 2" / ".python_packages"
if PACKAGE_DIR.exists():
    sys.path.insert(0, str(PACKAGE_DIR))

import numpy as np
import pandas as pd


BONUS_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BONUS_ROOT.parent
CH2_ANALYTICAL = PROJECT_ROOT / "Chapter 2" / "data" / "processed" / "sgvp_2023_chapter2_health_donor_analytical.csv"

for folder in ["data/processed", "data/powerbi", "docs", "outputs", "sql"]:
    (BONUS_ROOT / folder).mkdir(parents=True, exist_ok=True)

TARGET = "is_health_donor"
PREDICTORS = [
    "AGEGR10_label", "GENDER2_label", "PRV_label", "INCG2_label", "FAMINCG2_label",
    "ED4CAT_label", "MARSTAT_label", "HSDSIZEC_label", "DLFS_label",
    "FV1FVOL_label", "FV_030_label", "FV_100_label",
]
LEAKAGE_BLOCKLIST = [
    "health_donation_amount", "health_donation_count", "is_health_donor", "is_hospital_donor",
    "is_broader_health_related_donor", "hospital_donation_amount", "hospital_donation_count",
    "health_share_of_total_giving_pct", "total_donation_amount", "total_donation_count",
    "donor_group", "analysis_group",
]


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -35, 35)))


def train_test_split_stratified(y, test_size=0.30, seed=42):
    rng = np.random.default_rng(seed)
    train_idx, test_idx = [], []
    for cls in [0, 1]:
        idx = np.where(y == cls)[0]
        rng.shuffle(idx)
        n_test = int(round(len(idx) * test_size))
        test_idx.extend(idx[:n_test])
        train_idx.extend(idx[n_test:])
    return np.array(train_idx), np.array(test_idx)


def standardize(train, test):
    mean = train.mean(axis=0)
    std = train.std(axis=0)
    std[std == 0] = 1
    return (train - mean) / std, (test - mean) / std, mean, std


def fit_logistic(X, y, weights=None, lr=0.08, epochs=2500, l2=0.05):
    weights = np.ones(len(y)) if weights is None else weights / np.mean(weights)
    beta = np.zeros(X.shape[1])
    for _ in range(epochs):
        p = sigmoid(X @ beta)
        grad = (X.T @ ((p - y) * weights)) / len(y)
        grad[1:] += l2 * beta[1:] / len(y)
        beta -= lr * grad
    return beta


def roc_auc(y, scores):
    order = np.argsort(scores)
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(scores) + 1)
    pos = y == 1
    n_pos = pos.sum()
    n_neg = len(y) - n_pos
    return float((ranks[pos].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def metrics(y, scores, threshold=0.5):
    pred = (scores >= threshold).astype(int)
    tp = int(((pred == 1) & (y == 1)).sum())
    fp = int(((pred == 1) & (y == 0)).sum())
    tn = int(((pred == 0) & (y == 0)).sum())
    fn = int(((pred == 0) & (y == 1)).sum())
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    return {
        "threshold": threshold,
        "roc_auc": roc_auc(y, scores),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_positive": tp,
        "false_positive": fp,
        "true_negative": tn,
        "false_negative": fn,
    }


def prepare_data():
    df = pd.read_csv(CH2_ANALYTICAL)
    df[TARGET] = df[TARGET].astype(str).str.lower().eq("true").astype(int)
    for col in PREDICTORS:
        df[col] = df[col].fillna("Missing/not stated").astype(str)
    Xdf = pd.get_dummies(df[PREDICTORS], prefix=PREDICTORS, drop_first=True, dtype=float)
    X = np.column_stack([np.ones(len(Xdf)), Xdf.to_numpy()])
    names = ["Intercept"] + Xdf.columns.tolist()
    return df, X, df[TARGET].to_numpy(), df["WGHT_PER"].to_numpy(), names


def write_dictionary():
    rows = []
    for col in [TARGET] + PREDICTORS:
        rows.append({
            "variable_name": col,
            "role": "Target" if col == TARGET else "Predictor",
            "definition_source": "Chapter 2 validated analytical dataset and official SGVP 2023 English codebook references.",
            "leakage_assessment": "Target derived from Health donation amount/count." if col == TARGET else "Allowed predictor; does not directly reveal Health donation amount, count, or Health category status.",
        })
    pd.DataFrame(rows).to_csv(BONUS_ROOT / "docs" / "bonus_variable_dictionary.csv", index=False)


def write_sql():
    sql = """-- Bonus SQL layer: Health donor propensity analytical base.
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
"""
    (BONUS_ROOT / "sql" / "bonus_propensity_views.sql").write_text(sql, encoding="utf-8")


def audit_sql():
    sql = (BONUS_ROOT / "sql" / "bonus_propensity_views.sql").read_text(encoding="utf-8")
    create = sql.split("DROP VIEW IF EXISTS vw_bonus_score_summary;")[0]
    views = "DROP VIEW IF EXISTS vw_bonus_score_summary;" + sql.split("DROP VIEW IF EXISTS vw_bonus_score_summary;")[1]
    con = sqlite3.connect(":memory:")
    con.executescript(create)
    with open(BONUS_ROOT / "data" / "processed" / "bonus_health_donor_propensity_scored.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        con.executemany(f"INSERT INTO bonus_propensity_scored VALUES ({','.join(['?'] * len(header))})", reader)
    con.executescript(views)
    n = len(pd.read_sql_query("SELECT * FROM vw_bonus_score_summary", con))
    pd.DataFrame([{"check": "sql_score_summary_executes", "result": n, "status": "pass" if n == 2 else "fail"}]).to_csv(BONUS_ROOT / "outputs" / "bonus_sql_audit.csv", index=False)


def main():
    df, X, y, weights, names = prepare_data()
    leakage_hits = [p for p in PREDICTORS if p in LEAKAGE_BLOCKLIST or "health_donation" in p.lower()]
    train_idx, test_idx = train_test_split_stratified(y)
    X_train_raw, X_test_raw = X[train_idx, 1:], X[test_idx, 1:]
    X_train_s, X_test_s, _, _ = standardize(X_train_raw, X_test_raw)
    X_train = np.column_stack([np.ones(len(X_train_s)), X_train_s])
    X_test = np.column_stack([np.ones(len(X_test_s)), X_test_s])
    beta = fit_logistic(X_train, y[train_idx], weights=weights[train_idx])
    scores = sigmoid(X_test @ beta)
    threshold = y[train_idx].mean()
    result = metrics(y[test_idx], scores, threshold=threshold)
    train_scores = sigmoid(X_train @ beta)

    scored = df[["PUMFID", "WGHT_PER", TARGET]].copy()
    scored["split"] = "unused"
    scored.loc[train_idx, "split"] = "train"
    scored.loc[test_idx, "split"] = "test"
    scored["predicted_probability"] = np.nan
    scored.loc[train_idx, "predicted_probability"] = train_scores
    scored.loc[test_idx, "predicted_probability"] = scores
    scored["predicted_class"] = (scored["predicted_probability"] >= threshold).astype(int)
    scored.to_csv(BONUS_ROOT / "data" / "processed" / "bonus_health_donor_propensity_scored.csv", index=False)
    scored.to_csv(BONUS_ROOT / "data" / "powerbi" / "bonus_health_donor_propensity_scored.csv", index=False)

    coef = pd.DataFrame({"feature": names, "coefficient": beta})
    coef = coef[coef["feature"].ne("Intercept")].copy()
    coef["odds_ratio_per_standardized_unit"] = np.exp(coef["coefficient"])
    coef["direction"] = np.where(coef["coefficient"] > 0, "Higher predicted Health donor likelihood", "Lower predicted Health donor likelihood")
    coef.reindex(coef["coefficient"].abs().sort_values(ascending=False).index).head(30).to_csv(BONUS_ROOT / "outputs" / "bonus_top_model_coefficients.csv", index=False)
    coef.reindex(coef["coefficient"].abs().sort_values(ascending=False).index).head(30).to_csv(BONUS_ROOT / "data" / "powerbi" / "bonus_top_model_coefficients.csv", index=False)

    metrics_df = pd.DataFrame([{**result, "test_sample_n": len(test_idx), "train_sample_n": len(train_idx), "test_health_donor_rate": y[test_idx].mean(), "train_health_donor_rate": y[train_idx].mean(), "model": "Weighted logistic regression with demographic and volunteering predictors"}])
    metrics_df.to_csv(BONUS_ROOT / "outputs" / "bonus_model_metrics.csv", index=False)
    metrics_df.to_csv(BONUS_ROOT / "data" / "powerbi" / "bonus_model_metrics.csv", index=False)

    checks = [
        ("row_count", len(df), "pass" if len(df) == 26678 else "fail"),
        ("target_positive_sample_n", int(y.sum()), "pass" if int(y.sum()) == 6399 else "fail"),
        ("leakage_predictor_hits", ",".join(leakage_hits), "pass" if not leakage_hits else "fail"),
        ("test_has_both_classes", sorted(np.unique(y[test_idx]).tolist()), "pass" if len(np.unique(y[test_idx])) == 2 else "fail"),
        ("roc_auc_above_random", round(result["roc_auc"], 4), "pass" if result["roc_auc"] > 0.5 else "review"),
    ]
    pd.DataFrame(checks, columns=["check", "result", "status"]).to_csv(BONUS_ROOT / "outputs" / "bonus_validation_results.csv", index=False)

    write_dictionary()
    write_sql()
    audit_sql()
    top = pd.read_csv(BONUS_ROOT / "outputs" / "bonus_top_model_coefficients.csv").head(10)
    (BONUS_ROOT / "outputs" / "bonus_findings.md").write_text(
        "# Bonus Findings - Health Donor Propensity\n\n"
        f"Target: Health donor, using the validated Chapter 2 definition. Positive class sample count: {int(y.sum()):,} of {len(y):,} respondents.\n\n"
        f"Model: weighted logistic regression using demographic and volunteering predictors only. Test ROC-AUC: {result['roc_auc']:.3f}; precision: {result['precision']:.3f}; recall: {result['recall']:.3f}; F1: {result['f1']:.3f} at a prevalence-based threshold.\n\n"
        "Direct Health donation variables, total donation amount/count, channel variables, motivations, and barriers were excluded to reduce target leakage.\n\n"
        "Top associated features are exported in `bonus_top_model_coefficients.csv`. Coefficients are associations, not causal effects, and should not replace the descriptive Chapter 6 opportunity framework.\n",
        encoding="utf-8",
    )
    (BONUS_ROOT / "docs" / "bonus_methodology.md").write_text(
        "# Bonus Methodology\n\n"
        "This small extension tests whether interpretable respondent characteristics help distinguish Health donors from other respondents. "
        "The target is `is_health_donor`. Predictors are demographics and volunteering indicators from the validated Chapter 2 analytical dataset. "
        "The model uses deterministic stratified train/test splitting and a weighted logistic regression implemented with numpy. Survey weights are used in the fitting loss; metrics are reported on the held-out sample without claiming production readiness.\n",
        encoding="utf-8",
    )
    (BONUS_ROOT / "README.md").write_text(
        "# Bonus - Health Donor Propensity\n\n"
        "Small interpretable modeling extension. Run from the project root:\n\n"
        "```powershell\n& \"Chapter 2\\.venv\\Scripts\\python.exe\" \"Bonus - Health Donor Propensity\\scripts\\bonus_health_donor_propensity.py\"\n```\n\n"
        "The model is secondary to the descriptive analysis and should not be used alone for fundraising recommendations.\n",
        encoding="utf-8",
    )
    print(json.dumps({"bonus": "Health Donor Propensity", "roc_auc": result["roc_auc"], "test_sample_n": len(test_idx)}, indent=2))


if __name__ == "__main__":
    main()
