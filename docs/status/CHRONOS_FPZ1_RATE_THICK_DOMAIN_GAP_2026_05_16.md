# Chronos FPz1 rate-thick domain gap

Status: RATE_THICK_DOMAIN_GAP_CONDITIONAL_ONLY

## Formalized surface

The Lean module defines:

- `RateThickDomain`
- `EntropyFaithfulLowerEnvelopeAt`
- `EntropyFaithfulLowerEnvelope`
- `RateDependentUniversalFiberEntropyGap`

The Lean module proves:

- `rateThickDomain_positive_rate_isolated`
- `entropyFaithfulLowerEnvelopeAt_to_rateDependentUniversalFiberEntropyGap`
- `entropyFaithfulLowerEnvelope_to_rateDependentUniversalFiberEntropyGap`

## Unrestricted gap status

The unrestricted UniversalFiberEntropyGap is false/open.

It is false under the inverse-rate obstruction pattern already isolated by `InverseNatRateSequence`.

Without a repository-native proof that Chronos-admissible objects satisfy the inverse-rate obstruction pattern, the unrestricted UniversalFiberEntropyGap remains open.

## Boundary

This is a rate-thick conditional bridge only.

It does not prove:

- unrestricted RateSpectrumIsolation
- EntropyFaithfulLowerEnvelope
- unrestricted UniversalFiberEntropyGap
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem
