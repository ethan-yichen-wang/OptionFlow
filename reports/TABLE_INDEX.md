# OptionFlow table index

[English](TABLE_INDEX.md) | [简体中文](TABLE_INDEX.zh-CN.md)

All tables below are in [tables/](tables/). T1/T2 and the full wild-bootstrap table preserve the reviewed source bytes; other tables provide display conversions or benchmark context. No estimation or scoring was repeated for this documentation.

| ID | File | Content and units |
|---|---|---|
| T1a | [T1_annual_crosssection.csv](tables/T1_annual_crosssection.csv) | Daily cross-section minimum/median/maximum/mean product counts by outcome year; dates and rows |
| T1b | [T1_coverage.csv](tables/T1_coverage.csv) | Development coverage by exchange/product and first/last signal dates |
| T1c | [T1_main_selection_flow.csv](tables/T1_main_selection_flow.csv) | Development sample flow through contract selection, option matching, PCR and return availability |
| T2a | [T2_development_descriptive.csv](tables/T2_development_descriptive.csv) | Development descriptives; PCRs are ratios and returns decimal log returns |
| T2b | [T2_development_correlations.csv](tables/T2_development_correlations.csv) | Development correlations |
| T2c | [T2_denominator_diagnostics_R3_retired.csv](tables/T2_denominator_diagnostics_R3_retired.csv) | Denominator diagnostics retained after R3 was withdrawn; no additional regression |
| T3a | [T3_primary_readable.csv](tables/T3_primary_readable.csv) | Four primary inference terms, source values and IQR-scaled association intervals in log bp |
| T3b | [T3_supplementary_inference.csv](tables/T3_supplementary_inference.csv) | Commodity-only clustered SE/t and unadjusted WCR p-values for four terms |
| T3c | [T3_wild_descriptive.csv](tables/T3_wild_descriptive.csv) | Complete prespecified 10,000-draw WCR summary, unchanged |
| T4 | [T4_consistency_lossless.csv](tables/T4_consistency_lossless.csv) | All 158 estimated source rows plus the R3 not-estimated marker; supplementary p-values are unadjusted |
| T5a | [T5_primary_readable.csv](tables/T5_primary_readable.csv) | Eight primary evaluations; Delta in bp², R² in percent, both interval types and original values |
| T5b | [T5_secondary_readable.csv](tables/T5_secondary_readable.csv) | Twenty prespecified secondary point-estimate comparisons |
| T5c | [T5_zero_benchmark_context.csv](tables/T5_zero_benchmark_context.csv) | No-PCR/PCR context against zero forecasts; four no-PCR ratios are algebraic conversions of existing MSEs |
| T5d | [T5_short_history_10.csv](tables/T5_short_history_10.csv) | Training/evaluation counts and universe membership for ten short-history products |
| T5e | [T5_new_products_9.csv](tables/T5_new_products_9.csv) | Coverage for nine products absent from development; not scored |
| T5f | [T5_product_coverage_full.csv](tables/T5_product_coverage_full.csv) | Coverage metadata for all 61 products |
| A0 | [A0_contemporaneous.csv](tables/A0_contemporaneous.csv) | Four contemporaneous PCR terms; descriptive supplementary results |

Additional machine-readable exports are [all coefficients](tables/all_coefficients.csv), [all covariances](tables/all_covariances.csv), the [model registry](tables/model_registry.csv), and [primary coefficient source values](tables/T3_primary_coefficients.csv).

Tables retain unrounded numeric fields as well as display conversions. The release fingerprints are in [PUBLIC_MANIFEST.json](../PUBLIC_MANIFEST.json).

## Language and code labels

Numeric CSVs are preserved byte for byte. The optional `target_cn`, `signal_cn` and `universe_cn` columns in T5a are Chinese display labels; analysis uses the English `target`, `model` and `universe` identifiers. `absolute` means the signed raw log price return, while `relative` means the within-universe/date demeaned return. U_all has 51 products and U_120 has 41. T4's final Chinese note duplicates its English status `retired_before_freeze_not_estimated` for R3.

The official-source manifest retains original filenames, including Chinese text, so source identity and hashes remain traceable.
