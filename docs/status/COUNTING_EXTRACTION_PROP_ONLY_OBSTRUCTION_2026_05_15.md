# Counting Extraction Prop-Only Obstruction

Date: 2026-05-15

Status: PROP_ONLY_EXTRACTION_OBSTRUCTED

## Closed Result

The Prop-only extraction claim is false:

```lean
∀ (countingFiberSeparationFromNonProp nonPropInvariant : Prop),
  countingFiberSeparationFromNonProp → nonPropInvariant
Counterexample:
countingFiberSeparationFromNonProp := True
nonPropInvariant := False
Therefore the current Prop-only interface cannot prove the missing extraction lemma without a new witness/invariant ingredient.
Required New Ingredient
A genuine extraction witness:
countingFiberSeparationFromNonProp → nonPropInvariant
Boundary
This does not prove ordinary CountingFiberSeparationFromNonProp alone implies FiberMassBalanceFromNonProp.
It does not prove:
the extraction witness exists
unrestricted UniversalFiberEntropyGap
unrestricted Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay-problem closure
