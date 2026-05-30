# MASCON Baseline Gravity Model Prediction Vector — 2026-05-29

Status: `MASCON_BASELINE_GRAVITY_MODEL_PREDICTION_VECTOR_BOUND_CONTROL_ONLY`

This object binds the baseline control prediction vector required after `MASCON_MODEL_COMPARISON_EXECUTION_TARGET_2026_05_29`.

## Bound baseline

- Baseline model: `ZERO_ANOMALY_CONTROL_BASELINE_ON_AUTHENTICATED_MASCON_GRID`
- Generator: `constant_zero`
- Grid: authenticated MASCON `time × lat × lon`
- Vector representation: generator and digest only, not materialized

## Role

This is the control baseline needed before a competing deficit-mass or geometric prediction vector can be compared.

## Boundary

This is a baseline control vector only. The zero-anomaly baseline is not a GR theorem and is not a fitted physical model. It does not bind a deficit-mass prediction vector, bind a comparison metric, execute MASCON model comparison, assert an empirical gravity result, assert GR failure, assert new gravity, assert dark matter replacement, assert Lambda-CDM failure, assert quantum gravity, or assert any Clay-problem closure.

## Next admissible object

- `MASCON_DEFICIT_MASS_MODEL_PREDICTION_VECTOR`
