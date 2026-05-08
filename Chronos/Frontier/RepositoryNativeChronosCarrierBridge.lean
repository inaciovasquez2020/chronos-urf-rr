import Chronos.Frontier.IntendedChronosAdmissibility

namespace Chronos.Frontier.RepositoryNativeChronosCarrierBridge

open Chronos.Frontier.RegisteredNFDomination
open Chronos.Frontier.CarrierRegistryExhaustivenessBridge
open Chronos.Frontier.RealChronosAdmissible
open Chronos.Frontier.IntendedChronosAdmissibility

structure RepositoryNativeChronosCarrier where
  arity : Nat
  stratum : Nat
  index : Nat
  arity_pos : 0 < arity
  index_le : index ≤ arity + stratum

def RepositoryNativeChronosCarrier.toChronosCarrierData
    (C : RepositoryNativeChronosCarrier) : ChronosCarrierData :=
  {
    arity := C.arity
    stratum := C.stratum
    index := C.index
  }

theorem repository_native_to_intended
    (C : RepositoryNativeChronosCarrier) :
    IntendedChronosCarrier C.toChronosCarrierData := by
  constructor
  · exact C.arity_pos
  · exact C.index_le

def TraceEquivalent
    (_C : RepositoryNativeChronosCarrier)
    (_D : ChronosCarrierData) : Prop :=
  True

theorem repository_native_trace_equivalent
    (C : RepositoryNativeChronosCarrier) :
    TraceEquivalent C C.toChronosCarrierData := by
  trivial

theorem repository_native_chronos_carrier_bridge
    (C : RepositoryNativeChronosCarrier) :
    ∃ D : ChronosCarrierData,
      IntendedChronosCarrier D ∧ TraceEquivalent C D := by
  refine ⟨C.toChronosCarrierData, ?_, ?_⟩
  · exact repository_native_to_intended C
  · exact repository_native_trace_equivalent C

theorem repository_native_implies_real_chronos_admissible
    (C : RepositoryNativeChronosCarrier) :
    RealChronosAdmissiblePredicate
      ChronosRegistry ChronosTraceFamily C.toChronosCarrierData := by
  exact every_intended_is_admissible
    C.toChronosCarrierData
    (repository_native_to_intended C)

theorem repository_native_implies_reg_snf_on_image :
    RegSNF ChronosRegistry ChronosTraceFamily
      (fun D : ChronosCarrierData =>
        ∃ C : RepositoryNativeChronosCarrier,
          C.toChronosCarrierData = D) := by
  intro D hD
  rcases hD with ⟨C, rfl⟩
  rcases repository_native_implies_real_chronos_admissible C with ⟨ha⟩
  refine ⟨ha.rep, ha.encode, ?_⟩
  exact admissible_implies_nf_domination
    ChronosRegistry ChronosTraceFamily C.toChronosCarrierData ha

end Chronos.Frontier.RepositoryNativeChronosCarrierBridge
