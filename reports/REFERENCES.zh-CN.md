# 方法文献与出版信息

[English](REFERENCES.md) | [简体中文](REFERENCES.zh-CN.md)

出版元数据核对日期：2026-11-06。以下文献为推断或评价定义提供背景；项目实际实现仍以冻结方案、源码和独立数值核验为准。引用一般理论不等于已证明该理论的所有条件在本项目成立，也不把本项目改写为任何文献的完整复现。

| 对应位置 | 文献 | 在本项目中的用途 |
|---|---|---|
| METHODS第5节 | Petersen (2009)；Cameron, Gelbach & Miller (2011) | 面板误差依赖与多向聚类背景 |
| METHODS第5节、RESULTS第2节 | Holm (1979) | 四个核心检验的逐步多重校正 |
| METHODS第5节、RESULTS第2节 | Cameron, Gelbach & Miller (2008) | 商品单向wild cluster bootstrap补充推断 |
| METHODS第8节、RESULTS第4节 | Künsch (1989)；Politis & Romano (1992) | 时间依赖数据的区块重抽与循环区块背景 |
| METHODS第7节、RESULTS第4节 | Campbell & Thompson (2008) | 相对明确基准定义样本外平方误差比例 |

1. Petersen, M. A. (2009). Estimating Standard Errors in Finance Panel Data Sets: Comparing Approaches. *The Review of Financial Studies*, **22**(1), 435–480. DOI：[10.1093/rfs/hhn053](https://doi.org/10.1093/rfs/hhn053)。核对及作者材料：[作者页面](https://www.kellogg.northwestern.edu/faculty/petersen/htm/papers/standarderror.html)。

2. Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2011). Robust Inference With Multiway Clustering. *Journal of Business & Economic Statistics*, **29**(2), 238–249. DOI：[10.1198/jbes.2010.07136](https://doi.org/10.1198/jbes.2010.07136)。核对及作者材料：[2009年作者稿](https://cameron.econ.ucdavis.edu/research/JBESpaper2009version.pdf)。作者稿年份与正式期刊年份有别。

3. Holm, S. (1979). A Simple Sequentially Rejective Multiple Test Procedure. *Scandinavian Journal of Statistics*, **6**(2), 65–70. [JSTOR正式记录](https://www.jstor.org/stable/4615733)；核对：[该期目录](https://www.jstor.org/stable/i412579)。

4. Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2008). Bootstrap-Based Improvements for Inference with Clustered Errors. *The Review of Economics and Statistics*, **90**(3), 414–427. DOI：[10.1162/rest.90.3.414](https://doi.org/10.1162/rest.90.3.414)。核对：[NBER作者工作论文页面及Published Versions](https://www.nber.org/papers/t0344)。2007年工作论文与2008年正式发表分开标注；本项目只把商品单向WCR-t作为补充，不用它替代双向聚类。

5. Künsch, H. R. (1989). The Jackknife and the Bootstrap for General Stationary Observations. *The Annals of Statistics*, **17**(3), 1217–1241. DOI：[10.1214/aos/1176347265](https://doi.org/10.1214/aos/1176347265)。核对：[该期目录](https://www.jstor.org/stable/i312909)。

6. Politis, D. N., & Romano, J. P. (1992). A Circular Block-Resampling Procedure for Stationary Data. In R. LePage & L. Billard (Eds.), *Exploring the Limits of Bootstrap* (pp. 263–270). John Wiley. 核对：[Politis作者出版清单第37项](https://mathweb.ucsd.edu/~politis/DPpublication.html)、[Romano作者出版清单](https://profiles.stanford.edu/joseph-romano)。[Stanford技术报告](https://statistics.stanford.edu/technical-reports/circular-block-resampling-procedure-stationary-data)是1991年前身，并非1992年书章的发表年份。

7. Campbell, J. Y., & Thompson, S. B. (2008). Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average? *The Review of Financial Studies*, **21**(4), 1509–1531. DOI：[10.1093/rfs/hhm055](https://doi.org/10.1093/rfs/hhm055)。核对：[出版方文章页面](https://academic.oup.com/rfs/article-abstract/21/4/1509/1567518)。以正式卷期年份2008引用，区别于2007年在线发表。其历史平均基准不是本项目O0/R0的替代品；本项目始终明示每项R²_OS使用的基准。

区块文献不自动验证本项目固定20日区块、单一评估年份或条件于固定训练模型的区间具有精确覆盖。这里也没有借上述文献补做嵌套模型检验、选择新基准或改变已冻结推断。
