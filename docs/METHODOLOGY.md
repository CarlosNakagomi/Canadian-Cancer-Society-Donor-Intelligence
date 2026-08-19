# Methodology

## Source And Scope

The project analyzes the Statistics Canada 2023 Survey on Giving, Volunteering and Participating Public Use Microdata File. The analysis focuses on Canadian charitable giving overall and Health-related donors specifically.

The project is descriptive. It is intended for portfolio demonstration and executive-style donor intelligence, not causal evaluation.

## Data Preparation

The working project parsed the raw SGVP fixed-width data from `GVP_DBP_2023.zip` using official SGVP documentation and layout files.

Preparation steps verified in the project:

1. Inspect official English codebook, questionnaire, user guide, and SAS layout files.
2. Verify variable positions, labels, valid values, special codes, and universes.
3. Parse raw fixed-width survey data.
4. Apply variable-specific special-code rules.
5. Create chapter-level analytical datasets.
6. Export Power BI-ready aggregated tables.

## Survey Weighting

Population-level estimates use the person weight `WGHT_PER`.

Sample counts and weighted estimates are kept separate. Raw sample percentages are not treated as Canadian population percentages.

## Health Donor Definition

The validated Health donor definition is based on charitable donors with positive valid giving to the Health ICNPO category.

The project treats Health and Hospitals as separate categories. Hospitals are analyzed separately or as part of explicitly labelled broader Health-or-Hospital metrics, not merged into the primary Health donor definition.

## Descriptive Analysis

The project is organized by analytical chapter:

- Chapter 1: Canadian donor baseline.
- Chapter 2: Health donor profile and comparison groups.
- Chapter 3: Giving channels and behaviour.
- Chapter 4: Motivations.
- Chapter 5: Barriers.
- Chapter 6: Priority audiences and fundraising opportunities.

Outputs include weighted summary tables, validation files, findings notes, and Power BI-ready CSVs.

## SQL Layer

SQL files document analytical table schemas and aggregation logic for each chapter. They are written in a SQLite-style format and support reproducibility/auditability of the Python outputs.

Weighted medians and some survey-specific calculations remain in Python where generic SQL support is limited.

## Power BI Modeling

The PBIP semantic model uses imported pre-aggregated analytical tables and a focused set of validated relationships through lookup dimensions such as age group, income band, province, and channel.

Most business metrics are pre-aggregated in Python and exposed through DAX measures for presentation. The model avoids misleading cross-filtering between unrelated pre-aggregated tables.

## Exploratory Predictive Modeling

The bonus analysis uses an interpretable weighted logistic regression to model Health donor propensity.

Predictors include demographics and volunteering indicators. Direct Health donation variables, Health flags, donation amount/count, channels, motivations, and barriers are excluded to reduce target leakage.

The model is evaluated on a held-out test sample and reported as exploratory predictive association only.

## Validation Approach

Validation artifacts in the working project include:

- data quality profiles
- validation result CSVs
- SQL audit outputs
- Power BI import maps
- Power BI handoff/self-review files
- semantic model QA and report visual QA

The final Power BI report was opened and visually reviewed in Power BI Desktop before this publication repository was prepared.
