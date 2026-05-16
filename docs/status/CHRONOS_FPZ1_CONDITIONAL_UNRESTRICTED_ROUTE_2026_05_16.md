# Chronos FPz1 conditional unrestricted route

Status: CONDITIONAL_UNRESTRICTED_ROUTE_ONLY

## Formalized conditional route

The Lean module proves:

- `rateSpectrumIsolation_and_lowerEnvelope_to_quantitativeUnrestricted`
- `fpz1_conditional_unrestricted_route`

## Required hypotheses

The unrestricted route requires:

- `RateSpectrumIsolation`
- `EntropyFaithfulLowerEnvelope`
- `DepthBridgeUnrestricted`

## Boundary

This is a conditional composition theorem only.

It does not prove:

- RateSpectrumIsolation
- EntropyFaithfulLowerEnvelope
- DepthBridgeUnrestricted
- unrestricted UniversalFiberEntropyGap
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem
