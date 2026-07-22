import Chronos.Frontier.FiniteHardSoftEmissionChannel

namespace Chronos.Frontier

noncomputable section

/-!
# Conditional Regge–Wheeler deviation interface

The existing Regge–Wheeler bridge proves that identical equations and
identical initial data give identical solutions under the encoded uniqueness
property. Consequently, no nonzero observable deviation follows from the
standard Regge–Wheeler equation alone.

This module isolates the weakest conditional extension:

`(L_RW - λ U) Ψ_λ = 0`.

Corrections encoded here:

* gauge invariance of a deformed solution is not automatic and is not claimed;
* existence of the asymptotic radiation limit is not assumed silently;
* the retarded Green response is an explicit uninhabited ansatz;
* a nonzero first-order observable shift requires a nonzero first-order
  response;
* a nonzero first-order flux shift requires a nonzero interference
  coefficient, but a vanishing first-order coefficient does not exclude a
  quadratic shift;
* no covariant action or field equation deriving `λ U` is supplied.
-/

/--
Potential deformation of a linear Regge–Wheeler operator.
-/
def reggeWheelerDeformedOperator
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (principalOperator potentialInsertion :
      State →ₗ[ℝ] State)
    (lambda : ℝ) :
    State →ₗ[ℝ] State :=
  principalOperator -
    lambda • potentialInsertion

theorem reggeWheelerDeformedOperator_zero
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (principalOperator potentialInsertion :
      State →ₗ[ℝ] State) :
    reggeWheelerDeformedOperator
        principalOperator
        potentialInsertion
        0 =
      principalOperator := by
  simp [reggeWheelerDeformedOperator]

-- DERIVED_COUPLED_ODD_PARITY_OPERATOR

/--
The action-derived two-channel operator

  Lε (ψ, θ) =
    (D_RW ψ + ε W θ,
     ε W ψ + D_s θ + ε² Q θ).

The deformation is represented by a coupled operator rather than a freely
supplied scalar potential insertion.
-/
def reggeWheelerDerivedCoupledOperator
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (reggeWheelerOperator scalarOperator coupling scalarCorrection :
      State →ₗ[ℝ] State)
    (epsilon : ℝ) :
    (State × State) →ₗ[ℝ] (State × State) where
  toFun state :=
    ( reggeWheelerOperator state.1 +
        epsilon • coupling state.2,
      epsilon • coupling state.1 +
        scalarOperator state.2 +
        epsilon ^ 2 • scalarCorrection state.2 )
  map_add' := by
    intro left right
    ext <;>
      simp [add_assoc, add_left_comm, add_comm]
  map_smul' := by
    intro scalar state
    ext <;>
      simp [smul_add, smul_smul, mul_comm]

-- DERIVED_COUPLED_RESPONSE_INTERFACE

/--
Primary response carrier for the action-derived coupled system.

This interface contains no freely supplied scalar potential insertion.
-/
structure ReggeWheelerDerivedCoupledResponseData
    (State : Type*)
    [AddCommGroup State]
    [Module ℝ State] where
  reggeWheelerOperator : State →ₗ[ℝ] State
  scalarOperator : State →ₗ[ℝ] State
  coupling : State →ₗ[ℝ] State
  scalarCorrection : State →ₗ[ℝ] State
  epsilon : ℝ
  background : State
  scalarFirstOrder : State
  gravitationalFirstOrder : State
  backgroundEquation :
    reggeWheelerOperator background = 0
  scalarFirstOrderEquation :
    scalarOperator scalarFirstOrder =
      -(coupling background)
  gravitationalFirstOrderEquation :
    reggeWheelerOperator gravitationalFirstOrder =
      -(coupling scalarFirstOrder)

/-- The coupled operator determined by derived response data. -/
def ReggeWheelerDerivedCoupledResponseData.operator
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (data : ReggeWheelerDerivedCoupledResponseData State) :
    (State × State) →ₗ[ℝ] (State × State) :=
  reggeWheelerDerivedCoupledOperator
    data.reggeWheelerOperator
    data.scalarOperator
    data.coupling
    data.scalarCorrection
    data.epsilon

