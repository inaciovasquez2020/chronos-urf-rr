# Refinement Bandwidth Principle

## Statement

Let A be a refinement algorithm operating on structures of size n using FO^k-local rules.

Then the mutual information gained by a single refinement step is bounded by a constant depending only on k and the degree bound Δ.

## Formal Bound

Let I_t denote the information gained at step t.

Then

I_t ≤ C(k,Δ)

for some constant C(k,Δ).

## Interpretation

Local refinement algorithms can only observe bounded-radius neighborhoods.

Thus each refinement step can reveal only bounded information about the global structure.

## Consequence

If the initial uncertainty of the configuration space satisfies

H ≥ Ω(n),

then resolving that uncertainty requires

t ≥ Ω(n)

refinement steps.

## Role in Chronos

This principle provides the information-theoretic explanation for the Chronos Wall.
