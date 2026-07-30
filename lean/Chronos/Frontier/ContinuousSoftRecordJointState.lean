import Chronos.Frontier.FiniteSoftRecordGaussianState

namespace Chronos
namespace Frontier

noncomputable section

/-!
# Continuous soft-record joint state

This module defines a phase-zero two-branch hard/soft joint amplitude over the
continuous soft-record coordinate `x : ℝ`.

The two hard branches are assigned Gaussian records centered at
`memoryShift / 2` and `-memoryShift / 2`, each with amplitude weight `1 / √2`.

Only the joint amplitude and its pointwise density kernel are introduced here.
No integration, reduced density matrix, visibility identification, detector
map, or Regge–Wheeler interpretation is asserted.
-/

/-- Two-dimensional hard-sector basis for the continuous record model. -/
abbrev ContinuousSoftRecordHardBasis :=
  Fin 2

/--
Phase-zero joint amplitude for a hard qubit entangled with two continuous
Gaussian soft-record branches.

Hard basis state `0` carries the branch centered at `memoryShift / 2`.
Hard basis state `1` carries the branch centered at `-memoryShift / 2`.
-/
noncomputable def continuousSoftRecordJointAmplitude
    (memoryShift : ℝ)
    (hard : ContinuousSoftRecordHardBasis)
    (x : ℝ) :
    ℝ :=
  if hard = 0 then
    (Real.sqrt 2)⁻¹ *
      finiteSoftRecordGaussianWavefunction
        (memoryShift / 2)
        x
  else
    (Real.sqrt 2)⁻¹ *
      finiteSoftRecordGaussianWavefunction
        (-memoryShift / 2)
        x

/--
Pointwise hard-sector density kernel before integration over the continuous
soft-record coordinate.

For the present real, phase-zero model this is the product of the left and
right joint amplitudes.
-/
noncomputable def continuousSoftRecordJointDensityKernel
    (memoryShift : ℝ)
    (left right : ContinuousSoftRecordHardBasis)
    (x : ℝ) :
    ℝ :=
  continuousSoftRecordJointAmplitude
      memoryShift
      left
      x *
    continuousSoftRecordJointAmplitude
      memoryShift
      right
      x


/--
Integrating the pointwise density kernel between hard branches `0` and `1`
produces one half of the normalized Gaussian branch overlap.

This is the reduced hard-sector off-diagonal coherence for the phase-zero
two-branch joint amplitude. It is not yet identified with an experimentally
measured visibility.
-/
theorem continuousSoftRecordJointDensityKernel_offDiagonal_integral
    (memoryShift : ℝ) :
    ∫ x : ℝ,
        continuousSoftRecordJointDensityKernel
          memoryShift
          0
          1
          x =
      (1 / 2 : ℝ) *
        Real.exp (-(memoryShift ^ 2) / 4) := by
  have hAmplitudeZero
      (x : ℝ) :
      continuousSoftRecordJointAmplitude
          memoryShift
          0
          x =
        (Real.sqrt (2 : ℝ))⁻¹ *
          finiteSoftRecordGaussianWavefunction
            (memoryShift / 2)
            x := by
    simp [continuousSoftRecordJointAmplitude]

  have hAmplitudeOne
      (x : ℝ) :
      continuousSoftRecordJointAmplitude
          memoryShift
          1
          x =
        (Real.sqrt (2 : ℝ))⁻¹ *
          finiteSoftRecordGaussianWavefunction
            (-memoryShift / 2)
            x := by
    simp [continuousSoftRecordJointAmplitude]

  have hKernel
      (x : ℝ) :
      continuousSoftRecordJointDensityKernel
          memoryShift
          0
          1
          x =
        (Real.sqrt (2 : ℝ))⁻¹ ^ 2 *
          (
            finiteSoftRecordGaussianWavefunction
                (memoryShift / 2)
                x *
              finiteSoftRecordGaussianWavefunction
                (-memoryShift / 2)
                x
          ) := by
    unfold continuousSoftRecordJointDensityKernel
    rw [
      hAmplitudeZero x,
      hAmplitudeOne x
    ]
    ring

  have hSqrtTwoSq :
      Real.sqrt (2 : ℝ) ^ 2 = 2 := by
    norm_num

  have hWeightSq :
      (Real.sqrt (2 : ℝ))⁻¹ ^ 2 =
        (1 / 2 : ℝ) := by
    rw [inv_pow, hSqrtTwoSq]
    norm_num

  calc
    (∫ x : ℝ,
        continuousSoftRecordJointDensityKernel
          memoryShift
          0
          1
          x) =
      ∫ x : ℝ,
        (Real.sqrt (2 : ℝ))⁻¹ ^ 2 *
          (
            finiteSoftRecordGaussianWavefunction
                (memoryShift / 2)
                x *
              finiteSoftRecordGaussianWavefunction
                (-memoryShift / 2)
                x
          ) := by
            apply MeasureTheory.integral_congr_ae
            filter_upwards [] with x
            exact hKernel x
    _ =
      (Real.sqrt (2 : ℝ))⁻¹ ^ 2 *
        (
          ∫ x : ℝ,
            finiteSoftRecordGaussianWavefunction
                (memoryShift / 2)
                x *
              finiteSoftRecordGaussianWavefunction
                (-memoryShift / 2)
                x
        ) := by
          rw [MeasureTheory.integral_const_mul]
    _ =
      (Real.sqrt (2 : ℝ))⁻¹ ^ 2 *
        Real.exp (-(memoryShift ^ 2) / 4) := by
          rw [
            finiteSoftRecordGaussianWavefunction_symmetric_overlap
          ]
    _ =
      (1 / 2 : ℝ) *
        Real.exp (-(memoryShift ^ 2) / 4) := by
          rw [hWeightSq]