-- DERIVED_COUPLED_H2_DOMAIN

/--
The direct-sum operator domain encoding

  D(Aε) = H²(ℝ) ⊕ H²(ℝ).

`h2Domain` is the repository-side predicate representing membership in
`H²(ℝ)`.
-/
def reggeWheelerDerivedCoupledOperatorDomain
    {State : Type*}
    (h2Domain : Set State) :
    Set (State × State) :=
  { state | state.1 ∈ h2Domain ∧ state.2 ∈ h2Domain }

/--
Membership in the coupled domain is exactly componentwise membership in the
selected H² domain.
-/
theorem mem_reggeWheelerDerivedCoupledOperatorDomain_iff
    {State : Type*}
    (h2Domain : Set State)
    (state : State × State) :
    state ∈ reggeWheelerDerivedCoupledOperatorDomain h2Domain ↔
      state.1 ∈ h2Domain ∧ state.2 ∈ h2Domain :=
  Iff.rfl

-- PSI_ONE_FOURTH_DERIVATIVE_CERTIFICATE

/--
The zero-time derivative identities

  θ₁''(0) = -W p,
  Ψ₁⁽⁴⁾(0) = -W θ₁''(0).
-/
structure ReggeWheelerDerivativeCertificateData
    (State : Type*)
    [AddCommGroup State]
    [Module ℝ State] where
  coupling : State →ₗ[ℝ] State
  profile : State
  scalarSecondDerivativeAtZero : State
  psiFourthDerivativeAtZero : State
  scalarSecondDerivativeEquation :
    scalarSecondDerivativeAtZero =
      -(coupling profile)
  psiFourthDerivativeEquation :
    psiFourthDerivativeAtZero =
      -(coupling scalarSecondDerivativeAtZero)

/--
Exact derivative certificate

  Ψ₁⁽⁴⁾(0) = W²p.
-/
theorem reggeWheelerPsiOneFourthDerivativeAtZero
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (data : ReggeWheelerDerivativeCertificateData State) :
    data.psiFourthDerivativeAtZero =
      data.coupling (data.coupling data.profile) := by
  calc
    data.psiFourthDerivativeAtZero =
        -(data.coupling data.scalarSecondDerivativeAtZero) :=
      data.psiFourthDerivativeEquation
    _ = -(data.coupling (-(data.coupling data.profile))) := by
      rw [data.scalarSecondDerivativeEquation]
    _ = data.coupling (data.coupling data.profile) := by
      simp

-- SMALL_TIME_OBSERVABLE_POSITIVITY

/--
Leading term in the small-time detector expansion

  O_T[Ψ₁] =
    T⁵ / 120 · ‖Ψ₁⁽⁴⁾(0)‖² + remainder.
-/
def reggeWheelerSmallTimeObservableLeadingTerm
    {State : Type*}
    [NormedAddCommGroup State]
    (T : ℝ)
    (response : State) :
    ℝ :=
  T ^ 5 / 120 * ‖response‖ ^ 2

/--
A nonzero `W²p` and a remainder whose absolute value is strictly smaller than
the leading term imply

  O_T[Ψ₁] > 0.
-/
theorem reggeWheelerSmallTimeObservable_pos
    {State : Type*}
    [NormedAddCommGroup State]
    [NormedSpace ℝ State]
    (data : ReggeWheelerDerivativeCertificateData State)
    (T remainder observable : ℝ)
    (hT : 0 < T)
    (hResponse :
      data.coupling (data.coupling data.profile) ≠ 0)
    (hExpansion :
      observable =
        reggeWheelerSmallTimeObservableLeadingTerm
          T
          data.psiFourthDerivativeAtZero +
        remainder)
    (hRemainder :
      |remainder| <
        reggeWheelerSmallTimeObservableLeadingTerm
          T
          data.psiFourthDerivativeAtZero) :
    0 < observable := by
  have hFourthDerivative :
      data.psiFourthDerivativeAtZero =
        data.coupling (data.coupling data.profile) :=
    reggeWheelerPsiOneFourthDerivativeAtZero data

  have hFourthDerivativeNe :
      data.psiFourthDerivativeAtZero ≠ 0 := by
    rw [hFourthDerivative]
    exact hResponse

  have hNormPos :
      0 < ‖data.psiFourthDerivativeAtZero‖ :=
    norm_pos_iff.mpr hFourthDerivativeNe

  have hTimePower :
      0 < T ^ 5 :=
    pow_pos hT 5

  have hCoefficient :
      0 < T ^ 5 / 120 := by
    positivity

  have hNormSquare :
      0 < ‖data.psiFourthDerivativeAtZero‖ ^ 2 :=
    pow_pos hNormPos 2

  have hLeading :
      0 <
        reggeWheelerSmallTimeObservableLeadingTerm
          T
          data.psiFourthDerivativeAtZero := by
    unfold reggeWheelerSmallTimeObservableLeadingTerm
    exact mul_pos hCoefficient hNormSquare

  have hRemainderLower :
      -reggeWheelerSmallTimeObservableLeadingTerm
          T
          data.psiFourthDerivativeAtZero <
        remainder :=
    (abs_lt.mp hRemainder).1

  rw [hExpansion]
  linarith

-- DERIVED_FIRST_ORDER_GRAVITATIONAL_RESIDUAL

/--
The first-order gravitational approximation in the action-derived coupled
system satisfies the source-subtracted identity

  D_RW (Ψ₀ + λ Ψ₁) + λ W θ₁ = 0.
-/
theorem reggeWheelerDerivedFirstOrderApproximationResidual
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (data : ReggeWheelerDerivedCoupledResponseData State)
    (lambda : ℝ) :
    data.reggeWheelerOperator
          (data.background +
            lambda • data.gravitationalFirstOrder) +
        lambda • data.coupling data.scalarFirstOrder =
      0 := by
  simp [
    data.backgroundEquation,
    data.gravitationalFirstOrderEquation
  ]

-- DERIVED_COUPLED_EXACT_RESIDUAL

/--
For the action-derived coupled operator, the truncation

  (Ψ₀ + ε² Ψ₁, ε θ₁)

has zero gravitational residual. Its remaining scalar-channel residual consists
only of the cubic coupling and scalar-correction terms.
-/
theorem reggeWheelerDerivedCoupledApproximation_exactResidual
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (data : ReggeWheelerDerivedCoupledResponseData State) :
    data.operator
          ( data.background +
              data.epsilon ^ 2 • data.gravitationalFirstOrder,
            data.epsilon • data.scalarFirstOrder ) =
      ( 0,
        data.epsilon •
            data.coupling
              (data.epsilon ^ 2 • data.gravitationalFirstOrder) +
          data.epsilon ^ 2 •
            data.scalarCorrection
              (data.epsilon • data.scalarFirstOrder) ) := by
  change
    ( data.reggeWheelerOperator
          (data.background +
            data.epsilon ^ 2 • data.gravitationalFirstOrder) +
        data.epsilon •
          data.coupling
            (data.epsilon • data.scalarFirstOrder),
      data.epsilon •
          data.coupling
            (data.background +
              data.epsilon ^ 2 • data.gravitationalFirstOrder) +
        data.scalarOperator
          (data.epsilon • data.scalarFirstOrder) +
        data.epsilon ^ 2 •
          data.scalarCorrection
            (data.epsilon • data.scalarFirstOrder) ) =
      ( 0,
        data.epsilon •
            data.coupling
              (data.epsilon ^ 2 • data.gravitationalFirstOrder) +
          data.epsilon ^ 2 •
            data.scalarCorrection
              (data.epsilon • data.scalarFirstOrder) )
  ext
  · simp [
      data.backgroundEquation,
      data.gravitationalFirstOrderEquation,
      smul_smul,
      pow_two
    ]
  · simp [
      data.scalarFirstOrderEquation, smul_add, add_assoc
    ]

/--
A nontrivial formal deformation parameter and potential insertion.

This does not provide a covariant origin for either object.
-/
structure ReggeWheelerPotentialDeformation
    (State : Type*)
    [AddCommGroup State]
    [Module ℝ State] where
  principalOperator : State →ₗ[ℝ] State
  potentialInsertion : State →ₗ[ℝ] State
  lambda : ℝ
  lambda_ne_zero : lambda ≠ 0
  potentialInsertion_ne_zero :
    potentialInsertion ≠ 0

/--
Background and first-order response satisfying

`L Ψ₀ = 0`,
`L Ψ₁ = U Ψ₀`.

The second equation is the first-order coefficient obtained formally from
`(L - λU)(Ψ₀ + λΨ₁ + O(λ²)) = 0`.
-/
structure ReggeWheelerFirstOrderDeviationData
    (State : Type*)
    [AddCommGroup State]
    [Module ℝ State] where
  principalOperator : State →ₗ[ℝ] State
  potentialInsertion : State →ₗ[ℝ] State
  background : State
  firstOrderCorrection : State
  backgroundEquation :
    principalOperator background = 0
  firstOrderEquation :
    principalOperator firstOrderCorrection =
      potentialInsertion background

/--
The first-order approximation solves the deformed equation up to the omitted
term `-λ² U Ψ₁`.
-/
theorem reggeWheelerFirstOrderApproximationResidual
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (D : ReggeWheelerFirstOrderDeviationData State)
    (lambda : ℝ) :
    D.principalOperator
          (D.background +
            lambda • D.firstOrderCorrection) -
        lambda •
          D.potentialInsertion D.background =
      0 := by
  simp [
    D.backgroundEquation,
    D.firstOrderEquation
  ]

/--
The exact residual of the first-order approximation under the full deformed
operator is the quadratic term `-λ² U Ψ₁`.

This strengthens the earlier source-subtracted identity without introducing
a response operator, Green kernel, asymptotic assumption, or external theorem.
-/
theorem
    reggeWheelerFirstOrderApproximation_exactDeformedResidual
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (D : ReggeWheelerFirstOrderDeviationData State)
    (lambda : ℝ) :
    reggeWheelerDeformedOperator
          D.principalOperator
          D.potentialInsertion
          lambda
          (D.background +
            lambda • D.firstOrderCorrection) =
      -(lambda ^ 2) •
        D.potentialInsertion D.firstOrderCorrection := by
  change
    D.principalOperator
          (D.background +
            lambda • D.firstOrderCorrection) -
        lambda •
          D.potentialInsertion
            (D.background +
              lambda • D.firstOrderCorrection) =
      -(lambda ^ 2) •
        D.potentialInsertion D.firstOrderCorrection
  rw [
    map_add,
    map_smul,
    D.backgroundEquation,
    D.firstOrderEquation
  ]
  rw [map_add, map_smul]
  simp [smul_add, smul_smul, pow_two]

/--
For nonzero coupling, the first-order approximation is an exact solution of
the full deformed equation exactly when the potential insertion annihilates
the first-order correction.

This is a repository-native obstruction theorem: a genuinely nonzero
second insertion prevents the first-order truncation from being exact.
-/
theorem
    reggeWheelerFirstOrderApproximation_exact_iff
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (D : ReggeWheelerFirstOrderDeviationData State)
    (lambda : ℝ)
    (hLambda : lambda ≠ 0) :
    reggeWheelerDeformedOperator
          D.principalOperator
          D.potentialInsertion
          lambda
          (D.background +
            lambda • D.firstOrderCorrection) =
        0 ↔
      D.potentialInsertion D.firstOrderCorrection =
        0 := by
  rw [
    reggeWheelerFirstOrderApproximation_exactDeformedResidual
      D
      lambda
  ]
  constructor
  · intro hResidual
    have hScalar :
        -(lambda ^ 2) ≠ 0 := by
      exact
        neg_ne_zero.mpr
          (pow_ne_zero 2 hLambda)
    exact
      (smul_eq_zero.mp hResidual).resolve_left
        hScalar
  · intro hInsertion
    simp [hInsertion]

