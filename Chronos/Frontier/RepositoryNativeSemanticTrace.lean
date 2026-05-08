import Chronos.Frontier.TraceEquivalentEquiv

namespace Chronos.Frontier.RepositoryNativeSemanticTrace

open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.TraceEquivalentCardinality
open Chronos.Frontier.TraceEquivalentEquiv

def RepositoryNativeSemanticTrace
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) : Type :=
  Fin (C.arity.succ + b + lam)

def repositoryNativeSemanticTraceSize
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) : Nat :=
  C.arity.succ + b + lam

theorem repository_native_semantic_trace_size_eq_nativeTraceSize
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) :
    repositoryNativeSemanticTraceSize C b lam = nativeTraceSize C b lam := by
  rfl

def SemanticTraceEquivalent
    (C : RepositoryNativeChronosCarrier)
    (D : ChronosCarrierData) : Prop :=
  ∀ b lam : Nat,
    Nonempty (RepositoryNativeSemanticTrace C b lam ≃ ChronosTrace D b lam)

theorem repository_native_semantic_trace_equivalent
    (C : RepositoryNativeChronosCarrier) :
    SemanticTraceEquivalent C C.toChronosCarrierData := by
  intro b lam
  exact ⟨Equiv.refl _⟩

theorem semantic_trace_equivalent_implies_trace_equivalent_equiv
    (C : RepositoryNativeChronosCarrier)
    (D : ChronosCarrierData)
    (h : SemanticTraceEquivalent C D) :
    TraceEquivalentEquiv C D := by
  intro b lam
  exact h b lam

theorem repository_native_bridge_with_semantic_trace_equivalence
    (C : RepositoryNativeChronosCarrier) :
    ∃ D : ChronosCarrierData,
      IntendedChronosCarrier D ∧ SemanticTraceEquivalent C D := by
  refine ⟨C.toChronosCarrierData, ?_, ?_⟩
  · exact repository_native_to_intended C
  · exact repository_native_semantic_trace_equivalent C

end Chronos.Frontier.RepositoryNativeSemanticTrace
