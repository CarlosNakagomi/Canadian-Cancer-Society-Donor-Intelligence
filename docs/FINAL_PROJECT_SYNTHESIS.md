# Health Charity Donor Intelligence & Fundraising Strategy - Canada

## Executive Summary

This portfolio project analyzes the Statistics Canada 2023 Survey on Giving, Volunteering and Participating Public Use Microdata File to understand Canadian charitable giving, Health donors, donor behaviours, motivations, barriers, and fundraising opportunities.

The analysis is descriptive, weighted with `WGHT_PER` for Canadian population estimates, and designed for Power BI and executive reporting. It does not make causal claims.

Key synthesis:

- Health donors are a large subset of Canadian charitable donors: about 6.8 million weighted Canadians, or 20.6% of the represented population.
- Among charitable donors, 38.3% give to Health organizations.
- Health giving is highly concentrated: the exact weighted top 1% of Health donors account for about 46.8% of weighted Health donation dollars, and the top 10% account for about 71.3%.
- Health donors are more likely than non-Health donors to show personal connection, social prompting, and volunteering engagement.
- Core fundraising opportunities are retention, tribute/peer giving, high-value stewardship, trust-building, and careful channel-specific testing.

## The Canadian Donor

Chapter 1 established the Canadian donor baseline: who donates, how much they give, and how donor participation varies by demographic and socioeconomic characteristics.

Chapter 1 was previously audited and validated. Its donor/non-donor logic, survey weighting, and special-code handling are treated as the baseline for later chapters.

## The Health Donor

Chapter 2 defined a Health donor as:

`FG1FGIV = 1` and a positive valid value in either `GS1DAX05` or `GS1DNX05`.

Health and Hospitals are separate ICNPO categories. Hospitals are analyzed separately or as part of an explicitly labelled broader Health-or-Hospital metric, but not merged into the primary Health donor definition.

Validated Chapter 2 metrics:

- Sample Health donors: 6,399
- Weighted Health donors: 6,797,272
- Weighted Health donor rate among Canadian population: 20.6%
- Weighted Health donor rate among charitable donors: 38.3%
- Weighted Health donation dollars: $1.79 billion
- Weighted median Health donation: $60
- Weighted mean Health donation: $263.80
- Median total charitable giving among Health donors: $230
- Median total charitable giving among non-Health donors: $110

## How They Give

Chapter 3 analyzed documented giving channels and behaviours.

Most common channels among Health donors:

- Shopping centre: 44.5%
- In memory of someone: 42.1%
- Sponsoring someone: 35.4%
- Mail: 32.5%
- On own initiative: 32.0%
- Online: 29.1%

Channels more common among Health donors than non-Health donors:

- In memory of someone: +30.8 percentage points
- Sponsoring someone: +25.2 percentage points
- Mail: +19.2 percentage points
- Shopping centre: +11.7 percentage points
- Online: +11.3 percentage points

Important limitation: channel amount variables describe total charitable giving by channel among Health donors. They do not identify which channel was used specifically for the Health-category gift.

## Why They Give

Chapter 4 analyzed documented reasons for charitable giving.

Most common Health donor motivations:

- Belief in the cause: 86.5%
- Compassion: 85.7%
- Personally affected: 79.5%
- Community contribution: 74.6%
- Asked by someone you know: 51.5%

Motivations more common among Health donors than non-Health donors:

- Personally affected: +26.9 percentage points
- Asked by someone you know: +17.0 percentage points
- Tax credit: +7.4 percentage points
- Belief in the cause: +7.1 percentage points
- Compassion: +3.1 percentage points

These results support message themes for testing, not causal claims about what will increase giving.

## Why They Don't Give More

Chapter 5 analyzed documented barriers to giving more.

Most common core barriers among Health donors:

- Charity fraud: 75.0%
- Already gave enough: 74.9%
- Could not afford a larger donation: 65.9%
- So many organizations: 60.1%
- Gave directly to people: 36.7%
- No one asked: 24.7%