/--
Exact deviation of a linear observable on the first-order approximation.
-/
theorem reggeWheelerLinearObservableDeviation
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (observable : State →ₗ[ℝ] ℝ)
    (background correction : State)
    (lambda : ℝ) :
    observable (background + lambda • correction) -
        observable background =
      lambda * observable correction := by
  simp [smul_eq_mul]

/--
A nonzero first-order observable response produces a nonzero observable
deviation for nonzero coupling.
-/
theorem reggeWheelerLinearObservableDeviation_ne_zero
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (observable : State →ₗ[ℝ] ℝ)
    (background correction : State)
    (lambda : ℝ)
    (hLambda : lambda ≠ 0)
    (hResponse : observable correction ≠ 0) :
    observable (background + lambda • correction) -
        observable background ≠
      0 := by
  rw [
    reggeWheelerLinearObservableDeviation
      observable background correction lambda
  ]
  exact mul_ne_zero hLambda hResponse

/--
Real-amplitude asymptotic energy-flux normalization.

The complex-amplitude formula would require a real-part interference term.
This real version avoids silently identifying complex multiplication with a
real scalar product.
-/
def reggeWheelerRealAsymptoticFlux
    (amplitude : ℝ) : ℝ :=
  amplitude ^ 2 / (64 * Real.pi)

/--
Exact flux expansion for a first-order real amplitude:

`F(a₀ + λa₁) - F(a₀)`
equals its linear interference term plus the quadratic remainder.
-/
theorem reggeWheelerRealAsymptoticFluxDeviation
    (backgroundResponse firstOrderResponse lambda : ℝ) :
    reggeWheelerRealAsymptoticFlux
          (backgroundResponse +
            lambda * firstOrderResponse) -
        reggeWheelerRealAsymptoticFlux
          backgroundResponse =
      lambda *
          (backgroundResponse * firstOrderResponse /
            (32 * Real.pi)) +
        lambda ^ 2 *
          (firstOrderResponse ^ 2 /
            (64 * Real.pi)) := by
  unfold reggeWheelerRealAsymptoticFlux
  ring

/--
Coefficient of the first-order real flux shift.
-/
def reggeWheelerRealFluxFirstOrderCoefficient
    (backgroundResponse firstOrderResponse : ℝ) :
    ℝ :=
  backgroundResponse * firstOrderResponse /
    (32 * Real.pi)

/--
A retarded-response carrier for the formal equation `L Ψ₁ = U Ψ₀`.

No inhabitant is constructed. In particular, this module does not prove
existence of a retarded Green operator, support properties, asymptotic limits,
or boundedness on a function space.
-/
structure ReggeWheelerRetardedResponseAnsatz
    (State : Type*)
    [AddCommGroup State]
    [Module ℝ State] where
  principalOperator : State →ₗ[ℝ] State
  potentialInsertion : State →ₗ[ℝ] State
  retardedResponse : State →ₗ[ℝ] State
  responseEquation :
    principalOperator.comp retardedResponse =
      potentialInsertion

/--
An asymptotic observable is supplied as a linear functional together with an
explicit existence predicate for the intended limit construction.
-/
structure ReggeWheelerAsymptoticObservable
    (State : Type*)
    [AddCommGroup State]
    [Module ℝ State] where
  observable : State →ₗ[ℝ] ℝ
  asymptoticLimitExists : State → Prop

def reggeWheelerConditionalDeviationStatus : String :=
  "NONZERO_DEVIATION_REQUIRES_NONTRIVIAL_DEFORMED_DYNAMICS"

def reggeWheelerConditionalDeviationProved : String :=
  "FIRST_ORDER_SOURCE_RESIDUAL_LINEAR_OBSERVABLE_SHIFT_AND_EXACT_REAL_FLUX_EXPANSION"

def reggeWheelerConditionalDeviationBoundary : String :=
  "NO_COVARIANT_ACTION_NO_DEFORMATION_DERIVATION_NO_RETARDED_RESPONSE_INHABITANT_NO_ASYMPTOTIC_LIMIT_THEOREM"

end

end Chronos.Frontier
