# Observed Rotation Curve Budget Gate Bridge — 2026-05-28

Status: `CONDITIONAL_OBSERVED_RESIDUAL_TO_RESTRICTED_GATE_BRIDGE`.

This surface composes the rational-valued observed rotation residual bridge with the partitioned physical detector gate bridge through a finite natural-number budget layer.

It introduces:

- `PhysicalDetectorFieldWithDynamics`
- `requiredMassFromRotation`
- `physicalGDMBudget`
- `physicalGDMBudget_partitioned_certificate_from_observed_rotation_curve`
- `physicalGDM_observed_rotation_curve_feeds_gate`

The bridge is conditional on two supplied hypotheses:

1. active detector readings are pointwise bounded by the observed GDM budget;
2. each local observed GDM budget satisfies the partitioned capacity bound.

Does not prove: galaxy rotation curve fit, lensing fit, empirical dark-matter replacement, Lambda-CDM refutation, modified-gravity theorem, gravity closure, Chronos-RR, unrestricted H4.1/FGL, P vs NP, or any Clay problem.