/--
Integrating the pointwise density kernel on hard branch `0` gives probability
weight `1 / 2`.

This follows from the branch amplitude weight `1 / √2` and normalization of
the corresponding Gaussian soft-record wavefunction.
-/
theorem continuousSoftRecordJointDensityKernel_zeroDiagonal_integral
    (memoryShift : ℝ) :
    ∫ x : ℝ,
        continuousSoftRecordJointDensityKernel
          memoryShift
          0
          0
          x =
      (1 / 2 : ℝ) := by
  have hAmplitudeZero
      (x : ℝ) :
      continuousSoftRecordJointAmplitude
          memoryShift
          0
          x =
        (Real.sqrt (2 : ℝ))⁻¹ *
          finiteSoftRecordGaussianWavefunction
            (memoryShift / 2)
            x := by
    simp [continuousSoftRecordJointAmplitude]

  have hKernel
      (x : ℝ) :
      continuousSoftRecordJointDensityKernel
          memoryShift
          0
          0
          x =
        (Real.sqrt (2 : ℝ))⁻¹ ^ 2 *
          finiteSoftRecordGaussianWavefunction
              (memoryShift / 2)
              x ^ 2 := by
    unfold continuousSoftRecordJointDensityKernel
    rw [hAmplitudeZero x]
    ring

  have hSqrtTwoSq :
      Real.sqrt (2 : ℝ) ^ 2 = 2 := by
    norm_num

  have hWeightSq :
      (Real.sqrt (2 : ℝ))⁻¹ ^ 2 =
        (1 / 2 : ℝ) := by
    rw [inv_pow, hSqrtTwoSq]
    norm_num

  calc
    (∫ x : ℝ,
        continuousSoftRecordJointDensityKernel
          memoryShift
          0
          0
          x) =
      ∫ x : ℝ,
        (Real.sqrt (2 : ℝ))⁻¹ ^ 2 *
          finiteSoftRecordGaussianWavefunction
              (memoryShift / 2)
              x ^ 2 := by
            apply MeasureTheory.integral_congr_ae
            filter_upwards [] with x
            exact hKernel x
    _ =
      (Real.sqrt (2 : ℝ))⁻¹ ^ 2 *
        (
          ∫ x : ℝ,
            finiteSoftRecordGaussianWavefunction
                (memoryShift / 2)
                x ^ 2
        ) := by
          rw [MeasureTheory.integral_const_mul]
    _ =
      (Real.sqrt (2 : ℝ))⁻¹ ^ 2 * 1 := by
          rw [
            finiteSoftRecordGaussianWavefunction_normalized
          ]
    _ =
      (1 / 2 : ℝ) := by
          rw [hWeightSq]
          norm_num


/--
Integrating the pointwise density kernel on hard branch `1` gives probability
weight `1 / 2`.

