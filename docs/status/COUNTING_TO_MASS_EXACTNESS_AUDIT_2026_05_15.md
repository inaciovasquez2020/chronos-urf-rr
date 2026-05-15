# Counting-to-Mass Exactness Audit — 2026-05-15

## Target

FiberMassBalance from CountingFiberSeparation.

## Audit result

The repository currently proves CountingFiberSeparationFromNonProp and FiberMassBalanceFromNonProp from the same NonPropFinalCarrierInvariant.

It does not currently prove FiberMassBalanceFromNonProp from CountingFiberSeparationFromNonProp alone.

## Current route

NonPropFinalCarrierInvariant
→ CountingFiberSeparationFromNonProp

NonPropFinalCarrierInvariant
→ FiberMassBalanceFromNonProp

CountingFiberSeparationFromNonProp + FiberMassBalanceFromNonProp
→ UniversalFiberEntropyGapFromNonProp

## Weakest missing lemma

For every NonPropFinalCarrierInvariant I:

CountingFiberSeparationFromNonProp I
→ FiberMassBalanceFromNonProp I

## Equivalent repair path

Strengthen CountingFiberSeparationWitness so that it carries exactly the entropy-mass data needed to construct FiberMassBalanceWitness.

## Boundary

This audit does not prove:
- CountingFiberSeparationToFiberMassBalance
- FiberMassBalance from counting alone
- UniversalFiberEntropyGap
- unrestricted Chronos-RR
- unrestricted H4.1/FGL
- P vs NP
- any Clay problem
