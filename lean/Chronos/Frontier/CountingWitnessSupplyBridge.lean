import Chronos.Frontier.CountingExtractionInternalStructure

namespace Chronos.Frontier

/--
Bridge from an unstructured counting-separation proposition into the structured
witness interface introduced by CountingExtractionInternalStructure.
-/
structure CountingWitnessSupplyBridgeInput where
  rawCountingFiberSeparationFromNonProp : Prop
  internal : CountingExtractionInternalStructureInput
  supply :
    rawCountingFiberSeparationFromNonProp →
      SharedCountingExtractionWitnessExists internal

/--
The exact remaining witness-supply obligation.
-/
def RawCountingSeparationSuppliesSharedWitness
    (I : CountingWitnessSupplyBridgeInput) : Prop :=
  I.rawCountingFiberSeparationFromNonProp →
    SharedCountingExtractionWitnessExists I.internal

theorem raw_counting_separation_supplies_shared_witness
    (I : CountingWitnessSupplyBridgeInput) :
    RawCountingSeparationSuppliesSharedWitness I :=
  I.supply

/--
Once raw counting separation supplies the shared witness, it also supplies the
structured NonProp invariant.
-/
def RawCountingSeparationSuppliesStructuredNonPropInvariant
    (I : CountingWitnessSupplyBridgeInput) : Prop :=
  I.rawCountingFiberSeparationFromNonProp →
    StructuredNonPropInvariant I.internal

theorem raw_counting_separation_supplies_structured_nonprop_invariant
    (I : CountingWitnessSupplyBridgeInput) :
    RawCountingSeparationSuppliesStructuredNonPropInvariant I := by
  intro hRaw
  exact shared_witness_to_structured_nonprop_invariant I.internal
    (raw_counting_separation_supplies_shared_witness I hRaw)

end Chronos.Frontier
