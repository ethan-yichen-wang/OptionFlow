# OptionFlow 表格索引

下列文件均在本目录tables/。T1/T2及wild原表为逐字节复制，其余为已审核表的显示转换或补充背景。没有重新估计或评分。

| 编号 | 文件 | 内容及单位 |
|---|---|---|
| T1a | T1_annual_crosssection.csv | 按收益年记录日横截面品种数的最小/中位/最大/均值、日期数、行数 |
| T1b | T1_coverage.csv | 开发期各所/品种行数及首末信号日 |
| T1c | T1_main_selection_flow.csv | 开发期主力匹配、PCR和收益可用性流程 |
| T2a | T2_development_descriptive.csv | 开发期描述；PCR是比值、收益是小数对数收益 |
| T2b | T2_development_correlations.csv | 开发期相关表 |
| T2c | T2_denominator_diagnostics_R3_retired.csv | R3撤销后保留的分母诊断，不含额外回归 |
| T3a | T3_primary_readable.csv | 四项主要推断原值及IQR尺度关联区间（log bp） |
| T3b | T3_supplementary_inference.csv | 商品单向聚类SE/t、WCR未校正p，四项 |
| T3c | T3_wild_descriptive.csv | 已预登记、10,000次WCR的完整原表，复制不变 |
| T4 | T4_consistency_lossless.csv | 原158行字符串保留，加R3撤销标记；补充p未校正 |
| T5a | T5_primary_readable.csv | 八项主要评分，Delta bp²、R²百分数、两类区间和原值 |
| T5b | T5_secondary_readable.csv | 二十项预定次要评分，仅点估计 |
| T5c | T5_zero_benchmark_context.csv | 无PCR基准与PCR模型相对零预测的背景；4个无PCR比率来自既有MSE代数换算 |
| T5d | T5_short_history_10.csv | 10个短历史品种的训练/评估行数及集合归属 |
| T5e | T5_new_products_9.csv | 9个开发期无核心行品种的评估覆盖；不评分 |
| T5f | T5_product_coverage_full.csv | 61品种完整覆盖元数据 |
| A0 | A0_contemporaneous.csv | 同期回归四个PCR项；只作描述性补充 |

汇总表保留未四舍五入的字段和显示转换。发布指纹见根目录PUBLIC_MANIFEST.json。
