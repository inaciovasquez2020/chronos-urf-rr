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

-- DERIVED_COUPLED_ODD_PARITY_MEMORY_SHIFT

/--
Odd-parity memory response carried by the action-derived coupled system.

The gravitational correction enters at order `ε²`.
-/
def reggeWheelerOddParityDerivedFirstOrderMemoryShift
    (deviation :
      ReggeWheelerDerivedCoupledResponseData
        ReggeWheelerOddParityRadialJet)
    (rMinus rPlus : ℝ) :
    ℝ :=
  reggeWheelerOddParityMemoryShift
    rMinus
    rPlus
    (deviation.background +
      deviation.epsilon ^ 2 •
        deviation.gravitationalFirstOrder)

-- DERIVED_COUPLED_ODD_PARITY_MEMORY_SHIFT_EXPANSION

/--
Exact expansion of the action-derived odd-parity memory response:

  M(Ψ₀ + ε² Ψ₁) = M(Ψ₀) + ε² M(Ψ₁).
-/
theorem reggeWheelerOddParityDerivedFirstOrderMemoryShift_expansion
    (deviation :
      ReggeWheelerDerivedCoupledResponseData
        ReggeWheelerOddParityRadialJet)
    (rMinus rPlus : ℝ) :
    reggeWheelerOddParityDerivedFirstOrderMemoryShift
        deviation
        rMinus
        rPlus =
      reggeWheelerOddParityMemoryShift
          rMinus
          rPlus
          deviation.background +
        deviation.epsilon ^ 2 *
          reggeWheelerOddParityMemoryShift
            rMinus
            rPlus
            deviation.gravitationalFirstOrder := by
  unfold
    reggeWheelerOddParityDerivedFirstOrderMemoryShift
    reggeWheelerOddParityMemoryShift
  rw [map_add, map_smul]
  simp [smul_eq_mul]

-- DERIVED_COUPLED_ODD_PARITY_MEMORY_NONZERO

/--
A nonzero coupling parameter and nonzero correction memory imply that the
action-derived total memory differs from its background value.
-/
theorem reggeWheelerOddParityDerivedFirstOrderMemoryShift_ne_background
    (deviation :
      ReggeWheelerDerivedCoupledResponseData
        ReggeWheelerOddParityRadialJet)
    (rMinus rPlus : ℝ)
    (hEpsilon : deviation.epsilon ≠ 0)
    (hCorrectionMemory :
      reggeWheelerOddParityMemoryShift
          rMinus
          rPlus
          deviation.gravitationalFirstOrder ≠
        0) :
    reggeWheelerOddParityDerivedFirstOrderMemoryShift
        deviation
        rMinus
        rPlus ≠
      reggeWheelerOddParityMemoryShift
        rMinus
        rPlus
        deviation.background := by
  rw [
    reggeWheelerOddParityDerivedFirstOrderMemoryShift_expansion
  ]
  intro hEqual
  have hProduct :
      deviation.epsilon ^ 2 *
          reggeWheelerOddParityMemoryShift
            rMinus
            rPlus
            deviation.gravitationalFirstOrder =
        0 := by
    linarith
  exact
    (mul_ne_zero
      (pow_ne_zero 2 hEpsilon)
      hCorrectionMemory)
      hProduct

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

-- CONCRETE_PROFILE_AND_COUPLING

/--
Concrete benchmark profile `p`.

It is the already-certified unit-memory odd-parity radial jet.
-/
def reggeWheelerOddParityConcreteProfile :
    ReggeWheelerOddParityRadialJet :=
  reggeWheelerOddParityUnitMemoryJet

/--
Concrete benchmark coupling `W`.

This bounded algebraic witness uses the identity coupling. It is not asserted
to be the coupling obtained from a covariant action.
-/
def reggeWheelerOddParityConcreteCoupling :
    ReggeWheelerOddParityRadialJet →ₗ[ℝ]
      ReggeWheelerOddParityRadialJet :=
  LinearMap.id

/-- Exact computation `W (W p) = p`. -/
theorem reggeWheelerOddParityConcreteCoupling_squared_profile :
    reggeWheelerOddParityConcreteCoupling
        (reggeWheelerOddParityConcreteCoupling
          reggeWheelerOddParityConcreteProfile) =
      reggeWheelerOddParityConcreteProfile := by
  rfl

-- CONCRETE_ENDPOINT_SEPARATION

/-- The selected endpoints satisfy `r₋ < r₊`. -/
theorem reggeWheelerOddParityConcreteEndpoints_lt :
    (0 : ℝ) < 1 := by
  norm_num

