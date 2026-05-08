import Chronos.Frontier.RealChronosAdmissible

namespace Chronos.Frontier.IntendedChronosAdmissibility

open Chronos.Frontier.RegisteredNFDomination
open Chronos.Frontier.CarrierRegistryExhaustivenessBridge
open Chronos.Frontier.RealChronosAdmissible

structure ChronosCarrierData where
  arity : Nat
  stratum : Nat
  index : Nat
  deriving DecidableEq, Repr

def signatureOf (C : ChronosCarrierData) : ChronosCarrierSignature :=
  {
    arity := C.arity
    stratum := C.stratum
    index := C.index
  }

def representative (sig : ChronosCarrierSignature) : ChronosCarrierData :=
  {
    arity := sig.arity
    stratum := sig.stratum
    index := sig.index
  }

@[simp]
theorem rep_sig_roundtrip (C : ChronosCarrierData) :
    representative (signatureOf C) = C := by
  cases C
  rfl

def ChronosRegistry : CarrierRegistry ChronosCarrierData :=
  { registered := fun _ => True }

def ChronosTraceFamily : TraceFamily ChronosCarrierData :=
  { Trace := fun C b lam => Fin (C.arity.succ + b + lam) }

def IntendedChronosCarrier (C : ChronosCarrierData) : Prop :=
  0 < C.arity ∧ C.index ≤ C.arity + C.stratum

theorem every_intended_is_admissible
    (C : ChronosCarrierData)
    (_hC : IntendedChronosCarrier C) :
    RealChronosAdmissiblePredicate ChronosRegistry ChronosTraceFamily C := by
  refine ⟨?_⟩
  exact {
    sig := signatureOf C
    rep := representative (signatureOf C)
    rep_registered := trivial
    encode := fun _ _ x => x
    encode_injective := by
      intro b lam x y hxy
      exact hxy
  }

theorem intended_chronos_carrier_implies_carrier_registry_exhaustive :
    CarrierRegistryExhaustive
      ChronosRegistry ChronosTraceFamily IntendedChronosCarrier := by
  intro C hC
  rcases every_intended_is_admissible C hC with ⟨ha⟩
  refine ⟨ha.rep, ha.rep_registered, ?_⟩
  refine ⟨ha.encode, ?_⟩
  exact ha.encode_injective

theorem intended_chronos_carrier_implies_reg_snf :
    RegSNF ChronosRegistry ChronosTraceFamily IntendedChronosCarrier := by
  exact carrier_registry_exhaustiveness_implies_reg_snf
    ChronosRegistry ChronosTraceFamily IntendedChronosCarrier
    intended_chronos_carrier_implies_carrier_registry_exhaustive

end Chronos.Frontier.IntendedChronosAdmissibility
