# OptionFlow: Results and interpretation

[English](RESULTS.md) | [简体中文](RESULTS.zh-CN.md)

This report presents the research question, samples, primary and supplementary results, and limits of inference.

## 1. Research question and main finding

Using official data from five Chinese commodity exchanges, we ask whether the current day's option put–call volume and open-interest ratios contain information about the next-session price return of the same volume-selected futures contract. A second aggregation sums options across all regular delivery months of the same commodity.

**The prespecified daily linear specifications provide no clear evidence of a next-day conditional association in development. In the eight prespecified 2025 evaluation cells, the fixed PCR models also show no clear incremental forecast-accuracy difference relative to their corresponding no-PCR benchmarks.** Some contemporaneous associations remain, but they are not evidence of next-day prediction.

This is a negative finding with a defined scope. It does not establish that PCR is uninformative in every market, model, horizon or information set. It is neither a completed equivalence test nor a causal identification result. The data-construction and verification objectives were met; the tested predictive hypothesis did not receive clear support.

## 2. Development: coefficient signs are not predictive evidence

The development sample is assigned by outcome date and covers 2019–2024: 30,377 commodity-days, 52 products and 1,455 outcome dates. Model C includes contract-month CV and CP jointly; model G includes commodity-level GV and GP jointly. Both control for the return already realized on the signal day and log(1+x) of same-day single-sided futures volume and open interest. They absorb commodity and outcome-date fixed effects, with two-way clustering by those dimensions. The four core two-sided tests form one Holm-adjusted family.

| Predictor | Unadjusted p | Holm p | IQR association (log bp) | Pointwise 95% interval (log bp) |
|---|---|---|---|---|
| Contract-month volume PCR | 0.372 | 1.000 | -0.80 | [-2.58, 0.98] |
| Contract-month open-interest PCR | 0.779 | 1.000 | 0.41 | [-2.53, 3.35] |
| Commodity-level volume PCR | 0.539 | 1.000 | -2.03 | [-8.60, 4.55] |
| Commodity-level open-interest PCR | 0.568 | 1.000 | 1.49 | [-3.71, 6.69] |

IQR is the difference between the 75th and 25th percentiles of each PCR's pooled development distribution in model-input ratio units (after division by 100). The reported association equals IQR × coefficient × 10,000, holding the other model terms fixed. Each interval is a rescaling of that coefficient's pointwise 95% interval; it is neither a causal-effect interval nor simultaneous coverage of all four terms.

Unadjusted p-values range from 0.372 to 0.779; all Holm p-values equal 1. A value of 1 does not mean a 100% probability that the null hypothesis is true. CV/GV estimates are negative and CP/GP estimates positive, but these directions do not establish a next-day relationship. The intervals retain positive and negative possibilities: failure to reject zero does not prove an exactly zero effect.

The prespecified supplementary inference is below. SE and t use commodity clustering only. The restricted wild cluster bootstrap-t (WCR-t) imposes the zero null, uses Rademacher weights, 10,000 repetitions and seed 20261106. Its p-values are unadjusted.

| Predictor | Commodity-clustered SE | Commodity-clustered t | Wild bootstrap p (unadjusted) |
|---|---|---|---|
| Contract-month volume PCR | 1.526E-4 | -0.94 | 0.450 |
| Contract-month open-interest PCR | 1.653E-4 | 0.44 | 0.688 |
| Commodity-level volume PCR | 5.938E-4 | -0.66 | 0.716 |
| Commodity-level open-interest PCR | 4.198E-4 | 0.66 | 0.717 |

These supplementary results likewise provide no clear support for next-day association. They address commodity dependence only and do not replace the primary two-way covariance and Holm inference. Exact values are in [T3_wild_descriptive.csv](tables/T3_wild_descriptive.csv); the SE/t/WCR comparison is in [T3_supplementary_inference.csv](tables/T3_supplementary_inference.csv). These are existing estimates, not another round of estimation or resampling.

The IQR associations are approximately −0.80, +0.41, −2.03 and +1.49 log-return basis points. These are within-model scales. Their small size relative to daily variation does not statistically establish an economically zero effect.

## 3. Prespecified supplementary analyses

Exact lags, smoothed log quantity ratios, fixed winsorization, long-gap exclusions, stable selected contracts, option-history maturity, volume-only sample expansion, all-month coverage and leave-one-exchange-out analyses follow the recorded design. The additional R3 regression with a denominator >=50 was withdrawn before the protocol was frozen; T4 retains a not-estimated row.

