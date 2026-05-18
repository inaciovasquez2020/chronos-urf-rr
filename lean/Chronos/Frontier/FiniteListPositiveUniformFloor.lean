import Mathlib

namespace Chronos
namespace Frontier

/--
A nonempty finite list of strictly positive real masses has a strictly positive
uniform lower floor for every element of the list.
-/
theorem finite_list_positive_uniform_floor :
    ∀ masses : List ℝ,
      masses ≠ [] →
      (∀ x, x ∈ masses → 0 < x) →
      ∃ ε : ℝ, 0 < ε ∧ ∀ x, x ∈ masses → ε ≤ x
  | [], hne, _ => by
      exact False.elim (hne rfl)
  | a :: xs, _hne, hpos => by
      by_cases hxs : xs = []
      · refine ⟨a, ?_, ?_⟩
        · exact hpos a (by simp)
        · intro x hx
          have hx_eq : x = a := by
            simpa [hxs] using hx
          rw [hx_eq]
      · have hpos_xs : ∀ x, x ∈ xs → 0 < x := by
          intro x hx
          exact hpos x (by simp [hx])
        obtain ⟨ε, hε_pos, hε_floor⟩ :=
          finite_list_positive_uniform_floor xs hxs hpos_xs
        refine ⟨min a ε, ?_, ?_⟩
        · exact lt_min (hpos a (by simp)) hε_pos
        · intro x hx
          rcases List.mem_cons.mp hx with hx_head | hx_tail
          · rw [hx_head]
            exact min_le_left a ε
          · exact le_trans (min_le_right a ε) (hε_floor x hx_tail)

/--
Named finite-support mass-floor theorem specialized to list-coded finite support.
-/
theorem FiniteSupportPositiveMassUniformFloor_list
    (masses : List ℝ)
    (hne : masses ≠ [])
    (hpos : ∀ x, x ∈ masses → 0 < x) :
    ∃ ε : ℝ, 0 < ε ∧ ∀ x, x ∈ masses → ε ≤ x := by
  exact finite_list_positive_uniform_floor masses hne hpos

end Frontier
end Chronos
