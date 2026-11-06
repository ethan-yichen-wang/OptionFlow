# Historical holdout disclosure

The 2025 evaluation is a retrospective holdout assessment with disclosed prior data exposure.

[English](HOLDOUT_DISCLOSURE.md) | [简体中文](HOLDOUT_DISCLOSURE.zh-CN.md)

- Earlier analyses of overlapping development data were known before this protocol was fixed: one covered 2019–2024, and another used a snapshot ending on 2024-11-11. Neither included 2025 data.
- The protocol, code and hashes were fixed and recorded locally before scoring. They were not deposited in a public registry, and this repository was created after the 2025 evaluation. Public readers therefore rely on the disclosed process rather than an external prescoring timestamp. Local hash records establish content identity, not independently verifiable proof of when the choices were made.

- Raw 2025 records were processed, including return construction and row-level data verification, before forecast scoring.
- Prediction generation read signal-date features, including past_return, but did not explicitly load the 2025 y target column or calculate forecast errors at that stage.
- For adjacent observations of the same contract, y(t) equals past_return(t+1). Of 12,039 scored targets, 11,680 (97.018%) can be reproduced from later feature rows. This is an information-exposure limitation.
- Each prediction uses its own signal-date features and fixed parameters trained on 2019–2024. It does not retrieve a target from a future feature row, update parameters with 2025 outcomes, or use realized daily mean returns to generate predictions.
- Models were fixed before scoring; scoring code and shared resampling indices were fixed and hashed locally before explicitly reading target values. Independent computations checked the coefficients, forecasts and scores. Hashes support content consistency and recorded sequence, not a claim that all outcome information was inaccessible.
- The evaluation includes 51 products observed in development. Nine additional products are coverage-only. Relative targets and forecasts are centered separately within each evaluation universe.

The 2025 evaluation is complete. Any specification chosen using its results is exploratory and needs another evaluation period for an additional holdout claim.
