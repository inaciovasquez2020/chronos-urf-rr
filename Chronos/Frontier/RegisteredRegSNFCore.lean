namespace Chronos.Frontier.RegisteredRegSNFCore

universe u v

structure CarrierRegistry (Carrier : Type u) where
  registered : Carrier → Prop

structure TraceFamily (Carrier : Type u) where
  Trace : Carrier → Nat → Nat → Type v

def RegisteredDominates
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (C r : Carrier) : Prop :=
  registry.registered r ∧
  ∀ b lam : Nat, Function.Injective (fun x : T.Trace C b lam => x)

theorem registered_reg_snf_core
    {Carrier : Type u}
    (registry : CarrierRegistry Carrier)
    (T : TraceFamily Carrier)
    (C : Carrier)
    (hC : registry.registered C) :
    ∃ r : Carrier, RegisteredDominates registry T C r := by
  refine ⟨C, ?_⟩
  constructor
  · exact hC
  · intro b lam x y hxy
    exact hxy

end Chronos.Frontier.RegisteredRegSNFCore
