import Chronos.Frontier.RepositoryNativeChronosCarrierBridge

namespace Chronos.Frontier.TraceEquivalentCardinality

open Chronos.Frontier.IntendedChronosAdmissibility
open Chronos.Frontier.RepositoryNativeChronosCarrierBridge

def nativeTraceSize
    (C : RepositoryNativeChronosCarrier)
    (b lam : Nat) : Nat :=
  C.arity.succ + b + lam

def chronosTraceSize
    (D : ChronosCarrierData)
    (b lam : Nat) : Nat :=
  D.arity.succ + b + lam

def TraceEquivalentCardinality
    (C : RepositoryNativeChronosCarrier)
    (D : ChronosCarrierData) : Prop :=
  ∀ b lam : Nat, nativeTraceSize C b lam = chronosTraceSize D b lam

theorem repository_native_trace_equivalent_cardinality
    (C : RepositoryNativeChronosCarrier) :
    TraceEquivalentCardinality C C.toChronosCarrierData := by
  intro b lam
  rfl

theorem repository_native_bridge_with_cardinality_trace_equivalence
    (C : RepositoryNativeChronosCarrier) :
    ∃ D : ChronosCarrierData,
      IntendedChronosCarrier D ∧ TraceEquivalentCardinality C D := by
  refine ⟨C.toChronosCarrierData, ?_, ?_⟩
  · exact repository_native_to_intended C
  · exact repository_native_trace_equivalent_cardinality C

end Chronos.Frontier.TraceEquivalentCardinality
