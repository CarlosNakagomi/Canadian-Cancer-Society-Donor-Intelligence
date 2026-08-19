# Data Notes

## Source

This project uses the **Statistics Canada 2023 Survey on Giving, Volunteering and Participating (SGVP) Public Use Microdata File**.

Verified source archive name in the working project:

```text
GVP_DBP_2023.zip
```

Verified official documentation in the working project included:

- SGVP 2023 English PUMF codebook
- SGVP 2023 English user guide
- SGVP 2023 English questionnaire
- English SAS layout files for labels, positions, formats, and format values

## Why Raw Data Is Not Included

The raw Statistics Canada archive and extracted respondent-level data are not included in this repository because redistribution rights were not established during publication preparation.

To reproduce the full analysis, obtain the SGVP 2023 PUMF directly from Statistics Canada and place the archive at the project root as:

```text
GVP_DBP_2023.zip
```

Do not commit the raw archive or extracted raw files unless redistribution permission has been explicitly confirmed.

## Included Derived Outputs

This repository includes small aggregated Power BI-ready output tables under:

```text
outputs/powerbi/
```

These are derived analytical summary tables used by the dashboard. They are included for portfolio review and Power BI transparency, not as a substitute for the official source microdata.

The repository also includes the dashboard staging workbook:

```text
powerbi/data/PowerBI_Data.xlsx
```

This workbook contains the aggregated Power BI tables used by the PBIP semantic model.
