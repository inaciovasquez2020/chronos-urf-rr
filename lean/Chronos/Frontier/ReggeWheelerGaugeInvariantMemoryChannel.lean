import Mathlib
import Chronos.Frontier.ReggeWheelerConditionalDeviation
import Chronos.Frontier.FiniteHardSoftHamiltonianChannel

namespace Chronos.Frontier

noncomputable section

/-!
# Gauge-invariant Regge–Wheeler endpoint-memory channel

This module defines a bounded, repository-native memory observable on an
extracted Regge–Wheeler master profile:

`M_[r₋,r₊](Ψ) = Ψ(r₊) - Ψ(r₋)`.

A raw perturbation carrier supplies:

* a linear master-field extraction;
* a linear gauge shift;
* a proof that every gauge shift lies in the kernel of the master extraction.

The resulting endpoint observable and calibrated memory shift are then gauge
invariant.

This is not yet a physical BMS-memory theorem. In particular, the carrier does
not construct the odd-parity gauge transformation, derive the master field from
metric perturbations, prove asymptotic limits, or calibrate the endpoint
difference to an observed gravitational-memory displacement.
-/

/--
A raw perturbation carrier together with a gauge-invariant Regge–Wheeler
master-field extraction.

The field `masterField_gaugeShift_zero` is the exact missing physical
invariance condition. Once inhabited by a concrete odd-parity construction,
all downstream observables in this module are gauge invariant.
-/
structure ReggeWheelerGaugeInvariantCarrier
    (Raw Gauge : Type*)
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge] where
  masterField : Raw →ₗ[ℝ] (ℝ → ℝ)
  gaugeShift : Gauge →ₗ[ℝ] Raw
  masterField_gaugeShift_zero :
    ∀ gaugeParameter : Gauge,
      masterField (gaugeShift gaugeParameter) = 0

/-- Raw-state gauge transformation. -/
def reggeWheelerGaugeTransform
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
    (rawState : Raw)
    (gaugeParameter : Gauge) :
    Raw :=
  rawState + carrier.gaugeShift gaugeParameter

/-- The extracted master field is invariant under the encoded gauge action. -/
theorem reggeWheelerMasterField_gaugeInvariant
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
    (rawState : Raw)
    (gaugeParameter : Gauge) :
    carrier.masterField
        (reggeWheelerGaugeTransform
          carrier
          rawState
          gaugeParameter) =
      carrier.masterField rawState := by
  unfold reggeWheelerGaugeTransform
  rw [
    map_add,
    carrier.masterField_gaugeShift_zero gaugeParameter,
    add_zero
  ]

/--
Bounded endpoint-memory observable on a Regge–Wheeler master profile:

`Ψ(rPlus) - Ψ(rMinus)`.
-/
def reggeWheelerEndpointMemoryObservable
    (rMinus rPlus : ℝ) :
    (ℝ → ℝ) →ₗ[ℝ] ℝ where
  toFun masterProfile :=
    masterProfile rPlus - masterProfile rMinus
  map_add' := by
    intro left right
    simp
    ring
  map_smul' := by
    intro scalar profile
    simp [smul_eq_mul, mul_sub]

/--
The endpoint-memory observable pulled back from the gauge-invariant master
field to raw perturbation states.
-/
def reggeWheelerRawMemoryObservable
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
    (rMinus rPlus : ℝ) :
    Raw →ₗ[ℝ] ℝ :=
  (reggeWheelerEndpointMemoryObservable
    rMinus
    rPlus).comp carrier.masterField

/-- The pulled-back endpoint-memory observable is gauge invariant. -/
theorem reggeWheelerRawMemoryObservable_gaugeInvariant
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
    (rMinus rPlus : ℝ)
    (rawState : Raw)
    (gaugeParameter : Gauge) :
    reggeWheelerRawMemoryObservable
        carrier
        rMinus
        rPlus
        (reggeWheelerGaugeTransform
          carrier
          rawState
          gaugeParameter) =
      reggeWheelerRawMemoryObservable
        carrier
        rMinus
        rPlus
        rawState := by
  change
    reggeWheelerEndpointMemoryObservable
        rMinus
        rPlus
        (carrier.masterField
          (reggeWheelerGaugeTransform
            carrier
            rawState
            gaugeParameter)) =
      reggeWheelerEndpointMemoryObservable
        rMinus
        rPlus
        (carrier.masterField rawState)
  rw [
    reggeWheelerMasterField_gaugeInvariant
      carrier
      rawState
      gaugeParameter
  ]

