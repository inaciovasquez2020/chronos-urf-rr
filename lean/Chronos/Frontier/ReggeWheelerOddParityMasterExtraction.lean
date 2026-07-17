import Mathlib
import Chronos.Frontier.ReggeWheelerGaugeInvariantMemoryChannel

namespace Chronos.Frontier

noncomputable section

abbrev ReggeWheelerOddParityRadialJet :=
  (ℝ → ℝ) × ((ℝ → ℝ) × (ℝ → ℝ))

abbrev ReggeWheelerOddParityGaugeJet :=
  (ℝ → ℝ) × (ℝ → ℝ)

def reggeWheelerOddParityMasterField :
    ReggeWheelerOddParityRadialJet →ₗ[ℝ] (ℝ → ℝ) where
  toFun rawState :=
    fun rStar =>
      rawState.1 rStar -
        (1 / 2 : ℝ) * rawState.2.1 rStar +
        rawState.2.2 rStar
  map_add' := by
    intro left right
    funext rStar
    simp
    ring
  map_smul' := by
    intro scalar rawState
    funext rStar
    simp [smul_eq_mul]
    ring

def reggeWheelerOddParityGaugeShift :
    ReggeWheelerOddParityGaugeJet →ₗ[ℝ]
      ReggeWheelerOddParityRadialJet where
  toFun gaugeParameter :=
    (
      fun rStar =>
        -gaugeParameter.1 rStar +
          2 * gaugeParameter.2 rStar,
      (
        fun rStar =>
          -2 * gaugeParameter.1 rStar,
        fun rStar =>
          -2 * gaugeParameter.2 rStar
      )
    )
  map_add' := by
    intro left right
    apply Prod.ext
    · funext rStar
      simp
      ring
    · apply Prod.ext
      · funext rStar
        simp
        ring
      · funext rStar
        simp
        ring
  map_smul' := by
    intro scalar gaugeParameter
    apply Prod.ext
    · funext rStar
      simp [smul_eq_mul]
      ring
    · apply Prod.ext
      · funext rStar
        simp [smul_eq_mul]
        ring
      · funext rStar
        simp [smul_eq_mul]
        ring

theorem reggeWheelerOddParityMasterField_gaugeShift_zero
    (gaugeParameter : ReggeWheelerOddParityGaugeJet) :
    reggeWheelerOddParityMasterField
        (reggeWheelerOddParityGaugeShift gaugeParameter) =
      0 := by
  funext rStar
  simp [
    reggeWheelerOddParityMasterField,
    reggeWheelerOddParityGaugeShift
  ]

def reggeWheelerOddParityGaugeInvariantCarrier :
    ReggeWheelerGaugeInvariantCarrier
      ReggeWheelerOddParityRadialJet
      ReggeWheelerOddParityGaugeJet where
  masterField :=
    reggeWheelerOddParityMasterField
  gaugeShift :=
    reggeWheelerOddParityGaugeShift
  masterField_gaugeShift_zero :=
    reggeWheelerOddParityMasterField_gaugeShift_zero

def reggeWheelerOddParityGaugeTransform
    (rawState : ReggeWheelerOddParityRadialJet)
    (gaugeParameter : ReggeWheelerOddParityGaugeJet) :
    ReggeWheelerOddParityRadialJet :=
  reggeWheelerGaugeTransform
    reggeWheelerOddParityGaugeInvariantCarrier
    rawState
    gaugeParameter

theorem reggeWheelerOddParityMasterField_gaugeInvariant
    (rawState : ReggeWheelerOddParityRadialJet)
    (gaugeParameter : ReggeWheelerOddParityGaugeJet) :
    reggeWheelerOddParityMasterField
        (reggeWheelerOddParityGaugeTransform
          rawState
          gaugeParameter) =
      reggeWheelerOddParityMasterField rawState := by
  simpa [
    reggeWheelerOddParityGaugeTransform,
    reggeWheelerOddParityGaugeInvariantCarrier
  ] using
    reggeWheelerMasterField_gaugeInvariant
      reggeWheelerOddParityGaugeInvariantCarrier
      rawState
      gaugeParameter

def reggeWheelerOddParityMemoryObservable
    (rMinus rPlus : ℝ) :
    ReggeWheelerOddParityRadialJet →ₗ[ℝ] ℝ :=
  reggeWheelerRawMemoryObservable
    reggeWheelerOddParityGaugeInvariantCarrier
    rMinus
    rPlus

def reggeWheelerOddParityMemoryShift
    (rMinus rPlus : ℝ)
    (rawState : ReggeWheelerOddParityRadialJet) :
    ℝ :=
  reggeWheelerOddParityMemoryObservable
    rMinus
    rPlus
    rawState

theorem reggeWheelerOddParityMemoryShift_eq_endpoint
    (rMinus rPlus : ℝ)
    (rawState : ReggeWheelerOddParityRadialJet) :
    reggeWheelerOddParityMemoryShift
        rMinus
        rPlus
        rawState =
      reggeWheelerOddParityMasterField rawState rPlus -
        reggeWheelerOddParityMasterField rawState rMinus := by
  rfl

theorem reggeWheelerOddParityMemoryShift_gaugeInvariant
    (rMinus rPlus : ℝ)
    (rawState : ReggeWheelerOddParityRadialJet)
    (gaugeParameter : ReggeWheelerOddParityGaugeJet) :
    reggeWheelerOddParityMemoryShift
        rMinus
        rPlus
        (reggeWheelerOddParityGaugeTransform
          rawState
          gaugeParameter) =
      reggeWheelerOddParityMemoryShift
        rMinus
        rPlus
        rawState := by
  simpa [
    reggeWheelerOddParityMemoryShift,
    reggeWheelerOddParityMemoryObservable,
    reggeWheelerOddParityGaugeTransform
  ] using
    reggeWheelerRawMemoryObservable_gaugeInvariant
      reggeWheelerOddParityGaugeInvariantCarrier
      rMinus
      rPlus
      rawState
      gaugeParameter

