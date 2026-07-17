import Chronos.Frontier.ReggeWheelerConditionalDeviation

namespace Chronos.Frontier

noncomputable section

/-!
# Concrete bounded Regge–Wheeler deformation potential

This module introduces one explicit bounded potential,

`U(rStar) = 1` for `|rStar| ≤ 1`,
`U(rStar) = 0` otherwise.

It is a compact-window test deformation, not a physically derived potential.
No smoothness, covariant origin, response existence, or measurable prediction
is claimed.

The only deviation theorem proved here is:

if `lambda ≠ 0` and a certified first-order correction has
`observable correction ≠ 0`, then the corresponding linear observable
deviation is nonzero.
-/

/--
Concrete compact-window deformation potential.
-/
def reggeWheelerUnitWindowPotential
    (rStar : ℝ) : ℝ :=
  if |rStar| ≤ 1 then 1 else 0

theorem reggeWheelerUnitWindowPotential_abs_le_one
    (rStar : ℝ) :
    |reggeWheelerUnitWindowPotential rStar| ≤ 1 := by
  by_cases h : |rStar| ≤ 1
  · simp [reggeWheelerUnitWindowPotential, h]
  · simp [reggeWheelerUnitWindowPotential, h]

theorem reggeWheelerUnitWindowPotential_eq_zero_of_one_lt_abs
    {rStar : ℝ}
    (h : 1 < |rStar|) :
    reggeWheelerUnitWindowPotential rStar = 0 := by
  simp [
    reggeWheelerUnitWindowPotential,
    not_le.mpr h
  ]

theorem reggeWheelerUnitWindowPotential_zero :
    reggeWheelerUnitWindowPotential 0 = 1 := by
  simp [reggeWheelerUnitWindowPotential]

theorem reggeWheelerUnitWindowPotential_ne_zero :
    reggeWheelerUnitWindowPotential ≠ 0 := by
  intro h
  have hAtZero :=
    congrArg
      (fun potential : ℝ → ℝ => potential 0)
      h
  simp [reggeWheelerUnitWindowPotential] at hAtZero

/--
Pointwise multiplication by the concrete bounded deformation potential.
-/
def reggeWheelerUnitWindowPotentialInsertion :
    (ℝ → ℝ) →ₗ[ℝ] (ℝ → ℝ) where
  toFun profile :=
    fun rStar =>
      reggeWheelerUnitWindowPotential rStar *
        profile rStar
  map_add' := by
    intro left right
    ext rStar
    simp [mul_add]
  map_smul' := by
    intro scalar profile
    ext rStar
    simp [smul_eq_mul]
    ring

theorem reggeWheelerUnitWindowPotentialInsertion_ne_zero :
    reggeWheelerUnitWindowPotentialInsertion ≠ 0 := by
  intro h
  have hAtOneZero :=
    congrArg
      (fun insertion :
          (ℝ → ℝ) →ₗ[ℝ] (ℝ → ℝ) =>
        insertion (fun _ => 1) 0)
      h
  simp [
    reggeWheelerUnitWindowPotentialInsertion,
    reggeWheelerUnitWindowPotential
  ] at hAtOneZero

/--
The generic principal operator equipped with the concrete nonzero bounded
potential and a certified nonzero coupling.
-/
def reggeWheelerUnitWindowDeformation
    (principalOperator :
      (ℝ → ℝ) →ₗ[ℝ] (ℝ → ℝ))
    (lambda : ℝ)
    (hLambda : lambda ≠ 0) :
    ReggeWheelerPotentialDeformation (ℝ → ℝ) where
  principalOperator := principalOperator
  potentialInsertion :=
    reggeWheelerUnitWindowPotentialInsertion
  lambda := lambda
  lambda_ne_zero := hLambda
  potentialInsertion_ne_zero :=
    reggeWheelerUnitWindowPotentialInsertion_ne_zero

/--
Certificate for one first-order response to the concrete bounded potential.

