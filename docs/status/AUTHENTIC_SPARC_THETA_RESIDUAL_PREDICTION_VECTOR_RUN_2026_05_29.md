# AuthenticSPARCThetaResidualPredictionVectorRun

Status: `REPOSITORY_ARCHIVED_SPARC_DERIVED_NUMERIC_RUN_NO_RAW_PAYLOAD_CLAIM`

This executes the theta residual prediction rule against the repository-archived SPARC Step 3–5 baseline prediction vector.

Source:

```text
artifacts/sparc/rotation_curve_step3_5_2026_05_28/BASELINE_MODEL_PREDICTION_VECTOR_2026_05_28.csv
Output:
artifacts/sparc/authentic_sparc_theta_residual_prediction_vector_run_2026_05_29.csv
Rule:
theta = 1/2
observed_velocity_squared = Vobs^2
baryonic_velocity_squared = Vbar2_clamped
residual = max(observed_velocity_squared - baryonic_velocity_squared, 0)
theta_prediction_velocity_squared = baryonic_velocity_squared + theta * residual
Computed results:
row_count = 3391
galaxy_count = 175
positive_residual_rows = 3177
baryonic_overshoot_rows = 214
theta_squared_error = 383792666232.44586
baseline_squared_error = 1478821681950.1565
improvement = 1095029015717.7107
theta_improves_baseline = True
Boundary
Does not prove: raw SPARC payload authenticity newly verified.
Does not prove: authentic SPARC empirical validation.
Does not prove: independent real-data holdout validation.
Does not prove: predictive GDM law closure.
Does not prove: low-parameter deficit-mass model closure.
Does not prove: dark matter replacement claim.
Does not prove: Lambda-CDM failure claim.
Does not prove: physical validation claim.
Does not prove: SPARC empirical victory claim.
Does not prove: PhD-complete final result claim.
Does not prove: unrestricted Chronos-RR.
Does not prove: unrestricted H4.1/FGL.
Does not prove: P vs NP.
Does not prove: Clay problem.
Next Missing Object
RawSPARCRotmodPayloadBindingAndSchemaValidation

## Boundary

This is a repository-archived SPARC-derived numeric run only.

Does not prove: no raw SPARC payload authenticity newly verified; no authentic SPARC empirical validation; no independent real-data holdout validation; no predictive GDM law closure; no low-parameter deficit-mass model closure; no dark matter replacement claim; no Lambda-CDM failure claim; no physical validation claim; no SPARC empirical victory claim; no PhD-complete final result claim; no unrestricted Chronos-RR; no unrestricted H4.1/FGL; no P vs NP; no Clay problem.
