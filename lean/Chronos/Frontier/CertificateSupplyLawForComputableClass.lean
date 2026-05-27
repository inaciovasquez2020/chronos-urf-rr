import Chronos.Frontier.FiniteSupportBridgeForComputableClass

namespace Chronos
namespace Frontier

/--
A bridge law supplying the missing finite-support comparison for every
admissible computable finite class.

This is an explicit law, not an unrestricted proof from the raw fields of
`ComputableFiniteAdmissibleClass`.
-/
def FiniteSupportBridgeLawForComputableClass : Prop :=
  ∀ X : ComputableFiniteAdmissibleClass,
    X.admissible → SemanticRankRate X ≤ FiberEntropyGap X

theorem certificate_supply_from_finite_support_bridge_law
    (law : FiniteSupportBridgeLawForComputableClass) :
    FiniteSupportBridgeCertificateSupply := by
  intro X hX
  exact ⟨law X hX⟩

theorem finite_support_bridge_from_law
    (law : FiniteSupportBridgeLawForComputableClass)
    (X : ComputableFiniteAdmissibleClass)
    (hX : X.admissible) :
    SemanticRankRate X ≤ FiberEntropyGap X := by
  exact finite_support_bridge_from_supply
    (certificate_supply_from_finite_support_bridge_law law) X hX

/--
The remaining nontrivial theorem is to prove this law from intrinsic
admissibility structure rather than assume it as an explicit law.
-/
def IntrinsicFiniteSupportBridgeLawProblem : Prop :=
  FiniteSupportBridgeLawForComputableClass

end Frontier
end Chronos
