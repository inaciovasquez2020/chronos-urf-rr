import Chronos.Frontier.CarrierRegistryExhaustivenessBridge

namespace Chronos.Frontier.RealChronosAdmissible

open Chronos.Frontier.RegisteredNFDomination
open Chronos.Frontier.CarrierRegistryExhaustivenessBridge

universe u v

structure ChronosCarrierSignature where
  arity : Nat
  stratum : Nat
  index : Nat
  deriving DecidableEq, Repr

structure RealChronosAdmissible
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (C : Carrier) : Type (max u v) where
  sig : ChronosCarrierSignature
  rep : Carrier
  rep_registered : registry.registered rep
  encode : ∀ b lam : Nat, T.Trace C b lam → T.Trace rep b lam
  encode_injective : ∀ b lam : Nat, Function.Injective (encode b lam)

def registeredIsAdmissible
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (C : Carrier)
    (hC : registry.registered C) :
    RealChronosAdmissible registry T C where
  sig := ⟨0, 0, 0⟩
  rep := C
  rep_registered := hC
  encode := fun _ _ x => x
  encode_injective := by
    intro b lam x y hxy
    exact hxy

theorem admissible_implies_nf_domination
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (C : Carrier)
    (ha : RealChronosAdmissible registry T C) :
    DominatesVia registry T C ha.rep ha.encode := by
  exact dominated_by_registered_nf
    registry T C ha.rep ha.rep_registered ha.encode ha.encode_injective

def RealChronosAdmissiblePredicate
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier) : Carrier → Prop :=
  fun C => Nonempty (RealChronosAdmissible registry T C)

theorem real_chronos_admissible_predicate_implies_carrier_registry_exhaustive
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier) :
    CarrierRegistryExhaustive
      registry T (RealChronosAdmissiblePredicate registry T) := by
  intro C hC
  rcases hC with ⟨ha⟩
  refine ⟨ha.rep, ha.rep_registered, ?_⟩
  refine ⟨ha.encode, ?_⟩
  exact ha.encode_injective

theorem real_chronos_admissible_predicate_implies_reg_snf
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier) :
    RegSNF registry T (RealChronosAdmissiblePredicate registry T) := by
  exact carrier_registry_exhaustiveness_implies_reg_snf
    registry T (RealChronosAdmissiblePredicate registry T)
    (real_chronos_admissible_predicate_implies_carrier_registry_exhaustive
      registry T)

theorem registered_carrier_is_real_chronos_admissible
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (C : Carrier)
    (hC : registry.registered C) :
    RealChronosAdmissiblePredicate registry T C := by
  exact ⟨registeredIsAdmissible registry T C hC⟩

end Chronos.Frontier.RealChronosAdmissible
