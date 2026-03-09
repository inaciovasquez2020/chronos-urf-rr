import Mathlib
import Oblivion.Visibility.LocalityCompletion

namespace Oblivion
namespace Visibility

open scoped BigOperators

def k0Bound (Δ R0 : Nat) : Nat :=
  Nat.ceil (Real.log ((Δ : Real) ^ R0 + 1) / Real.log 2) + 2

def DistinctBallTypesLowerBound (Δ R0 : Nat) (c : Real) : Real :=
  c / ((2 : Real) * (Δ : Real) ^ R0)

structure LocalRigidityHypotheses (Δ R0 : Nat) where
  c : Real
  hc : 0 < c
  hΔ : 1 ≤ Δ
  hCPI : ∀ n : Nat, c * n ≤ CPIloc n

theorem k0Bound_ge_two (Δ R0 : Nat) : 2 ≤ k0Bound Δ R0 := by
  unfold k0Bound
  omega

theorem denominator_pos (Δ R0 : Nat) (hΔ : 1 ≤ Δ) :
    0 < (2 : Real) * (Δ : Real) ^ R0 := by
  have hΔ' : 0 < (Δ : Real) := by
    exact_mod_cast lt_of_lt_of_le (show (0 : Nat) < 1 by decide) hΔ
  positivity

theorem distinctBallTypes_linear_lower_bound
    (Δ R0 : Nat)
    (h : LocalRigidityHypotheses Δ R0) :
    ∀ n : Nat, DistinctBallTypesLowerBound Δ R0 h.c * n ≤ FOTypeCount n := by
  intro n
  unfold DistinctBallTypesLowerBound
  exact localCPI_rigidity Δ R0 h.c h.hc h.hΔ h.hCPI n

def FOTypeGrowthProperty (Δ R0 : Nat) : Prop :=
  ∃ c : Real, 0 < c ∧ ∀ n : Nat, c * n ≤ FOTypeCount n

theorem local_cpi_implies_linear_type_growth
    (Δ R0 : Nat)
    (h : LocalRigidityHypotheses Δ R0) :
    FOTypeGrowthProperty Δ R0 := by
  refine ⟨DistinctBallTypesLowerBound Δ R0 h.c, ?_, ?_⟩
  · unfold DistinctBallTypesLowerBound
    have hpos := denominator_pos Δ R0 h.hΔ
    positivity
  · intro n
    exact distinctBallTypes_linear_lower_bound Δ R0 h n

def AsymptoticOmega (f : Nat → Real) : Prop :=
  ∃ c : Real, 0 < c ∧ ∀ n : Nat, c * n ≤ f n

theorem local_cpi_implies_omega_types
    (Δ R0 : Nat)
    (h : LocalRigidityHypotheses Δ R0) :
    AsymptoticOmega FOTypeCount := by
  exact local_cpi_implies_linear_type_growth Δ R0 h

theorem local_cpi_implies_explicit_constant
    (Δ R0 : Nat)
    (h : LocalRigidityHypotheses Δ R0) :
    ∀ n : Nat,
      (h.c / ((2 : Real) * (Δ : Real) ^ R0)) * n ≤ FOTypeCount n := by
  intro n
  exact localCPI_rigidity Δ R0 h.c h.hc h.hΔ h.hCPI n

theorem witness_bound_rearranged
    (Δ R0 : Nat)
    (hΔ : 1 ≤ Δ)
    (n : Nat) :
    WitnessCount n / ((2 : Real) * (Δ : Real) ^ R0) ≤ FOTypeCount n := by
  have hw := witness_count_bound_types Δ R0 n
  have hpos := denominator_pos Δ R0 hΔ
  exact (le_div_iff hpos).mpr hw

theorem cpi_to_types_via_witnesses
    (Δ R0 : Nat)
    (h : LocalRigidityHypotheses Δ R0)
    (n : Nat) :
    CPIloc n / ((2 : Real) * (Δ : Real) ^ R0) ≤ FOTypeCount n := by
  rw [← witness_count_eq_cpi]
  exact witness_bound_rearranged Δ R0 h.hΔ n

theorem final_local_rigidity_statement
    (Δ R0 : Nat)
    (h : LocalRigidityHypotheses Δ R0) :
    ∀ n : Nat,
      (DistinctBallTypesLowerBound Δ R0 h.c) * n ≤ FOTypeCount n := by
  exact distinctBallTypes_linear_lower_bound Δ R0 h

#print axioms local_cpi_implies_linear_type_growth
#print axioms final_local_rigidity_statement

end Visibility
end Oblivion
