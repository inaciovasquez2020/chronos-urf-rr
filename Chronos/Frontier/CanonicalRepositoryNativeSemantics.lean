import Chronos.Frontier.ErasingSemanticsIntended

namespace Chronos.Frontier.CanonicalRepositoryNativeSemantics

open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.OperationalTraceSyntax
open Chronos.Frontier.OperationalTraceSemanticInterpretation
open Chronos.Frontier.ErasingSemanticsIntended

structure CanonicalRepositoryNativeSemantics : Prop where
  erasing_intended : ErasingSemanticsIntended

theorem erasing_semantics_intended_implies_canonical_repository_native_semantics
    (h : ErasingSemanticsIntended) :
    CanonicalRepositoryNativeSemantics := by
  exact ⟨h⟩

theorem canonical_repository_native_semantics :
    CanonicalRepositoryNativeSemantics := by
  exact erasing_semantics_intended_implies_canonical_repository_native_semantics
    erasing_semantics_intended

theorem canonical_lift_relabel_semantics
    (h : CanonicalRepositoryNativeSemantics)
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    SemanticallyEquivalent (OperationalTraceSyntax.lift x) x ∧
    SemanticallyEquivalent (OperationalTraceSyntax.relabel x) x := by
  exact erasing_semantics_preservation_pair h.erasing_intended x

end Chronos.Frontier.CanonicalRepositoryNativeSemantics
