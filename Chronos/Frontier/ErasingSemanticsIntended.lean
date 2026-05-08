import Chronos.Frontier.OperationalTraceSemanticInterpretation

namespace Chronos.Frontier.ErasingSemanticsIntended

open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.OperationalTraceSyntax
open Chronos.Frontier.OperationalTraceSemanticInterpretation

structure ErasingSemanticsIntended : Prop where
  lift_preserved :
    ∀ {C : RepositoryNativeChronosCarrier}
      {b lam : Nat}
      (x : OperationalTraceSyntax C b lam),
      SemanticallyEquivalent (OperationalTraceSyntax.lift x) x
  relabel_preserved :
    ∀ {C : RepositoryNativeChronosCarrier}
      {b lam : Nat}
      (x : OperationalTraceSyntax C b lam),
      SemanticallyEquivalent (OperationalTraceSyntax.relabel x) x

theorem erasing_semantics_intended :
    ErasingSemanticsIntended := by
  constructor
  · intro C b lam x
    exact lift_semantics_preserved x
  · intro C b lam x
    exact relabel_semantics_preserved x

theorem erasing_semantics_preservation_pair
    (h : ErasingSemanticsIntended)
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    SemanticallyEquivalent (OperationalTraceSyntax.lift x) x ∧
    SemanticallyEquivalent (OperationalTraceSyntax.relabel x) x := by
  exact ⟨h.lift_preserved x, h.relabel_preserved x⟩

end Chronos.Frontier.ErasingSemanticsIntended