The response itself remains supplied data. In particular, this structure
does not construct the response from a Green operator or PDE theorem.
-/
structure ReggeWheelerUnitWindowResponseCertificate
    (principalOperator :
      (ℝ → ℝ) →ₗ[ℝ] (ℝ → ℝ))
    (observable :
      (ℝ → ℝ) →ₗ[ℝ] ℝ) where
  background : ℝ → ℝ
  firstOrderCorrection : ℝ → ℝ
  backgroundEquation :
    principalOperator background = 0
  firstOrderEquation :
    principalOperator firstOrderCorrection =
      reggeWheelerUnitWindowPotentialInsertion
        background
  observableResponse_ne_zero :
    observable firstOrderCorrection ≠ 0

/--
For the concrete bounded potential, the exact residual of the first-order
approximation under the full deformed operator is the quadratic term
`-λ² U Ψ₁`.
-/
theorem
    reggeWheelerUnitWindow_exactDeformedResidual
    (principalOperator :
      (ℝ → ℝ) →ₗ[ℝ] (ℝ → ℝ))
    (observable :
      (ℝ → ℝ) →ₗ[ℝ] ℝ)
    (certificate :
      ReggeWheelerUnitWindowResponseCertificate
        principalOperator
        observable)
    (lambda : ℝ) :
    reggeWheelerDeformedOperator
          principalOperator
          reggeWheelerUnitWindowPotentialInsertion
          lambda
          (certificate.background +
            lambda •
              certificate.firstOrderCorrection) =
      -(lambda ^ 2) •
        reggeWheelerUnitWindowPotentialInsertion
          certificate.firstOrderCorrection := by
  let D :
      ReggeWheelerFirstOrderDeviationData
        (ℝ → ℝ) :=
    {
      principalOperator := principalOperator
      potentialInsertion :=
        reggeWheelerUnitWindowPotentialInsertion
      background := certificate.background
      firstOrderCorrection :=
        certificate.firstOrderCorrection
      backgroundEquation :=
        certificate.backgroundEquation
      firstOrderEquation :=
        certificate.firstOrderEquation
    }
  exact
    reggeWheelerFirstOrderApproximation_exactDeformedResidual
      D
      lambda

/--
For the concrete bounded deformation potential, a certified nonzero
first-order observable response and a nonzero coupling imply a nonzero
linear observable deviation.
-/
theorem
    reggeWheelerUnitWindow_nonzeroResponse_implies_nonzeroDeviation
    (principalOperator :
      (ℝ → ℝ) →ₗ[ℝ] (ℝ → ℝ))
    (observable :
      (ℝ → ℝ) →ₗ[ℝ] ℝ)
    (certificate :
      ReggeWheelerUnitWindowResponseCertificate
        principalOperator
        observable)
    (lambda : ℝ)
    (hLambda : lambda ≠ 0) :
    observable
          (certificate.background +
            lambda •
              certificate.firstOrderCorrection) -
        observable certificate.background ≠ 0 := by
  exact
    reggeWheelerLinearObservableDeviation_ne_zero
      observable
      certificate.background
      certificate.firstOrderCorrection
      lambda
      hLambda
      certificate.observableResponse_ne_zero

/--
The standard smooth bump profile on the unit tortoise-coordinate window:

`exp (-1 / (1 - rStar²))` for `|rStar| < 1`,
and zero outside the window.

The analytic `C∞` theorem is not claimed here; this block proves the
repository-native pointwise, support, and energy-order properties.
-/
def reggeWheelerSmoothCompactPotential
    (rStar : ℝ) : ℝ :=
  if |rStar| < 1 then
    Real.exp (-(1 / (1 - rStar ^ 2)))
  else
    0

theorem reggeWheelerSmoothCompactPotential_nonneg
    (rStar : ℝ) :
    0 ≤ reggeWheelerSmoothCompactPotential rStar := by
  by_cases hWindow : |rStar| < 1
  · unfold reggeWheelerSmoothCompactPotential
    rw [if_pos hWindow]
    exact (Real.exp_pos _).le
  · simp [
      reggeWheelerSmoothCompactPotential,
      hWindow
    ]

