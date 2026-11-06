# OptionFlow 数据字典

[English](DATA_DICTIONARY.md) | [简体中文](DATA_DICTIONARY.zh-CN.md)

## 身份与来源

- exchange/product/commodity：实际交易所、商品代码及二者组合；INE的SC/NR/LU/BC/EC不因文件放在SHFE目录而改归属。
- date：交易所给定交易日，夜盘不自行改自然日。
- delivery：YYYYMM完整标的交割年月。三位月份代码按冻结规则复原，且期权标的须匹配同日普通期货。
- entity：交易所:商品:交割年月:期货家族。普通与F月均价家族分离。
- contract_id：期货为entity；期权追加series、C/P及精确行权价。series为regular或MS。
- strike：精确十进制字符串；期权系列采用entity+series身份，不冒充已外核的精确到期日期。本数据接口没有另造官方到期日期字段。
- source_id/sheet/source_row：对应source_manifest的哈希前缀、工作表、源文件物理行号。副本路径在duplicates登记，跨文件重复原行在row_duplicate_provenance登记。

## 原始量和单边量

volume_raw / oi_raw：官方下载原始数量，不改原值。volume_single / oi_single：按unit_factor标准化的单边手数。oi是持仓存量，不是持仓变化。

DCE本批历史全期0.5；CZCE/SHFE/INE在2020-01-01之前0.5，之后1；GFEX为1。按日期和下载来源家族定义，不泛指其他网页端点。价格从不乘除2。成交额等未用于本研究特征，其原值仍在只读源文件，不作未经核实的单位换算。

## PCR

cv/cp：标的月份常规期权的成交量/持仓PCR，100×看跌/看涨。gv/gp：同商品全部普通标的月份的看跌总量/看涨总量×100；不平均月份比率。分母0置缺失，分子0且分母正置0。

原始期权明细的cp表示C/P方向；汇总表和研究面板的cp表示持仓PCR。期货研究面板删除了原来为空的方向字段，避免同名合并。两个上下文不能混读。

八个数量字段为：contract_call_volume、contract_put_volume、contract_call_oi、contract_put_oi，以及对应的commodity_前缀四列。前者是主力标的月份的常规期权加总，后者是商品全部常规月份加总；均为统一单边后的原数量，未经对数变换，不是下载文件中的双边原量。PCR分母、平滑变换和流动性敏感性可直接由这些列计算，无需重新合并。核心样本筛选规则见主力与可用性一节。

lcv/lcp按同entity前一预期交易日；lgv/lgp按同commodity前一预期交易日。主力换月不改变当前entity的滞后身份。主规格不汇入MS；MS与F仍完整保存在基础表/特殊合约表。

## 价格、收益与时点

- close_raw/settlement：官方公布收盘/结算价，保留源报价单位。
- close_traded：只有当日volume_single>0且close_raw>0才保留。
- current_return/past_return：同合约前一预期交易日至t，两个端点有成交且收盘价正时的对数收益。
- forward_return/y：同合约t到下一预期交易日，两端有成交且收盘价正时的对数收益。均不乘100。
- *_published：使用官方公布收盘，零价无效；无成交日正收盘通常为结算价，因此仅作公布口径敏感性，不声称成交收益。
- *_settlement：独立的两端结算价收益，绝不逐行填补主收益。
- prev_date/next_date：所内预期相邻交易日；prev_observed/next_observed：该entity实际相邻记录日期，构造收益时要求二者一致。
- calendar_gap_days：t至下一预期交易日自然日数，不是漏交易日数量。
- log_volume/log_oi：ln(1+当日期货单边成交量/持仓量)，在t已知。

## 主力与可用性

普通期货正成交量最大者为主力；并列依次按持仓大、交割月早、稳定entity排序。选择时不检查是否有期权、有效收盘或有效未来收益。

option_matched/pcr_complete/valid_forward_return：当前主力有期权、四种当前PCR完整、严格次日主收益有效。

history_eligible：以上三项全真；core_eligible再要求t>=2019-01-01。未筛选的商品主力日保存在main_contract_panel；核心分析行保存在analysis_panel。

split按outcome_date划分：history(<2019)、development(2019—2024)、evaluation_2025(2025)、no_in_range_outcome。2025是已完成评分的历史留出期，其PCR/收益在预处理时已被接触；接触范围见报告。

volume_tie_count记录最大成交量并列数；first_main_observation标明首个可观察主力日。roll_at_t仅在相邻预期交易日都有主力时表示主力身份是否改变；首日或中间无活跃主力时缺失，后者另标main_history_gap。

核心面板要求四种当期PCR和y有效，不要求全部滞后都有效。lcv/lcp/lgv/lgp分别仍有45/37/36/36个缺失；后续含滞后模型必须明确自己的完整样本，不能把核心行数直接当作所有模型的有效观测数。

## 仅供事后诊断的字段

series_last_observed_date/option_series_last_day：某标的月份+系列最后出现在完整文件中的日期及当日标志，并非已核实的官方到期日。series_right_censored为其最后观察日恰在交易所本批样本截止日；样本截止日不能冒充到期日。

option_series_last_day与series_right_censored为可空boolean（未匹配期权的主力日为NA）；Stata中导出为0/1数值。

last_observed_day、source_terminal_pattern等也是事后质量标记。它们不得直接作为t时点可知的预测特征。到期敏感性若使用这些观测终点，应明确其事后性质，不能宣传为可实时策略。
