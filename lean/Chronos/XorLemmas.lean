import Mathlib
import Chronos.ParityPair

namespace Chronos

universe v
variable {E : Type v}

theorem parityPair_ne_of_single_diff
  (edges : List E) (h1 h2 : E → Bool)
  (h_nodup : edges.Nodup) :
  (∃! e, e ∈ edges ∧ h1 e ≠ h2 e) →
  parityPair edges h1 ≠ parityPair edges h2 := by
  intro h
  classical
  rcases h with ⟨e, ⟨he_mem, he_diff⟩, huniq⟩

  have h_tail_eq :
    List.map h1 (edges.erase e) = List.map h2 (edges.erase e) := by
    apply List.map_congr
    intro x hx
    have hx_mem : x ∈ edges := List.mem_of_mem_erase hx
    have hx_ne : x ≠ e := List.ne_of_mem_erase hx
    by_contra h_diff'
    exact hx_ne (huniq x ⟨hx_mem, h_diff'⟩)

  simp [parityPair, parityPair_map]
  have := List.perm_cons_erase he_mem
  simp [xorFold_cons, h_tail_eq, he_diff]

end Chronos

lemma bool_ne_cancel_right (a b c : Bool) :
  (a ≠ c) = (b ≠ c) → a = b := by
  cases a <;> cases b <;> cases c <;> decide

