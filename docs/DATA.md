# Data and construction

OptionFlow uses official historical option and futures downloads from DCE, CZCE, SHFE, INE and GFEX. The input snapshot contains 588 files with underlying dates in 2017–2025. The research panel uses signals from 2019 and outcomes through 2025-12-31. [source_manifest.csv](../config/source_manifest.csv) records the relative filenames, byte counts and SHA256 hashes of the official input snapshot; it contains file metadata rather than trading observations.

## Construction rules

1. Identify exchange, product, full delivery year/month, futures family, option series, call/put and strike. Source file, sheet, row and hash identify provenance. Three-digit delivery codes are resolved in a trade-year-constrained decade window.
2. Standardize volume and open interest to single-sided counts. In this download family DCE uses factor 0.5 throughout; CZCE/SHFE/INE use 0.5 before 2020 and 1 thereafter; GFEX uses 1. These rules are source-family-specific, not universal rules for every exchange endpoint. Prices are unchanged.
3. Keep ordinary futures and regular options for primary analysis. Monthly-average F futures and MS options remain separate.
4. Select the positive-volume ordinary futures contract with greatest same-day volume per product. Break ties by open interest, earlier delivery and stable contract ID. Select first, then match options and evaluate outcome availability; do not substitute another contract after a failed match.
5. Sum put and call quantities before taking their ratio. Form month-level and commodity-level volume/open-interest PCRs. A zero denominator is missing; a zero numerator with a positive denominator is valid.
6. Define returns from positive closes with actual trading at both adjacent expected exchange sessions. Keep the signal-date contract for the next session. Published-close and settlement variants are separate; do not fill a missing primary return from another price definition.
7. Lag month PCRs within the identical contract and commodity PCRs within the product. Do not skip missing expected sessions or use the previous retained dominant-contract row as a substitute.
8. Split by outcome date: 2019–2024 for development and 2025 for evaluation. Coverage, liquidity and finite-variable requirements produce an unbalanced common sample.

The calendar uses cross-exchange observations and a fixed XSHG proxy calendar. Last-observed-series dates are diagnostic labels, not certified official expiry dates or prediction features. Contract specifications and end-of-day information availability limit trading interpretations.

## Public interface and availability

[DATA_DICTIONARY.md](DATA_DICTIONARY.md) describes the complete panel interface and quantity fields. Report tables provide sample flow, annual cross-sections, descriptive statistics and coverage. Download files and row-level panels are not part of this repository. This release documents construction and supplies the inference/scoring core; a downloader or full ingestion command is not included.
