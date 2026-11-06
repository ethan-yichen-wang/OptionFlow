# Reproducibility scope

## Included

- A study specification recording the completed analysis choices.
- Reviewed aggregate tables, model summaries, forecast parameters and confidence-interval figures.
- A numerical library for fixed effects, clustered inference, Holm adjustment, restricted wild bootstrap and fixed-model scoring.
- Synthetic tests and a standard-library release/results verifier.

The numerical functions preserve the reviewed mathematical implementation; packaging removes machine-specific runtime imports. Table CSVs, model JSONs and figures retain their original bytes. PUBLIC_MANIFEST.json fingerprints this release. Source-to-release correspondence is recorded in the local release audit; original research snapshots remain intact.

## What the checks establish

`python scripts/verify_release.py` checks public file fingerprints and the internal consistency of reported summary tables. `python -m unittest discover -s tests -v` exercises the numerical library on synthetic examples. Neither command refits the empirical models or opens 2025 targets.

The package does not include raw downloads, row-level panels, row-level sealed forecasts, bootstrap draw arrays, the complete ingestion runner or the full private audit environment. Summary checks alone cannot independently reconstruct all published coefficients or uncertainty intervals. Full empirical replication requires separately obtained inputs, construction under the documented rules, and the complete study workflow.

## Environment and review

The numerical analysis was executed with Python 3.12, NumPy 2.5.4, pandas 3.0.6, SciPy 1.18.1, pyhdfe 0.2.1 and PyArrow 26.0.1. Numerical-core dependencies are pinned in pyproject.toml. Exchange preprocessing used a separately recorded environment; the public package does not claim a single installation rebuilds that pipeline.

Implementation and computational checks used AI assistance (ChatGPT and Claude). Agreement between independent implementations supports computational consistency; it does not replace the stated model assumptions or external peer review. See the methods and holdout disclosure for inference and exposure limits.
