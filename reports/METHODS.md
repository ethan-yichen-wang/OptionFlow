# OptionFlow: Methods

[English](METHODS.md) | [简体中文](METHODS.zh-CN.md)

## 1. Observation unit and signal aggregation

A primary-panel row is an exchange × commodity × signal-date observation. Among a commodity's available delivery months, the contract with the highest daily futures volume is selected. Contract-month PCR uses regular options on that futures month; commodity-level PCR sums put and call quantities across all regular option months of the same commodity. Both models target the next-session price return of the one futures contract selected on the signal date.

Selection uses all ordinary futures contracts with positive volume. Ties are broken by greater open interest, earlier delivery month and the complete stable entity code. Only then are options, finite PCRs and future endpoints checked. A failure does not trigger substitution of another option-covered month. Base data retain all months; the selected-contract panel is a choice of observation unit. Prespecified R8 uses all months with within-commodity-day weights.

## 2. Sources, units and contract identity

Inputs are 588 official historical downloads from DCE, CZCE, SHFE, INE and GFEX, with base dates in 2017–2025 starting at each product's available coverage. Content-based deduplication and parsing yield 18,653,445 business rows: 1,369,363 futures and 17,284,082 options. These include 612 F and 6,896 MS special-instrument rows, retained separately and excluded from primary specifications.

File hashes, physical source rows, sheets, original codes, parse status and header-only downloads are recorded. The 111 header-only download tasks are not 111 damaged files; their coverage explanations are separate from certification of official contract lifecycles. Actual products determine INE membership, rather than folder names alone.

Quantities are standardized to single-sided contract counts while retaining downloaded raw quantities:

| Downloaded source family | Multiplier on raw counts |
|---|---|
| DCE, all downloaded years | 0.5 |
| CZCE/SHFE/INE, before 2020 | 0.5 |
| CZCE/SHFE/INE, from 2020 | 1 |
| GFEX | 1 |

Factors apply to this download family and date, not every exchange web endpoint. Prices are never divided or multiplied by two. Scaling numerator and denominator together leaves PCR unchanged but changes log(1+quantity), so controls use standardized single-sided counts.

The futures entity is `exchange:product:full YYYYMM:family`. Three-digit delivery codes are resolved in a unique trade-year-constrained decade window to avoid cross-decade collisions. Options additionally identify regular/MS series, C/P and exact strike. Every option-underlying day is verified against its same-day futures contract, with call/put pairing checked at strike level. Last-observed and right-censoring flags are ex post diagnostics, not certified official expiry dates or usable forecasting features.

See the [data dictionary](../docs/DATA_DICTIONARY.md). Detailed data and key aggregates were independently rebuilt with another parser. Calendar checks use cross-exchange date unions and a fixed-version XSHG proxy; they do not certify every year's official futures holiday notices or historical contract specifications.

## 3. PCR, returns, lags and usable observations

For contract month m or commodity i, sum put and call quantities before division:

$$
PCR^V=100\frac{\sum V^{put}}{\sum V^{call}},\qquad
PCR^{OI}=100\frac{\sum OI^{put}}{\sum OI^{call}}.
$$

Do not average strike-level or month-level PCRs. A zero denominator is missing; a zero numerator with a positive denominator is valid zero. Missing values are not filled, and large values do not justify guessing another percentage conversion. Stored PCRs are percentage-scaled. Model-level cv/cp/gv/gp and their lags are all divided by 100 to obtain ratios.

Let d(t) be the next expected exchange session and c(i,t) the futures contract selected at t. The target is

$$
y_{i,t}=\log P_{c(i,t),d(t)}-\log P_{c(i,t),t}.
$$

Both endpoints must have actual trading, positive closes and adjacent expected session dates. A next-day change in the selected month does not change the target contract. A positive published close on a no-trade day can be a settlement price; it is not mixed into the primary return. Published-close and settlement variants are stored separately. This is a log price change, not a portfolio return incorporating margin, interest, fees or slippage.

past_return is the same contract's log return from the previous expected session to t. lcv/lcp use that entity's previous expected session; lgv/lgp use the commodity's previous expected session. Neither a previous retained selected-contract row nor a gap-skipping observation substitutes for the required session. Calendar-day spans across holidays are recorded, but the primary target remains an adjacent-session return without division by calendar days.

