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
