# Counting Witness Supply Bridge

Date: 2026-05-15

Status: CONDITIONAL_WITNESS_SUPPLY_BRIDGE_CLOSED

## Minimal Missing Lemma

```lean
rawCountingFiberSeparationFromNonProp →
  SharedCountingExtractionWitnessExists internal
Conditional Input
structure CountingWitnessSupplyBridgeInput where
  rawCountingFiberSeparationFromNonProp : Prop
  internal : CountingExtractionInternalStructureInput
  supply :
    rawCountingFiberSeparationFromNonProp →
      SharedCountingExtractionWitnessExists internal
Closed Surface
RawCountingSeparationSuppliesSharedWitness I
RawCountingSeparationSuppliesStructuredNonPropInvariant I
Boundary
Conditional: this requires a supply map from raw counting separation to the shared witness.
This does not prove:
the supply map exists
raw Prop-only extraction
ordinary CountingFiberSeparationFromNonProp alone implies FiberMassBalanceFromNonProp
unrestricted UniversalFiberEntropyGap
unrestricted Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay-problem closure
