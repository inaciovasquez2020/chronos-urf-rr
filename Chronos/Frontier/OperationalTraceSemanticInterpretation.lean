import Chronos.Frontier.OperationalTraceNormalizationLaws

namespace Chronos.Frontier.OperationalTraceSemanticInterpretation

open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.RepositoryNativeTraceSyntax
open Chronos.Frontier.OperationalTraceSyntax
open Chronos.Frontier.OperationalTraceNormalizationLaws

def OperationalTraceSemantics
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    RepositoryNativeTraceSyntax C b lam :=
  normalize x

def SemanticallyEquivalent
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x y : OperationalTraceSyntax C b lam) : Prop :=
  OperationalTraceSemantics x = OperationalTraceSemantics y

theorem lift_semantics_preserved
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    SemanticallyEquivalent (OperationalTraceSyntax.lift x) x := by
  rfl

theorem relabel_semantics_preserved
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    SemanticallyEquivalent (OperationalTraceSyntax.relabel x) x := by
  rfl

theorem lift_relabel_semantics_preserved
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    SemanticallyEquivalent
      (OperationalTraceSyntax.lift (OperationalTraceSyntax.relabel x)) x := by
  rfl

theorem relabel_lift_semantics_preserved
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    SemanticallyEquivalent
      (OperationalTraceSyntax.relabel (OperationalTraceSyntax.lift x)) x := by
  rfl

end Chronos.Frontier.OperationalTraceSemanticInterpretation
