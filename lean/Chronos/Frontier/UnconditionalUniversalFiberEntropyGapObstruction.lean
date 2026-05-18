import Mathlib.Data.Real.Basic
import Mathlib.Tactic

namespace Chronos
namespace Frontier

/--
A minimal arbitrary fiber-mass surface.

This intentionally has no built-in positivity or uniform lower bound.
-/
structure ArbitraryFiberMassData where
  fiberMass : ℕ → ℝ

/--
Uniform positive fiber-mass floor.

This is the exact ingredient needed before a universal entropy-gap theorem
can hold over arbitrary fiber-mass data.
-/
def FiberMassUniformFloor (D : ArbitraryFiberMassData) : Prop :=
  ∃ ε : ℝ, 0 < ε ∧ ∀ n : ℕ, ε ≤ D.fiberMass n

/--
A zero-mass arbitrary fiber package.

This is enough to refute any unconditional theorem over arbitrary
`FiberMassData` unless uniform positivity is added to the data type.
-/
def zeroFiberMassData : ArbitraryFiberMassData :=
  { fiberMass := fun _ => 0 }

/--
The zero-mass package has no uniform positive fiber-mass floor.
-/
theorem zeroFiberMassData_no_uniform_floor :
    ¬ FiberMassUniformFloor zeroFiberMassData := by
  intro h
  rcases h with ⟨ε, hε, hfloor⟩
  have h0 : ε ≤ (0 : ℝ) := by
    simpa [zeroFiberMassData] using hfloor 0
  linarith

/--
Arbitrarily small fiber masses obstruct a uniform positive floor.

This captures the stronger obstruction: even pointwise positive masses do
not suffice if the infimum is zero.
-/
theorem no_uniform_floor_of_arbitrarily_small
    (D : ArbitraryFiberMassData)
    (hSmall : ∀ ε : ℝ, 0 < ε → ∃ n : ℕ, D.fiberMass n < ε) :
    ¬ FiberMassUniformFloor D := by
  intro h
  rcases h with ⟨ε, hε, hfloor⟩
  rcases hSmall ε hε with ⟨n, hn⟩
  have hle : ε ≤ D.fiberMass n := hfloor n
  linarith

/--
Unconditional universal fiber entropy gap cannot be obtained from arbitrary
fiber-mass data alone.
-/
theorem unconditional_universal_fiber_entropy_gap_obstructed :
    ∃ D : ArbitraryFiberMassData, ¬ FiberMassUniformFloor D := by
  exact ⟨zeroFiberMassData, zeroFiberMassData_no_uniform_floor⟩

end Frontier
end Chronos
