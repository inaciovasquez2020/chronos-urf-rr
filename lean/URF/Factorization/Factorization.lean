import Mathlib

variable {G : Type} {α : Type}

def LocalType (G : Type) (k R : Nat) := G

def FactorsThrough (η : G → α) (I : G → α) : Prop :=
∃ f : α → α, ∀ x, I x = f (η x)

theorem factorsThrough_id (η : G → α) :
FactorsThrough η (fun x => η x) := by
refine ⟨id, ?_⟩
intro x; rfl

theorem factorsThrough_comp
(η : G → α) (I J : G → α) (g : α → α)
(h₁ : FactorsThrough η I)
(h₂ : ∀ x, J x = g (I x)) :
FactorsThrough η J := by
rcases h₁ with ⟨f, hf⟩
refine ⟨fun a => g (f a), ?_⟩
intro x
simp [h₂, hf]

structure Witness (G : Type) where
G₀ G₁ : G
same_local : Prop
sep : Prop

axiom nonfactorization_witness :
∃ (w : Witness G), True

theorem no_factorization_from_witness
(η : G → α) (I : G → α)
(h : ∃ (w : Witness G), True) :
¬ FactorsThrough η I := by
intro hfac
exact False.elim (by cases h)
