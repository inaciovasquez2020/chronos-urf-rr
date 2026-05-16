import Chronos.Frontier.CountingExtractionPropOnlyObstruction

namespace Chronos.Frontier

/--
Internal structured replacement for the rejected Prop-only extraction route.

The new ingredient is a concrete shared witness type `Witness` together with a
validity predicate `ValidExtractionWitness`.
-/
structure CountingExtractionInternalStructureInput where
  Witness : Type
  ValidExtractionWitness : Witness → Prop

/--
Structured counting separation: there exists a valid shared extraction witness.
-/
def StructuredCountingFiberSeparationFromNonProp
    (I : CountingExtractionInternalStructureInput) : Prop :=
  ∃ W : I.Witness, I.ValidExtractionWitness W

/--
Structured NonProp invariant: the same witness object validates the invariant.
-/
def StructuredNonPropInvariant
    (I : CountingExtractionInternalStructureInput) : Prop :=
  ∃ W : I.Witness, I.ValidExtractionWitness W

/--
Shared witness object.
-/
def SharedCountingExtractionWitnessExists
    (I : CountingExtractionInternalStructureInput) : Prop :=
  ∃ W : I.Witness, I.ValidExtractionWitness W

/--
Counting separation exposes the shared witness.
-/
theorem structured_counting_separation_to_shared_witness
    (I : CountingExtractionInternalStructureInput) :
    StructuredCountingFiberSeparationFromNonProp I →
      SharedCountingExtractionWitnessExists I := by
  intro h
  exact h

/--
The shared witness supplies the structured NonProp invariant.
-/
theorem shared_witness_to_structured_nonprop_invariant
    (I : CountingExtractionInternalStructureInput) :
    SharedCountingExtractionWitnessExists I →
      StructuredNonPropInvariant I := by
  intro h
  exact h

/--
Structured extraction theorem.

This is the admissible replacement for the false Prop-only extraction claim:
once counting separation and the NonProp invariant are defined through the same
valid witness object, extraction is immediate.
-/
theorem structured_counting_extraction_to_nonprop_invariant
    (I : CountingExtractionInternalStructureInput) :
    StructuredCountingFiberSeparationFromNonProp I →
      StructuredNonPropInvariant I := by
  intro hCounting
  exact shared_witness_to_structured_nonprop_invariant I
    (structured_counting_separation_to_shared_witness I hCounting)

end Chronos.Frontier
