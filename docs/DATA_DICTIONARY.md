# OptionFlow data dictionary

[English](DATA_DICTIONARY.md) | [简体中文](DATA_DICTIONARY.zh-CN.md)

## Identity and provenance

- `exchange` / `product` / `commodity`: actual exchange, product code and their combined identifier. INE products SC/NR/LU/BC/EC are not assigned to SHFE merely because a file was placed in an SHFE folder.
- `date`: the exchange-assigned trading date. Night sessions are not reassigned to another calendar date.
- `delivery`: full underlying delivery year/month in YYYYMM. Three-digit codes follow the frozen reconstruction rule; each option underlying must match same-day futures.
- `entity`: `exchange:product:delivery YYYYMM:futures family`. Ordinary and F monthly-average futures are separate families.
- `contract_id`: entity for futures; options append series, C/P and exact strike. `series` is regular or MS.
- `strike`: an exact decimal string. Option series use entity+series identity, not an externally certified expiry date. No synthetic official-expiry field is introduced.
- `source_id` / `sheet` / `source_row`: source-manifest hash prefix, worksheet and physical source-file row. Duplicate paths and cross-file row duplication are recorded in the construction audit's `duplicates` and `row_duplicate_provenance` records.

## Downloaded and single-sided quantities

`volume_raw` / `oi_raw` retain downloaded counts. `volume_single` / `oi_single` multiply them by `unit_factor` to obtain single-sided contract counts. Open interest is a position stock, not its daily change.

For this download family, DCE uses factor 0.5 throughout; CZCE/SHFE/INE use 0.5 before 2020-01-01 and 1 thereafter; GFEX uses 1. Factors are specific to date and source family, not all web endpoints. Prices are never multiplied or divided by two. Turnover and other unused fields remain in read-only sources without unverified unit conversion.

## PCR and underlying quantities

`cv` / `cp` are regular-option volume/open-interest PCRs for one underlying month: 100 × put/call. `gv` / `gp` first sum put and call quantities over all regular underlying months of the same commodity, then form that ratio ×100. Month ratios are not averaged. A zero denominator gives missing; zero put with positive call is valid zero.

In strike-level option records, `cp` denotes C/P direction. In aggregates/research panels, `cp` denotes open-interest PCR. The futures research panel drops its unused direction column to avoid a same-name join. These contexts must remain distinct.

Eight quantity columns are available: `contract_call_volume`, `contract_put_volume`, `contract_call_oi`, `contract_put_oi`, and the four corresponding `commodity_` columns. Contract quantities sum regular options on the selected futures month; commodity quantities sum regular options across its months. All are standardized single-sided quantities before logs, rather than downloaded double-sided counts. They support direct denominator, smoothing and liquidity checks without another join. Core eligibility follows the rules below.

`lcv` / `lcp` use the same entity's previous expected session. `lgv` / `lgp` use the same commodity's previous expected session. A selected-month change does not alter the current entity's lag identity. Primary specifications exclude MS; MS and F details remain separately recorded in the base/special-instrument data.

## Prices, returns and timing

- `close_raw` / `settlement`: official published close/settlement, in original quotation units.
- `close_traded`: retained only where same-day `volume_single>0` and `close_raw>0`.
- `current_return` / `past_return`: log return for the same contract from the previous expected session to t, requiring trading and a positive close at both endpoints.
- `forward_return` / `y`: same-contract t-to-next-expected-session log return, under the same endpoint requirements. Neither return is multiplied by 100.
- `*_published`: official published-close variants. Zero prices are invalid; a positive no-trade close commonly represents settlement. This is a published-price sensitivity measure, not a claimed traded return.
- `*_settlement`: separate two-endpoint settlement returns; never used as row-wise fills for the primary return.
- `prev_date` / `next_date`: expected adjacent exchange sessions. `prev_observed` / `next_observed`: actual adjacent entity records. Return construction requires the corresponding expected/observed dates to agree.
- `calendar_gap_days`: calendar-day distance from t to the next expected session, not a count of missing trading sessions.
- `log_volume` / `log_oi`: ln(1+same-day single-sided futures volume/open interest), observable at t.

## Contract selection and sample availability

Select the ordinary futures contract with the greatest positive daily volume. Break ties by greater open interest, earlier delivery month and stable entity code. Selection does not inspect option availability, valid closes or valid future returns.

`option_matched`, `pcr_complete` and `valid_forward_return` respectively mark matching options, all four current PCRs being valid, and a valid strict next-session primary return.

`history_eligible` requires all three flags. `core_eligible` additionally requires t>=2019-01-01. `main_contract_panel` retains unscreened selected-contract days; `analysis_panel` retains core observations.

`split` uses `outcome_date`: history (<2019), development (2019–2024), evaluation_2025 (2025), or no_in_range_outcome. The 2025 historical evaluation is complete; PCR/return values were exposed during preprocessing. See the [holdout disclosure](../reports/HOLDOUT_DISCLOSURE.md).

`volume_tie_count` counts contracts tied for maximum volume. `first_main_observation` marks the first observed selected-contract day. `roll_at_t` identifies a change in selected contract only when both adjacent expected sessions have a selected contract. It is missing on the first observation or across an inactive-session gap; `main_history_gap` separately marks the latter.

The core requires four valid current PCRs and y, not every lag. `lcv` / `lcp` / `lgv` / `lgp` have 45/37/36/36 missing values respectively. Lagged models must state their own complete-case sample rather than reuse the core count as their effective N.

## Ex post diagnostic fields

`series_last_observed_date` / `option_series_last_day` record the last appearance of an underlying-month+series in the full files and its day flag. They are not certified official expiries. `series_right_censored` marks a final observation coinciding with the snapshot endpoint for that exchange; a sample endpoint is not an expiry date.

`option_series_last_day` and `series_right_censored` are nullable booleans, with NA when options do not match. Stata exports use numeric 0/1 values.

`last_observed_day`, `source_terminal_pattern` and related fields are also ex post quality diagnostics. They are not signal-date forecasting features. Sensitivity analyses using observed endpoints must disclose that ex post nature and cannot be presented as real-time trading strategies.