None of the 56 predictive PCR coefficients in this summary has an unadjusted p<0.10; the smallest is approximately 0.165. The set excludes contemporaneous A0 and the four A1 paired-baseline terms (their p-values are approximately 0.38–0.75), and includes the R7 core/expanded single-PCR regressions. These are not 56 independent tests, and the count of non-rejections is not a vote proving the null. See [T4_consistency_lossless.csv](tables/T4_consistency_lossless.csv) for coefficients and references; supplementary p-values are descriptive.

R7 expands the common core to 30,726 rows. All 349 additional development commodity-days are last-observed option-series days with zero call open interest: contract-month open-interest PCR is undefined, while commodity-level open-interest PCR remains valid. None is right-censored by the sample endpoint. This comparison targets selection into the common complete-case sample, does not replace a zero denominator with a finite ratio, and does not certify every last-observed day as an official expiry date.

R8 includes all ordinary delivery months: 144,160 contract-days and 32,552 commodity-days, with month weights summing to 1 within each commodity-day. Coverage, weights and the PCR tail distribution differ from the selected-contract panel. Independent checks found large ratios in distant months with small denominators. Smaller coefficients alone cannot establish weaker or more robust prediction; no threshold was added after scoring. In R8-G, delivery months within one commodity-day share GV/GP, so they do not add independent PCR signals.

## 4. 2025: raw and relative returns

Predictions use models trained on 2019–2024 and then fixed: no 2025 retraining, parameter updates or ex post date effects. O0/OC/OG predict the raw price return. Relative forecasts use the non-date component of models trained with date fixed effects, with predictions and realized returns centered separately within each universe and date. R0 remains a no-PCR model, not a zero forecast.

The code label `absolute` and the figure label “Absolute” denote the **signed raw log price return**, not the absolute value of a return or a total investment return including financing or collateral income.

U_all contains 51 previously observed products and 12,039 rows. U_120 is its subset of 41 products with >=120 development core rows, totaling 9,692 rows. Both cover 243 outcome dates. Losses are first averaged equally across products within a date, then equally across dates. Nine new-to-development products receive coverage reporting only.

Delta MSE = no-PCR benchmark MSE − PCR-model MSE; a positive value means a smaller model error. One log bp is 0.0001 log-return units, so multiplying MSE and its interval by 10⁸ expresses them in bp². Multiplying R²_OS by 100 expresses it as a percentage.

| Target | Universe | PCR aggregation | Delta MSE (bp²) | Conditional 95% interval (bp²) | R²_OS (%) | Conditional 95% interval (%) |
|---|---|---|---|---|---|---|
| Raw return | U_all | Contract-month | 4.79 | [-1.28, 9.86] | 0.029 | [-0.008, 0.063] |
| Raw return | U_all | Commodity-level | 12.93 | [-2.59, 26.60] | 0.079 | [-0.015, 0.171] |
| Relative return | U_all | Contract-month | -0.78 | [-3.81, 2.39] | -0.006 | [-0.030, 0.018] |
| Relative return | U_all | Commodity-level | 2.94 | [-4.55, 10.00] | 0.023 | [-0.035, 0.079] |
| Raw return | U_120 | Contract-month | 0.23 | [-3.63, 3.64] | 0.001 | [-0.022, 0.023] |
| Raw return | U_120 | Commodity-level | 1.82 | [-8.21, 12.40] | 0.011 | [-0.050, 0.081] |
| Relative return | U_120 | Contract-month | -1.12 | [-4.07, 1.79] | -0.009 | [-0.034, 0.015] |
| Relative return | U_120 | Commodity-level | -1.73 | [-8.18, 4.41] | -0.014 | [-0.066, 0.036] |

All eight Delta MSE intervals span 0. Under the frozen interpretation rule, every cell shows no clear error difference. All four raw-return point estimates are positive; the four relative-return estimates have one positive and three negatives. The cells share dates and block indices; both PCR models for one target share a benchmark, and U_120 is nested within U_all. These signs are therefore not independent evidence and cannot be counted as votes. The difference between universes has no reported interval, and their product composition differs, so it cannot be attributed to training-history length.

Intervals use the same 20-outcome-date circular blocks and 10,000 resamples, taking 95% empirical percentiles conditional on fixed training models. They are not familywise simultaneous intervals and do not include all training-parameter uncertainty. Spanning zero is not a general proof of every nested-model null. The independent Monte Carlo endpoint check supports the present zero-crossing interpretation as not driven by finite resampling noise; it does not guarantee identical conclusions under every possible resample.

