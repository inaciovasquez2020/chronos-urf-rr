import Mathlib

namespace Chronos.Frontier

open Filter

/--
The five pieces of charge-and-low-multipole data held fixed in the
conditional Spartan theorem.
-/
structure QuznorSpartanFixedFiberData where
  s2 : ℝ
  s3 : Fin 4 → ℝ
  s4 : Matrix (Fin 4) (Fin 4) ℝ
  q1 : ℝ
  q5 : ℝ

/--
A conditional certificate for the Spartan curvature-blowup implication.

The structure does not prove profile-scale convergence, endpoint-ratio
limits, the six-dimensional curvature identity, or higher-derivative
control.
-/
structure QuznorSpartanConditionalCurvatureBlowupData where
  fiberData : ℕ → QuznorSpartanFixedFiberData
  fixedFiberData : QuznorSpartanFixedFiberData
  fiberData_fixed :
    ∀ n : ℕ, fiberData n = fixedFiberData
  scalarCurvatureAtSample : ℕ → ℝ
  scalarCurvatureSup : ℕ → ℝ
  sample_le_sup :
    ∀ n : ℕ,
      scalarCurvatureAtSample n ≤ scalarCurvatureSup n
  c0 : ℝ
  c0_pos : 0 < c0
  normalizedSampleTendsto :
    Tendsto
      (fun n : ℕ =>
        scalarCurvatureAtSample n / (n : ℝ))
      atTop
      (nhds c0)

/-- The certificate preserves one fixed abstract fiber. -/
theorem quznorSpartanConditionalFiber_fixed
    (data : QuznorSpartanConditionalCurvatureBlowupData) :
    ∀ n : ℕ, data.fiberData n = data.fixedFiberData :=
  data.fiberData_fixed

/--
A positive normalized sampled-curvature limit forces sampled curvature
to diverge to positive infinity.
-/
theorem quznorSpartanConditionalSampleCurvature_tendsto_atTop
    (data : QuznorSpartanConditionalCurvatureBlowupData) :
    Tendsto data.scalarCurvatureAtSample atTop atTop := by
  exact Filter.Tendsto.num
    (f := data.scalarCurvatureAtSample)
    (g := fun n : ℕ => (n : ℝ))
    (l := atTop)
    tendsto_natCast_atTop_atTop
    data.c0_pos
    data.normalizedSampleTendsto

/--
The curvature supremum diverges because it dominates the sampled
curvature pointwise.
-/
theorem quznorSpartanConditionalCurvatureSup_tendsto_atTop
    (data : QuznorSpartanConditionalCurvatureBlowupData) :
    Tendsto data.scalarCurvatureSup atTop atTop := by
  exact Filter.tendsto_atTop_mono
    data.sample_le_sup
    (quznorSpartanConditionalSampleCurvature_tendsto_atTop data)

/--
Spartan Theorem — conditional Lean package.

The theorem does not discharge the analytic or supergravity hypotheses
stored in the certificate.
-/
theorem quznorSpartanConditionalCurvatureBlowup
    (data : QuznorSpartanConditionalCurvatureBlowupData) :
    (∀ n : ℕ,
      data.fiberData n = data.fixedFiberData) ∧
    Tendsto data.scalarCurvatureSup atTop atTop := by
  exact ⟨
    quznorSpartanConditionalFiber_fixed data,
    quznorSpartanConditionalCurvatureSup_tendsto_atTop data
  ⟩

end Chronos.Frontier
