# CDT-SM-01 Stage 0 classifier v2: isolated null-control correction

Status: **SYNTHETIC_REGRESSION_PASS_ONLY**, pending independent CI and physical execution.

Base design: `artifacts/external_validation/carbon_gravity_stage0_internal_execution_package_2026_07_12.json`.
Its locked v1 `analysis_lock.canonical_code` and SHA-256
`4291599bea04eb267dc832ad673f22aff27a6a008cbb2ace96c2746ddafa4ccc`
remain unchanged. No sample manufacture, calibration, blinded run, physical detection,
or gravitational-coupling proof is claimed.

## Demonstrated defect

With balanced 16 synthetic entries, means `C1=6e-8`, `C2=-6e-8`,
`C3=+1e-6`, `C4=-1e-6`, original v1 uses `(C3+C4)/2=0` as its
sole null-control gate and incorrectly returns `SINGLE_LAB_CANDIDATE_ONLY`.
The nominal uncertainty `u_c=1.0269828382207759e-8`; each individual null
control is about 97 times this uncertainty.

## Versioned correction

`tools/cdt_stage0_classifier_v2.py` preserves the original signal,
reversal, missing-configuration and exclusion behavior, but requires both
`abs(mean(C3)) < 2*u_c` **and** `abs(mean(C4)) < 2*u_c`.
The legacy combined `null_estimator` is retained for audit only; new fields
`null_control_pass` and `null_controls_pass` expose separate gate outcomes.
This corrects cross-control cancellation, but **does not** establish that
within-configuration drift/systematic effects cannot cancel in the mean.

## Verification

Run from repository root:

```sh
python3 -m unittest discover -s tests -p 'test_cdt_stage0_classifier_v2.py' -v
```

The regression suite reads the original locked v1 source fingerprint,
checks its unchanged SHA-256 and `NOT_EXECUTED` status, tests clean candidates,
same-sign/non-reversing candidates, low signal, excluded outliers, missing
configurations, one-sided and opposite-sign contaminated controls, and all
49 combinations of seven discrete null-control values.

## Boundary

`SINGLE_LAB_CANDIDATE_ONLY` is a synthetic classification, never a physical
measurement, discovery, or replication. V2 is an isolated candidate algorithm,
not an amendment to or execution of the frozen 2026-07-12 preregistration.
Any actual experiment requires its own documented pre-run lock and calibration.
