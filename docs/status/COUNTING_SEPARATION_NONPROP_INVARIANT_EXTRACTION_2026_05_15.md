# Counting Separation NonProp Invariant Extraction

Date: 2026-05-15

Status: THEOREM_TARGET_ISOLATED

## Minimal Missing Lemma

CountingFiberSeparationFromNonProp supplies the NonProp invariant required by CountingToMassUnderNonPropInvariant.

## Closed Surface

Given an extraction map

```lean
countingFiberSeparationFromNonProp → nonPropInvariant
and the already-isolated bridge
countingFiberSeparationFromNonProp →
nonPropInvariant →
fiberMassBalanceFromNonProp
the composed bridge closes:
countingFiberSeparationFromNonProp → fiberMassBalanceFromNonProp
Boundary
This does not prove ordinary CountingFiberSeparationFromNonProp alone implies FiberMassBalanceFromNonProp unless the extraction hypothesis is supplied.
It does not prove:
unrestricted UniversalFiberEntropyGap
unrestricted Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay-problem closure
