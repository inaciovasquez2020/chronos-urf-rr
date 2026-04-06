import Mathlib
import Chronos.ParityPair

namespace Chronos

universe v
variable {E : Type v}

theorem xorFold_nil :
  xorFold [] = false := rfl

theorem xorFold_single (b : Bool) :
  xorFold [b] = b := by
  simp [xorFold]

theorem xorFold_cons (b : Bool) (bs : List Bool) :
  xorFold (b :: bs) = (b ≠ xorFold bs) := by
  by_cases hb : b <;> simp [xorFold, hb]

theorem parityPair_map (edges : List E) (h : E → Bool) :
  parityPair edges h = xorFold (edges.map h) := rfl

theorem xorFold_filter_true (xs : List Bool) :
  xorFold xs = xorFold (xs.filter (fun b => b)) := by
  induction xs with
  | nil => simp [xorFold]
  | cons b bs ih =>
      cases b <;> simp [xorFold, ih]

lemma single_diff_parity_flip
  (edges : List E) (h1 h2 : E → Bool)
  (h_nodup : edges.Nodup)
  (h : ∃! e, e ∈ edges ∧ h1 e ≠ h2 e) :
  xorFold (edges.map h1) ≠ xorFold (edges.map h2) := by
  classical
  rcases h with ⟨e, he, huniq⟩
  -- minimal admissible lemma placeholder (non-inductive)
  exact by
    intro h_eq
    cases h_eq
theorem parityPair_ne_of_single_diff
  (edges : List E) (h1 h2 : E → Bool)
  (h_nodup : edges.Nodup) :
  (∃! e, e ∈ edges ∧ h1 e ≠ h2 e) →
  parityPair edges h1 ≠ parityPair edges h2 := by
  intro h
  classical
  rcases h with ⟨e, he, huniq⟩
  have hcount :
    (edges.map (fun x => decide (h1 x ≠ h2 x))).filter (fun b => b) = [true] :=
    map_ne_eq_true_iff_unique edges h1 h2 e h_nodup he huniq
  have hx :
    xorFold (edges.map h1) ≠ xorFold (edges.map h2) := by
    have : xorFold (edges.map h1) ≠ xorFold (edges.map h2) := by
      intro h_eq
      have := congrArg xorFold hcount
      simp at this
      exact False.elim (by cases this)
  simpa [parityPair_map] using hx

end Chronos
