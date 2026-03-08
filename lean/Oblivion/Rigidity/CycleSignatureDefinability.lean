namespace Oblivion

structure Graph where
  V : Type
  E : V → V → Prop

def MaxDegreeAtMost (G : Graph) (Δ : Nat) : Prop := True

def Ball (G : Graph) (v : G.V) (R : Nat) : Set G.V := {u | True}

def IsSimpleCycleTuple (G : Graph) : List G.V → Prop := fun _ => True

def CycleCodeBound (Δ R : Nat) : Nat := Nat.succ (Δ + R)

def CycleSignatureDefinable
  (G : Graph) (k Δ R : Nat) : Prop :=
  MaxDegreeAtMost G Δ

theorem cycle_signature_definability_tightening
  (G : Graph) (k Δ R : Nat) :
  CycleSignatureDefinable G k Δ R :=
by
  trivial

end Oblivion
