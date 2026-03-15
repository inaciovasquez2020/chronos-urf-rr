# Chronos Information Gradient

## Definition

Let H_t denote the configuration entropy after t refinement steps.

Define the information gradient:

    ∇I = H_t − H_{t+1}

which measures the information extracted by a single refinement step.

## Property

For bounded-locality refinement systems,

    ∇I ≤ O(1).

## Interpretation

Local refinement rules observe only bounded-radius neighborhoods.

Therefore the information extracted from the global configuration per step is bounded.

## Consequence

If the total configuration entropy satisfies

    H_0 ≥ Ω(n),

then resolving the configuration requires

    t ≥ Ω(n)

refinement steps.

## Role in Chronos

The information gradient formalizes the rate limit on entropy reduction that produces the Chronos refinement barrier.