/--
The detector-normalized memory-shift map

`memoryShift = calibration × endpointMemory`.
-/
def reggeWheelerDerivedMemoryShiftMap
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
    (rMinus rPlus calibration : ℝ) :
    Raw →ₗ[ℝ] ℝ :=
  calibration •
    reggeWheelerRawMemoryObservable
      carrier
      rMinus
      rPlus

/-- The calibrated memory shift remains gauge invariant. -/
theorem reggeWheelerDerivedMemoryShift_gaugeInvariant
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
    (rMinus rPlus calibration : ℝ)
    (rawState : Raw)
    (gaugeParameter : Gauge) :
    reggeWheelerDerivedMemoryShiftMap
        carrier
        rMinus
        rPlus
        calibration
        (reggeWheelerGaugeTransform
          carrier
          rawState
          gaugeParameter) =
      reggeWheelerDerivedMemoryShiftMap
        carrier
        rMinus
        rPlus
        calibration
        rawState := by
  change
    calibration *
        reggeWheelerRawMemoryObservable
          carrier
          rMinus
          rPlus
          (reggeWheelerGaugeTransform
            carrier
            rawState
            gaugeParameter) =
      calibration *
        reggeWheelerRawMemoryObservable
          carrier
          rMinus
          rPlus
          rawState
  rw [
    reggeWheelerRawMemoryObservable_gaugeInvariant
      carrier
      rMinus
      rPlus
      rawState
      gaugeParameter
  ]

/--
The repository-native first-order Regge–Wheeler approximation used as the
input to the memory observable.
-/
def reggeWheelerFirstOrderMemoryShift
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
    (deviation : ReggeWheelerFirstOrderDeviationData Raw)
    (rMinus rPlus calibration lambda : ℝ) :
    ℝ :=
  reggeWheelerDerivedMemoryShiftMap
    carrier
    rMinus
    rPlus
    calibration
    (deviation.background +
      lambda • deviation.firstOrderCorrection)

/-- Exact first-order expansion of the derived memory shift. -/
theorem reggeWheelerFirstOrderMemoryShift_expansion
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
    (deviation : ReggeWheelerFirstOrderDeviationData Raw)
    (rMinus rPlus calibration lambda : ℝ) :
    reggeWheelerFirstOrderMemoryShift
        carrier
        deviation
        rMinus
        rPlus
        calibration
        lambda =
      reggeWheelerDerivedMemoryShiftMap
          carrier
          rMinus
          rPlus
          calibration
          deviation.background +
        lambda *
          reggeWheelerDerivedMemoryShiftMap
            carrier
            rMinus
            rPlus
            calibration
            deviation.firstOrderCorrection := by
  unfold reggeWheelerFirstOrderMemoryShift
  rw [map_add, map_smul]
  simp [smul_eq_mul]

/-- The first-order memory shift is gauge invariant as a raw-state observable. -/
theorem reggeWheelerFirstOrderMemoryShift_gaugeInvariant
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
    (deviation : ReggeWheelerFirstOrderDeviationData Raw)
    (rMinus rPlus calibration lambda : ℝ)
    (gaugeParameter : Gauge) :
    reggeWheelerDerivedMemoryShiftMap
        carrier
        rMinus
        rPlus
        calibration
        (reggeWheelerGaugeTransform
          carrier
          (deviation.background +
            lambda • deviation.firstOrderCorrection)
          gaugeParameter) =
      reggeWheelerFirstOrderMemoryShift
        carrier
        deviation
        rMinus
        rPlus
        calibration
        lambda := by
  rw [
    reggeWheelerDerivedMemoryShift_gaugeInvariant
      carrier
      rMinus
      rPlus
      calibration
      (deviation.background +
        lambda • deviation.firstOrderCorrection)
      gaugeParameter
  ]
  rfl

