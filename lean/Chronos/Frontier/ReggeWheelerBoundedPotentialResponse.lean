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

def reggeWheelerBoundedPotentialResponseStatus : String :=
  "CONCRETE_BOUNDED_WINDOW_POTENTIAL_AND_CERTIFIED_NONZERO_RESPONSE_IMPLICATION"

def reggeWheelerBoundedPotentialResponseBoundary : String :=
  "NO_COVARIANT_ORIGIN_NO_SMOOTH_POTENTIAL_NO_RESPONSE_CONSTRUCTION_NO_MEASURABLE_NONZERO_PREDICTION"

end

end Chronos.Frontier
