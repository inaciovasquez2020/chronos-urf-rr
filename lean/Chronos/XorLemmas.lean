import Mathlib
import Chronos.ParityPair

namespace Chronos

universe v
variable {E : Type v}

/-- Local helper: if two functions agree on all elements of a list, their maps are equal. -/
theorem map_ext {l : List E} {f g : E → Bool} (h : ∀ x, x ∈ l → f x = g x) :
    l.map f = l.map g := by
  induction l with
  | nil => rfl
  | cons a t ih => 
      simp [ih (λ x hx => h x (List.mem_cons_of_mem a hx)), h a (List.mem_cons_self a t)]

/-- Structural induction for XOR parity changes. -/
theorem parity_flip_induction [DecidableEq E] (l : List E) (h1 h2 : E → Bool) (target : E)
    (h_nodup : l.Nodup)
    (h_mem : target ∈ l)
    (h_diff : h1 target ≠ h2 target)
    (h_others : ∀ x ∈ l, x ≠ target → h1 x = h2 x) :
    xorFold (l.map h1) ≠ xorFold (l.map h2) := by
  induction l with
  | nil => cases h_mem
  | cons a t ih =>
      simp at h_nodup h_mem
      rcases h_nodup with ⟨ha_notin, ht_nodup⟩
      simp only [List.map_cons, xorFold]
      by_cases hae : a = target
      · subst hae
        -- Head is target; tails must match because all other elements agree.
        have h_tails : t.map h1 = t.map h2 := by
          apply map_ext
          intro x hx
          apply h_others x (List.mem_cons_of_mem _ hx)
          intro h_rev; subst h_rev; contradiction
        rw [h_tails]
        -- Core XOR logic via case exhaustion
        cases h1 target <;> cases h2 target <;> cases xorFold (t.map h2) <;> 
        simp at h_diff <;> (try simp [h_diff])
      · -- Head is not target; bits match and target is in the tail.
        have ha_eq : h1 a = h2 a := h_others a (List.mem_cons_self _ _) hae
        rw [ha_eq]
        have h_mem_t : target ∈ t := by
          cases h_mem with | inl h => exact False.elim (hae h.symm) | inr h => exact h
        have iht := ih ht_nodup h_mem_t (λ x hx hxe => h_others x (List.mem_cons_of_mem _ hx) hxe)
        -- Bool cancellation logic
        cases h1 a <;> simp [iht]

theorem parityPair_ne_of_single_diff [DecidableEq E]
    (edges : List E) (h1 h2 : E → Bool)
    (h_nodup : edges.Nodup) :
    (∃! e, e ∈ edges ∧ h1 e ≠ h2 e) →
    parityPair edges h1 ≠ parityPair edges h2 := by
  intro h
  rcases h with ⟨e, ⟨he_mem, he_diff⟩, huniq⟩
  simp [parityPair]
  apply parity_flip_induction edges h1 h2 e h_nodup he_mem he_diff
  intro x hx hxe
  by_contra h_neq
  exact hxe (huniq x ⟨hx, h_neq⟩)

end Chronos

lemma xor_tail_diff (P1 P2 b : Bool) :
  P1 ≠ P2 → (b != P1) ≠ (b != P2) := by
  cases P1 <;> cases P2 <;> cases b <;> simp