Core rows require all four current PCRs and y to be valid; controls are finite throughout the primary development sample. Missing options, zero denominators and invalid future endpoints are recorded in sample flow. Position-related exclusions systematically affect some series' final observations, so inference is not extended to every excluded day. Final-day flags are not predictors. Contract/X construction uses t information, while future-endpoint observability remains a sample-selection condition.

## 4. Date assignment and product coverage

Signals begin in 2019. Split by outcome date rather than signal year: D=2019–2024 and E=2025. A 2024-12-31 signal with a 2025-01-02 outcome belongs to E. A 2025-12-31 signal lacks an in-snapshot 2026 endpoint and is excluded from the core outcome sample.

| Sample | Products | Rows | Role |
|---|---|---|---|
| Core D+E union | 61 | 43,079 | Unbalanced panel interface |
| D | 52 | 30,377 | Primary estimation and all model training |
| E core candidates | 60 | 12,702 | Candidate coverage; not all scored |
| U_all | 51 | 12,039 | Products seen in D; primary scoring |
| U_120 | 41 | 9,692 | U_all products with >=120 development core rows; parallel primary scoring |
| Short-history subset of U_all | 10 | 2,347 | U_all only |
| Products first observed in E | 9 | 663 | No trained intercept; coverage only |

“New” means no development core rows, not necessarily a recently listed futures product. CZCE:ZC appears only in development, with 392 rows and no E core rows. No pre-listing values or missing dates are imputed, and products need not span all of 2019–2024. T1 reports yearly daily cross-section sizes. Primary rows receive equal weight, while yearly/product contributions differ.

The >=120 threshold counts original D core rows. U_120 is only a scoring subset: models still train on all D, without pooling short-history intercepts or retraining for the subset. This differs from R6's requirement of at least 120 observed regular-option sessions through t. The ten short-history and nine new-product lists are in the [table index](TABLE_INDEX.md).

## 5. Primary development models and inference

Two models are fitted separately; all four PCRs are not jointly entered into one primary model:

$$
\begin{aligned}
C:\ y_{i,t}&=\alpha_i+\lambda_{d(t)}+\beta_{CV}cv_{i,t}+\beta_{CP}cp_{i,t}+\gamma'W_{i,t}+u_{i,t},\\
G:\ y_{i,t}&=\alpha_i+\lambda_{d(t)}+\beta_{GV}gv_{i,t}+\beta_{GP}gp_{i,t}+\gamma'W_{i,t}+u_{i,t}.
\end{aligned}
$$

PCRs are divided by 100; y is not multiplied by 100. W is fixed to past_return, log_volume=ln(1+same-day single-sided futures volume), and log_oi=ln(1+same-day single-sided futures open interest). Alpha denotes commodity effects and lambda outcome-date effects. Each primary commodity-day has OLS weight 1. B_FE includes only the same fixed effects and W.

Coefficients use variation after removing commodity and date effects. They describe relative conditional associations after fixed product differences and common date levels, not independent time-series forecasts for each commodity or causal effects. Date effects remove common additive levels, not every heterogeneous risk exposure or source of endogeneity.

After finite-value/model-validity screening, singleton groups are removed iteratively under the actual absorbed effects. C/G and paired comparisons share final keys. Multiple months in one R8 commodity-day are not automatically a singleton. A1 starts with 30,345 common lagged rows and drops 2 singletons to 30,343; R6 starts with 25,668 and drops 1 to 25,667. The primary sample has no singletons. N, K and cluster counts use final samples.

