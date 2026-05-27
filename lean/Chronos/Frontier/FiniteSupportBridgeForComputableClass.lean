import Chronos.Frontier.ComputableFiniteAdmissibleClass

namespace Chronos
namespace Frontier

/--
A finite-support bridge certificate for a computable finite admissible class.

This is the weakest theorem-level finite-support bridge: the comparison is
proved from explicit certificate data. It does not construct the certificate
for every computable finite admissible class and does not imply any
unrestricted bridge.
-/
structure FiniteSupportBridgeCertificate
    (X : ComputableFiniteAdmissibleClass) where
  semantic_rank_le_entropy_gap :
    SemanticRankRate X ≤ FiberEntropyGap X

theorem finite_support_bridge_from_certificate
    (X : ComputableFiniteAdmissibleClass)
    (h : FiniteSupportBridgeCertificate X) :
    SemanticRankRate X ≤ FiberEntropyGap X := by
  exact h.semantic_rank_le_entropy_gap

theorem finite_support_bridge_preserves_finite_support
    (X : ComputableFiniteAdmissibleClass)
    (_h : FiniteSupportBridgeCertificate X) :
    X.objectCount > 0 := by
  exact X.finite_support

/--
The next nontrivial missing theorem is certificate supply:
every admissible computable finite class must admit a bridge certificate.
-/
def FiniteSupportBridgeCertificateSupply : Prop :=
  ∀ X : ComputableFiniteAdmissibleClass,
    X.admissible → FiniteSupportBridgeCertificate X

theorem finite_support_bridge_from_supply
    (supply : FiniteSupportBridgeCertificateSupply)
    (X : ComputableFiniteAdmissibleClass)
    (hX : X.admissible) :
    SemanticRankRate X ≤ FiberEntropyGap X := by
  exact finite_support_bridge_from_certificate X (supply X hX)

end Frontier
end Chronos
