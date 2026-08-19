# Bonus Methodology

This small extension tests whether interpretable respondent characteristics help distinguish Health donors from other respondents. The target is `is_health_donor`. Predictors are demographics and volunteering indicators from the validated Chapter 2 analytical dataset. The model uses deterministic stratified train/test splitting and a weighted logistic regression implemented with numpy. Survey weights are used in the fitting loss; metrics are reported on the held-out sample without claiming production readiness.
