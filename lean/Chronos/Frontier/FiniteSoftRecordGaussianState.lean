import Mathlib.Analysis.SpecialFunctions.Gaussian.GaussianIntegral
import Mathlib.MeasureTheory.Group.Integral

namespace Chronos
namespace Frontier

open MeasureTheory

noncomputable section

/-!
# Finite soft-record Gaussian state

This module introduces a repository-native real Gaussian soft-record
wavefunction. Its normalization is derived from Mathlib's Gaussian integral
and translation invariance of Lebesgue measure.

No branch overlap, visibility law, detector map, or Regge–Wheeler
identification is asserted here.
-/

/--
A unit-width real Gaussian wavefunction centered at `center`.

The prefactor is the positive square root of `1 / √π`; consequently its square
has density

`(1 / √π) * exp (-(x - center)²)`.
-/
noncomputable def finiteSoftRecordGaussianWavefunction
    (center x : ℝ) :
    ℝ :=
  Real.sqrt ((Real.sqrt Real.pi)⁻¹) *
    Real.exp (-((x - center) ^ 2) / 2)

/--
The pointwise square of the soft-record wavefunction is its translated
normalized Gaussian density.
-/
theorem finiteSoftRecordGaussianWavefunction_sq
    (center x : ℝ) :
    finiteSoftRecordGaussianWavefunction center x ^ 2 =
      (Real.sqrt Real.pi)⁻¹ *
        Real.exp (-((x - center) ^ 2)) := by
  have hPiSqrtPos :
      0 < Real.sqrt Real.pi :=
    Real.sqrt_pos.2 Real.pi_pos

  have hInverseNonnegative :
      0 ≤ (Real.sqrt Real.pi)⁻¹ :=
    inv_nonneg.mpr hPiSqrtPos.le

  have hExponentialSquare :
      Real.exp (-((x - center) ^ 2) / 2) ^ 2 =
        Real.exp (-((x - center) ^ 2)) := by
    rw [pow_two, ← Real.exp_add]
    congr 1
    ring

  unfold finiteSoftRecordGaussianWavefunction
  rw [
    mul_pow,
    Real.sq_sqrt hInverseNonnegative,
    hExponentialSquare
  ]

/--
The Gaussian soft-record wavefunction has unit integrated square for every
center.
-/
theorem finiteSoftRecordGaussianWavefunction_normalized
    (center : ℝ) :
    ∫ x : ℝ,
        finiteSoftRecordGaussianWavefunction center x ^ 2 =
      1 := by
  have hPiSqrtPos :
      0 < Real.sqrt Real.pi :=
    Real.sqrt_pos.2 Real.pi_pos

  have hTranslatedGaussian :
      (∫ x : ℝ,
          Real.exp (-((x - center) ^ 2))) =
        ∫ x : ℝ,
          Real.exp (-(x ^ 2)) := by
    simpa using
      (integral_sub_right_eq_self
        (fun x : ℝ => Real.exp (-(x ^ 2)))
        center)

  have hCenteredGaussian :
      (∫ x : ℝ,
          Real.exp (-(x ^ 2))) =
        Real.sqrt Real.pi := by
    simpa using
      (integral_gaussian (1 : ℝ))

  simp_rw [
    finiteSoftRecordGaussianWavefunction_sq
  ]

  rw [
    integral_const_mul,
    hTranslatedGaussian,
    hCenteredGaussian,
    inv_mul_cancel₀ hPiSqrtPos.ne'
  ]


/--
The overlap of two normalized soft-record Gaussian branches centered at
`memoryShift / 2` and `-memoryShift / 2` is the exponential

`exp (-(memoryShift²) / 4)`.

The exponential is derived from the explicit normalized wavefunctions and the
Gaussian integral. It is not introduced as a visibility definition.
-/
theorem finiteSoftRecordGaussianWavefunction_symmetric_overlap
    (memoryShift : ℝ) :
    ∫ x : ℝ,
        finiteSoftRecordGaussianWavefunction
            (memoryShift / 2)
            x *
          finiteSoftRecordGaussianWavefunction
            (-memoryShift / 2)
            x =
      Real.exp (-(memoryShift ^ 2) / 4) := by
  have hPiSqrtPos :
      0 < Real.sqrt Real.pi :=
    Real.sqrt_pos.2 Real.pi_pos

  have hInverseNonnegative :
      0 ≤ (Real.sqrt Real.pi)⁻¹ :=
    inv_nonneg.mpr hPiSqrtPos.le

  have hCenteredGaussian :
      (∫ x : ℝ,
          Real.exp (-(x ^ 2))) =
        Real.sqrt Real.pi := by
    simpa using
      (integral_gaussian (1 : ℝ))

  have hPointwise :
      ∀ x : ℝ,
        finiteSoftRecordGaussianWavefunction
              (memoryShift / 2)
              x *
            finiteSoftRecordGaussianWavefunction
              (-memoryShift / 2)
              x =
          (
            (Real.sqrt Real.pi)⁻¹ *
              Real.exp (-(memoryShift ^ 2) / 4)
          ) *
            Real.exp (-(x ^ 2)) := by
    intro x

    have hExponent :
        -((x - memoryShift / 2) ^ 2) / 2 +
              -((x - (-memoryShift / 2)) ^ 2) / 2 =
            -(memoryShift ^ 2) / 4 + -(x ^ 2) := by
      ring

    unfold finiteSoftRecordGaussianWavefunction

    calc
      (
          Real.sqrt ((Real.sqrt Real.pi)⁻¹) *
            Real.exp
              (-((x - memoryShift / 2) ^ 2) / 2)
        ) *
          (
            Real.sqrt ((Real.sqrt Real.pi)⁻¹) *
              Real.exp
                (-((x - (-memoryShift / 2)) ^ 2) / 2)
          ) =
        Real.sqrt ((Real.sqrt Real.pi)⁻¹) ^ 2 *
          (
            Real.exp
                (-((x - memoryShift / 2) ^ 2) / 2) *
              Real.exp
                (-((x - (-memoryShift / 2)) ^ 2) / 2)
          ) := by
            ring
      _ =
        (Real.sqrt Real.pi)⁻¹ *
          Real.exp
            (
              -((x - memoryShift / 2) ^ 2) / 2 +
                -((x - (-memoryShift / 2)) ^ 2) / 2
            ) := by
              rw [
                Real.sq_sqrt hInverseNonnegative,
                ← Real.exp_add
              ]
      _ =
        (Real.sqrt Real.pi)⁻¹ *
          Real.exp
            (-(memoryShift ^ 2) / 4 + -(x ^ 2)) := by
              rw [hExponent]
      _ =
        (Real.sqrt Real.pi)⁻¹ *
          (
            Real.exp (-(memoryShift ^ 2) / 4) *
              Real.exp (-(x ^ 2))
          ) := by
              rw [Real.exp_add]
      _ =
        (
          (Real.sqrt Real.pi)⁻¹ *
            Real.exp (-(memoryShift ^ 2) / 4)
        ) *
          Real.exp (-(x ^ 2)) := by
            ring

  calc
    (∫ x : ℝ,
        finiteSoftRecordGaussianWavefunction
              (memoryShift / 2)
              x *
            finiteSoftRecordGaussianWavefunction
              (-memoryShift / 2)
              x) =
      ∫ x : ℝ,
        (
          (Real.sqrt Real.pi)⁻¹ *
            Real.exp (-(memoryShift ^ 2) / 4)
        ) *
          Real.exp (-(x ^ 2)) := by
            apply integral_congr_ae
            filter_upwards [] with x
            exact hPointwise x
    _ =
      (
        (Real.sqrt Real.pi)⁻¹ *
          Real.exp (-(memoryShift ^ 2) / 4)
      ) *
        (∫ x : ℝ,
          Real.exp (-(x ^ 2))) := by
            rw [integral_const_mul]
    _ =
      (
        (Real.sqrt Real.pi)⁻¹ *
          Real.exp (-(memoryShift ^ 2) / 4)
      ) *
        Real.sqrt Real.pi := by
            rw [hCenteredGaussian]
    _ =
      Real.exp (-(memoryShift ^ 2) / 4) := by
        calc
          (
            (Real.sqrt Real.pi)⁻¹ *
              Real.exp (-(memoryShift ^ 2) / 4)
          ) *
              Real.sqrt Real.pi =
            Real.exp (-(memoryShift ^ 2) / 4) *
              (
                (Real.sqrt Real.pi)⁻¹ *
                  Real.sqrt Real.pi
              ) := by
                ring
          _ =
            Real.exp (-(memoryShift ^ 2) / 4) := by
              rw [inv_mul_cancel₀ hPiSqrtPos.ne']
              ring

def finiteSoftRecordGaussianStateStatus : String :=
  "NORMALIZED_REAL_GAUSSIAN_SOFT_RECORD_STATE"

def finiteSoftRecordGaussianStateBoundary : String :=
  "BRANCH_OVERLAP_REDUCED_COHERENCE_VISIBILITY_AND_PHYSICAL_IDENTIFICATION_NOT_PROVED"

end
end Frontier
end Chronos
