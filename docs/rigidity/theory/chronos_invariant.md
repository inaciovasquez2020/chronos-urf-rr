# Chronos Invariant

## Definition

Let G be a bounded-degree structure with configuration entropy H(G).

Let a refinement algorithm operate using bounded-radius rules.

Define the Chronos invariant:

    χ(G) = minimal number of refinement steps required to reduce configuration entropy to zero.

## Property

If the entropy reduction per step is bounded by a constant:

    ΔH ≤ O(1),

then the Chronos invariant satisfies

    χ(G) ≥ Ω(H(G)).

## Interpretation

The Chronos invariant measures the intrinsic refinement depth required to resolve the configuration space.

## Role

EntropyDepth(G) = χ(G).

Thus the Chronos invariant provides the invariant formulation of the refinement depth barrier.
