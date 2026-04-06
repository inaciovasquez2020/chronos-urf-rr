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

lemma map_ne_eq_true_iff_unique
  (edges : List E) (h1 h2 : E → Bool) (e : E)
  (h_nodup : edges.Nodup)
  (he : e ∈ edges ∧ h1 e ≠ h2 e)
  (huniq : ∀ x, x ∈ edges ∧ h1 x ≠ h2 x → x = e) :
  (edges.map (fun x => decide (h1 x ≠ h2 x))).filter (fun b => b) = [true] := by
  classical
  induction edges with
  | nil => cases he.1
  | cons a t ih =>
      simp at h_nodup
      rcases h_nodup with ⟨ha_notin, ht_nodup⟩
      by_cases ha : h1 a ≠ h2 a
      · have : a = e := huniq a ⟨by simp, ha⟩
        subst this
        have ht_false : ∀ x, x ∈ t → h1 x = h2 x := by
          intro x hx
          by_cases hxne : h1 x ≠ h2 x
          · have : x = e := huniq x ⟨by simp [hx], hxne⟩
            subst this
            exact False.elim (ha_notin hx)
          · exact Classical.byContradiction fun hEq => hxne hEq
        simp [ha]
        have : (t.map fun x => h1 x ≠ h2 x).filter (fun b => b) = [] := by
          induction t with
          | nil => simp
          | cons x xs ih2 =>
              have hx := ht_false x (by simp)
              simp [hx, ih2]
        simp [this]
      · have he_t : e ∈ t ∧ h1 e ≠ h2 e := by
          rcases he with ⟨he_mem, he_ne⟩
          simp at he_mem
          cases he_mem with
          | inl h => subst h; exact False.elim (ha he_ne)
          | inr h => exact ⟨h, he_ne⟩
        have huniq_t : ∀ x, x ∈ t ∧ h1 x ≠ h2 x → x = e := by
          intro x hx
          exact huniq x ⟨by simp [hx.1], hx.2⟩
        simp [ha, ih ht_nodup he_t huniq_t]

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
    have := congrArg xorFold hcount
    simp at this
    exact this
  simpa [parityPair_map] using hx

end Chronos
