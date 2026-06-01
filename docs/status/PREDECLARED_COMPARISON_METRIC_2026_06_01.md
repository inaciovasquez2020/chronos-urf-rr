# Predeclared Comparison Metric — 2026-06-01

## Status

`PREDECLARED_COMPARISON_METRIC_SUPPLIED_NO_COMPARISON_RUN_OUTPUT`

## Object

`PREDECLARED_COMPARISON_METRIC`

## Decision

`PASS`

This packet records the predeclared comparison metric for the aligned baseline gravity vector and model-or-deficit-mass vector.

## Primary Metric

`canonical_rmse_between_aligned_vectors_v1`

## Formula

`sqrt(mean(((baseline_i * factor_to_canonical + offset_to_canonical) - (model_i * factor_to_canonical + offset_to_canonical))^2))`

## Direction

`lower_is_better`

## Canonical Unit

`meter liquid-water-equivalent thickness`

## Resolved Missing Input

`predeclared_comparison_metric`

## Remaining Missing Inputs

1. `reproducible_comparison_run_output`

## Certified Non-Claims

This packet records:

- predeclared comparison metric only;
- no reproducible comparison run output supplied;
- no empirical gravity result supplied;
- no anomaly detection result;
- no model-favored result;
- no baseline-favored result;
- no DFM-MKC validation;
- no Lambda-CDM failure;
- no dark matter resolution;
- no dark energy resolution;
- no physical discovery claim;
- no Chronos-RR closure;
- no H4.1/FGL closure;
- no P vs NP claim;
- no Clay-problem claim.

## Next Admissible Object

`REPRODUCIBLE_COMPARISON_RUN_OUTPUT`
