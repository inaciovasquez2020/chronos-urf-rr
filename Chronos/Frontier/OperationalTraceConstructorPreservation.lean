import Chronos.Frontier.ConcreteExportSemanticPreservation
import Chronos.Frontier.CanonicalRepositoryNativeSemantics

namespace Chronos.Frontier.OperationalTraceConstructorPreservation

open Chronos.Frontier.ConcreteExportSemanticPreservation
open Chronos.Frontier.CanonicalRepositoryNativeSemantics

def OperationalTraceConstructorPreservation : Prop :=
  ConcreteExportSemanticPreservation ∧
  ∀ {C : RepositoryNativeChronosCarrier} {b lam : Nat}
      (x : OperationalTraceSyntax C b lam),
    SemanticallyEquivalent (OperationalTraceSyntax.lift x) x ∧
    SemanticallyEquivalent (OperationalTraceSyntax.relabel x) x

theorem operational_trace_constructor_preservation :
    OperationalTraceConstructorPreservation := by
  constructor
  · exact concrete_export_semantic_preservation
  · intro C b lam x
    exact canonical_repository_native_semantics_preserves_erasing_constructors
      canonical_repository_native_semantics x

end Chronos.Frontier.OperationalTraceConstructorPreservation
