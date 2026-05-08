import chronos.Frontier.RegisteredNFDomination

namespace Chronos.Frontier.CarrierRegistryExhaustivenessBridge

open Chronos.Frontier.RegisteredNFDomination

universe u v

def CarrierRegistryExhaustive
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (Admissible : Carrier → Prop) : Prop :=
  ∀ C : Carrier, Admissible C →
    ∃ r : Carrier,
      registry.registered r ∧
      ∃ phi : (∀ b lam : Nat, T.Trace C b lam → T.Trace r b lam),
        ∀ b lam : Nat, Function.Injective (phi b lam)

def RegSNF
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (Admissible : Carrier → Prop) : Prop :=
  ∀ C : Carrier, Admissible C →
    ∃ r : Carrier,
      ∃ phi : (∀ b lam : Nat, T.Trace C b lam → T.Trace r b lam),
        DominatesVia registry T C r phi

theorem carrier_registry_exhaustiveness_implies_reg_snf
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (Admissible : Carrier → Prop)
    (hExh : CarrierRegistryExhaustive registry T Admissible) :
    RegSNF registry T Admissible := by
  intro C hC
  rcases hExh C hC with ⟨r, hr, phi, hphi⟩
  refine ⟨r, phi, ?_⟩
  exact dominated_by_registered_nf registry T C r hr phi hphi

end Chronos.Frontier.CarrierRegistryExhaustivenessBridge
