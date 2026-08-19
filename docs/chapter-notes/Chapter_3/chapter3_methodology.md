# Chapter 3 Methodology

Business question: Which giving channels and behaviours matter for Health donors?

Variables were selected from the official SGVP 2023 English codebook/SAS layout after verifying labels, positions, and formats. The chapter uses `WGHT_PER` for weighted Canadian estimates and distinguishes Health donors from non-Health charitable donors using the validated Chapter 2 definition.

Donation channel flags (`FG1A_*`) are analyzed with valid yes/no denominators. Matching channel count (`FG1DND*`) and amount (`FG1DAD*`) variables are used for frequency and channel-dollar summaries. Valid skips, don't know, refusals, and not stated responses are excluded from denominators; legitimate zero/none values are retained where documented.

Important limitation: SGVP channel amount variables describe total charitable giving by channel. They do not identify which channel was used specifically for Health-category donations.
