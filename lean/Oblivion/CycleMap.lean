import Oblivion.ClosedWalk

namespace Oblivion

variable {G : Graph}

/-- Cycle length bounded by twice the diameter via two-path decomposition. -/
lemma cycle_length_le_two_mul_diameter
    (C : ClosedWalk G)
    (hC : C.IsCycle) :
    C.length ≤ 2 * cycleDiameter C := by
  classical
  obtain ⟨x, y, hxy⟩ := exists_pair_realizing_cycleDiameter C
  obtain ⟨p₁, p₂, hp, hlen⟩ := cycle_two_path_decomposition C hC x y
  have hdist :
      cycleDistance C x y ≤ min p₁.length p₂.length := by
    exact cycleDistance_le_shorter_arc C hC hp
  have hdiam : cycleDiameter C ≤ min p₁.length p₂.length := by
    simpa [hxy] using hdist
  have hsum : p₁.length + p₂.length = C.length := by
    simpa [hp] using hlen
  have hmin :
      p₁.length + p₂.length ≤ 2 * min p₁.length p₂.length := by
    omega
  omega

end Oblivion
