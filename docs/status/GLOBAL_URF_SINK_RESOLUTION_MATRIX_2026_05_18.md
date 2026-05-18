# Global URF Sink Resolution Matrix

Status: `SINK_RESOLUTION_MATRIX_ONLY`

Global verdict preserved: `OPEN`

This file converts the ranked next-level targets into an executable resolution matrix.

Resolution rule:

`Every open sink must exit by either an explicit conditional closure theorem under named hypotheses or a machine-checkable countermodel schema.`

## Matrix

| Rank | Sink | Closure exit | Countermodel exit |
|---:|---|---|---|
| 1 | `uniform_positive_mass_or_countermodel` | `UniformPositiveFiberMassFloor` | `NoUniformPositiveFiberMassFloorCountermodel` |
| 2 | `domain_lift_from_finite_support` | `FiniteSupportToAdmissibleDomainLift` | `FiniteSupportLiftFailureCountermodel` |
| 3 | `countermodel_or_closure_dichotomy` | `SinkClosureCertificate` | `SinkCountermodelCertificate` |

## Weakest next formal object

`UniformPositiveFiberMassFloor`

Minimal form:

`For the intended admissible domain D, prove exists epsilon > 0 such that every admissible fiber mass is at least epsilon.`

Alternative countermodel:

`Construct an admissible sequence whose positive fiber masses tend to 0.`

## Boundary

Does not prove:

- uniform positive fiber-mass floor
- finite-support-to-admissible-domain lift
- unrestricted `UniversalFiberEntropyGap`
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem
