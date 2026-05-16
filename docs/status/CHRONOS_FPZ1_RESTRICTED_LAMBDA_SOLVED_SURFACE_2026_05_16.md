# Chronos FPz1 restricted lambda solved surface

Status: RESTRICTED_LAMBDA_ROUTE_SOLVED_SURFACE_ONLY

## Closed surface

For fixed lambda greater than zero, the lambda-thick admissible domain gives restricted rate-spectrum isolation by definition.

The Lean file proves:

- `restrictedRateSpectrumIsolation`
- `lowerEnvelope_to_quantitativeLambda`
- `fpz1_restricted_lambda_route`

## Required hypotheses

The restricted lambda route requires:

- `EntropyFaithfulLowerEnvelope`
- `DepthBridgeLambda`

## Boundary

This is a restricted lambda-domain solved surface only.

It does not prove:

- unrestricted RateSpectrumIsolation
- unrestricted UniformRateGap
- unrestricted UniversalFiberEntropyGap
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem
