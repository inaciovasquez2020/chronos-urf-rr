# Counting Extraction Internal Structure

Date: 2026-05-15

Status: STRUCTURED_EXTRACTION_SURFACE_CLOSED

## Internal Structure

The rejected Prop-only route is replaced by a structured witness interface.

```lean
structure CountingExtractionInternalStructureInput where
  Witness : Type
  ValidExtractionWitness : Witness → Prop
Structured Counting Separation
StructuredCountingFiberSeparationFromNonProp I :=
  ∃ W : I.Witness, I.ValidExtractionWitness W
Structured NonProp Invariant
StructuredNonPropInvariant I :=
  ∃ W : I.Witness, I.ValidExtractionWitness W
Shared Witness
SharedCountingExtractionWitnessExists I :=
  ∃ W : I.Witness, I.ValidExtractionWitness W
Closed Surface
StructuredCountingFiberSeparationFromNonProp I →
  SharedCountingExtractionWitnessExists I
SharedCountingExtractionWitnessExists I →
  StructuredNonPropInvariant I
StructuredCountingFiberSeparationFromNonProp I →
  StructuredNonPropInvariant I
Boundary
This does not prove raw Prop-only extraction.
It does not prove:
ordinary CountingFiberSeparationFromNonProp alone implies FiberMassBalanceFromNonProp
an unstructured counting separation proposition supplies this witness
unrestricted UniversalFiberEntropyGap
unrestricted Chronos-RR
unrestricted H4.1/FGL
P vs NP
any Clay-problem closure
