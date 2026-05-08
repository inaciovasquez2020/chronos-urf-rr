import Chronos.Frontier.OperationalTraceSyntax

namespace Chronos.Frontier.OperationalTraceNormalizationLaws

open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.RepositoryNativeTraceSyntax
open Chronos.Frontier.OperationalTraceSyntax

theorem normalize_lift
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    normalize (OperationalTraceSyntax.lift x) = normalize x := by
  rfl

theorem normalize_relabel
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    normalize (OperationalTraceSyntax.relabel x) = normalize x := by
  rfl

theorem normalize_lift_relabel
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    normalize (OperationalTraceSyntax.lift (OperationalTraceSyntax.relabel x))
      = normalize x := by
  rfl

theorem normalize_relabel_lift
    {C : RepositoryNativeChronosCarrier}
    {b lam : Nat}
    (x : OperationalTraceSyntax C b lam) :
    normalize (OperationalTraceSyntax.relabel (OperationalTraceSyntax.lift x))
      = normalize x := by
  rfl

end Chronos.Frontier.OperationalTraceNormalizationLaws
