# Chapter 2 - The Health Donor

This chapter answers: What makes Health donors different?

It builds on the Chapter 1 Canadian donor baseline and focuses on donors who financially support the ICNPO Health category in the Statistics Canada 2023 Survey on Giving, Volunteering and Participating PUMF.

## Reproduce

Use Python 3.10 or newer. In this publication repository, install the shared dependencies from the repository root:

```powershell
py -3 -m venv .venv
& ".venv\Scripts\python.exe" -m pip install --upgrade pip
& ".venv\Scripts\python.exe" -m pip install -r requirements.txt
```

The archived source file is available at `src/python/chapter2_health_donor_analysis.py`. It preserves the original chapter-folder output assumptions used during analysis, so full upstream regeneration requires the SGVP archive plus either the original chapter layout or path adaptation before execution.

The final dashboard does not require rerunning this script; it refreshes from `powerbi/data/PowerBI_Data.xlsx` after setting the `PowerBIWorkbookPath` parameter.
## Folder Structure

- `data/processed/`: analytical respondent-level Chapter 2 dataset.
- `data/powerbi/`: clean Power BI-ready tables.
- `docs/`: variable dictionary, Health donor definition, derivation rules.
- `outputs/`: DQA, validation, analytical tables, findings.
- `scripts/`: Python/pandas workflow.
- `sql/`: SQL transformation and aggregation layer.

## Method Notes

- Raw data is read directly from `..\GVP_DBP_2023.zip`.
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
