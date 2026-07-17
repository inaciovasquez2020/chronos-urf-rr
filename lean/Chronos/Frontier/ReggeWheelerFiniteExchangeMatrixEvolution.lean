import Mathlib
import Chronos.Frontier.FiniteHardSoftHamiltonianChannel
import Chronos.Frontier.ReggeWheelerOddParityMasterExtraction

namespace Chronos.Frontier

noncomputable section

abbrev FiniteExchangeComplexMatrix :=
  Matrix FiniteExchangeBasis FiniteExchangeBasis ℂ

abbrev FiniteExchangeComplexState :=
  FiniteExchangeBasis → ℂ

def finiteExchangeHamiltonianMatrix
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    FiniteExchangeComplexMatrix :=
  fun i j =>
    (finiteExchangeHamiltonianEntry H k i j : ℂ)

def finiteExchangeChargeMatrix :
    FiniteExchangeComplexMatrix :=
  fun i j =>
    if i = j then
      (finiteExchangeCharge i : ℂ)
    else
      0

def finiteExchangeMatrixAdjoint
    (M : FiniteExchangeComplexMatrix) :
    FiniteExchangeComplexMatrix :=
  fun i j =>
    star (M j i)

theorem finiteExchangeHamiltonianMatrix_adjoint_eq
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    finiteExchangeMatrixAdjoint
        (finiteExchangeHamiltonianMatrix H k) =
      finiteExchangeHamiltonianMatrix H k := by
  ext i j
  cases i <;> cases j <;>
    simp [
      finiteExchangeMatrixAdjoint,
      finiteExchangeHamiltonianMatrix,
      finiteExchangeHamiltonianEntry
    ]

def finiteExchangeChargeCommutatorMatrix
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    FiniteExchangeComplexMatrix :=
  fun i j =>
    finiteExchangeHamiltonianMatrix H k i j *
        finiteExchangeChargeMatrix j j -
      finiteExchangeChargeMatrix i i *
        finiteExchangeHamiltonianMatrix H k i j

theorem finiteExchangeHamiltonianMatrix_chargeCommutator_zero
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    finiteExchangeChargeCommutatorMatrix H k =
      0 := by
  ext i j
  cases i <;> cases j <;>
    simp [
      finiteExchangeChargeCommutatorMatrix,
      finiteExchangeHamiltonianMatrix,
      finiteExchangeChargeMatrix,
      finiteExchangeHamiltonianEntry,
      finiteExchangeCharge
    ]

def finiteExchangeResidualKet :
    FiniteExchangeComplexState
  | .residual => 1
  | _ => 0

def finiteExchangeHardKet :
    FiniteExchangeComplexState
  | .hard => 1
  | _ => 0

def finiteExchangeSoftKet :
    FiniteExchangeComplexState
  | .soft => 1
  | _ => 0

def finiteExchangeBrightKet
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    FiniteExchangeComplexState
  | .hard => (H.hardMixing k : ℂ)
  | .soft => (H.softMixing k : ℂ)
  | _ => 0

def finiteExchangeStateScale
    (scalar : ℂ)
    (state : FiniteExchangeComplexState) :
    FiniteExchangeComplexState :=
  fun basis =>
    scalar * state basis

def finiteExchangeHamiltonianOperator
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (state : FiniteExchangeComplexState) :
    FiniteExchangeComplexState
  | .vacuum => 0
  | .residual =>
      (H.frequency k : ℂ) *
        (
          (H.hardMixing k : ℂ) * state .hard +
          (H.softMixing k : ℂ) * state .soft
        )
  | .hard =>
      (H.frequency k : ℂ) *
        (H.hardMixing k : ℂ) *
        state .residual
  | .soft =>
      (H.frequency k : ℂ) *
        (H.softMixing k : ℂ) *
        state .residual

theorem finiteExchangeHamiltonianOperator_residual
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    finiteExchangeHamiltonianOperator
        H
        k
        finiteExchangeResidualKet =
      finiteExchangeStateScale
        (H.frequency k : ℂ)
        (finiteExchangeBrightKet H k) := by
  funext basis
  cases basis <;>
    simp [
      finiteExchangeHamiltonianOperator,
      finiteExchangeResidualKet,
      finiteExchangeBrightKet,
      finiteExchangeStateScale
    ]

theorem finiteExchangeHamiltonianOperator_bright
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    finiteExchangeHamiltonianOperator
        H
        k
        (finiteExchangeBrightKet H k) =
      finiteExchangeStateScale
        (H.frequency k : ℂ)
        finiteExchangeResidualKet := by
  have hMixReal :
      H.hardMixing k ^ 2 +
          H.softMixing k ^ 2 =
        1 :=
    H.mixingNormalization k
  have hMixComplex :
      (H.hardMixing k : ℂ) *
            (H.hardMixing k : ℂ) +
          (H.softMixing k : ℂ) *
            (H.softMixing k : ℂ) =
        1 := by
    norm_cast
    nlinarith [hMixReal]
  funext basis
  cases basis <;>
    simp [
      finiteExchangeHamiltonianOperator,
      finiteExchangeBrightKet,
      finiteExchangeResidualKet,
      finiteExchangeStateScale,
      hMixComplex
    ]

def finiteExchangeResidualFormalMatrixExponentialAction
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    FiniteExchangeComplexState
  | .vacuum => 0
  | .residual =>
      (Real.cos (H.frequency k * tau) : ℂ)
  | .hard =>
      -Complex.I *
        (
          H.hardMixing k *
            Real.sin (H.frequency k * tau) : ℝ
        )
  | .soft =>
      -Complex.I *
        (
          H.softMixing k *
            Real.sin (H.frequency k * tau) : ℝ
        )

@[simp]
theorem finiteExchangeResidualFormalMatrixExponentialAction_vacuum
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    finiteExchangeResidualFormalMatrixExponentialAction
        H
        k
        tau
        .vacuum =
      0 := by
  rfl

@[simp]
theorem finiteExchangeResidualFormalMatrixExponentialAction_residual
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    finiteExchangeResidualFormalMatrixExponentialAction
        H
        k
        tau
        .residual =
      (Real.cos (H.frequency k * tau) : ℂ) := by
  rfl

@[simp]
theorem finiteExchangeResidualFormalMatrixExponentialAction_hard
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    finiteExchangeResidualFormalMatrixExponentialAction
        H
        k
        tau
        .hard =
      -Complex.I *
        (
          H.hardMixing k *
            Real.sin (H.frequency k * tau) : ℝ
        ) := by
  rfl

@[simp]
theorem finiteExchangeResidualFormalMatrixExponentialAction_soft
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    finiteExchangeResidualFormalMatrixExponentialAction
        H
        k
        tau
        .soft =
      -Complex.I *
        (
          H.softMixing k *
            Real.sin (H.frequency k * tau) : ℝ
        ) := by
  rfl

theorem finiteExchangeResidualFormalMatrixExponentialAction_zero
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    finiteExchangeResidualFormalMatrixExponentialAction
        H
        k
        0 =
      finiteExchangeResidualKet := by
  funext basis
  cases basis <;>
    simp [
      finiteExchangeResidualFormalMatrixExponentialAction,
      finiteExchangeResidualKet
    ]

theorem finiteExchangeResidualFormalAmplitudeNormalization
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    Real.cos (H.frequency k * tau) ^ 2 +
          (
            H.hardMixing k *
              Real.sin (H.frequency k * tau)
          ) ^ 2 +
          (
            H.softMixing k *
              Real.sin (H.frequency k * tau)
          ) ^ 2 =
      1 := by
  calc
    Real.cos (H.frequency k * tau) ^ 2 +
          (
            H.hardMixing k *
              Real.sin (H.frequency k * tau)
          ) ^ 2 +
          (
            H.softMixing k *
              Real.sin (H.frequency k * tau)
          ) ^ 2 =
        Real.cos (H.frequency k * tau) ^ 2 +
          (
            H.hardMixing k ^ 2 +
              H.softMixing k ^ 2
          ) *
            Real.sin (H.frequency k * tau) ^ 2 := by
              ring
    _ =
        Real.cos (H.frequency k * tau) ^ 2 +
          Real.sin (H.frequency k * tau) ^ 2 := by
            rw [H.mixingNormalization k]
            ring
    _ = 1 :=
      Real.cos_sq_add_sin_sq
        (H.frequency k * tau)

def finiteNormalizedExchangeFrequency
    (hardCoupling softCoupling : ℝ) :
    ℝ :=
  Real.sqrt
    (
      hardCoupling ^ 2 +
        softCoupling ^ 2
    )

def finiteNormalizedHardMixing
    (hardCoupling softCoupling : ℝ) :
    ℝ :=
  let frequency :=
    finiteNormalizedExchangeFrequency
      hardCoupling
      softCoupling
  if frequency = 0 then
    1
  else
    hardCoupling / frequency

def finiteNormalizedSoftMixing
    (hardCoupling softCoupling : ℝ) :
    ℝ :=
  let frequency :=
    finiteNormalizedExchangeFrequency
      hardCoupling
      softCoupling
  if frequency = 0 then
    0
  else
    softCoupling / frequency

theorem finiteNormalizedMixing_sq_add
    (hardCoupling softCoupling : ℝ) :
    (finiteNormalizedHardMixing
          hardCoupling
          softCoupling) ^ 2 +
        (finiteNormalizedSoftMixing
          hardCoupling
          softCoupling) ^ 2 =
      1 := by
  unfold
    finiteNormalizedHardMixing
    finiteNormalizedSoftMixing
  by_cases hFrequency :
      finiteNormalizedExchangeFrequency
          hardCoupling
          softCoupling =
        0
  · simp [hFrequency]
  · rw [if_neg hFrequency, if_neg hFrequency]
    have hRadicand :
        0 ≤
          hardCoupling ^ 2 +
            softCoupling ^ 2 := by
      positivity
    have hFrequencySq :
        finiteNormalizedExchangeFrequency
              hardCoupling
              softCoupling ^ 2 =
          hardCoupling ^ 2 +
            softCoupling ^ 2 := by
      unfold finiteNormalizedExchangeFrequency
      exact Real.sq_sqrt hRadicand
    field_simp [hFrequency]
    nlinarith [hFrequencySq]

def reggeWheelerHardExchangeCoupling
    (rPlus : ℝ)
    (rawState : ReggeWheelerOddParityRadialJet) :
    ℝ :=
  abs
    (
      reggeWheelerOddParityMasterField
        rawState
        rPlus
    )

def reggeWheelerSoftExchangeCoupling
    (rMinus rPlus : ℝ)
    (rawState : ReggeWheelerOddParityRadialJet) :
    ℝ :=
  abs
    (
      reggeWheelerOddParityMemoryShift
        rMinus
        rPlus
        rawState
    )

def reggeWheelerExchangeFrequency
    (rMinus rPlus : ℝ)
    (rawState : ReggeWheelerOddParityRadialJet) :
    ℝ :=
  finiteNormalizedExchangeFrequency
    (reggeWheelerHardExchangeCoupling
      rPlus
      rawState)
    (reggeWheelerSoftExchangeCoupling
      rMinus
      rPlus
      rawState)

def reggeWheelerExchangeHardMixing
    (rMinus rPlus : ℝ)
    (rawState : ReggeWheelerOddParityRadialJet) :
    ℝ :=
  finiteNormalizedHardMixing
    (reggeWheelerHardExchangeCoupling
      rPlus
      rawState)
    (reggeWheelerSoftExchangeCoupling
      rMinus
      rPlus
      rawState)

def reggeWheelerExchangeSoftMixing
    (rMinus rPlus : ℝ)
    (rawState : ReggeWheelerOddParityRadialJet) :
    ℝ :=
  finiteNormalizedSoftMixing
    (reggeWheelerHardExchangeCoupling
      rPlus
      rawState)
    (reggeWheelerSoftExchangeCoupling
      rMinus
      rPlus
      rawState)

def reggeWheelerFiniteExchangeHamiltonian
    (rawState : Nat → ReggeWheelerOddParityRadialJet)
    (rMinus rPlus duration : Nat → ℝ) :
    FiniteChargeConservingExchangeHamiltonian where
  frequency k :=
    reggeWheelerExchangeFrequency
      (rMinus k)
      (rPlus k)
      (rawState k)
  duration :=
    duration
  hardMixing k :=
    reggeWheelerExchangeHardMixing
      (rMinus k)
      (rPlus k)
      (rawState k)
  softMixing k :=
    reggeWheelerExchangeSoftMixing
      (rMinus k)
      (rPlus k)
      (rawState k)
  mixingNormalization := by
    intro k
    exact
      finiteNormalizedMixing_sq_add
        (reggeWheelerHardExchangeCoupling
          (rPlus k)
          (rawState k))
        (reggeWheelerSoftExchangeCoupling
          (rMinus k)
          (rPlus k)
          (rawState k))

theorem reggeWheelerUnitMemoryHardCoupling_eq_one :
    reggeWheelerHardExchangeCoupling
        1
        reggeWheelerOddParityUnitMemoryJet =
      1 := by
  simp [
    reggeWheelerHardExchangeCoupling,
    reggeWheelerOddParityUnitMemoryJet_master
  ]

theorem reggeWheelerUnitMemorySoftCoupling_eq_one :
    reggeWheelerSoftExchangeCoupling
        0
        1
        reggeWheelerOddParityUnitMemoryJet =
      1 := by
  simp [
    reggeWheelerSoftExchangeCoupling,
    reggeWheelerOddParityUnitMemoryShift_eq_one
  ]

theorem reggeWheelerUnitMemoryFrequency_eq_sqrt_two :
    reggeWheelerExchangeFrequency
        0
        1
        reggeWheelerOddParityUnitMemoryJet =
      Real.sqrt 2 := by
  unfold reggeWheelerExchangeFrequency
  rw [
    reggeWheelerUnitMemoryHardCoupling_eq_one,
    reggeWheelerUnitMemorySoftCoupling_eq_one
  ]
  norm_num [finiteNormalizedExchangeFrequency]

theorem finiteNormalizedHardMixing_one_one_sq :
    finiteNormalizedHardMixing 1 1 ^ 2 =
      (1 / 2 : ℝ) := by
  have hFrequency :
      finiteNormalizedExchangeFrequency 1 1 ≠
        0 := by
    unfold finiteNormalizedExchangeFrequency
    positivity
  unfold finiteNormalizedHardMixing
  rw [if_neg hFrequency]
  rw [div_pow]
  have hFrequencySq :
      finiteNormalizedExchangeFrequency 1 1 ^ 2 =
        2 := by
    unfold finiteNormalizedExchangeFrequency
    norm_num
  rw [hFrequencySq]
  norm_num

theorem finiteNormalizedSoftMixing_one_one_sq :
    finiteNormalizedSoftMixing 1 1 ^ 2 =
      (1 / 2 : ℝ) := by
  have hFrequency :
      finiteNormalizedExchangeFrequency 1 1 ≠
        0 := by
    unfold finiteNormalizedExchangeFrequency
    positivity
  unfold finiteNormalizedSoftMixing
  rw [if_neg hFrequency]
  rw [div_pow]
  have hFrequencySq :
      finiteNormalizedExchangeFrequency 1 1 ^ 2 =
        2 := by
    unfold finiteNormalizedExchangeFrequency
    norm_num
  rw [hFrequencySq]
  norm_num

theorem reggeWheelerUnitMemoryHardMixing_sq_eq_half :
    reggeWheelerExchangeHardMixing
          0
          1
          reggeWheelerOddParityUnitMemoryJet ^ 2 =
      (1 / 2 : ℝ) := by
  unfold reggeWheelerExchangeHardMixing
  rw [
    reggeWheelerUnitMemoryHardCoupling_eq_one,
    reggeWheelerUnitMemorySoftCoupling_eq_one
  ]
  exact finiteNormalizedHardMixing_one_one_sq

theorem reggeWheelerUnitMemorySoftMixing_sq_eq_half :
    reggeWheelerExchangeSoftMixing
          0
          1
          reggeWheelerOddParityUnitMemoryJet ^ 2 =
      (1 / 2 : ℝ) := by
  unfold reggeWheelerExchangeSoftMixing
  rw [
    reggeWheelerUnitMemoryHardCoupling_eq_one,
    reggeWheelerUnitMemorySoftCoupling_eq_one
  ]
  exact finiteNormalizedSoftMixing_one_one_sq

theorem reggeWheelerUnitMemoryVisibility_eq :
    finiteCoherentSoftMemoryVisibility
        (
          reggeWheelerSoftExchangeCoupling
            0
            1
            reggeWheelerOddParityUnitMemoryJet
        ) =
      Real.exp (-(1 : ℝ) / 4) := by
  rw [reggeWheelerUnitMemorySoftCoupling_eq_one]
  norm_num [finiteCoherentSoftMemoryVisibility]

theorem reggeWheelerUnitMemoryGenericDephasingDiscriminator_eq_half :
    finiteSoftMemoryDiscriminator
        (
          finiteCoherentSoftMemoryVisibility
            (
              reggeWheelerSoftExchangeCoupling
                0
                1
                reggeWheelerOddParityUnitMemoryJet
            )
        )
        0 =
      (1 / 2 : ℝ) := by
  rw [reggeWheelerUnitMemorySoftCoupling_eq_one]
  simpa using
    finiteCoherentVisibility_zeroMemoryDiscriminator
      (1 : ℝ)

theorem reggeWheelerUnitMemoryCoherentDiscriminator_eq_zero :
    finiteSoftMemoryDiscriminator
        (
          finiteCoherentSoftMemoryVisibility
            (
              reggeWheelerSoftExchangeCoupling
                0
                1
                reggeWheelerOddParityUnitMemoryJet
            )
        )
        (
          reggeWheelerSoftExchangeCoupling
            0
            1
            reggeWheelerOddParityUnitMemoryJet
        ) =
      0 := by
  rw [reggeWheelerUnitMemorySoftCoupling_eq_one]
  exact
    finiteCoherentSoftMemoryDiscriminator_zero
      (1 : ℝ)

theorem reggeWheelerUnitMemoryDiscriminatorGap_eq_half :
    finiteSoftMemoryDiscriminator
          (
            finiteCoherentSoftMemoryVisibility
              (
                reggeWheelerSoftExchangeCoupling
                  0
                  1
                  reggeWheelerOddParityUnitMemoryJet
              )
          )
          0 -
        finiteSoftMemoryDiscriminator
          (
            finiteCoherentSoftMemoryVisibility
              (
                reggeWheelerSoftExchangeCoupling
                  0
                  1
                  reggeWheelerOddParityUnitMemoryJet
              )
          )
          (
            reggeWheelerSoftExchangeCoupling
              0
              1
              reggeWheelerOddParityUnitMemoryJet
          ) =
      (1 / 2 : ℝ) := by
  rw [
    reggeWheelerUnitMemoryGenericDephasingDiscriminator_eq_half,
    reggeWheelerUnitMemoryCoherentDiscriminator_eq_zero
  ]
  ring

def reggeWheelerFiniteExchangeMatrixEvolutionStatus : String :=
  "EXPLICIT_COMPLEX_MATRIX_HERMITIAN_CHARGE_COMMUTING_FORMAL_RESIDUAL_EVOLUTION_AND_RW_BALANCED_PREDICTION"

def reggeWheelerFiniteExchangeMatrixEvolutionBoundary : String :=
  "FORMAL_RESIDUAL_SUBSPACE_EVOLUTION_NOT_YET_IDENTIFIED_WITH_MATHLIB_MATRIX_EXP_AND_PHYSICAL_COUPLING_CALIBRATION_NOT_PROVED"

end

end Chronos.Frontier
