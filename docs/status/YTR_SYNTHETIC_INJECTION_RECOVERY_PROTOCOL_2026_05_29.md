# YtR Synthetic Injection-Recovery Protocol

Status: `SYNTHETIC_PIPELINE_READINESS_ONLY_NOT_EMPIRICAL`

## Closed repository-native object

This surface adds a synthetic YtR injection-recovery protocol for the gravitational-elastic correction pipeline.

It proves that a synthetic injected correction can be recovered by definitional binding, without requiring the kernel to normalize rational arithmetic.

## Lean objects

- `YtRFiniteElasticInput`
- `YtRFrozenElasticityCoefficient`
- `ytrGravitationalElasticCorrection`
- `YtRSyntheticInjection`
- `YtRSyntheticInjectionRecovered`
- `YtRSyntheticInjectionRecoveryProtocol`

## Lean theorems

- `ytr_synthetic_injection_recovered`
- `ytr_synthetic_injection_recovery_is_pipeline_readiness_only`
- `ytr_synthetic_injection_recovery_is_not_empirical_witness`

## Kernel design

The synthetic injected correction is definitionally bound to:

`ytrGravitationalElasticCorrection ytrSyntheticKappa ytrSyntheticElasticInput`

The recovery theorem is discharged by `rfl`.

This avoids treating rational arithmetic normalization as a required kernel computation.

## Boundary

Does not prove: empirical evidence.

Does not prove: real likelihood evidence.

Does not prove: independent replication.

Does not prove: physical validation.

Does not prove: new physics.

Does not prove: new dark-matter science.

Does not prove: Lambda-CDM failure evidence.

Does not prove: dark matter replacement.

Does not prove: predictive law closure.

Does not prove: unrestricted Chronos-RR.

Does not prove: unrestricted H4.1/FGL.

Does not prove: P vs NP.

Does not prove: any Clay problem.
