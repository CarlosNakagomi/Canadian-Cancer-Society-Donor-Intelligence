# Health Donor Definition

Primary Chapter 2 definition:

`Health donor = charitable donor (FG1FGIV = 1) with a positive valid value in either GS1DAX05 or GS1DNX05.`

This definition is traceable to the official SGVP 2023 English codebook:

- `GS1DAX05`: Amount of donations (15) - Health; universe `FG1FGIV = 1`.
- `GS1DNX05`: Number of donations (15) - Health; universe `FG1FGIV = 1`.
- `GS1DAX05 = 000000000.00` means None.
- `GS1DNX05 = 00` means No donations.
- `999999999.96` and `96` are Valid skip for non-givers.

Hospitals are not combined into the primary Health donor definition because the codebook documents them as separate ICNPO categories:

- `GS1DAX06`: Amount of donations (15) - Hospitals.
- `GS1DNX06`: Number of donations (15) - Hospitals.

A secondary derived metric, `broader_health_related_donor`, is included only for context and equals Health donor OR Hospital donor. It should be labelled clearly if used.

Validated Health donor sample count: 6,399.
Validated weighted Health donor population estimate: 6,797,272.
