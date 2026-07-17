import Chronos.Frontier.ReggeWheelerBoundedPotentialResponse

namespace Chronos.Frontier

noncomputable section

/-!
# Flagship exact-residual theorem

## Purpose

This module freezes the current Regge–Wheeler deformation program around one
precise flagship result. It packages the strongest completed theorem chain
without presenting the supplied first-order response as a constructed PDE
solution.

## Accepted hypotheses

For a real module `State`, two linear maps `L` and `U`, and states `Ψ₀`, `Ψ₁`,
the input data supplies

`L Ψ₀ = 0`

and

`L Ψ₁ = U Ψ₀`.

The module does not construct `Ψ₁`, prove an operator-domain theorem, or prove
that `U Ψ₁ ≠ 0`.

## Constructed conclusions

The full deformed residual of the first-order approximation is exactly

`(L - λU)(Ψ₀ + λΨ₁) = -λ² U Ψ₁`.

For nonzero `λ`, exactness is equivalent to `U Ψ₁ = 0`.

## Exact boundary

The next flagship milestone is a repository-native, domain-bearing construction
of one response `Ψ₁` together with a proof that `U Ψ₁ ≠ 0`.
-/

/--
For nonzero coupling, the first-order approximation solves the full deformed
equation exactly if and only if the second potential insertion vanishes.
-/
theorem reggeWheelerFlagship_exactnessCriterion
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
A nonzero second insertion is the exact obstruction to first-order exactness
when the coupling is nonzero.
-/
theorem reggeWheelerFlagship_nonzeroSecondInsertion_notExact
    {State : Type*}
    [AddCommGroup State]
    [Module ℝ State]
    (D : ReggeWheelerFirstOrderDeviationData State)
    (lambda : ℝ)
    (hLambda : lambda ≠ 0)
    (hInsertion :
      D.potentialInsertion D.firstOrderCorrection ≠
        0) :
    reggeWheelerDeformedOperator
          D.principalOperator
          D.potentialInsertion
          lambda
          (D.background +
            lambda • D.firstOrderCorrection) ≠
        0 := by
  intro hExact
  exact
    hInsertion
      ((reggeWheelerFlagship_exactnessCriterion
          D
          lambda
          hLambda).mp hExact)

/--
Paper-style package of the exact residual identity and its exactness
criterion. The equations in `D` remain accepted input hypotheses.
-/
theorem reggeWheelerFlagship_exactResidualPackage
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
        -(lambda ^ 2) •
          D.potentialInsertion
            D.firstOrderCorrection
      ∧
    (
      reggeWheelerDeformedOperator
            D.principalOperator
            D.potentialInsertion
            lambda
            (D.background +
              lambda • D.firstOrderCorrection) =
          0 ↔
        D.potentialInsertion
            D.firstOrderCorrection =
          0
    ) := by
  exact
    ⟨
      reggeWheelerFirstOrderApproximation_exactDeformedResidual
        D
        lambda,
      reggeWheelerFlagship_exactnessCriterion
        D
        lambda
        hLambda
    ⟩

def reggeWheelerFlagshipAcceptedHypotheses :
    List String :=
  [
    "STATE_IS_A_REAL_MODULE",
    "PRINCIPAL_OPERATOR_IS_LINEAR",
    "POTENTIAL_INSERTION_IS_LINEAR",
    "BACKGROUND_EQUATION_IS_SUPPLIED",
    "FIRST_ORDER_RESPONSE_EQUATION_IS_SUPPLIED"
  ]

def reggeWheelerFlagshipConstructedConclusions :
    List String :=
  [
    "EXACT_QUADRATIC_DEFORMED_RESIDUAL",
    "NONZERO_COUPLING_EXACTNESS_IFF_SECOND_INSERTION_VANISHES",
    "NONZERO_SECOND_INSERTION_FORCES_NONEXACT_FIRST_ORDER_TRUNCATION"
  ]

def reggeWheelerFlagshipProgramLock : String :=
  "SUSPEND_UNRELATED_EXPANSION_UNTIL_A_DOMAIN_BEARING_NONZERO_RESPONSE_IS_CONSTRUCTED"

def reggeWheelerFlagshipProgressMetric : String :=
  "COUNT_ELIMINATED_HYPOTHESES_NOT_MODULES"

def reggeWheelerFlagshipNextMilestone : String :=
  "CONSTRUCT_PSI1_AND_PROVE_POTENTIAL_INSERTION_PSI1_NE_ZERO"

def reggeWheelerFlagshipBoundary : String :=
  "NO_OPERATOR_DOMAIN_NO_PDE_EXISTENCE_NO_CONSTRUCTED_RESPONSE_NO_VERIFIED_NONZERO_OBSERVABLE"

end

end Chronos.Frontier