def reggeWheelerOddParityFirstOrderMemoryShift
    (deviation :
      ReggeWheelerFirstOrderDeviationData
        ReggeWheelerOddParityRadialJet)
    (rMinus rPlus lambda : ℝ) :
    ℝ :=
  reggeWheelerOddParityMemoryShift
    rMinus
    rPlus
    (deviation.background +
      lambda • deviation.firstOrderCorrection)

theorem reggeWheelerOddParityFirstOrderMemoryShift_expansion
    (deviation :
      ReggeWheelerFirstOrderDeviationData
        ReggeWheelerOddParityRadialJet)
    (rMinus rPlus lambda : ℝ) :
    reggeWheelerOddParityFirstOrderMemoryShift
        deviation
        rMinus
        rPlus
        lambda =
      reggeWheelerOddParityMemoryShift
          rMinus
          rPlus
          deviation.background +
        lambda *
          reggeWheelerOddParityMemoryShift
            rMinus
            rPlus
            deviation.firstOrderCorrection := by
  unfold
    reggeWheelerOddParityFirstOrderMemoryShift
    reggeWheelerOddParityMemoryShift
  rw [map_add, map_smul]
  simp [smul_eq_mul]

theorem reggeWheelerOddParityCoherentDiscriminator_zero
    (rMinus rPlus : ℝ)
    (rawState : ReggeWheelerOddParityRadialJet) :
    finiteSoftMemoryDiscriminator
        (finiteCoherentSoftMemoryVisibility
          (reggeWheelerOddParityMemoryShift
            rMinus
            rPlus
            rawState))
        (reggeWheelerOddParityMemoryShift
          rMinus
          rPlus
          rawState) =
      0 :=
  finiteCoherentSoftMemoryDiscriminator_zero
    (reggeWheelerOddParityMemoryShift
      rMinus
      rPlus
      rawState)

theorem reggeWheelerOddParityMemory_distinguishesGenericDephasing
    (rMinus rPlus : ℝ)
    (rawState : ReggeWheelerOddParityRadialJet)
    (hMemory :
      reggeWheelerOddParityMemoryShift
          rMinus
          rPlus
          rawState ≠
        0) :
    finiteSoftMemoryDiscriminator
        (finiteCoherentSoftMemoryVisibility
          (reggeWheelerOddParityMemoryShift
            rMinus
            rPlus
            rawState))
        0 ≠
      finiteSoftMemoryDiscriminator
        (finiteCoherentSoftMemoryVisibility
          (reggeWheelerOddParityMemoryShift
            rMinus
            rPlus
            rawState))
        (reggeWheelerOddParityMemoryShift
          rMinus
          rPlus
          rawState) :=
  finiteNonzeroCoherentMemory_distinguishesGenericDephasing
    (reggeWheelerOddParityMemoryShift
      rMinus
      rPlus
      rawState)
    hMemory

def reggeWheelerOddParityUnitMemoryJet :
    ReggeWheelerOddParityRadialJet :=
  (
    fun rStar => rStar,
    (
      fun _ => 0,
      fun _ => 0
    )
  )

theorem reggeWheelerOddParityUnitMemoryJet_master
    (rStar : ℝ) :
    reggeWheelerOddParityMasterField
        reggeWheelerOddParityUnitMemoryJet
        rStar =
      rStar := by
  simp [
    reggeWheelerOddParityMasterField,
    reggeWheelerOddParityUnitMemoryJet
  ]

theorem reggeWheelerOddParityUnitMemoryShift_eq_one :
    reggeWheelerOddParityMemoryShift
        0
        1
        reggeWheelerOddParityUnitMemoryJet =
      1 := by
  rw [reggeWheelerOddParityMemoryShift_eq_endpoint]
  norm_num [reggeWheelerOddParityUnitMemoryJet_master]

theorem reggeWheelerOddParityUnitMemoryShift_ne_zero :
    reggeWheelerOddParityMemoryShift
        0
        1
        reggeWheelerOddParityUnitMemoryJet ≠
      0 := by
  rw [reggeWheelerOddParityUnitMemoryShift_eq_one]
  norm_num

theorem reggeWheelerOddParityConcreteNonzeroDistinction :
    finiteSoftMemoryDiscriminator
        (finiteCoherentSoftMemoryVisibility
          (reggeWheelerOddParityMemoryShift
            0
            1
            reggeWheelerOddParityUnitMemoryJet))
        0 ≠
      finiteSoftMemoryDiscriminator
        (finiteCoherentSoftMemoryVisibility
          (reggeWheelerOddParityMemoryShift
            0
            1
            reggeWheelerOddParityUnitMemoryJet))
        (reggeWheelerOddParityMemoryShift
          0
          1
          reggeWheelerOddParityUnitMemoryJet) :=
  reggeWheelerOddParityMemory_distinguishesGenericDephasing
    0
    1
    reggeWheelerOddParityUnitMemoryJet
    reggeWheelerOddParityUnitMemoryShift_ne_zero

def reggeWheelerOddParityMasterExtractionStatus : String :=
  "CONCRETE_ODD_PARITY_RADIAL_JET_MASTER_EXTRACTION_MEMORY_AND_NONZERO_DISCRIMINATOR"

def reggeWheelerOddParityMasterExtractionBoundary : String :=
  "RADIAL_JET_INTEGRABILITY_ASYMPTOTIC_BMS_IDENTIFICATION_AND_DIMENSIONFUL_DETECTOR_CALIBRATION_NOT_PROVED"

end

end Chronos.Frontier