/--
The master field of `W (W p)` has unequal values at the selected endpoints.
-/
theorem reggeWheelerOddParityConcreteDoubleCoupling_endpoints_ne :
    reggeWheelerOddParityMasterField
          (reggeWheelerOddParityConcreteCoupling
            (reggeWheelerOddParityConcreteCoupling
              reggeWheelerOddParityConcreteProfile))
          0 ≠
      reggeWheelerOddParityMasterField
          (reggeWheelerOddParityConcreteCoupling
            (reggeWheelerOddParityConcreteCoupling
              reggeWheelerOddParityConcreteProfile))
          1 := by
  simp [
    reggeWheelerOddParityConcreteCoupling,
    reggeWheelerOddParityConcreteProfile,
    reggeWheelerOddParityUnitMemoryJet_master
  ]

/-- Consequently, the endpoint memory of `W (W p)` is nonzero. -/
theorem reggeWheelerOddParityConcreteDoubleCoupling_memory_ne_zero :
    reggeWheelerOddParityMemoryShift
          0
          1
          (reggeWheelerOddParityConcreteCoupling
            (reggeWheelerOddParityConcreteCoupling
              reggeWheelerOddParityConcreteProfile)) ≠
      0 := by
  simpa [
    reggeWheelerOddParityConcreteCoupling,
    reggeWheelerOddParityConcreteProfile
  ] using
    reggeWheelerOddParityUnitMemoryShift_ne_zero


-- CONCRETE_W2P_DERIVATIVE_CERTIFICATE

/--
Concrete derivative data with

  θ₁''(0) = -W p,
  Ψ₁⁽⁴⁾(0) = W (W p).
-/
def reggeWheelerOddParityConcreteDerivativeCertificate :
    ReggeWheelerDerivativeCertificateData
      ReggeWheelerOddParityRadialJet where
  coupling :=
    reggeWheelerOddParityConcreteCoupling
  profile :=
    reggeWheelerOddParityConcreteProfile
  scalarSecondDerivativeAtZero :=
    -reggeWheelerOddParityConcreteProfile
  psiFourthDerivativeAtZero :=
    reggeWheelerOddParityConcreteProfile
  scalarSecondDerivativeEquation := by
    simp [reggeWheelerOddParityConcreteCoupling]
  psiFourthDerivativeEquation := by
    simp [reggeWheelerOddParityConcreteCoupling]

/-- The concrete fourth derivative is exactly `W (W p)`. -/
theorem reggeWheelerOddParityConcretePsiFourthDerivative_eq_W2p :
    (reggeWheelerOddParityConcreteDerivativeCertificate).psiFourthDerivativeAtZero =
      reggeWheelerOddParityConcreteCoupling
        (reggeWheelerOddParityConcreteCoupling
          reggeWheelerOddParityConcreteProfile) :=
  reggeWheelerPsiOneFourthDerivativeAtZero
    reggeWheelerOddParityConcreteDerivativeCertificate


-- CONCRETE_DERIVED_MEMORY_RESPONSE

/--
Concrete coupled response carrier whose gravitational correction is the
certified `W²p` state.
-/
def reggeWheelerOddParityConcreteDerivedResponse :
    ReggeWheelerDerivedCoupledResponseData
      ReggeWheelerOddParityRadialJet where
  reggeWheelerOperator := 0
  scalarOperator := 0
  coupling :=
    reggeWheelerOddParityConcreteCoupling
  scalarCorrection := 0
  epsilon := 1
  background := 0
  scalarFirstOrder := 0
  gravitationalFirstOrder :=
    (reggeWheelerOddParityConcreteDerivativeCertificate).psiFourthDerivativeAtZero
  backgroundEquation := by
    simp
  scalarFirstOrderEquation := by
    simp [reggeWheelerOddParityConcreteCoupling]
  gravitationalFirstOrderEquation := by
    simp [reggeWheelerOddParityConcreteCoupling]

/--
The concrete derived gauge-invariant memory differs from its background
memory.
-/
theorem
    reggeWheelerOddParityConcreteDerivedMemoryShift_ne_background :
    reggeWheelerOddParityDerivedFirstOrderMemoryShift
          reggeWheelerOddParityConcreteDerivedResponse
          0
          1 ≠
      reggeWheelerOddParityMemoryShift
        0
        1
        reggeWheelerOddParityConcreteDerivedResponse.background := by
  apply
    reggeWheelerOddParityDerivedFirstOrderMemoryShift_ne_background
  · norm_num [reggeWheelerOddParityConcreteDerivedResponse]
  · change
      reggeWheelerOddParityMemoryShift
          0
          1
          (reggeWheelerOddParityConcreteDerivativeCertificate).psiFourthDerivativeAtZero ≠
        0
    rw [reggeWheelerOddParityConcretePsiFourthDerivative_eq_W2p]
    exact
      reggeWheelerOddParityConcreteDoubleCoupling_memory_ne_zero

def reggeWheelerOddParityConcreteDerivedMemoryBoundary : String :=
  "IDENTITY_COUPLING_BENCHMARK_ONLY_NOT_A_COVARIANT_ACTION_DERIVATION"

end

end Chronos.Frontier
