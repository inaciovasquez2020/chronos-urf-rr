import Chronos.Frontier.ReggeWheelerGaugeInvariantMemoryChannel

namespace Chronos
namespace Frontier

noncomputable section

/-!
# Regge–Wheeler memory–visibility prediction

This module states a dimensionless, two-observable consistency prediction for
the coherent soft-memory channel.

For a nonzero detector-normalized memory shift `Δ` and visibility `V`, define

`R_MV = (-2 log V) / Δ²`.

The coherent-memory channel predicts the parameter-free value `R_MV = 1/2`.
Equivalently, its residual

`D_MV = -2 log V - Δ² / 2`

vanishes. At the same visibility, a zero-correlated-memory model differs by the
strictly positive gap `Δ² / 2` whenever `Δ ≠ 0`.

This module does not construct the physical Regge–Wheeler carrier, establish
the asymptotic BMS-memory limit, or provide detector calibration.
-/

/--
Dimensionless memory–visibility ratio constructed from two operational
observables.
-/
def reggeWheelerMemoryVisibilityRatio
    (visibility memoryShift : ℝ) :
    ℝ :=
  (-2 * Real.log visibility) / memoryShift ^ 2

/--
The coherent soft-memory visibility law predicts the exact parameter-free
memory–visibility ratio `1/2` for every nonzero memory shift.
-/
theorem finiteCoherentMemoryVisibilityRatio_eq_half
    (memoryShift : ℝ)
    (hMemoryShift : memoryShift ≠ 0) :
    reggeWheelerMemoryVisibilityRatio
        (finiteCoherentSoftMemoryVisibility memoryShift)
        memoryShift =
      (1 : ℝ) / 2 := by
  unfold
    reggeWheelerMemoryVisibilityRatio
    finiteCoherentSoftMemoryVisibility
  rw [Real.log_exp]
  have hSquare : memoryShift ^ 2 ≠ 0 :=
    pow_ne_zero 2 hMemoryShift
  apply (div_eq_iff hSquare).2
  ring

/--
Specialization of the parameter-free ratio prediction to the gauge-invariant
first-order Regge–Wheeler-derived memory shift.
-/
theorem reggeWheelerDerivedMemoryVisibilityRatio_eq_half
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier : ReggeWheelerGaugeInvariantCarrier Raw Gauge)
    (deviation : ReggeWheelerFirstOrderDeviationData Raw)
    (rMinus rPlus calibration lambda : ℝ)
    (hCalibration : calibration ≠ 0)
    (hEndpointResponse :
      reggeWheelerRawMemoryObservable
          carrier
          rMinus
          rPlus
          (deviation.background +
            lambda • deviation.firstOrderCorrection) ≠
        0) :
    reggeWheelerMemoryVisibilityRatio
        (finiteCoherentSoftMemoryVisibility
          (reggeWheelerFirstOrderMemoryShift
            carrier
            deviation
            rMinus
            rPlus
            calibration
            lambda))
        (reggeWheelerFirstOrderMemoryShift
          carrier
          deviation
          rMinus
          rPlus
          calibration
          lambda) =
      (1 : ℝ) / 2 := by
  apply finiteCoherentMemoryVisibilityRatio_eq_half
  exact
    reggeWheelerFirstOrderMemoryShift_ne_zero
      carrier
      deviation
      rMinus
      rPlus
      calibration
      lambda
      hCalibration
      hEndpointResponse

/--
Difference between the zero-correlated-memory discriminator and the coherent
memory discriminator when both are evaluated at the coherent visibility.
-/
def reggeWheelerMemoryVisibilityZeroMemoryGap
    (memoryShift : ℝ) :
    ℝ :=
  finiteSoftMemoryDiscriminator
      (finiteCoherentSoftMemoryVisibility memoryShift)
      0 -
    finiteSoftMemoryDiscriminator
      (finiteCoherentSoftMemoryVisibility memoryShift)
      memoryShift

/--
The zero-memory alternative differs from the coherent-memory prediction by the
exact measurable amount `memoryShift² / 2`.
-/
theorem reggeWheelerMemoryVisibilityZeroMemoryGap_eq
    (memoryShift : ℝ) :
    reggeWheelerMemoryVisibilityZeroMemoryGap memoryShift =
      memoryShift ^ 2 / 2 := by
  unfold reggeWheelerMemoryVisibilityZeroMemoryGap
  rw [
    finiteCoherentVisibility_zeroMemoryDiscriminator,
    finiteCoherentSoftMemoryDiscriminator_zero
  ]
  ring

/--
Every nonzero memory shift produces a strictly positive separation from the
zero-correlated-memory alternative at the same visibility.
-/
theorem reggeWheelerMemoryVisibilityZeroMemoryGap_pos
    (memoryShift : ℝ)
    (hMemoryShift : memoryShift ≠ 0) :
    0 <
      reggeWheelerMemoryVisibilityZeroMemoryGap memoryShift := by
  rw [reggeWheelerMemoryVisibilityZeroMemoryGap_eq]
  have hSquare : 0 < memoryShift ^ 2 := by
    simpa [pow_two] using (mul_self_pos.mpr hMemoryShift)
  exact div_pos hSquare (by norm_num)

def reggeWheelerMemoryVisibilityPredictionStatus : String :=
  "PARAMETER_FREE_MEMORY_VISIBILITY_RATIO_AND_POSITIVE_ZERO_MEMORY_GAP"

def reggeWheelerMemoryVisibilityPredictionBoundary : String :=
  "PHYSICAL_MASTER_EXTRACTION_BMS_LIMIT_CALIBRATION_UNCERTAINTY_AND_NOVELTY_CERTIFICATION_NOT_CLOSED"

end
end Chronos.Frontier
