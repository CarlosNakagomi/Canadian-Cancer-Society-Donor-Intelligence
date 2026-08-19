# Canadian Cancer Society Donor Intelligence

**Independent portfolio analysis - not an official Canadian Cancer Society publication.**

This project is a Data Analyst / Business Intelligence portfolio case study using public Statistics Canada survey microdata to understand Canadian charitable giving, with a focus on Health-related donors and fundraising strategy.

The project combines Python, SQL, weighted survey analysis, Power BI semantic modeling, DAX measures, and an exploratory predictive model. It is not affiliated with, commissioned by, or endorsed by the Canadian Cancer Society or Statistics Canada.

## Project Overview

The business objective is to translate national charitable giving survey data into practical donor intelligence for a hypothetical Canadian health charity. The report is designed for executive review: it summarizes who Health donors are, how they give, what motivates them, what barriers they report, and where descriptive fundraising opportunities may exist.

## Business Questions

- Who gives to charities in Canada, and how much do they give?
- How do Health donors differ from other charitable donors?
- Which channels and giving behaviours are most relevant to Health donors?
- What motivations are most common among Health donors?
- What barriers prevent donors from giving more?
- Which priority audiences and stewardship opportunities are supported by the evidence?
- Which demographic and volunteering features are associated with Health donor propensity?

## Data Source

The analysis uses the **Statistics Canada 2023 Survey on Giving, Volunteering and Participating (SGVP) Public Use Microdata File**.

Raw source data is not included in this repository because redistribution rights were not established during project preparation. See [data/README.md](data/README.md) for source-data setup notes.

## Tools & Technologies

- Python
- pandas
- numpy
- SQL / SQLite-style analytical views
- Power BI
- Power Query
- DAX
- TMDL / PBIP
- Weighted survey analysis
- Exploratory weighted logistic regression

## Analytical Workflow

Verified project workflow:

1. Statistics Canada SGVP 2023 PUMF source archive and official documentation.
2. Python/JavaScript data understanding and parsing of fixed-width survey data.
3. Chapter-level weighted descriptive analysis.
4. SQL views for analytical validation and aggregation logic.
5. Power BI-ready aggregated CSV outputs.
6. Exploratory Health donor propensity model.
7. Consolidated Power BI staging workbook.
8. PBIP semantic model and 8-page Power BI report.

## Dashboard

The Power BI report contains 8 pages:

1. Executive Overview
2. Who Are Health Donors?
3. Giving Behaviour & Channels
4. Motivations
5. Barriers
6. Fundraising Opportunities
7. Exploratory Predictive Insights
8. Methodology / Data Notes

The PBIP project is in [powerbi/](powerbi/). The report has been visually reviewed in Power BI Desktop before publication preparation.

## Key Findings

From the validated project synthesis:

- Health donors represent about 6.8 million weighted Canadians, or 20.6% of the represented population.
- Among charitable donors, 38.3% give to Health organizations.
- Weighted Health donation dollars are about $1.79 billion.
- Health donors are more likely than non-Health donors to report personal connection, social prompting, and volunteering engagement.
- Health giving appears connected to personal relevance and social prompts, especially in-memory and sponsorship giving.
- Core descriptive opportunities include retention, stewardship, tribute/peer giving, high-value donor care, trust-building, and respectful solicitation.

These findings are descriptive and should not be interpreted as causal campaign effects.

## Exploratory Predictive Analysis

The bonus model is an interpretable weighted logistic regression predicting `is_health_donor` using demographics and volunteering indicators.

Validated held-out metrics:

- ROC AUC: 0.720
- Precision: 0.368
- Recall: 0.696
- F1: 0.481
- Test sample size: 8,004

Direct Health donation variables, Health flags, total giving amount/count, channels, motivations, and barriers were excluded to reduce target leakage. The model is exploratory and demonstrates predictive association only; it is not a production fundraising model and does not establish causality.

## Repository Structure

```text
docs/       Methodology, limitations, synthesis, chapter notes, and Power BI build docs
src/        Python, JavaScript, and SQL analytical source files
data/       Source-data acquisition and data policy notes
outputs/    Approved aggregated Power BI-ready outputs
powerbi/    Clean PBIP report and semantic model
images/     Placeholder for dashboard screenshots
```

## Reproducing The Analysis

The raw SGVP source archive is required to fully reproduce the chapter analyses. After obtaining the source data, place it at the project root as `GVP_DBP_2023.zip`.

Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

The copied source files are organized for publication. The original working project used chapter folders and project-root-relative paths, so reproducing the full workflow may require running scripts from a restored chapter-folder layout or adapting paths. The analytical logic is preserved in `src/`; raw data is intentionally excluded.

The Power BI report uses a copied aggregated staging workbook at:

```text
powerbi/data/PowerBI_Data.xlsx
```

Power BI Desktop requires `File.Contents` paths to be absolute at refresh time, so the PBIP uses a Power Query text parameter named `PowerBIWorkbookPath`.

After cloning or copying the repository:

1. Open `powerbi/Canadian_Cancer_Society_Donor_Intelligence.pbip` in Power BI Desktop.
2. Go to **Transform data** > **Edit parameters**.
3. Set `PowerBIWorkbookPath` to the absolute path of your local workbook, for example:

```text
C:\Your\Local\Path\Canadian-Cancer-Society-Donor-Intelligence\powerbi\data\PowerBI_Data.xlsx
```

4. Apply the parameter change.
5. Refresh the semantic model.

Do not commit a personal absolute path after changing the parameter locally.

## Limitations

- The analysis uses cross-sectional survey data.
- Weighted descriptive associations do not establish causality.
- No bootstrap confidence intervals are displayed in the report layer.
- Channel amount variables describe total charitable giving by channel among Health donors and may not identify the specific channel used for a Health-category gift.
- Some barrier variables use narrower conditional denominators.
- The predictive model is exploratory and not operationally validated.

## Disclaimer

This is an independent portfolio project. It is not affiliated with, endorsed by, or commissioned by the Canadian Cancer Society. Statistics Canada is the source of the underlying survey data. Analytical interpretations, dashboard design, and fundraising implications are the author's own.