| Target | Universe | No-PCR benchmark | Benchmark RMSE (log bp) |
|---|---|---|---|
| Raw return | U_all | O0 | 127.86 |
| Relative return | U_all | R0 | 113.48 |
| Raw return | U_120 | O0 | 126.57 |
| Relative return | U_120 | R0 | 111.12 |

The following is the cell with the largest Delta MSE point estimate among the eight, used only to explain units: commodity-level PCR for U_all raw returns has Delta MSE approximately 12.93 bp² and R²_OS approximately 0.079%. This is not a profit of 12.93 bp. It is a difference in squared prediction errors: benchmark RMSE is approximately 127.86 log bp and model RMSE approximately 127.81 log bp. R²_OS of 0.079% is not an investment return.

All 20 prespecified secondary comparisons are in [T5_secondary_readable.csv](tables/T5_secondary_readable.csv). Equal-row weighting leaves the main picture unchanged. PCR-model R²_OS point estimates against zero forecasts are all negative. Using training-product means as the benchmark yields small positive and negative estimates; no additional intervals or confirmatory tests are introduced for these secondary values. They do not replace the agreed primary benchmarks or complete eight-cell reporting.

Zero-forecast comparisons also require the no-PCR context. The no-PCR column below is an algebraic conversion of the reported primary benchmark MSE and secondary zero-forecast MSE; both PCR columns use existing secondary scores. No new forecasts, loss sequences, intervals or tests were generated.

| Target | Universe | Model order | No-PCR vs zero R² (%) | Contract-month PCR vs zero R² (%) | Commodity PCR vs zero R² (%) |
|---|---|---|---|---|---|
| Raw return | U_all | O0 / OC / OG | -1.09 | -1.06 | -1.01 |
| Raw return | U_120 | O0 / OC / OG | -0.23 | -0.23 | -0.22 |
| Relative return | U_all | R0 / RC / RG | -0.78 | -0.79 | -0.76 |
| Relative return | U_120 | R0 / RC / RG | -0.30 | -0.31 | -0.32 |

The no-PCR benchmarks themselves perform worse than zero: O0 is approximately −1.09%/−0.23%, and R0 approximately −0.78%/−0.30%, similar to the corresponding PCR models. Thus, the PCR models' higher error than zero cannot be attributed to PCR. The phenomenon already appears in the no-PCR benchmarks. These comparisons do not decompose commodity intercepts, controls, estimation noise or their joint contributions, and cannot establish a specific cause. Incremental PCR information is assessed against each model's own O0/R0 benchmark.

The interval plot is [T5_MSE_forest.png](figures/T5_MSE_forest.png), also available as [SVG](figures/T5_MSE_forest.svg). It plots the reviewed estimates and endpoints without new resampling.

## 5. Why contemporaneous association is not next-day prediction

A0 uses the same development sample but changes the dependent variable to the return already realized on the signal day. It controls for quantities and commodity/signal-date fixed effects, clusters by commodity/signal date, and does not also include that same return on the right-hand side.

| Predictor | Coefficient per unit of the PCR ratio | Unadjusted p |
|---|---|---|
| Contract-month volume PCR | -0.001546 | 5.998E-2 |
| Contract-month open-interest PCR | 0.001869 | 5.762E-4 |
| Commodity-level volume PCR | -0.006323 | 2.647E-14 |
| Commodity-level open-interest PCR | 0.004665 | 1.613E-9 |

Both commodity-level PCRs and contract-month open-interest PCR show stronger unadjusted contemporaneous associations. Contract-month volume PCR has p approximately 0.060 and does not meet the 5% threshold; the four terms cannot all be described as significant. Contemporaneous and next-day specifications differ in their dependent variable and controls. Significance does not transfer from one to the other, and “significant now, insignificant tomorrow” is not itself a direct test of a coefficient difference.

The results are consistent with trading responses to current price movements, hedging activity or common shocks, but the design identifies neither direction nor mechanism. PCR measures activity/position ratios without identifying order-initiator-side net buying pressure. Its coefficient is not a causal estimate of sentiment-driven price correction.

## 6. Coverage: which products were scored?

The full core has 61 products and 43,079 rows in an unbalanced panel. Development contains 52 products and the 2025 candidate core 60. Their intersection has 51; nine products appearing only in evaluation have no trained intercept. CZCE:ZC has 392 development rows and no evaluation core rows.

The following ten products have fewer than 120 development training rows. They enter U_all but not the parallel primary U_120 evaluation. The threshold uses original development core counts and differs from R6's cumulative option-session maturity measure.

