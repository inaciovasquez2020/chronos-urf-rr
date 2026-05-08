import Chronos.Frontier.TraceEquivalentCardinality

namespace Chronos.Frontier.TraceEquivalentEquiv

open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.RepositoryNativeChronosCarrierBridge
open Chronos.Frontier.TraceEquivalentCardinality

def NativeTrace
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) : Type :=
  Fin (nativeTraceSize C b lam)

def ChronosTrace
    (D : ChronosCarrierData)
    (b lam : Nat) : Type :=
  Fin (chronosTraceSize D b lam)

def TraceEquivalentEquiv
    (C : RepositoryNativeChronosCarrier)
    (D : ChronosCarrierData) : Prop :=
  ∀ b lam : Nat, Nonempty (NativeTrace C b lam ≃ ChronosTrace D b lam)

theorem repository_native_trace_equivalent_equiv
    (C : RepositoryNativeChronosCarrier) :
    TraceEquivalentEquiv C C.toChronosCarrierData := by
  intro b lam
  exact ⟨Equiv.refl _⟩

theorem repository_native_bridge_with_equiv_trace_equivalence
    (C : RepositoryNativeChronosCarrier) :
    ∃ D : ChronosCarrierData,
      IntendedChronosCarrier D ∧ TraceEquivalentEquiv C D := by
  refine ⟨C.toChronosCarrierData, ?_, ?_⟩
  · exact repository_native_to_intended C
  · exact repository_native_trace_equivalent_equiv C

end Chronos.Frontier.TraceEquivalentEquiv