Barriers more common among Health donors than non-Health donors:

- Already gave enough: +9.4 percentage points
- Tax credit not enough incentive: +4.3 percentage points
- Did not like way requests were made: +3.8 percentage points
- Gave directly to people: +2.7 percentage points
- Money would not be used efficiently: +2.0 percentage points

Financial barriers should be separated from trust, engagement, information, and solicitation barriers. Conditional follow-up barriers are kept separate because their denominators are narrower.

## The Opportunity

Chapter 6 synthesizes Chapters 1-5 into priority audiences and evidence-linked fundraising implications.

Priority audiences:

1. Established older Health donors: high participation / retention
2. Higher-income Health donors: high value / upgrade potential
3. Volunteer-engaged Health donors: engagement / relationship depth
4. Tribute and socially prompted Health donors: channel/message fit
5. Trust-sensitive donors: retention / barrier reduction

Fundraising implications:

- Prioritize retention and stewardship because many Health donors already give and report satisfaction or financial constraints.
- Treat tribute, sponsorship, mail, own-initiative, and online channels as distinct donor journeys.
- Use personal connection, cause, compassion, and community contribution as message territories for testing.
- Address trust with transparent impact, credibility cues, simple choices, and respectful solicitation controls.
- Do not infer individual capacity or campaign lift from descriptive associations alone.

## Bonus: Health Donor Propensity

The Bonus analysis is a small interpretable modeling extension.

Target:

`is_health_donor`, using the validated Chapter 2 Health donor definition.

Predictors:

Demographics and volunteering indicators only. Direct Health donation variables, Health flags, total donation amount/count, channel variables, motivations, and barriers were excluded to reduce target leakage.

Model:

Weighted logistic regression implemented with numpy.

Held-out test metrics:

- ROC-AUC: 0.720
- Precision: 0.368
- Recall: 0.696
- F1: 0.481
- Test sample size: 8,004

Top positive associations included older age groups, Woman+, married status, fundraising volunteering, and formal volunteering. These are associations, not causal effects.

## Key Fundraising Implications

- Health donors are numerous enough to support both broad participation strategies and focused high-value stewardship.
- Health giving appears strongly connected to personal relevance and social prompts, especially in-memory and sponsorship giving.
- Digital giving is important, but traditional and situational channels remain material.
- Trust and solicitation concerns should be treated as donor experience issues, not only acquisition obstacles.
- High-value donor work should be transparent and careful because donation dollars are concentrated but barriers around trust and satisfaction are prominent.

## Limitations

- The PUMF supports descriptive associations, not causal inference.
- No bootstrap confidence intervals were implemented, so province and smaller segment comparisons are descriptive.
- Channel variables do not identify the channel used for Health-category gifts specifically.
- Some barriers are conditional follow-ups and should not be compared with core barriers using the same denominator.
- The Bonus model is interpretive and secondary; it is not a production fundraising model.

## Methodology

Each chapter followed a reproducible workflow:

1. Inspect official SGVP English documentation and SAS layout files.
2. Verify variables, labels, values, special codes, and applicability.
3. Parse raw fixed-width data from `GVP_DBP_2023.zip`.
4. Apply variable-specific special-code rules.
5. Use `WGHT_PER` for population estimates.
6. Produce analytical outputs, Power BI-ready tables, SQL views, documentation, findings, and validation files.
7. Audit SQL/Python consistency and selected raw-data calculations.

## Data Source

Statistics Canada 2023 Survey on Giving, Volunteering and Participating Public Use Microdata File.

Raw source:

`GVP_DBP_2023.zip`

Official documentation used:

- SGVP 2023 English codebook/PUMF documentation
- English SAS layout files: labels, positions, formats, and format values

## Survey Weighting

Population-level estimates use `WGHT_PER`. Sample counts are reported separately from weighted Canadian estimates. Raw sample percentages are not presented as Canadian population percentages.