This follows from the branch amplitude weight `1 / √2` and normalization of
the corresponding Gaussian soft-record wavefunction.
-/
theorem continuousSoftRecordJointDensityKernel_oneDiagonal_integral
    (memoryShift : ℝ) :
    ∫ x : ℝ,
        continuousSoftRecordJointDensityKernel
          memoryShift
          1
          1
          x =
      (1 / 2 : ℝ) := by
  have hAmplitudeOne
      (x : ℝ) :
      continuousSoftRecordJointAmplitude
          memoryShift
          1
          x =
        (Real.sqrt (2 : ℝ))⁻¹ *
          finiteSoftRecordGaussianWavefunction
            (-memoryShift / 2)
            x := by
    simp [continuousSoftRecordJointAmplitude]

  have hKernel
      (x : ℝ) :
      continuousSoftRecordJointDensityKernel
          memoryShift
          1
          1
          x =
        (Real.sqrt (2 : ℝ))⁻¹ ^ 2 *
          finiteSoftRecordGaussianWavefunction
              (-memoryShift / 2)
              x ^ 2 := by
    unfold continuousSoftRecordJointDensityKernel
    rw [hAmplitudeOne x]
    ring

  have hSqrtTwoSq :
      Real.sqrt (2 : ℝ) ^ 2 = 2 := by
    norm_num

  have hWeightSq :
      (Real.sqrt (2 : ℝ))⁻¹ ^ 2 =
        (1 / 2 : ℝ) := by
    rw [inv_pow, hSqrtTwoSq]
    norm_num

  calc
    (∫ x : ℝ,
        continuousSoftRecordJointDensityKernel
          memoryShift
          1
          1
          x) =
      ∫ x : ℝ,
        (Real.sqrt (2 : ℝ))⁻¹ ^ 2 *
          finiteSoftRecordGaussianWavefunction
              (-memoryShift / 2)
              x ^ 2 := by
            apply MeasureTheory.integral_congr_ae
            filter_upwards [] with x
            exact hKernel x
    _ =
      (Real.sqrt (2 : ℝ))⁻¹ ^ 2 *
        (
          ∫ x : ℝ,
            finiteSoftRecordGaussianWavefunction
                (-memoryShift / 2)
                x ^ 2
        ) := by
          rw [MeasureTheory.integral_const_mul]
    _ =
      (Real.sqrt (2 : ℝ))⁻¹ ^ 2 * 1 := by
          rw [
            finiteSoftRecordGaussianWavefunction_normalized
          ]
    _ =
      (1 / 2 : ℝ) := by
          rw [hWeightSq]
          norm_num


/--
Normalized hard-sector coherence visibility extracted from the reduced
two-branch density entries.

The numerator is twice the magnitude of the off-diagonal coherence. The
denominator is the total diagonal population. This is an algebraic reduced
state quantity; no detector response or Regge–Wheeler calibration is asserted.
-/
noncomputable def continuousSoftRecordNormalizedVisibility
    (memoryShift : ℝ) :
    ℝ :=
  (
    2 *
      abs
        (
          ∫ x : ℝ,
            continuousSoftRecordJointDensityKernel
              memoryShift
              0
              1
              x
        )
  ) /
    (
      (
        ∫ x : ℝ,
          continuousSoftRecordJointDensityKernel
            memoryShift
            0
            0
            x
      ) +
        (
          ∫ x : ℝ,
            continuousSoftRecordJointDensityKernel
              memoryShift
              1
              1
              x
        )
    )

/--
The normalized reduced hard-sector visibility is the Gaussian branch-overlap
factor `exp (-(memoryShift²) / 4)`.

Unlike the earlier definitional visibility candidate, this equality follows
from the explicit joint amplitude, both normalized diagonal entries, and the
derived off-diagonal coherence.
-/
theorem continuousSoftRecordNormalizedVisibility_eq_exp
    (memoryShift : ℝ) :
    continuousSoftRecordNormalizedVisibility memoryShift =
      Real.exp (-(memoryShift ^ 2) / 4) := by
  have hOffDiagonalNonnegative :
      0 ≤
        (1 / 2 : ℝ) *
          Real.exp (-(memoryShift ^ 2) / 4) :=
    mul_nonneg
      (by norm_num)
      (Real.exp_pos _).le

  unfold continuousSoftRecordNormalizedVisibility

  rw [
    continuousSoftRecordJointDensityKernel_offDiagonal_integral,
    continuousSoftRecordJointDensityKernel_zeroDiagonal_integral,
    continuousSoftRecordJointDensityKernel_oneDiagonal_integral,
    abs_of_nonneg hOffDiagonalNonnegative
  ]

  ring

def continuousSoftRecordJointStateStatus : String :=
  "CONTINUOUS_TWO_BRANCH_GAUSSIAN_REDUCED_HARD_SECTOR_VISIBILITY_DERIVED"

def continuousSoftRecordJointStateBoundary : String :=
  "DETECTOR_INTERPRETATION_AND_PHYSICAL_REGGE_WHEELER_MEMORY_SHIFT_IDENTIFICATION_NOT_PROVED"

end
end Frontier
end Chronos
