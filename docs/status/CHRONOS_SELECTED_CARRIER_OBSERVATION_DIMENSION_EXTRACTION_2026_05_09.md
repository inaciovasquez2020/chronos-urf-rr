# Chronos Selected-Carrier Observation Dimension Extraction

STATUS: SELECTED_CARRIER_OBSERVATION_DIMENSION_EXTRACTION_VERIFIED_SURFACE

## Solved object

The theorem

    selected_carrier_observation_dimension_extraction

proves a carrier-indexed selected observation-dimension extraction.

## Model

The extracted bridge uses:

    Lambda := ChronosCarrierData × Nat

so that the observation dimension can depend on carrier data while still fitting the existing DepthBridgeInstance interface:

    ObsDim := fun p => 2 * (p.1.arity.succ + p.2)
    TranscriptDim := fun _ p => p.1.arity.succ + p.2

The verified strict gap uses:

    alpha_num = 1
    alpha_den = 2

and proves:

    2 * TranscriptDim <= (2 - 1) * ObsDim

which reduces to:

    2 * (C.arity.succ + lam) <= 2 * (C.arity.succ + lam)

## Nontriviality

The theorem

    selected_carrier_extracted_observation_nontrivial

records that transcript dimension is not identically zero and observation dimension is not the unit constant placeholder.

## Obstruction retained

The theorem

    selected_carrier_constant_obs_trace_growth_obstruction

proves that the trace-size transcript model cannot satisfy a strict gap against constant observation dimension 1.

## Boundary

This is a carrier-indexed selected observation-dimension extraction only.

It does not assert unrestricted Chronos-RR closure.
It does not assert H4.1/FGL closure.
It does not assert P-vs-NP closure.
It does not assert Clay-problem closure.
It does not assert unrestricted admissible-predicate coverage.
It does not assert universal FiberEntropyGap.
It does not close the original constant-observation selected interface.
