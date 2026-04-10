import Mathlib

universe u v

variable {G : Type u} {α : Type v}

/-- Local type abstraction parameterized by a concrete encoder. -/
def FactorsThrough (η : G → α) (I : G → α) : Prop :=
∃ f : α → α, ∀ x, I x = f (η x)

theorem factorsThrough_id (η : G → α) :
FactorsThrough η (fun x => η x) := by
refine ⟨id, ?_⟩
intro x
rfl

theorem factorsThrough_comp
(η : G → α) (I J : G → α) (g : α → α)
(hI : FactorsThrough η I)
(hJ : ∀ x, J x = g (I x)) :
FactorsThrough η J := by
rcases hI with ⟨f, hf⟩
refine ⟨fun a => g (f a), ?_⟩
intro x
simp [hJ, hf]

structure Witness (G : Type u) (α : Type v) where
G₀ G₁ : G
η : G → α
I : G → α
same_local : η G₀ = η G₁
separated : I G₀ ≠ I G₁

structure HasWitness (G : Type u) (α : Type v) where
w : Witness G α

theorem no_factorization_from_witness
(hw : HasWitness G α) :
¬ FactorsThrough hw.w.η hw.w.I := by
intro hfac
rcases hfac with ⟨f, hf⟩
have h0 : hw.w.I hw.w.G₀ = f (hw.w.η hw.w.G₀) := hf hw.w.G₀
have h1 : hw.w.I hw.w.G₁ = f (hw.w.η hw.w.G₁) := hf hw.w.G₁
have : hw.w.I hw.w.G₀ = hw.w.I hw.w.G₁ := by
rw [h0, h1, hw.w.same_local]
exact hw.w.separated this

theorem separation_blocks_factorization
(w : Witness G α) :
¬ FactorsThrough w.η w.I := by
exact no_factorization_from_witness ⟨w⟩

