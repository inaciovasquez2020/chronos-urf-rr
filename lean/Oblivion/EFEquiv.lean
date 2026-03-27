universe u

structure Graph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

structure EFState (G : Graph) (t : Nat) where
  pebbles : Fin t → G.V

class RadiusRCode (G : Graph) where
  code : Nat → Nat → EFState G · → Nat

def preservesCodeType
  {G₀ G₁ : Graph}
  [RadiusRCode G₀] [RadiusRCode G₁]
  (R t : Nat)
  (s₀ : EFState G₀ t)
  (s₁ : EFState G₁ t) : Prop :=
  RadiusRCode.code (G := G₀) R t s₀ = RadiusRCode.code (G := G₁) R t s₁

def DuplicatorWinsAt
  {G₀ G₁ : Graph}
  [RadiusRCode G₀] [RadiusRCode G₁] :
  Nat → Nat → Prop
| R, 0 => True
| R, t + 1 =>
    (∀ s₀ : EFState G₀ t, ∀ s₁ : EFState G₁ t,
      preservesCodeType R t s₀ s₁ →
        (∀ v : G₀.V, ∃ w : G₁.V,
          preservesCodeType R (t + 1)
            ⟨fun i => if h : i.val < t then s₀.pebbles ⟨i.val, h⟩ else v⟩
            ⟨fun i => if h : i.val < t then s₁.pebbles ⟨i.val, h⟩ else w⟩) ∧
        (∀ w : G₁.V, ∃ v : G₀.V,
          preservesCodeType R (t + 1)
            ⟨fun i => if h : i.val < t then s₀.pebbles ⟨i.val, h⟩ else v⟩
            ⟨fun i => if h : i.val < t then s₁.pebbles ⟨i.val, h⟩ else w⟩))
    ∧ DuplicatorWinsAt R t

def FO_equiv
  {G₀ G₁ : Graph}
  [RadiusRCode G₀] [RadiusRCode G₁]
  (R k : Nat) : Prop :=
  DuplicatorWinsAt (G₀ := G₀) (G₁ := G₁) R k