theorem reggeWheelerSmoothCompactPotential_le_one
    (rStar : ℝ) :
    reggeWheelerSmoothCompactPotential rStar ≤ 1 := by
  by_cases hWindow : |rStar| < 1
  · unfold reggeWheelerSmoothCompactPotential
    rw [if_pos hWindow]
    rcases abs_lt.mp hWindow with
      ⟨hLower, hUpper⟩
    have hLeftPositive :
        0 < 1 + rStar := by
      linarith
    have hRightPositive :
        0 < 1 - rStar := by
      linarith
    have hProductPositive :
        0 < (1 - rStar) * (1 + rStar) :=
      mul_pos hRightPositive hLeftPositive
    have hDenominator :
        0 < 1 - rStar ^ 2 := by
      nlinarith
    have hReciprocal :
        0 ≤ 1 / (1 - rStar ^ 2) :=
      (one_div_pos.mpr hDenominator).le
    calc
      Real.exp (-(1 / (1 - rStar ^ 2))) ≤
          Real.exp 0 := by
        exact
          Real.exp_le_exp.mpr
            (neg_nonpos.mpr hReciprocal)
      _ = 1 := Real.exp_zero
  · simp [
      reggeWheelerSmoothCompactPotential,
      hWindow
    ]

theorem reggeWheelerSmoothCompactPotential_abs_le_one
    (rStar : ℝ) :
    |reggeWheelerSmoothCompactPotential rStar| ≤ 1 := by
  rw [
    abs_of_nonneg
      (reggeWheelerSmoothCompactPotential_nonneg
        rStar)
  ]
  exact
    reggeWheelerSmoothCompactPotential_le_one
      rStar

theorem
    reggeWheelerSmoothCompactPotential_eq_zero_of_one_le_abs
    {rStar : ℝ}
    (hOutside : 1 ≤ |rStar|) :
    reggeWheelerSmoothCompactPotential rStar = 0 := by
  simp [
    reggeWheelerSmoothCompactPotential,
    not_lt.mpr hOutside
  ]

/--
Exact support certificate: every nonzero point lies in the open unit window.
Consequently the support closure is contained in the compact interval
`[-1, 1]`.
-/
theorem
    reggeWheelerSmoothCompactPotential_nonzero_implies_abs_lt_one
    {rStar : ℝ}
    (hNonzero :
      reggeWheelerSmoothCompactPotential rStar ≠ 0) :
    |rStar| < 1 := by
  by_contra hWindow
  exact
    hNonzero
      (reggeWheelerSmoothCompactPotential_eq_zero_of_one_le_abs
        (le_of_not_gt hWindow))

theorem reggeWheelerSmoothCompactPotential_zero :
    reggeWheelerSmoothCompactPotential 0 =
      Real.exp (-1) := by
  norm_num [reggeWheelerSmoothCompactPotential]

theorem reggeWheelerSmoothCompactPotential_ne_zero :
    reggeWheelerSmoothCompactPotential ≠ 0 := by
  intro hZero
  have hAtZero :
      reggeWheelerSmoothCompactPotential 0 = 0 := by
    simpa using
      congrArg
        (fun potential : ℝ → ℝ =>
          potential 0)
        hZero
  rw [
    reggeWheelerSmoothCompactPotential_zero
  ] at hAtZero
  exact
    (Real.exp_ne_zero (-1))
      hAtZero

/--
Pointwise multiplication by the smooth compact-window potential.
-/
def reggeWheelerSmoothCompactPotentialInsertion :
    (ℝ → ℝ) →ₗ[ℝ] (ℝ → ℝ) where
  toFun profile :=
    fun rStar =>
      reggeWheelerSmoothCompactPotential rStar *
        profile rStar
  map_add' := by
    intro left right
    ext rStar
    simp [mul_add]
  map_smul' := by
    intro scalar profile
    ext rStar
    simp [smul_eq_mul]
    ring

/--
Repulsive-sign deformation:

`H_lambda = H_RW + lambda U_smooth`.
-/
def reggeWheelerSmoothRepulsiveOperator
    (reggeWheelerOperator :
      (ℝ → ℝ) →ₗ[ℝ] (ℝ → ℝ))
    (lambda : ℝ) :
    (ℝ → ℝ) →ₗ[ℝ] (ℝ → ℝ) :=
  reggeWheelerOperator +
    lambda •
      reggeWheelerSmoothCompactPotentialInsertion

theorem reggeWheelerSmoothRepulsiveOperator_zero
    (reggeWheelerOperator :
      (ℝ → ℝ) →ₗ[ℝ] (ℝ → ℝ)) :
    reggeWheelerSmoothRepulsiveOperator
        reggeWheelerOperator
        0 =
      reggeWheelerOperator := by
  simp [reggeWheelerSmoothRepulsiveOperator]

