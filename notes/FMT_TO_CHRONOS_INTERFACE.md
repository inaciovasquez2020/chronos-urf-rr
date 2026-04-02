# Canonical Note: Interface from `cslib-fmt` to the Next URF Layer

## Status

Conditional.

## Purpose

This note records the theorem-level interface from the finite-model-theoretic slice `cslib-fmt` to the next URF layer.

## Formalized input from `cslib-fmt`

The `FMT` slice provides:

1. A local type layer.
2. An indistinguishability/game-facing locality layer.
3. A graph/distance substrate for bounded-radius reasoning.
4. A factorization/nonfactorization interface.
5. A local/global bridge scaffold.

## Interface claim

If an invariant is exhibited at the `FMT.Invariants` level as not factoring through local types, then any downstream URF layer that treats local-type factorization as sufficient must record a non-collapse obstruction at the interface boundary.

## Consequence for the next layer

The Chronos / EntropyDepth layer may consume the `FMT` output only through the following conditional rule:

- local-type collapse available  => no obstruction certified by `FMT`;
- nonfactorization witness available => obstruction must be preserved by the next layer.

## Precise status

This note is canonical interface documentation.
It is not yet a complete formal proof of the entire downstream URF implication chain.
Therefore the interface is classified as conditional in `URF_STATUS.md`.
