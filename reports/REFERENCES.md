# Research and methodological references

[English](REFERENCES.md) | [简体中文](REFERENCES.zh-CN.md)

Publication metadata were checked on 2026-11-06. These sources provide background for the inference/evaluation definitions; actual implementation follows the frozen study design, source code and independent numerical checks. General theory citations do not establish that every assumption holds in this sample or make the study a complete replication of any cited paper.

| Study location | Reference | Use in OptionFlow |
|---|---|---|
| METHODS Section 5 | Petersen (2009); Cameron, Gelbach & Miller (2011) | Panel dependence and multiway clustering |
| METHODS Section 5; RESULTS Section 2 | Holm (1979) | Step-down adjustment of four core tests |
| METHODS Section 5; RESULTS Section 2 | Cameron, Gelbach & Miller (2008) | Supplementary commodity-only wild cluster bootstrap |
| METHODS Section 8; RESULTS Section 4 | Künsch (1989); Politis & Romano (1992) | Dependent-data block resampling and circular blocks |
| METHODS Section 7; RESULTS Section 4 | Campbell & Thompson (2008) | Benchmark-specific out-of-sample squared-error ratios |

1. Petersen, M. A. (2009). Estimating Standard Errors in Finance Panel Data Sets: Comparing Approaches. *The Review of Financial Studies*, **22**(1), 435–480. DOI: [10.1093/rfs/hhn053](https://doi.org/10.1093/rfs/hhn053). Verification and materials: [author's page](https://www.kellogg.northwestern.edu/faculty/petersen/htm/papers/standarderror.html).

2. Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2011). Robust Inference With Multiway Clustering. *Journal of Business & Economic Statistics*, **29**(2), 238–249. DOI: [10.1198/jbes.2010.07136](https://doi.org/10.1198/jbes.2010.07136). Verification/materials: [2009 author manuscript](https://cameron.econ.ucdavis.edu/research/JBESpaper2009version.pdf). The manuscript year differs from the journal publication year.

3. Holm, S. (1979). A Simple Sequentially Rejective Multiple Test Procedure. *Scandinavian Journal of Statistics*, **6**(2), 65–70. [JSTOR record](https://www.jstor.org/stable/4615733); verification: [issue contents](https://www.jstor.org/stable/i412579).

4. Cameron, A. C., Gelbach, J. B., & Miller, D. L. (2008). Bootstrap-Based Improvements for Inference with Clustered Errors. *The Review of Economics and Statistics*, **90**(3), 414–427. DOI: [10.1162/rest.90.3.414](https://doi.org/10.1162/rest.90.3.414). Verification: [NBER working-paper page and Published Versions](https://www.nber.org/papers/t0344). The 2007 working paper and 2008 journal article are distinct versions. OptionFlow uses commodity-only WCR-t as a supplement, not a replacement for two-way clustering.

5. Künsch, H. R. (1989). The Jackknife and the Bootstrap for General Stationary Observations. *The Annals of Statistics*, **17**(3), 1217–1241. DOI: [10.1214/aos/1176347265](https://doi.org/10.1214/aos/1176347265). Verification: [issue contents](https://www.jstor.org/stable/i312909).

6. Politis, D. N., & Romano, J. P. (1992). A Circular Block-Resampling Procedure for Stationary Data. In R. LePage & L. Billard (Eds.), *Exploring the Limits of Bootstrap* (pp. 263–270). John Wiley. Verification: [Politis publication list, item 37](https://mathweb.ucsd.edu/~politis/DPpublication.html), [Romano publication list](https://profiles.stanford.edu/joseph-romano). The [Stanford technical report](https://statistics.stanford.edu/technical-reports/circular-block-resampling-procedure-stationary-data) is a 1991 predecessor, not the publication year of the 1992 book chapter.

7. Campbell, J. Y., & Thompson, S. B. (2008). Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average? *The Review of Financial Studies*, **21**(4), 1509–1531. DOI: [10.1093/rfs/hhm055](https://doi.org/10.1093/rfs/hhm055). Verification: [publisher page](https://academic.oup.com/rfs/article-abstract/21/4/1509/1567518). The citation uses the 2008 issue year, distinguished from online publication in 2007. That paper's historical-average benchmark does not replace OptionFlow's O0/R0; every R²_OS comparison states its own benchmark.

Block-bootstrap references do not automatically establish exact coverage for a fixed 20-day block, one evaluation year or intervals conditional on fixed training models. They are not used here to add nested-model tests, choose another benchmark or alter the frozen inference.

## Related option-market research

Pan, J., & Poteshman, A. M. (2006). The Information in Option Volume for Future Stock Prices. *The Review of Financial Studies*, **19**(3), 871–908. DOI: [10.1093/rfs/hhj024](https://doi.org/10.1093/rfs/hhj024). Verified against the [author-hosted published article](https://www.mit.edu/~junpan/volume.pdf).

Their principal signal uses buyer-initiated option volume opening new positions on U.S. equities. OptionFlow uses publicly available daily volume and open interest on Chinese commodity futures, without trade-initiation or opening/closing classification. These are different information sets; OptionFlow does not directly replicate or refute that paper's finding. Related-research metadata checked on 2026-11-07.
