# Health Charity Donor Intelligence & Fundraising Strategy - Canada

This portfolio project uses the Statistics Canada 2023 Survey on Giving, Volunteering and Participating (SGVP) Public Use Microdata File to develop donor intelligence for a hypothetical Canadian health charity.

## Current Scope

Completed through Chapter 1 only: The Canadian Donor - who gives and how much.

The health-donor chapter, channels, motivations, barriers, recommendations, dashboard, and optional ML extension are intentionally not started yet.

## Sources

- Raw archive: `GVP_DBP_2023.zip`
- Official English codebook: `data/raw/GVP_DBP_2023/Codebook_Dictionaire de données/GVP_2023_PUMF_EN.pdf`
- Official English user guide: `data/raw/GVP_DBP_2023/Guide/2023_GVP_PUMF_User_Guide.pdf`
- Official English questionnaire: `data/raw/GVP_DBP_2023/Questionnaire/GVP_2023_Questionnaire_EN.pdf`
- Official layout files: `data/raw/GVP_DBP_2023/Layout_MisEnPages/`
- Project brief: `Health_Charity_Donor_Intelligence_Project_Brief.pdf`

## Folder Structure

- `data/raw/`: extracted official raw files; do not edit.
- `data/processed/`: analytical datasets derived from raw data.
- `docs/official/`: space for source notes from official documentation.
- `outputs/data_understanding/`: variable dictionary, DQA, validation.
- `outputs/chapter1/`: Chapter 1 analytical tables for Power BI.
- `scripts/`: reproducible analysis scripts.
- `sql/`: SQL views and aggregation scripts.

## Methodology

The workflow is raw data, data understanding, data quality assessment, cleaning rules, analytical dataset, analysis. Cleaning rules are traceable to the official codebook and layout files. Survey weights are used for population-level estimates; sample counts and weighted Canadian estimates are reported separately.

## Reproduce

Run:

```powershell
node scripts/chapter1_data_understanding_analysis.js
```

Python/pandas is the intended portfolio stack. A pandas version of the workflow can mirror the fixed-width positions and cleaning rules documented here; local execution used Node because Python is not available on this machine's PATH.