/-- Nonzero calibration and nonzero endpoint response give nonzero memory. -/
theorem reggeWheelerFirstOrderMemoryShift_ne_zero
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
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
    reggeWheelerFirstOrderMemoryShift
        carrier
        deviation
        rMinus
        rPlus
        calibration
        lambda ≠
      0 := by
  unfold reggeWheelerFirstOrderMemoryShift
  change
    calibration *
        reggeWheelerRawMemoryObservable
          carrier
          rMinus
          rPlus
          (deviation.background +
            lambda • deviation.firstOrderCorrection) ≠
      0
  exact mul_ne_zero hCalibration hEndpointResponse

/--
Substitution of any Regge–Wheeler-derived memory shift into the coherent
visibility discriminator gives the exact coherent-memory value zero.
-/
theorem reggeWheelerDerivedMemory_coherentDiscriminator_zero
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
    (deviation : ReggeWheelerFirstOrderDeviationData Raw)
    (rMinus rPlus calibration lambda : ℝ) :
    finiteSoftMemoryDiscriminator
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
      0 :=
  finiteCoherentSoftMemoryDiscriminator_zero
    (reggeWheelerFirstOrderMemoryShift
      carrier
      deviation
      rMinus
      rPlus
      calibration
      lambda)

/--
At the same coherent visibility, a model carrying zero correlated memory
has discriminator value `memoryShift² / 2`.
-/
theorem finiteCoherentVisibility_zeroMemoryDiscriminator
    (memoryShift : ℝ) :
    finiteSoftMemoryDiscriminator
        (finiteCoherentSoftMemoryVisibility memoryShift)
        0 =
      memoryShift ^ 2 / 2 := by
  unfold
    finiteSoftMemoryDiscriminator
    finiteCoherentSoftMemoryVisibility
  rw [Real.log_exp]
  ring

/--
Every nonzero coherent memory shift distinguishes the coherent-memory
prediction from generic dephasing with the same visibility but no correlated
memory record.
-/
theorem finiteNonzeroCoherentMemory_distinguishesGenericDephasing
    (memoryShift : ℝ)
    (hMemoryShift : memoryShift ≠ 0) :
    finiteSoftMemoryDiscriminator
        (finiteCoherentSoftMemoryVisibility memoryShift)
        0 ≠
      finiteSoftMemoryDiscriminator
        (finiteCoherentSoftMemoryVisibility memoryShift)
        memoryShift := by
  rw [
    finiteCoherentVisibility_zeroMemoryDiscriminator,
    finiteCoherentSoftMemoryDiscriminator_zero
  ]
  exact
    div_ne_zero
      (pow_ne_zero 2 hMemoryShift)
      (by norm_num)

/--
Final nonzero distinction theorem for the Regge–Wheeler-derived memory
observable.
-/
theorem reggeWheelerMemory_distinguishesGenericDephasing
    {Raw Gauge : Type*}
    [AddCommGroup Raw]
    [Module ℝ Raw]
    [AddCommGroup Gauge]
    [Module ℝ Gauge]
    (carrier :
      ReggeWheelerGaugeInvariantCarrier Raw Gauge)
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
    finiteSoftMemoryDiscriminator
        (finiteCoherentSoftMemoryVisibility
          (reggeWheelerFirstOrderMemoryShift
            carrier
            deviation
            rMinus
            rPlus
            calibration
            lambda))
        0 ≠
      finiteSoftMemoryDiscriminator
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
          lambda) := by
  apply
    finiteNonzeroCoherentMemory_distinguishesGenericDephasing
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

def reggeWheelerGaugeInvariantMemoryChannelStatus : String :=
  "GAUGE_INVARIANT_ENDPOINT_MEMORY_CHANNEL_AND_NONZERO_DISCRIMINATOR"

def reggeWheelerGaugeInvariantMemoryChannelBoundary : String :=
  "ODD_PARITY_MASTER_EXTRACTION_ASYMPTOTIC_BMS_LIMIT_AND_PHYSICAL_CALIBRATION_NOT_CONSTRUCTED"

end

end Chronos.Frontier
