# Cleaning And Derivation Rules

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
