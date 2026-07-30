import Chronos.Frontier.ReggeWheelerFlagshipExactResidual
import Chronos.Frontier.FiniteSoftRecordGaussianState

namespace Chronos.Frontier

noncomputable section

/-!
# Domain-bearing nonzero Regge–Wheeler bounded-potential response

This module inhabits the exact-residual interface with one explicit,
square-integrable Gaussian correction.

The principal operator constructed here is a rank-one algebraic operator. It
is not identified with the physical Regge–Wheeler differential operator.
-/

noncomputable def reggeWheelerGaussianFirstOrderCorrection :
    ℝ → ℝ :=
  finiteSoftRecordGaussianWavefunction 0

noncomputable def reggeWheelerGaussianBackground :
    ℝ → ℝ :=
  fun rStar =>
    rStar *
      reggeWheelerGaussianFirstOrderCorrection rStar

theorem reggeWheelerGaussianFirstOrderCorrection_at_zero_pos :
    0 <
      reggeWheelerGaussianFirstOrderCorrection 0 := by
  unfold reggeWheelerGaussianFirstOrderCorrection
  unfold finiteSoftRecordGaussianWavefunction
  positivity

noncomputable def reggeWheelerGaussianUnitWindowSource :
    ℝ → ℝ :=
  reggeWheelerUnitWindowPotentialInsertion
    reggeWheelerGaussianBackground

noncomputable def reggeWheelerGaussianRankOnePrincipalOperator :
    (ℝ → ℝ) →ₗ[ℝ] (ℝ → ℝ) where
  toFun profile :=
    fun rStar =>
      (
        profile 0 /
          reggeWheelerGaussianFirstOrderCorrection 0
      ) *
        reggeWheelerGaussianUnitWindowSource rStar
  map_add' := by
    intro left right
    funext rStar
    simp
    ring
  map_smul' := by
    intro scalar profile
    funext rStar
    simp [smul_eq_mul]
    ring

theorem reggeWheelerGaussianRankOnePrincipalOperator_background_eq_zero :
    reggeWheelerGaussianRankOnePrincipalOperator
        reggeWheelerGaussianBackground =
      0 := by
  ext rStar
  simp [
    reggeWheelerGaussianRankOnePrincipalOperator,
    reggeWheelerGaussianBackground
  ]

theorem reggeWheelerGaussianRankOnePrincipalOperator_firstOrderEquation :
    reggeWheelerGaussianRankOnePrincipalOperator
        reggeWheelerGaussianFirstOrderCorrection =
      reggeWheelerUnitWindowPotentialInsertion
        reggeWheelerGaussianBackground := by
  have hCorrectionZero :
      reggeWheelerGaussianFirstOrderCorrection 0 ≠ 0 :=
    reggeWheelerGaussianFirstOrderCorrection_at_zero_pos.ne'
  ext rStar
  simp [
    reggeWheelerGaussianRankOnePrincipalOperator,
    reggeWheelerGaussianUnitWindowSource,
    hCorrectionZero
  ]

theorem reggeWheelerGaussianFirstOrderCorrection_square_integrable :
    MeasureTheory.Integrable
      (fun rStar =>
        reggeWheelerGaussianFirstOrderCorrection rStar ^ 2) := by
  by_contra hNotIntegrable

  have hIntegralZero :
      (∫ rStar : ℝ,
          reggeWheelerGaussianFirstOrderCorrection rStar ^ 2) =
        0 :=
    MeasureTheory.integral_undef hNotIntegrable

  have hIntegralOne :
      (∫ rStar : ℝ,
          reggeWheelerGaussianFirstOrderCorrection rStar ^ 2) =
        1 := by
    simpa [
      reggeWheelerGaussianFirstOrderCorrection,
      pow_two
    ] using
      finiteSoftRecordGaussianWavefunction_normalized 0

  rw [hIntegralOne] at hIntegralZero
  norm_num at hIntegralZero

noncomputable def reggeWheelerGaussianFirstOrderCorrectionOnDomain :
    ReggeWheelerSquareIntegrableProfile where
  profile :=
    reggeWheelerGaussianFirstOrderCorrection
  square_integrable :=
    reggeWheelerGaussianFirstOrderCorrection_square_integrable

