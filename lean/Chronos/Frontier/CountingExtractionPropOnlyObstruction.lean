import Chronos.Frontier.CountingSeparationNonPropInvariantExtraction

namespace Chronos.Frontier

/--
Prop-only counting extraction would assert that an arbitrary counting
separation proposition implies an arbitrary NonProp invariant proposition.
-/
def PropOnlyCountingSeparationExtractionClaim : Prop :=
  ∀ (countingFiberSeparationFromNonProp nonPropInvariant : Prop),
    countingFiberSeparationFromNonProp → nonPropInvariant

/--
The Prop-only extraction claim is false.

Counterexample:
- countingFiberSeparationFromNonProp := True
- nonPropInvariant := False
-/
theorem prop_only_counting_separation_extraction_obstructed :
    ¬ PropOnlyCountingSeparationExtractionClaim := by
  intro h
  exact h True False True.intro

/--
Weakest admissible new ingredient: an actual extraction witness from counting
separation to the NonProp invariant.
-/
structure CountingSeparationExtractionWitnessInput where
  countingFiberSeparationFromNonProp : Prop
  nonPropInvariant : Prop
  witness : countingFiberSeparationFromNonProp → nonPropInvariant

def CountingSeparationExtractionWitnessSufficient
    (I : CountingSeparationExtractionWitnessInput) : Prop :=
  I.countingFiberSeparationFromNonProp → I.nonPropInvariant

theorem counting_separation_extraction_witness_sufficient
    (I : CountingSeparationExtractionWitnessInput) :
    CountingSeparationExtractionWitnessSufficient I :=
  I.witness

end Chronos.Frontier
