import «Continuum».Support

namespace Continuum

theorem support_mass_linear
  (F : SupportFamily) {s a K : Rat}
  (h : Admissible F s a K) :
  (s * F.m) ≤ F.totalSupport := by
  exact totalSupport_lower_of_uniform F h.left

theorem diagonal_gram_linear
  (F : SupportFamily) {s a K : Rat}
  (h : Admissible F s a K) :
  (a * a * F.m) ≤ F.gramLowerDiagonal := by
  exact gramLowerDiagonal_lower_of_uniform F h.2.1

theorem continuum_rigidity_core
  (F : SupportFamily) {s K : Rat}
  (h : Admissible F s 1 K) :
  (s * F.m) ≤ F.totalSupport ∧ (1 * 1 * F.m) ≤ F.gramLowerDiagonal := by
  constructor
  · exact support_mass_linear F h
  · exact diagonal_gram_linear F h

theorem continuum_rigidity_unit_norm
  (F : SupportFamily) {s K : Rat}
  (h : Admissible F s 1 K) :
  (s * F.m) ≤ F.totalSupport ∧ (F.m : Rat) ≤ F.gramLowerDiagonal := by
  constructor
  · exact support_mass_linear F h
  · simpa using diagonal_gram_linear F h

def DiscreteRealization (m : Nat) (supportMass : Nat → Rat) (overlapMass : Nat → Nat → Rat) :
    SupportFamily :=
  { m := m
    supportMass := supportMass
    overlapMass := overlapMass
    normSq := fun _ => 1 }

theorem discrete_to_continuum_bridge
  (m : Nat) (supportMass : Nat → Rat) (overlapMass : Nat → Nat → Rat)
  {s K : Rat}
  (hs : ∀ i, i < m → s ≤ supportMass i)
  (hK : HasControlledOverlap (DiscreteRealization m supportMass overlapMass) K) :
  (s * m) ≤ (DiscreteRealization m supportMass overlapMass).totalSupport ∧
  (m : Rat) ≤ (DiscreteRealization m supportMass overlapMass).gramLowerDiagonal := by
  let F := DiscreteRealization m supportMass overlapMass
  have hnorm : HasUniformNormLower F 1 := by
    intro i hi
    simp [DiscreteRealization]
  have hadm : Admissible F s 1 K := by
    exact ⟨hs, hnorm, hK⟩
  simpa [F] using continuum_rigidity_unit_norm F hadm

end Continuum