theorem
    reggeWheelerUnitWindowPotentialInsertion_gaussianCorrection_ne_zero :
    reggeWheelerUnitWindowPotentialInsertion
        reggeWheelerGaussianFirstOrderCorrection ≠
      0 := by
  intro hZero

  have hAtZero :=
    congrFun hZero 0

  simp [
    reggeWheelerUnitWindowPotentialInsertion,
    reggeWheelerUnitWindowPotential
  ] at hAtZero

  exact
    reggeWheelerGaussianFirstOrderCorrection_at_zero_pos.ne'
      hAtZero

noncomputable def reggeWheelerGaussianDomainBearingDeviation :
    ReggeWheelerFirstOrderDeviationData (ℝ → ℝ) where
  principalOperator :=
    reggeWheelerGaussianRankOnePrincipalOperator
  potentialInsertion :=
    reggeWheelerUnitWindowPotentialInsertion
  background :=
    reggeWheelerGaussianBackground
  firstOrderCorrection :=
    reggeWheelerGaussianFirstOrderCorrection
  backgroundEquation :=
    reggeWheelerGaussianRankOnePrincipalOperator_background_eq_zero
  firstOrderEquation :=
    reggeWheelerGaussianRankOnePrincipalOperator_firstOrderEquation

theorem reggeWheelerGaussianDomainBearingDeviation_correction_integrable :
    MeasureTheory.Integrable
      (fun rStar =>
        (
          ReggeWheelerFirstOrderDeviationData.firstOrderCorrection
            reggeWheelerGaussianDomainBearingDeviation
        ) rStar ^ 2) := by
  simpa [reggeWheelerGaussianDomainBearingDeviation] using
    reggeWheelerGaussianFirstOrderCorrection_square_integrable

theorem reggeWheelerGaussianDomainBearingDeviation_secondInsertion_ne_zero :
    (
      ReggeWheelerFirstOrderDeviationData.potentialInsertion
        reggeWheelerGaussianDomainBearingDeviation
    )
        (
          ReggeWheelerFirstOrderDeviationData.firstOrderCorrection
            reggeWheelerGaussianDomainBearingDeviation
        ) ≠
      0 := by
  simpa [reggeWheelerGaussianDomainBearingDeviation] using
    reggeWheelerUnitWindowPotentialInsertion_gaussianCorrection_ne_zero

theorem reggeWheelerGaussianDomainBearingDeviation_notExact
    (lambda : ℝ)
    (hLambda : lambda ≠ 0) :
    reggeWheelerDeformedOperator
          (
            ReggeWheelerFirstOrderDeviationData.principalOperator
              reggeWheelerGaussianDomainBearingDeviation
          )
          (
            ReggeWheelerFirstOrderDeviationData.potentialInsertion
              reggeWheelerGaussianDomainBearingDeviation
          )
          lambda
          (
            ReggeWheelerFirstOrderDeviationData.background
                reggeWheelerGaussianDomainBearingDeviation +
              lambda •
                ReggeWheelerFirstOrderDeviationData.firstOrderCorrection
                  reggeWheelerGaussianDomainBearingDeviation
          ) ≠
      0 := by
  exact
    reggeWheelerFlagship_nonzeroSecondInsertion_notExact
      reggeWheelerGaussianDomainBearingDeviation
      lambda
      hLambda
      reggeWheelerGaussianDomainBearingDeviation_secondInsertion_ne_zero

def reggeWheelerDomainBearingNonzeroResponseStatus : String :=
  "EXPLICIT_SQUARE_INTEGRABLE_RESPONSE_AND_NONZERO_SECOND_INSERTION_PROVED"

def reggeWheelerDomainBearingNonzeroResponseBoundary : String :=
  "RANK_ONE_PRINCIPAL_OPERATOR_NOT_IDENTIFIED_WITH_THE_PHYSICAL_REGGE_WHEELER_PDE_OPERATOR"

end

end Chronos.Frontier