/--
Repository-native Vasquez realization of the standard Lebesgue integral
over the Regge–Wheeler tortoise coordinate.

This is a named realization of Mathlib's integral, not a new integration
theory.
-/
def vasquezReggeWheelerIntegral
    (profile : ℝ → ℝ) :
    ℝ :=
  ∫ rStar, profile rStar

theorem vasquezReggeWheelerIntegral_nonneg
    (profile : ℝ → ℝ)
    (hProfile :
      ∀ rStar, 0 ≤ profile rStar) :
    0 ≤ vasquezReggeWheelerIntegral profile := by
  unfold vasquezReggeWheelerIntegral
  exact MeasureTheory.integral_nonneg hProfile

/--
A square-integrable profile produces an integrable smooth-potential
quadratic density.

The premise is the direct real-valued `L²` condition that `profile²`
is Lebesgue integrable.
-/
theorem
    reggeWheelerSmoothPotentialWeightedSquare_integrable_of_integrable_sq
    (profile : ℝ → ℝ)
    (hProfileSquare :
      MeasureTheory.Integrable
        (fun rStar =>
          profile rStar ^ 2)) :
    MeasureTheory.Integrable
      (fun rStar =>
        reggeWheelerSmoothCompactPotential rStar *
          profile rStar ^ 2) := by
  have hWindowMeasurable :
      MeasurableSet
        {rStar : ℝ | |rStar| < 1} := by
    change
      MeasurableSet
        ((fun rStar : ℝ => |rStar|) ⁻¹'
          Set.Iio 1)
    exact
      measurableSet_Iio.preimage
        continuous_abs.measurable
  have hInsideMeasurable :
      Measurable
        (fun rStar : ℝ =>
          Real.exp
            (-(1 / (1 - rStar ^ 2)))) := by
    measurability
  have hPotentialMeasurable :
      Measurable
        reggeWheelerSmoothCompactPotential := by
    unfold reggeWheelerSmoothCompactPotential
    exact
      Measurable.ite
        hWindowMeasurable
        hInsideMeasurable
        measurable_const
  have hWeightedMeasurable :
      MeasureTheory.AEStronglyMeasurable
        (fun rStar =>
          reggeWheelerSmoothCompactPotential rStar *
            profile rStar ^ 2) := by
    exact
      hPotentialMeasurable.aestronglyMeasurable.mul
        hProfileSquare.aestronglyMeasurable
  apply
    hProfileSquare.mono
      hWeightedMeasurable
  filter_upwards with rStar
  simp only [Real.norm_eq_abs]
  have hPotentialNonnegative :
      0 ≤ reggeWheelerSmoothCompactPotential rStar :=
    reggeWheelerSmoothCompactPotential_nonneg
      rStar
  have hPotentialAtMostOne :
      reggeWheelerSmoothCompactPotential rStar ≤ 1 :=
    reggeWheelerSmoothCompactPotential_le_one
      rStar
  have hSquareNonnegative :
      0 ≤ profile rStar ^ 2 :=
    sq_nonneg (profile rStar)
  rw [
    abs_of_nonneg
      (mul_nonneg
        hPotentialNonnegative
        hSquareNonnegative),
    abs_of_nonneg hSquareNonnegative
  ]
  exact
    mul_le_of_le_one_left
      hSquareNonnegative
      hPotentialAtMostOne

/--
A domain-bearing Regge–Wheeler profile carrying the exact square-integrability
condition needed by the smooth-potential quadratic energy.
-/
structure ReggeWheelerSquareIntegrableProfile where
  profile : ℝ → ℝ
  square_integrable :
    MeasureTheory.Integrable
      (fun rStar =>
        profile rStar ^ 2)

/--
Concrete Vasquez-integral potential contribution

`Q_U[Psi] = ∫ U_smooth(rStar) Psi(rStar)^2 drStar`.
-/
def reggeWheelerSmoothPotentialQuadraticEnergy
    (profile : ℝ → ℝ) :
    ℝ :=
  vasquezReggeWheelerIntegral
    (fun rStar =>
      reggeWheelerSmoothCompactPotential rStar *
        profile rStar ^ 2)

