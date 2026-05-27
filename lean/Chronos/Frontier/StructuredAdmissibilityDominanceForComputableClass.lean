import Chronos.Frontier.CertificateSupplyLawForComputableClass

namespace Chronos
namespace Frontier

/--
Structured admissibility for a computable finite admissible class.

This strengthens opaque `X.admissible : Prop` by carrying the exact
rank/entropy dominance datum needed for the finite-support bridge law.
-/
structure StructuredAdmissibilityDominance
    (X : ComputableFiniteAdmissibleClass) where
  admissible_witness : X.admissible
  rank_entropy_dominance :
    SemanticRankRate X ≤ FiberEntropyGap X

theorem structured_admissibility_supplies_bridge
    (X : ComputableFiniteAdmissibleClass)
    (h : StructuredAdmissibilityDominance X) :
    SemanticRankRate X ≤ FiberEntropyGap X := by
  exact h.rank_entropy_dominance

/--
A strengthened intrinsic bridge law: every admissible computable finite class
with structured admissibility dominance satisfies the finite-support bridge.
-/
def StructuredFiniteSupportBridgeLaw : Prop :=
  ∀ X : ComputableFiniteAdmissibleClass,
    StructuredAdmissibilityDominance X →
      SemanticRankRate X ≤ FiberEntropyGap X

theorem structured_finite_support_bridge_law :
    StructuredFiniteSupportBridgeLaw := by
  intro X h
  exact structured_admissibility_supplies_bridge X h

/--
If raw admissibility can be lifted to structured admissibility dominance,
then the explicit finite-support bridge law follows.
-/
def RawToStructuredAdmissibilityDominance : Prop :=
  ∀ X : ComputableFiniteAdmissibleClass,
    X.admissible → StructuredAdmissibilityDominance X

theorem finite_support_bridge_law_from_raw_to_structured
    (lift : RawToStructuredAdmissibilityDominance) :
    FiniteSupportBridgeLawForComputableClass := by
  intro X hX
  exact (lift X hX).rank_entropy_dominance

theorem certificate_supply_from_raw_to_structured
    (lift : RawToStructuredAdmissibilityDominance) :
    FiniteSupportBridgeCertificateSupply := by
  exact certificate_supply_from_finite_support_bridge_law
    (finite_support_bridge_law_from_raw_to_structured lift)

/--
The remaining theorem-level obstruction is the raw-to-structured lift.
-/
def RawToStructuredAdmissibilityDominanceProblem : Prop :=
  RawToStructuredAdmissibilityDominance

end Frontier
end Chronos
