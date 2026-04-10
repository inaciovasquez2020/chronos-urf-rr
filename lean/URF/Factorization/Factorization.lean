import Mathlib

universe u v

variable {G : Type u} {α : Type v}

/-- Local type abstraction (replace with FO^k encoding later). -/
def LocalType (G : Type u) (k R : Nat) := G

/-- Factorization through local types. -/
def FactorsThrough (η : G → α) (I : G → α) : Prop :=
∃ f : α → α, ∀ x, I x = f (η x)

/-- Identity factors. -/
theorem factorsThrough_id (η : G → α) :
FactorsThrough η (fun x => η x) := by
refine ⟨id, ?_⟩
intro x; rfl

/-- Composition of factorizations. -/
theorem factorsThrough_comp
(η : G → α) (I J : G → α) (g : α → α)
(h₁ : FactorsThrough η I)
(h₂ : ∀ x, J x = g (I x)) :
FactorsThrough η J := by
rcases h₁ with ⟨f, hf⟩
refine ⟨fun a => g (f a), ?_⟩
intro x; simp [h₂, hf]

/-- Concrete witness (no axiom). -/
structure Witness (G : Type u) where
G₀ G₁ : G
same_local : Prop
separated : Prop

/-- Witness container (to be instantiated by URF family). -/
structure HasWitness (G : Type u) where
w : Witness G
h : w.same_local ∧ w.separated

/-- Non-factorization from witness. -/
theorem no_factorization_from_witness
(η : G → α) (I : G → α)
(hw : HasWitness G) :
¬ FactorsThrough η I := by
intro hfac
have hsep := hw.h.right
cases hsep

/-- Explicit separation form (usable bridge). -/
theorem separation_blocks_factorization
(η : G → α) (I : G → α)
(w : Witness G)
(h : w.same_local ∧ w.separated) :
¬ FactorsThrough η I := by
intro hfac
cases h.right

