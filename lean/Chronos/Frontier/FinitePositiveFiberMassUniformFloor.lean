import Chronos.Frontier.TerminalAdmissibleBoundaryChainCertificate

/-!
Finite positive fiber-mass uniform floor.

This proves the finite compactness principle:

  finite positive fiber masses have a positive uniform lower floor.

This is not an unrestricted floor over arbitrary `FiberMassData`; PR #362
already refuted that unrestricted route.
-/

namespace Chronos.Frontier

structure FiniteFiberMassData (N : ℕ) where
  mass : Fin N → ℝ

def FiniteFiberMassUniformFloor
    {N : ℕ}
    (M : FiniteFiberMassData N) : Prop :=
  ∃ ε : ℝ, 0 < ε ∧ ∀ i : Fin N, ε ≤ M.mass i

theorem finite_positive_fiber_mass_uniform_floor
    {N : ℕ}
    (hN : 0 < N)
    (M : FiniteFiberMassData N)
    (hpos : ∀ i : Fin N, 0 < M.mass i) :
    FiniteFiberMassUniformFloor M := by
  classical
  let s : Finset ℝ := Finset.univ.image M.mass
  have hs : s.Nonempty := by
    refine ⟨M.mass ⟨0, hN⟩, ?_⟩
    simp [s]
  refine ⟨s.min' hs, ?_, ?_⟩
  · have hmem : s.min' hs ∈ s := Finset.min'_mem s hs
    rcases Finset.mem_image.mp hmem with ⟨i, _, hi⟩
    simpa [hi] using hpos i
  · intro i
    exact Finset.min'_le s (M.mass i) (by simp [s])

def FinitePositiveFiberMassUniformFloorTheorem : Prop :=
  ∀ {N : ℕ}
    (_ : 0 < N)
    (M : FiniteFiberMassData N),
    (∀ i : Fin N, 0 < M.mass i) →
    FiniteFiberMassUniformFloor M

theorem FinitePositiveFiberMassUniformFloorTheorem_solved :
    FinitePositiveFiberMassUniformFloorTheorem := by
  intro N hN M hpos
  exact finite_positive_fiber_mass_uniform_floor hN M hpos

end Chronos.Frontier