/--
Domain-bearing realization of the smooth-potential quadratic energy.
-/
def reggeWheelerSmoothPotentialQuadraticEnergyOnDomain
    (profile : ReggeWheelerSquareIntegrableProfile) :
    ℝ :=
  reggeWheelerSmoothPotentialQuadraticEnergy
    profile.profile

theorem
    reggeWheelerSmoothPotentialQuadraticEnergyOnDomain_density_integrable
    (profile : ReggeWheelerSquareIntegrableProfile) :
    MeasureTheory.Integrable
      (fun rStar =>
        reggeWheelerSmoothCompactPotential rStar *
          profile.profile rStar ^ 2) := by
  exact
    reggeWheelerSmoothPotentialWeightedSquare_integrable_of_integrable_sq
      profile.profile
      profile.square_integrable

theorem
    reggeWheelerSmoothPotentialQuadraticEnergy_nonneg
    (profile : ℝ → ℝ) :
    0 ≤
      reggeWheelerSmoothPotentialQuadraticEnergy
        profile := by
  apply vasquezReggeWheelerIntegral_nonneg
  intro rStar
  exact
    mul_nonneg
      (reggeWheelerSmoothCompactPotential_nonneg
        rStar)
      (sq_nonneg (profile rStar))

/--
Repulsive quadratic energy with a concrete integral:

`E_lambda[Psi] = E_0[Psi] + lambda Q_U[Psi]`.
-/
def reggeWheelerSmoothRepulsiveEnergy
    (baseEnergy : (ℝ → ℝ) → ℝ)
    (lambda : ℝ)
    (profile : ℝ → ℝ) :
    ℝ :=
  baseEnergy profile +
    lambda *
      reggeWheelerSmoothPotentialQuadraticEnergy
        profile

/--
Domain-bearing repulsive energy for square-integrable profiles.
-/
def reggeWheelerSmoothRepulsiveEnergyOnDomain
    (baseEnergy : (ℝ → ℝ) → ℝ)
    (lambda : ℝ)
    (profile : ReggeWheelerSquareIntegrableProfile) :
    ℝ :=
  reggeWheelerSmoothRepulsiveEnergy
    baseEnergy
    lambda
    profile.profile

theorem reggeWheelerSmoothRepulsiveEnergy_ge_base
    (baseEnergy : (ℝ → ℝ) → ℝ)
    (lambda : ℝ)
    (hLambda : 0 ≤ lambda)
    (profile : ℝ → ℝ) :
    baseEnergy profile ≤
      reggeWheelerSmoothRepulsiveEnergy
        baseEnergy
        lambda
        profile := by
  unfold reggeWheelerSmoothRepulsiveEnergy
  exact
    le_add_of_nonneg_right
      (mul_nonneg
        hLambda
        (reggeWheelerSmoothPotentialQuadraticEnergy_nonneg
          profile))

theorem reggeWheelerSmoothRepulsiveEnergyOnDomain_ge_base
    (baseEnergy : (ℝ → ℝ) → ℝ)
    (lambda : ℝ)
    (hLambda : 0 ≤ lambda)
    (profile : ReggeWheelerSquareIntegrableProfile) :
    baseEnergy profile.profile ≤
      reggeWheelerSmoothRepulsiveEnergyOnDomain
        baseEnergy
        lambda
        profile := by
  unfold reggeWheelerSmoothRepulsiveEnergyOnDomain
  exact
    reggeWheelerSmoothRepulsiveEnergy_ge_base
      baseEnergy
      lambda
      hLambda
      profile.profile

theorem reggeWheelerSmoothRepulsiveEnergy_nonneg
    (baseEnergy : (ℝ → ℝ) → ℝ)
    (lambda : ℝ)
    (hLambda : 0 ≤ lambda)
    (hReggeWheelerPositive :
      ∀ profile, 0 ≤ baseEnergy profile)
    (profile : ℝ → ℝ) :
    0 ≤
      reggeWheelerSmoothRepulsiveEnergy
        baseEnergy
        lambda
        profile := by
  exact
    le_trans
      (hReggeWheelerPositive profile)
      (reggeWheelerSmoothRepulsiveEnergy_ge_base
        baseEnergy
        lambda
        hLambda
        profile)

