import Mathlib

/-!
Order-theoretic closure of the domain-indexed positive-entropy witness route.

This file replaces:
- abstract `r0_ne_r1` with imported real arithmetic;
- equality-projection with entropy-order projection;
- two-point obstruction with an unbounded-family obstruction;
- vacuous projection admissibility with local realization.
-/

universe u v

namespace Chronos.Frontier

example : (0 : ℝ) ≠ 1 := by
  exact zero_ne_one

structure PositiveEntropyWitness {I : Type u} (i : I) where
  entropy_bound : ℝ
  nonneg : 0 ≤ entropy_bound

structure PositiveEntropyUniformWitness where
  global_entropy : ℝ

structure UniformProjectionAdmissible
    (P : Prop)
    (I : Type u)
    (D : I → Type v)
    (W : ∀ i, D i → PositiveEntropyWitness i)
    (projectsToUniform :
      {i : I} → PositiveEntropyWitness i → PositiveEntropyUniformWitness → Prop) : Prop where
  locally_realized :
    ∀ d : Sigma D,
      ∃ U : PositiveEntropyUniformWitness,
        projectsToUniform (W d.1 d.2) U
  entropy_sound :
    ∀ U : PositiveEntropyUniformWitness,
      (∀ d : Sigma D, projectsToUniform (W d.1 d.2) U) →
      ∀ d : Sigma D, (W d.1 d.2).entropy_bound ≤ U.global_entropy
  uniform_witness_complete :
    (∃ U : PositiveEntropyUniformWitness,
      ∀ d : Sigma D, projectsToUniform (W d.1 d.2) U) →
    P

def DomainIndexedPositiveEntropyWitnessConstruction_order
    (P : Prop) : Prop :=
  ∃ (I : Type u)
    (D : I → Type v)
    (W : ∀ i, D i → PositiveEntropyWitness i)
    (projectsToUniform :
      {i : I} → PositiveEntropyWitness i → PositiveEntropyUniformWitness → Prop),
    UniformProjectionAdmissible P I D W projectsToUniform ∧
    ¬ ∃ U : PositiveEntropyUniformWitness,
      ∀ d : Sigma D, projectsToUniform (W d.1 d.2) U

def I0 : Type := ℕ

def D0 : I0 → Type := fun _ => PUnit

def W0 : ∀ i : ℕ, D0 i → PositiveEntropyWitness i :=
  fun i _ =>
    { entropy_bound := (i : ℝ)
      nonneg := by exact Nat.cast_nonneg i }

def projectsToUniform0 :
    {i : I0} → PositiveEntropyWitness i → PositiveEntropyUniformWitness → Prop :=
  fun {_} w U => w.entropy_bound ≤ U.global_entropy

theorem no_common_uniform_bound
    (B : ℝ) :
    ¬ ∀ n : ℕ, (n : ℝ) ≤ B := by
  intro h
  obtain ⟨n, hn⟩ := exists_nat_gt B
  exact (not_le_of_gt hn) (h n)

theorem no_uniform_projection0 :
    ¬ ∃ U : PositiveEntropyUniformWitness,
      ∀ d : Sigma D0, projectsToUniform0 (W0 d.1 d.2) U := by
  intro h
  rcases h with ⟨U, hU⟩
  exact no_common_uniform_bound U.global_entropy (by
    intro n
    simpa [D0, W0, projectsToUniform0] using hU ⟨n, PUnit.unit⟩)

theorem admissible0
    (P : Prop) :
    UniformProjectionAdmissible P I0 D0 W0 projectsToUniform0 := by
  refine ⟨?_, ?_, ?_⟩
  · intro d
    exact ⟨⟨(W0 d.1 d.2).entropy_bound⟩, by
      simp [projectsToUniform0]⟩
  · intro U hU d
    exact hU d
  · intro h
    exact False.elim (no_uniform_projection0 h)

theorem DomainIndexedPositiveEntropyWitnessConstruction_order_solved
    (P : Prop) :
    DomainIndexedPositiveEntropyWitnessConstruction_order.{0,0} P := by
  exact ⟨I0, D0, W0, projectsToUniform0, admissible0 P, no_uniform_projection0⟩

end Chronos.Frontier