| Product | Development training rows | 2025 coverage rows | U_all | U_120 |
|---|---|---|---|---|
| CZCE:PR | 2 | 237 | Included | Excluded |
| DCE:CS | 52 | 231 | Included | Excluded |
| DCE:JD | 74 | 242 | Included | Excluded |
| DCE:LG | 30 | 228 | Included | Excluded |
| DCE:LH | 59 | 243 | Included | Excluded |
| GFEX:PS | 2 | 212 | Included | Excluded |
| SHFE:AO | 48 | 239 | Included | Excluded |
| SHFE:NI | 47 | 240 | Included | Excluded |
| SHFE:PB | 48 | 242 | Included | Excluded |
| SHFE:SN | 46 | 233 | Included | Excluded |

These products contribute 2,347 evaluation rows. CZCE:PR and GFEX:PS have only 2 training rows each. U_all therefore does not represent uniformly long training histories, and U_120 does not solve the new-product problem.

| New product | Development training rows | 2025 coverage rows | Scoring treatment |
|---|---|---|---|
| CZCE:PL | 0 | 104 | Coverage only |
| DCE:BZ | 0 | 119 | Coverage only |
| GFEX:PD | 0 | 23 | Coverage only |
| GFEX:PT | 0 | 23 | Coverage only |
| SHFE:AD | 0 | 139 | Coverage only |
| SHFE:BU | 0 | 54 | Coverage only |
| SHFE:FU | 0 | 74 | Coverage only |
| SHFE:OP | 0 | 73 | Coverage only |
| SHFE:SP | 0 | 54 | Coverage only |

The new-to-development products contribute 663 candidate rows and receive coverage reporting only. The scoring program did not read their target columns, invent intercepts or use 2025 means to supply them. “New” means absent from this study's development core, not necessarily a futures listing in 2025. Rows are assigned by outcome date and can include a 2024-12-31 signal.

These tables use the frozen coverage inventory and verified training counts, without reading targets to recompute coverage. See [T5_product_coverage_full.csv](tables/T5_product_coverage_full.csv) for all products.

## 7. Precise disclosure of holdout exposure

**This is a historical holdout evaluation conducted after rule freezing under disclosed data exposure, not a strictly blinded test of entirely unseen 2025 return information.** Preprocessing constructed 2025 returns and checked them row by row. Prediction generation did not read the named 2025 y column or calculate forecast errors, but did read valid past_return features.

For adjacent feature observations of the same contract, y(t)=past_return(t+1). Independent verification found that 11,680 of the 12,039 scored targets (approximately 97.0%) can be reproduced exactly from later feature rows. Statements that 2025 returns had never been read, or were inaccessible before scoring, would be inaccurate. See [HOLDOUT_DISCLOSURE.md](HOLDOUT_DISCLOSURE.md).

This cross-row overlap does not automatically imply that a prediction used its future answer. The signal-day past_return covers the previous session to t, whereas y covers t to the next session. Fixed predictions use their own t features and development parameters, without retrieving a target from t+1, retraining on 2025 or adjusting forecasts with realized daily mean returns. Realized means enter only the relative scoring target.

Support for the evaluation rests on rules/models being fixed before scoring, scoring code and indices being committed before explicit target-column access, no model changes based on 2025 errors, and independent recomputations agreeing. Hash checks support content consistency and recorded ordering; they do not prove that researchers had no earlier exposure or replace time-index checks in the code.

## 8. Scope and contribution

The evidence does not clearly support incremental value from the tested linear next-day PCR specifications. It neither rules out information in other models/horizons nor guarantees that another model would work. Any specification proposed after viewing the 2025 scores must be treated as exploratory; 2025 cannot remain an unused final test set.

Limits include a single evaluation year, unbalanced listing coverage, zero-position-related missingness, selection on observable future endpoints, end-of-day availability, heavy-tailed predictors, short histories for some products, and persistent predictive regressors. Fixed effects and clustering address particular mean/dependence structures, not every source of bias. See [METHODS.md](METHODS.md).

[TABLE_INDEX.md](TABLE_INDEX.md) locates T1 annual cross-sections, coverage and sample flow, T2 development descriptives/correlations, and T3–T5 results. [REFERENCES.md](REFERENCES.md) lists the methodological literature and verified publication details.

The verifiable contributions are official-data construction with source provenance; explicit units, contract identity, adjacent sessions and sample attrition; separation of contemporaneous association, next-day conditional association and fixed-model extrapolation; and complete reporting of a predictive hypothesis that was not supported in the frozen comparisons. Data construction, development estimation, holdout scoring and result statements have undergone independent computational checks.
