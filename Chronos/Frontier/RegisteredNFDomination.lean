namespace Chronos.Frontier.RegisteredNFDomination

universe u v

structure CarrierRegistry (Carrier : Type u) where
  registered : Carrier → Prop

structure TraceFamily (Carrier : Type u) where
  Trace : Carrier → Nat → Nat → Type v

def DominatesVia
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (C r : Carrier)
    (phi : ∀ b lam : Nat, T.Trace C b lam → T.Trace r b lam) : Prop :=
  registry.registered r ∧
  ∀ b lam : Nat, Function.Injective (phi b lam)

theorem dominated_by_registered_nf
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (C r : Carrier)
    (hr : registry.registered r)
    (phi : ∀ b lam : Nat, T.Trace C b lam → T.Trace r b lam)
    (hphi : ∀ b lam : Nat, Function.Injective (phi b lam)) :
    DominatesVia registry T C r phi := by
  constructor
  · exact hr
  · exact hphi

theorem registered_identity_via_nf_domination
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (C : Carrier)
    (hC : registry.registered C) :
    DominatesVia registry T C C (fun _ _ x => x) := by
  exact dominated_by_registered_nf registry T C C hC
    (fun _ _ x => x)
    (fun _ _ x y hxy => hxy)

end Chronos.Frontier.RegisteredNFDomination
