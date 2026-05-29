# SPARC rotation-curve Step 3–5 accounting run and predictive-target boundary — 2026-05-28

## Formal status

`SATURATED_ACCOUNTING_RUN_ARCHIVED_PREDICTIVE_DEFICIT_MODEL_TARGET_OPEN`

## Closed objects

1. `BaryonicVelocityConventionForSPARC`
2. `FixedYdiskYbulForSPARC`
3. `BaselineModelPredictionVector`
4. `DeficitMassModelPredictionVector_saturated_accounting`
5. `LikelihoodComparisonResult_saturated_accounting`

## Archived artifacts

- `SPARC_STEP3_5_PREDICTION_LIKELIHOOD_ARTIFACTS_2026_05_28.zip`
- `SPARC_STEP3_5_COMPLETION_SUMMARY_2026_05_28.txt`
- `BARYONIC_VELOCITY_CONVENTION_FOR_SPARC_2026_05_28.txt`
- `BASELINE_MODEL_PREDICTION_VECTOR_2026_05_28.csv`
- `DEFICIT_MASS_MODEL_PREDICTION_VECTOR_2026_05_28.csv`
- `LIKELIHOOD_COMPARISON_RESULT_2026_05_28.json`
- `LIKELIHOOD_COMPARISON_PER_GALAXY_2026_05_28.csv`
- `SPARC_ROTATION_CURVE_STEP3_5_ACCOUNTING_RUN_AND_PREDICTIVE_TARGET_2026_05_28.json`

## Fixed convention

```text
Ydisk = 0.5
Ybul  = 0.7
Ygas  = 1.0

Vbar² = Vgas * |Vgas| + 0.5 * Vdisk² + 0.7 * Vbul²
Vbaseline = sqrt(max(Vbar², 0))

deficit_v² = max(Vobs² - max(Vbar², 0), 0)
Vgdm_saturated = sqrt(max(Vbar², 0) + deficit_v²)
```

## Recorded metrics

```text
galaxies_used = 175
rows_used = 3391
positive_deficit_rows = 3177
baryonic_overshoot_rows = 214

chi2_baseline = 1960466.562888448
chi2_gdm_saturated_accounting = 4511.003922882878
delta_chi2_gdm_minus_baseline = -1955955.558965565

reduced_chi2_baseline = 578.1381783805508
reduced_chi2_gdm_saturated_accounting = 21.079457583564853

AIC_baseline = 1960466.562888448
AIC_gdm_saturated = 10865.00392288288
delta_AIC_gdm_minus_baseline = -1949601.558965565

BIC_baseline = 1960466.562888448
BIC_gdm_saturated = 30336.456134416032
delta_BIC_gdm_minus_baseline = -1930130.106754032
```

## Open object

`PredictiveDeficitMassLawOrLowParameterDeficitMassModel`

## Minimum closure condition

A fixed low-parameter law must predict nonnegative deficit mass from radius/galaxy observables without assigning one fitted residual degree of freedom per positive-deficit row.

## Boundary

This archive records a saturated residual-accounting comparison.

It does not prove:

- predictive GDM law closure
- low-parameter deficit-mass model closure
- dark matter replacement
- Lambda-CDM failure
- physical validation
- independent holdout validation
- lensing validation
- cosmological validation
- PhD-complete final result
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem
