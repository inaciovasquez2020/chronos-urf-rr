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


open scoped Matrix Matrix.Norms.Operator

def finiteExchangeSchrodingerGeneratorMatrix
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    FiniteExchangeComplexMatrix :=
  (-Complex.I * (tau : ℂ)) •
    finiteExchangeHamiltonianMatrix H k

theorem finiteExchangeMatrixExpSeries_hasSum
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    HasSum
      (fun n : Nat =>
        ((n.factorial : ℂ)⁻¹) •
          (finiteExchangeSchrodingerGeneratorMatrix H k tau) ^ n)
      (NormedSpace.exp
        (finiteExchangeSchrodingerGeneratorMatrix H k tau)) := by
  exact
    NormedSpace.exp_series_hasSum_exp'
      (finiteExchangeSchrodingerGeneratorMatrix H k tau)


def finiteExchangeMulVecRightLinearMap
    (state : FiniteExchangeComplexState) :
    FiniteExchangeComplexMatrix →ₗ[ℂ]
      FiniteExchangeComplexState where
  toFun matrix := matrix *ᵥ state
  map_add' left right :=
    Matrix.add_mulVec left right state
  map_smul' scalar matrix :=
    Matrix.smul_mulVec scalar matrix state

def finiteExchangeMulVecRightContinuousLinearMap
    (state : FiniteExchangeComplexState) :
    FiniteExchangeComplexMatrix →L[ℂ]
      FiniteExchangeComplexState :=
  LinearMap.toContinuousLinearMap
    (finiteExchangeMulVecRightLinearMap state)

@[simp]
theorem finiteExchangeMulVecRightContinuousLinearMap_apply
    (state : FiniteExchangeComplexState)
    (matrix : FiniteExchangeComplexMatrix) :
    finiteExchangeMulVecRightContinuousLinearMap state matrix =
      matrix *ᵥ state := by
  rfl

theorem finiteExchangeResidualMatrixExpSeries_hasSum_expAction
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    HasSum
      (fun n : Nat =>
        ((n.factorial : ℂ)⁻¹) •
          ((finiteExchangeSchrodingerGeneratorMatrix H k tau) ^ n *ᵥ
            finiteExchangeResidualKet))
      (NormedSpace.exp
          (finiteExchangeSchrodingerGeneratorMatrix H k tau) *ᵥ
        finiteExchangeResidualKet) := by
  have hMapped :
      HasSum
        (fun n : Nat =>
          finiteExchangeMulVecRightContinuousLinearMap
            finiteExchangeResidualKet
            (((n.factorial : ℂ)⁻¹) •
              (finiteExchangeSchrodingerGeneratorMatrix H k tau) ^ n))
        (finiteExchangeMulVecRightContinuousLinearMap
          finiteExchangeResidualKet
          (NormedSpace.exp
            (finiteExchangeSchrodingerGeneratorMatrix H k tau))) :=
    (finiteExchangeMulVecRightContinuousLinearMap
      finiteExchangeResidualKet).hasSum
        (finiteExchangeMatrixExpSeries_hasSum H k tau)

  simpa only [
    finiteExchangeMulVecRightContinuousLinearMap_apply,
    Matrix.smul_mulVec
  ] using hMapped


theorem finiteExchangeBasis_univ_matrix_exp_closed :
    (Finset.univ : Finset FiniteExchangeBasis) =
      ({.vacuum, .residual, .hard, .soft} :
        Finset FiniteExchangeBasis) := by
  decide

theorem finiteExchangeHamiltonianMatrix_mulVec_eq_operator_matrix_exp_closed
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (state : FiniteExchangeComplexState) :
    finiteExchangeHamiltonianMatrix H k *ᵥ state =
      finiteExchangeHamiltonianOperator H k state := by
  funext basis
  cases basis <;>
    simp [
      finiteExchangeHamiltonianMatrix,
      finiteExchangeHamiltonianOperator,
      finiteExchangeHamiltonianEntry,
      Matrix.mulVec,
      dotProduct,
      finiteExchangeBasis_univ_matrix_exp_closed
    ];
    ring

theorem finiteExchangeStateScale_eq_smul_matrix_exp_closed
    (scalar : ℂ)
    (state : FiniteExchangeComplexState) :
    finiteExchangeStateScale scalar state = scalar • state := by
  rfl

theorem finiteExchangeHamiltonianMatrix_mulVec_residual_matrix_exp_closed
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    finiteExchangeHamiltonianMatrix H k *ᵥ
        finiteExchangeResidualKet =
      (H.frequency k : ℂ) • finiteExchangeBrightKet H k := by
  rw [
    finiteExchangeHamiltonianMatrix_mulVec_eq_operator_matrix_exp_closed,
    finiteExchangeHamiltonianOperator_residual,
    finiteExchangeStateScale_eq_smul_matrix_exp_closed
  ]

theorem finiteExchangeHamiltonianMatrix_mulVec_bright_matrix_exp_closed
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat) :
    finiteExchangeHamiltonianMatrix H k *ᵥ
        finiteExchangeBrightKet H k =
      (H.frequency k : ℂ) • finiteExchangeResidualKet := by
  rw [
    finiteExchangeHamiltonianMatrix_mulVec_eq_operator_matrix_exp_closed,
    finiteExchangeHamiltonianOperator_bright,
    finiteExchangeStateScale_eq_smul_matrix_exp_closed
  ]

theorem finiteExchangeMatrix_pow_even_odd_on_matrix_exp_closed
    (A : FiniteExchangeComplexMatrix)
    (residual bright : FiniteExchangeComplexState)
    (omega : ℂ)
    (hResidual : A *ᵥ residual = omega • bright)
    (hBright : A *ᵥ bright = omega • residual) :
    (∀ n : Nat,
        A ^ (2 * n) *ᵥ residual =
          omega ^ (2 * n) • residual) ∧
      (∀ n : Nat,
        A ^ (2 * n + 1) *ᵥ residual =
          omega ^ (2 * n + 1) • bright) := by
  have h :
      ∀ n : Nat,
        (A ^ (2 * n) *ᵥ residual =
            omega ^ (2 * n) • residual) ∧
          (A ^ (2 * n + 1) *ᵥ residual =
            omega ^ (2 * n + 1) • bright) := by
    intro n
    induction n with
    | zero =>
        constructor
        · simp
        · simpa using hResidual
    | succ n ih =>
        rcases ih with ⟨hEven, hOdd⟩

        have hEvenNext :
            A ^ (2 * (n + 1)) *ᵥ residual =
              omega ^ (2 * (n + 1)) • residual := by
          calc
            A ^ (2 * (n + 1)) *ᵥ residual =
                A *ᵥ (A ^ (2 * n + 1) *ᵥ residual) := by
              rw [
                show 2 * (n + 1) = 1 + (2 * n + 1) by omega,
                pow_add,
                pow_one,
                Matrix.mulVec_mulVec
              ]
            _ =
                A *ᵥ (omega ^ (2 * n + 1) • bright) := by
              rw [hOdd]
            _ =
                omega ^ (2 * n + 1) • (A *ᵥ bright) := by
              rw [Matrix.mulVec_smul]
            _ =
                omega ^ (2 * n + 1) • (omega • residual) := by
              rw [hBright]
            _ =
                omega ^ (2 * (n + 1)) • residual := by
              rw [smul_smul]
              congr 1

        have hOddNext :
            A ^ (2 * (n + 1) + 1) *ᵥ residual =
              omega ^ (2 * (n + 1) + 1) • bright := by
          calc
            A ^ (2 * (n + 1) + 1) *ᵥ residual =
                A *ᵥ
                  (A ^ (2 * (n + 1)) *ᵥ residual) := by
              rw [
                show 2 * (n + 1) + 1 =
                    1 + 2 * (n + 1) by omega,
                pow_add,
                pow_one,
                Matrix.mulVec_mulVec
              ]
            _ =
                A *ᵥ
                  (omega ^ (2 * (n + 1)) • residual) := by
              rw [hEvenNext]
            _ =
                omega ^ (2 * (n + 1)) •
                  (A *ᵥ residual) := by
              rw [Matrix.mulVec_smul]
            _ =
                omega ^ (2 * (n + 1)) •
                  (omega • bright) := by
              rw [hResidual]
            _ =
                omega ^ (2 * (n + 1) + 1) • bright := by
              rw [smul_smul, pow_succ]

        exact ⟨hEvenNext, hOddNext⟩

  exact ⟨fun n => (h n).1, fun n => (h n).2⟩

def finiteExchangeSchrodingerPhase
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    ℂ :=
  (-Complex.I * (tau : ℂ)) * (H.frequency k : ℂ)

def finiteExchangeSchrodingerAngle
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    ℂ :=
  ((H.frequency k * tau : ℝ) : ℂ)

theorem finiteExchangeSchrodingerPhase_eq_neg_I_mul_angle
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    finiteExchangeSchrodingerPhase H k tau =
      -Complex.I * finiteExchangeSchrodingerAngle H k tau := by
  unfold
    finiteExchangeSchrodingerPhase
    finiteExchangeSchrodingerAngle
  push_cast
  ring

theorem finiteExchangeSchrodingerGeneratorMatrix_mulVec_residual
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    finiteExchangeSchrodingerGeneratorMatrix H k tau *ᵥ
        finiteExchangeResidualKet =
      finiteExchangeSchrodingerPhase H k tau •
        finiteExchangeBrightKet H k := by
  unfold
    finiteExchangeSchrodingerGeneratorMatrix
    finiteExchangeSchrodingerPhase
  rw [
    Matrix.smul_mulVec,
    finiteExchangeHamiltonianMatrix_mulVec_residual_matrix_exp_closed,
    smul_smul
  ]

theorem finiteExchangeSchrodingerGeneratorMatrix_mulVec_bright
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    finiteExchangeSchrodingerGeneratorMatrix H k tau *ᵥ
        finiteExchangeBrightKet H k =
      finiteExchangeSchrodingerPhase H k tau •
        finiteExchangeResidualKet := by
  unfold
    finiteExchangeSchrodingerGeneratorMatrix
    finiteExchangeSchrodingerPhase
  rw [
    Matrix.smul_mulVec,
    finiteExchangeHamiltonianMatrix_mulVec_bright_matrix_exp_closed,
    smul_smul
  ]

theorem finiteExchangeSchrodingerGeneratorMatrix_pow_even_odd
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    (∀ n : Nat,
        (finiteExchangeSchrodingerGeneratorMatrix H k tau) ^
              (2 * n) *ᵥ
            finiteExchangeResidualKet =
          (finiteExchangeSchrodingerPhase H k tau) ^
              (2 * n) •
            finiteExchangeResidualKet) ∧
      (∀ n : Nat,
        (finiteExchangeSchrodingerGeneratorMatrix H k tau) ^
              (2 * n + 1) *ᵥ
            finiteExchangeResidualKet =
          (finiteExchangeSchrodingerPhase H k tau) ^
              (2 * n + 1) •
            finiteExchangeBrightKet H k) := by
  exact
    finiteExchangeMatrix_pow_even_odd_on_matrix_exp_closed
      (finiteExchangeSchrodingerGeneratorMatrix H k tau)
      finiteExchangeResidualKet
      (finiteExchangeBrightKet H k)
      (finiteExchangeSchrodingerPhase H k tau)
      (finiteExchangeSchrodingerGeneratorMatrix_mulVec_residual
        H k tau)
      (finiteExchangeSchrodingerGeneratorMatrix_mulVec_bright
        H k tau)

theorem finiteExchange_neg_I_mul_pow_even
    (angle : ℂ)
    (n : Nat) :
    (-Complex.I * angle) ^ (2 * n) =
      (-1 : ℂ) ^ n * angle ^ (2 * n) := by
  have hNegISq :
      (-Complex.I : ℂ) ^ 2 = -1 := by
    calc
      (-Complex.I : ℂ) ^ 2 =
          Complex.I * Complex.I := by
        ring
      _ = -1 := Complex.I_mul_I

  calc
    (-Complex.I * angle) ^ (2 * n) =
        (-Complex.I : ℂ) ^ (2 * n) *
          angle ^ (2 * n) := by
      rw [mul_pow]
    _ =
        (((-Complex.I : ℂ) ^ 2) ^ n) *
          angle ^ (2 * n) := by
      rw [pow_mul]
    _ =
        (-1 : ℂ) ^ n * angle ^ (2 * n) := by
      rw [hNegISq]

theorem finiteExchange_neg_I_mul_pow_odd
    (angle : ℂ)
    (n : Nat) :
    (-Complex.I * angle) ^ (2 * n + 1) =
      -Complex.I *
        ((-1 : ℂ) ^ n * angle ^ (2 * n + 1)) := by
  calc
    (-Complex.I * angle) ^ (2 * n + 1) =
        (-Complex.I * angle) ^ (2 * n) *
          (-Complex.I * angle) := by
      rw [pow_succ]
    _ =
        ((-1 : ℂ) ^ n * angle ^ (2 * n)) *
          (-Complex.I * angle) := by
      rw [finiteExchange_neg_I_mul_pow_even]
    _ =
        -Complex.I *
          ((-1 : ℂ) ^ n * angle ^ (2 * n + 1)) := by
      rw [pow_succ]
      ring

def finiteExchangeResidualExponentialSeriesTerm
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ)
    (n : Nat) :
    FiniteExchangeComplexState :=
  ((n.factorial : ℂ)⁻¹) •
    ((finiteExchangeSchrodingerGeneratorMatrix H k tau) ^ n *ᵥ
      finiteExchangeResidualKet)

theorem finiteExchangeResidualExponentialSeriesTerm_even
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k n : Nat)
    (tau : ℝ) :
    finiteExchangeResidualExponentialSeriesTerm
        H k tau (2 * n) =
      (((-1 : ℂ) ^ n *
          (finiteExchangeSchrodingerAngle H k tau) ^ (2 * n) /
          ((2 * n).factorial : ℂ)) •
        finiteExchangeResidualKet) := by
  unfold finiteExchangeResidualExponentialSeriesTerm
  rw [
    (finiteExchangeSchrodingerGeneratorMatrix_pow_even_odd
      H k tau).1 n,
    finiteExchangeSchrodingerPhase_eq_neg_I_mul_angle,
    finiteExchange_neg_I_mul_pow_even,
    smul_smul
  ]
  congr 1
  ring

theorem finiteExchangeResidualExponentialSeriesTerm_odd
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k n : Nat)
    (tau : ℝ) :
    finiteExchangeResidualExponentialSeriesTerm
        H k tau (2 * n + 1) =
      (-Complex.I *
          (((-1 : ℂ) ^ n *
              (finiteExchangeSchrodingerAngle H k tau) ^
                (2 * n + 1)) /
            ((2 * n + 1).factorial : ℂ))) •
        finiteExchangeBrightKet H k := by
  unfold finiteExchangeResidualExponentialSeriesTerm
  rw [
    (finiteExchangeSchrodingerGeneratorMatrix_pow_even_odd
      H k tau).2 n,
    finiteExchangeSchrodingerPhase_eq_neg_I_mul_angle,
    finiteExchange_neg_I_mul_pow_odd,
    smul_smul
  ]
  congr 1
  ring

theorem finiteExchangeResidualExponentialSeries_even_hasSum
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    HasSum
      (fun n =>
        finiteExchangeResidualExponentialSeriesTerm
          H k tau (2 * n))
      (Complex.cos
          (finiteExchangeSchrodingerAngle H k tau) •
        finiteExchangeResidualKet) := by
  simpa only [
    finiteExchangeResidualExponentialSeriesTerm_even
  ] using
    (Complex.hasSum_cos
      (finiteExchangeSchrodingerAngle H k tau)).smul_const
        finiteExchangeResidualKet

theorem finiteExchangeResidualExponentialSeries_odd_hasSum
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    HasSum
      (fun n =>
        finiteExchangeResidualExponentialSeriesTerm
          H k tau (2 * n + 1))
      ((-Complex.I *
          Complex.sin
            (finiteExchangeSchrodingerAngle H k tau)) •
        finiteExchangeBrightKet H k) := by
  have hSin :
      HasSum
        (fun n =>
          (((-1 : ℂ) ^ n *
              (finiteExchangeSchrodingerAngle H k tau) ^
                (2 * n + 1) /
              ((2 * n + 1).factorial : ℂ)) •
            finiteExchangeBrightKet H k))
        (Complex.sin
            (finiteExchangeSchrodingerAngle H k tau) •
          finiteExchangeBrightKet H k) :=
    (Complex.hasSum_sin
      (finiteExchangeSchrodingerAngle H k tau)).smul_const
        (finiteExchangeBrightKet H k)

  have hScaled :=
    HasSum.const_smul (-Complex.I) hSin

  simpa only [
    finiteExchangeResidualExponentialSeriesTerm_odd,
    smul_smul
  ] using hScaled

theorem finiteExchangeResidualExponentialSeries_hasSum_closed
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    HasSum
      (finiteExchangeResidualExponentialSeriesTerm H k tau)
      (Complex.cos
            (finiteExchangeSchrodingerAngle H k tau) •
          finiteExchangeResidualKet +
        (-Complex.I *
            Complex.sin
              (finiteExchangeSchrodingerAngle H k tau)) •
          finiteExchangeBrightKet H k) := by
  exact
    (finiteExchangeResidualExponentialSeries_even_hasSum
      H k tau).even_add_odd
        (finiteExchangeResidualExponentialSeries_odd_hasSum
          H k tau)

theorem finiteExchangeResidualMatrixExponentialAction_closed
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    NormedSpace.exp
        (finiteExchangeSchrodingerGeneratorMatrix H k tau) *ᵥ
      finiteExchangeResidualKet =
        Complex.cos
            (finiteExchangeSchrodingerAngle H k tau) •
          finiteExchangeResidualKet +
        (-Complex.I *
            Complex.sin
              (finiteExchangeSchrodingerAngle H k tau)) •
          finiteExchangeBrightKet H k := by
  have hExp :
      HasSum
        (finiteExchangeResidualExponentialSeriesTerm H k tau)
        (NormedSpace.exp
            (finiteExchangeSchrodingerGeneratorMatrix H k tau) *ᵥ
          finiteExchangeResidualKet) := by
    simpa only [
      finiteExchangeResidualExponentialSeriesTerm
    ] using
      finiteExchangeResidualMatrixExpSeries_hasSum_expAction
        H k tau

  exact
    hExp.unique
      (finiteExchangeResidualExponentialSeries_hasSum_closed
        H k tau)


theorem finiteExchangeResidualMatrixExponentialAction_eq_formal
    (H : FiniteChargeConservingExchangeHamiltonian)
    (k : Nat)
    (tau : ℝ) :
    NormedSpace.exp
        (finiteExchangeSchrodingerGeneratorMatrix H k tau) *ᵥ
      finiteExchangeResidualKet =
        finiteExchangeResidualFormalMatrixExponentialAction H k tau := by
  rw [finiteExchangeResidualMatrixExponentialAction_closed]
  funext basis
  cases basis <;>
    simp [
      finiteExchangeSchrodingerAngle,
      finiteExchangeResidualKet,
      finiteExchangeBrightKet,
      finiteExchangeResidualFormalMatrixExponentialAction
    ] <;>
    ring

def reggeWheelerFiniteExchangeMatrixEvolutionStatus : String :=
  "EXPLICIT_COMPLEX_MATRIX_HERMITIAN_CHARGE_COMMUTING_FORMAL_RESIDUAL_EVOLUTION_AND_RW_BALANCED_PREDICTION"

def reggeWheelerFiniteExchangeMatrixEvolutionBoundary : String :=
  "FORMAL_RESIDUAL_SUBSPACE_EVOLUTION_NOT_YET_IDENTIFIED_WITH_MATHLIB_MATRIX_EXP_AND_PHYSICAL_COUPLING_CALIBRATION_NOT_PROVED"

end

end Chronos.Frontier