theorem reggeWheelerSmoothRepulsiveEnergyOnDomain_nonneg
    (baseEnergy : (ℝ → ℝ) → ℝ)
    (lambda : ℝ)
    (hLambda : 0 ≤ lambda)
    (hReggeWheelerPositive :
      ∀ profile : ReggeWheelerSquareIntegrableProfile,
        0 ≤ baseEnergy profile.profile)
    (profile : ReggeWheelerSquareIntegrableProfile) :
    0 ≤
      reggeWheelerSmoothRepulsiveEnergyOnDomain
        baseEnergy
        lambda
        profile := by
  exact
    le_trans
      (hReggeWheelerPositive profile)
      (reggeWheelerSmoothRepulsiveEnergyOnDomain_ge_base
        baseEnergy
        lambda
        hLambda
        profile)

/--
A domain-valid negative quadratic-energy mode is a square-integrable profile
whose domain-bearing energy is strictly negative.
-/
def ReggeWheelerNegativeQuadraticEnergyModeOnDomain
    (energy :
      ReggeWheelerSquareIntegrableProfile → ℝ) :
    Prop :=
  ∃ profile, energy profile < 0

/--
Positivity of the undeformed energy on the square-integrable domain and
`lambda ≥ 0` exclude negative quadratic-energy modes for the domain-bearing
repulsive branch.
-/
theorem
    reggeWheelerSmoothRepulsiveOnDomain_noNegativeQuadraticEnergyMode
    (baseEnergy : (ℝ → ℝ) → ℝ)
    (lambda : ℝ)
    (hLambda : 0 ≤ lambda)
    (hReggeWheelerPositive :
      ∀ profile : ReggeWheelerSquareIntegrableProfile,
        0 ≤ baseEnergy profile.profile) :
    ¬ ReggeWheelerNegativeQuadraticEnergyModeOnDomain
        (reggeWheelerSmoothRepulsiveEnergyOnDomain
          baseEnergy
          lambda) := by
  rintro ⟨profile, hNegative⟩
  exact
    (not_lt_of_ge
      (reggeWheelerSmoothRepulsiveEnergyOnDomain_nonneg
        baseEnergy
        lambda
        hLambda
        hReggeWheelerPositive
        profile))
      hNegative

/--
A negative quadratic-energy mode is a profile whose quadratic energy is
strictly negative.
-/
def ReggeWheelerNegativeQuadraticEnergyMode
    (energy : (ℝ → ℝ) → ℝ) :
    Prop :=
  ∃ profile, energy profile < 0

/--
Positivity of the undeformed Regge–Wheeler energy and `lambda ≥ 0`
exclude negative quadratic-energy profiles for the concrete
Vasquez-integral repulsive branch.
-/
theorem
    reggeWheelerSmoothRepulsive_noNegativeQuadraticEnergyMode
    (baseEnergy : (ℝ → ℝ) → ℝ)
    (lambda : ℝ)
    (hLambda : 0 ≤ lambda)
    (hReggeWheelerPositive :
      ∀ profile, 0 ≤ baseEnergy profile) :
    ¬ ReggeWheelerNegativeQuadraticEnergyMode
        (reggeWheelerSmoothRepulsiveEnergy
          baseEnergy
          lambda) := by
  rintro ⟨profile, hNegative⟩
  exact
    (not_lt_of_ge
      (reggeWheelerSmoothRepulsiveEnergy_nonneg
        baseEnergy
        lambda
        hLambda
        hReggeWheelerPositive
        profile))
      hNegative

def reggeWheelerSmoothRepulsiveEnergyBoundary : String :=
  "CONCRETE_LEBESGUE_INTEGRAL_REALIZED_WEIGHTED_PROFILE_INTEGRABILITY_ENFORCED_ON_SQUARE_INTEGRABLE_DOMAIN_C_INFINITY_NOT_FORMALIZED_NO_SELF_ADJOINT_SPECTRAL_EIGENMODE_THEOREM"

def reggeWheelerBoundedPotentialResponseStatus : String :=
  "CONCRETE_BOUNDED_WINDOW_POTENTIAL_AND_CERTIFIED_NONZERO_RESPONSE_IMPLICATION"

def reggeWheelerBoundedPotentialResponseBoundary : String :=
  "NO_COVARIANT_ORIGIN_NO_SMOOTH_POTENTIAL_NO_RESPONSE_CONSTRUCTION_NO_MEASURABLE_NONZERO_PREDICTION"

end

end Chronos.Frontier