For residualized X, define B=(X'WX)^−1 and s_g=Σ_(r∈g) w_r X_r u_r. Each clustered covariance component is

$$
V_j=\frac{G_j}{G_j-1}\frac{N-1}{N-K_{full}}\,B\Big(\sum_gs_gs_g'\Big)B,
\quad V=V_i+V_{d(t)}-V_{i,d(t)}.
$$

Primary w=1; R8 uses month weights. Intersection scores are aggregated by commodity-day; independent month-level HC0 is not a substitute in R8. K_full includes full fixed-effect rank and identified slopes: it is 1,511 for primary C/G, with N=30,377. Tests use t(min(G−1,T−1))=t(51), with G=52 and T=1,455. Negative estimated variances are not silently set to zero to change significance; collinear terms are treated as unidentified.

The four two-sided zero-PCR-coefficient hypotheses form one family at alpha=5%, with Holm adjustment. Unadjusted p-values and pointwise 95% intervals are retained. Supplementary p-values are unadjusted/descriptive. IQR associations only rescale the same coefficients; no equivalence margin was registered, so non-significance does not establish a zero effect.

A supplementary commodity-clustered restricted WCR-t imposes the zero null and uses Rademacher weights, 10,000 repetitions, seed 20261106 and PCG64. Its p-value is (exceedances+1)/(B+1). This one-way-dependence supplement does not replace two-way inference. Projection-matrix precomputation reproduces the statistic from a full fixed-effect refit in each draw. It was checked against explicit-dummy synthetic refits and independently reproduced weights.

The four WCR p-values are 0.450/0.688/0.716/0.717; commodity-only t statistics are approximately −0.94/+0.44/−0.66/+0.66. Exact SE/t/p values are in [T3_supplementary_inference.csv](tables/T3_supplementary_inference.csv) and [T3_wild_descriptive.csv](tables/T3_wild_descriptive.csv). These are prespecified results, not new inference.

pyhdfe/FWL was checked against explicit-dummy balanced, unbalanced, weighted and multi-month synthetic examples. Stata reghdfe separately checked the four core and control slopes. Its native two-way VCE also uses a common minimum-cluster correction, so a single K-factor conversion is insufficient. Each of its three one-way components was converted from its actual degrees-of-freedom convention to the frozen full-rank correction, then combined using CGM. Software defaults did not replace the protocol.

## 6. Supplementary analyses and their interpretation

Prespecified analyses are A0 contemporaneous association, A1 exact lags, R1 smoothed log quantity ratios, R2 fixed development 1%/99% winsorization, R4 exclusion of >=4-calendar-day gaps, R5 stable signal-date selected contracts, R6 cumulative option-history maturity, R7 volume-only expansion, R8 all delivery months, and five leave-one-exchange-out specifications. R3 was withdrawn before freezing; no outcome-sensitive denominator threshold was substituted. Analyses are reported without combining them into a specification-search grid.

A0 uses past_return as its dependent variable, controls only log_volume/log_oi, and uses commodity/signal-date effects and clustering. A1 uses a common valid sample for the four lags and refits the no-lag specification on that same subset. R1 uses ln(1+put)−ln(1+call). R2 winsorizes only the four PCRs, not y or controls, with thresholds fitted on D only.

R7 requires valid cv/gv/y/W but not finite open-interest PCRs, giving 30,726 rows. Each single volume-PCR model is paired across the original and expanded D samples; it is not assumed to estimate the same effect as a two-PCR model. All 349 added rows are last-observed-series days with missing cp and valid gp. The exercise locates a selection mechanism without imputing undefined position ratios.

For R8, if n months remain valid in a commodity-day, each gets weight 1/n. Counts/weights are recomputed after singleton removal and verified to sum to 1. Fixed effects and clustering remain commodity/outcome-date; months are not independent clusters. Its 144,160 rows include all 30,377 primary observations with identical PCR/return/control values. Repeated GV/GP do not add independent signal. With month-varying controls, R8-G is not automatically equivalent to regressing only average returns on average controls.

## 7. Two 2025 targets with fixed training models

Raw-return models O0/OC/OG are trained only on D, with commodity intercepts and W. OC/OG add their respective PCR pair. They contain no future date effects, and O0 is the primary benchmark. Parameters are not updated in E; E means/quantiles do not transform features. The implementation calls this signed raw-price-return target `absolute`; it is not the absolute value of returns.

Relative forecasts use the non-date components of development B_FE/C/G:

$$
p^m_{i,t}=\hat\alpha^m_i+x^m_{i,t}\hat\beta^m+W_{i,t}\hat\gamma^m,\quad
\tilde p^m_{i,t}=p^m_{i,t}-\bar p^m_{U,d},\quad
\tilde y_{i,t}=y_{i,t}-\bar y_{U,d}.
$$

Means are computed separately within U_all and U_120 on the same outcome date. Common date levels and normalization constants cancel; no 2025 date effect is estimated. R0 comes from B_FE and RC/RG from C/G. Realized return means construct scoring targets only and never enter prediction generation. Evaluation conditions on valid observable outcomes; it does not claim a real-time-known final universe or an executable portfolio.

Two targets × two parallel universes × two PCR models give all 8 primary comparisons. Both universes have 243 common dates and at least two distinct products per date. MSE/MAE average equally across products within date, then equally across dates. RMSE is the square root of the overall date-averaged MSE, not the average of daily RMSEs.

$$
\Delta MSE=MSE_{baseline}-MSE_{model},\qquad R^2_{OS}=1-\frac{MSE_{model}}{MSE_{baseline}}.
$$

The 20 secondary comparisons comprise equal-row weighting (8), raw-return zero benchmarks (4), development-product-mean benchmarks (4), and relative zero benchmarks (4). Mean benchmarks use sealed training means; zero forecasts do not replace primary R0/O0. Secondary comparisons receive no additional intervals or confirmatory p-values.

The zero-benchmark context table converts existing no-PCR and zero-forecast MSEs into 4 background ratios; see [T5_zero_benchmark_context.csv](tables/T5_zero_benchmark_context.csv). This adds no predictions, loss sequences, intervals or tests, and does not decompose intercept/control contributions.

## 8. Block intervals and units

Before explicit target-column access, PCG64, seed 20261107 and 10,000 circular moving-block samples were fixed. Each sample concatenates 13 segments of 20 consecutive outcome dates, wraps modulo the observed date count, and truncates to 243 dates. All 8 comparisons share date indices; products are not resampled independently. Resampling uses fixed daily losses without refitting, changing predictions or sharing centering means across universes.

Delta and R² intervals take the 2.5%/97.5% empirical quantiles using linear interpolation. They are conditional on the training sample/fixed models and rely on the block approximation and sample-period stability. They do not capture all training-parameter uncertainty, provide simultaneous family coverage, or establish an unqualified nested-model test. When benchmark MSE is zero, R² is NA: there is no epsilon, substitute benchmark or silent omission of zero-denominator draws. That branch was not triggered here.

| Stored quantity | Displayed unit | Multiplier |
|---|---|---|
| Decimal log returns and their RMSE/MAE | log bp | 10,000 |
| MSE, Delta and their intervals | log-return bp² | 100,000,000 |
| R²_OS ratios and intervals | % | 100 |

bp² is not a return measured in bp, and R²_OS is not an investment return. Display conversion leaves the reviewed calculation tables intact.

## 9. Exposure, limitations and replication boundaries

Raw 2025 data were read during construction/verification. Prediction generation did not load the y column, but did read valid past-return features whose later rows reproduce many earlier targets. This is not a strictly blinded evaluation; see [HOLDOUT_DISCLOSURE.md](HOLDOUT_DISCLOSURE.md).

A row's valid past_return is not its own future y. Fixed predictions use t features and D parameters, without retrieving future-row answers, updating training or choosing methods from E errors. The protections are frozen models/methods, pre-score code/index commitments and independent checks, not a claim that all target information was inaccessible.

The scope is commodity-days with matching options, four finite PCRs and observable future prices. Zero positions, liquidity, month coverage, listing cohorts and endpoint observability affect selection; fixed effects do not remove every bias. Persistent predictors and short product histories can affect within-sample slopes. Clustering/bootstrap address particular error dependence and do not guarantee correction of slope bias. One evaluation year does not establish performance in every future year or commodity.

End-of-day indicators become available after the close is formed. Without an executable entry point, transaction costs/slippage and portfolio margin analysis, the close-to-close target is not a demonstrated real-time profitable trading strategy.

## 10. Code and computational checks

Public code supplies the numerical core for fixed effects/two-way clustering, restricted wild bootstrap, relative-target construction and paired circular-block scoring. Unit tests use synthetic data. Release checks read aggregate tables/fingerprints without refitting empirical models or opening row-level targets.

Data construction was independently rebuilt; 38 development models, 184 coefficients and forecast parameters were independently checked. The eight primary and twenty secondary evaluations were also independently recomputed. Their inferential and exposure limits remain as stated above.

See [REPRODUCIBILITY.md](../docs/REPRODUCIBILITY.md) for execution and public-data boundaries.

The [references](REFERENCES.md) document Petersen (2009) and Cameron, Gelbach & Miller (2011) for dependence/clustering; Holm (1979) for familywise adjustment; Cameron, Gelbach & Miller (2008) for one-way wild-bootstrap supplementation; Künsch (1989) and Politis & Romano (1992) for block resampling; and Campbell & Thompson (2008) for benchmark-specific out-of-sample error ratios. These references do not change the study's benchmark, block length or frozen inference, or automatically establish interval coverage. Software differences were checked against fixed local reghdfe 6.14.1 source and numerical results, not assumed away through citation.
