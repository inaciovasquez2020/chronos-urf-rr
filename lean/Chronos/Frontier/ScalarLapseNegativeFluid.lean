import Mathlib

namespace Chronos.Frontier

noncomputable section

/--
Pointwise scalar-lapse plus irrotational negative-fluid
Lagrangian density.

This is an algebraic density interface. It does not by itself
derive the Euler-Lagrange PDEs.
-/
def scalarLapseNegativeFluidLagrangianDensity
    (A cgInvSq phiDotSq gradPhiSq
      varrho thetaDot speedSq expNegPhi
      epsilonAtVarRho : ℝ) : ℝ :=
  (A / 2) * (cgInvSq * phiDotSq - gradPhiSq) +
    varrho * (thetaDot - speedSq / 2) -
    expNegPhi * epsilonAtVarRho

/--
Pointwise Hamiltonian density associated with the toy model.
-/
def scalarLapseNegativeFluidHamiltonianDensity
    (A cgInvSq phiDotSq gradPhiSq
      varrho speedSq expNegPhi
      epsilonAtVarRho : ℝ) : ℝ :=
  (A / 2) * (cgInvSq * phiDotSq + gradPhiSq) +
    varrho * speedSq / 2 +
    expNegPhi * epsilonAtVarRho

theorem
    scalarLapseNegativeFluidHamiltonianDensity_nonneg
    (A cgInvSq phiDotSq gradPhiSq
      varrho speedSq expNegPhi
      epsilonAtVarRho : ℝ)
    (hA : 0 ≤ A)
    (hCg : 0 ≤ cgInvSq)
    (hPhiDot : 0 ≤ phiDotSq)
    (hGradPhi : 0 ≤ gradPhiSq)
    (hVarRho : 0 ≤ varrho)
    (hSpeed : 0 ≤ speedSq)
    (hExp : 0 ≤ expNegPhi)
    (hEpsilon : 0 ≤ epsilonAtVarRho) :
    0 ≤
      scalarLapseNegativeFluidHamiltonianDensity
        A
        cgInvSq
        phiDotSq
        gradPhiSq
        varrho
        speedSq
        expNegPhi
        epsilonAtVarRho := by
  unfold scalarLapseNegativeFluidHamiltonianDensity
  positivity

/--
Cancellation of equal and opposite scalar-fluid exchange terms.
-/
theorem
    scalarLapseNegativeFluid_localEnergyConservation
    (scalarTime scalarFlux
      fluidTime fluidFlux exchange : ℝ)
    (hScalar :
      scalarTime + scalarFlux = exchange)
    (hFluid :
      fluidTime + fluidFlux = -exchange) :
    (scalarTime + fluidTime) +
        (scalarFlux + fluidFlux) =
      0 := by
  linarith

/--
Algebraic residual carrier for the coupled linearized system.
-/
structure ScalarLapseNegativeFluidLinearizedResiduals where
  continuity : ℝ
  euler : ℝ
  scalarField : ℝ

def scalarLapseNegativeFluidContinuityResidual
    (sigmaDot divVarRhoU : ℝ) : ℝ :=
  sigmaDot + divVarRhoU

def scalarLapseNegativeFluidEulerResidual
    (uDot gradLinearizedChemicalPotential : ℝ) : ℝ :=
  uDot + gradLinearizedChemicalPotential

def scalarLapseNegativeFluidScalarResidual
    (cgInvSq chiDDot laplacianChi coupling
      expNegPhi hStar sigma epsilonStar chi : ℝ) :
    ℝ :=
  cgInvSq * chiDDot -
    laplacianChi -
    coupling *
      expNegPhi *
      (hStar * sigma - epsilonStar * chi)

/--
Exterior scalar charge when positive and negative sectors coexist.
-/
def scalarLapseEffectiveCharge
    (qPlus qMinus : ℝ) : ℝ :=
  qPlus - qMinus

theorem scalarLapseEffectiveCharge_negative
    (qPlus qMinus : ℝ)
    (h : qPlus < qMinus) :
    scalarLapseEffectiveCharge qPlus qMinus < 0 := by
  unfold scalarLapseEffectiveCharge
  linarith

theorem scalarLapseEffectiveCharge_zero
    (q : ℝ) :
    scalarLapseEffectiveCharge q q = 0 := by
  simp [scalarLapseEffectiveCharge]

/--
Leading finite-distance time shift with the positive geometry
factor supplied explicitly.
-/
def scalarLapseLeadingTimeShift
    (G c qPlus qMinus geometryFactor : ℝ) : ℝ :=
  G *
    scalarLapseEffectiveCharge qPlus qMinus /
    c ^ 3 *
    geometryFactor

/--
Signed asymptotic deflection coefficient.

The physical directional convention must be supplied separately.
-/
def scalarLapseLeadingAsymptoticDeflection
    (G c b qPlus qMinus : ℝ) : ℝ :=
  2 *
    G *
    scalarLapseEffectiveCharge qPlus qMinus /
    (b * c ^ 2)

/--
Dimensionless Hardy sufficient-coercivity ratio.
-/
def scalarLapseCompactBumpHardyRatio
    (compactness dimensionlessWSup : ℝ) : ℝ :=
  16 *
    Real.pi *
    compactness *
    dimensionlessWSup

/--
A certified interval enclosing a spectral quantity.

Creating a value of this structure requires proofs of both interval
endpoints. Floating-point output alone does not construct one.
-/
structure ScalarLapseCompactBumpSpectralInterval
    (spectralBottom : ℝ) where
  lower : ℝ
  upper : ℝ
  lower_le_spectralBottom :
    lower ≤ spectralBottom
  spectralBottom_le_upper :
    spectralBottom ≤ upper

/--
A certified nonnegative lower endpoint excludes negative spectrum.
-/
theorem
    scalarLapseCompactBump_noNegativeSpectrum_of_certifiedInterval
    {spectralBottom : ℝ}
    (certificate :
      ScalarLapseCompactBumpSpectralInterval
        spectralBottom)
    (hLower :
      0 ≤ certificate.lower) :
    0 ≤ spectralBottom := by
  exact
    le_trans
      hLower
      certificate.lower_le_spectralBottom

/--
A strictly positive certified lower endpoint implies a positive
spectral gap. No such certificate is presently supplied.
-/
theorem
    scalarLapseCompactBump_positiveSpectrum_of_certifiedInterval
    {spectralBottom : ℝ}
    (certificate :
      ScalarLapseCompactBumpSpectralInterval
        spectralBottom)
    (hLower :
      0 < certificate.lower) :
    0 < spectralBottom := by
  exact
    lt_of_lt_of_le
      hLower
      certificate.lower_le_spectralBottom

/--
A strictly negative certified upper endpoint proves negative spectrum.
No such certificate is presently supplied.
-/
theorem
    scalarLapseCompactBump_negativeSpectrum_of_certifiedInterval
    {spectralBottom : ℝ}
    (certificate :
      ScalarLapseCompactBumpSpectralInterval
        spectralBottom)
    (hUpper :
      certificate.upper < 0) :
    spectralBottom < 0 := by
  exact
    lt_of_le_of_lt
      certificate.spectralBottom_le_upper
      hUpper

def scalarLapseNegativeFluidStatus : String :=
  "ALGEBRAIC_ACTION_DENSITY_HAMILTONIAN_NONNEGATIVITY_EXCHANGE_CANCELLATION_LINEARIZED_RESIDUALS_EFFECTIVE_CHARGE_REGISTERED"

def scalarLapseNegativeFluidBoundary : String :=
  "NO_VARIATIONAL_PDE_DERIVATION_NO_FUNCTION_SPACE_NO_NUMERICAL_CERTIFICATE_NO_SPECTRAL_STABILITY_NO_PHYSICAL_NEGATIVE_COUPLING_EVIDENCE"


/--
Finite-box radii used in the floating-point radial-spectrum scan.

These are recorded data only. They are not interval enclosures.
-/
def scalarLapseCompactBumpFiniteBoxRadius :
    Fin 5 → ℚ
  | 0 => 4
  | 1 => 8
  | 2 => 12
  | 3 => 16
  | 4 => 20

/--
Finite-element resolution, measured in elements per unit source radius.
-/
def scalarLapseCompactBumpFiniteBoxElementsPerRadius :
    Fin 5 → ℕ
  | 0 => 50
  | 1 => 50
  | 2 => 50
  | 3 => 25
  | 4 => 25

/--
Recorded lowest generalized finite-box eigenvalues for compactness
`C = 0.1`.

Decimal notation is represented exactly as rational data. These values
do not constitute certified enclosures of the continuum operator.
-/
def scalarLapseCompactBumpFiniteBoxLambdaOne :
    Fin 5 → ℚ
  | 0 => 0.6397331833444341
  | 1 => 0.15713010762299523
  | 2 => 0.06940249458005165
  | 3 => 0.038917191339309695
  | 4 => 0.024860213880436244

/--
Lowest Dirichlet eigenvalue `π² / L²` of the corresponding free
finite-box comparison problem, recorded from the same numerical scan.
-/
def scalarLapseCompactBumpFiniteBoxFreeLambdaOne :
    Fin 5 → ℚ
  | 0 => 0.6168502750680849
  | 1 => 0.15421256876702122
  | 2 => 0.06853891945200943
  | 3 => 0.038553142191755305
  | 4 => 0.024674011002723394

/--
Recorded Schur-complement denominator from the finite-element scan.
-/
def scalarLapseCompactBumpFiniteBoxSchurDenominator :
    Fin 5 → ℚ
  | 0 => 3.117747717095451
  | 1 => 3.117747717095451
  | 2 => 3.117747717095451
  | 3 => 3.117747716773997
  | 4 => 3.117747716773997

theorem
    scalarLapseCompactBumpFiniteBoxLambdaOne_positive
    (index : Fin 5) :
    0 <
      scalarLapseCompactBumpFiniteBoxLambdaOne
        index := by
  fin_cases index <;>
    norm_num [
      scalarLapseCompactBumpFiniteBoxLambdaOne
    ]

theorem
    scalarLapseCompactBumpFiniteBoxLambdaOne_above_free
    (index : Fin 5) :
    scalarLapseCompactBumpFiniteBoxFreeLambdaOne
        index <
      scalarLapseCompactBumpFiniteBoxLambdaOne
        index := by
  fin_cases index <;>
    norm_num [
      scalarLapseCompactBumpFiniteBoxLambdaOne,
      scalarLapseCompactBumpFiniteBoxFreeLambdaOne
    ]

theorem
    scalarLapseCompactBumpFiniteBoxLambdaOne_strictly_decreases :
    scalarLapseCompactBumpFiniteBoxLambdaOne 4 <
        scalarLapseCompactBumpFiniteBoxLambdaOne 3 ∧
      scalarLapseCompactBumpFiniteBoxLambdaOne 3 <
        scalarLapseCompactBumpFiniteBoxLambdaOne 2 ∧
      scalarLapseCompactBumpFiniteBoxLambdaOne 2 <
        scalarLapseCompactBumpFiniteBoxLambdaOne 1 ∧
      scalarLapseCompactBumpFiniteBoxLambdaOne 1 <
        scalarLapseCompactBumpFiniteBoxLambdaOne 0 := by
  norm_num [
    scalarLapseCompactBumpFiniteBoxLambdaOne
  ]

theorem
    scalarLapseCompactBumpFiniteBox_noRecordedNegativeLambdaOne :
    ¬ ∃ index : Fin 5,
        scalarLapseCompactBumpFiniteBoxLambdaOne
            index <
          0 := by
  rintro ⟨index, hNegative⟩
  exact
    (not_lt_of_ge
      (le_of_lt
        (scalarLapseCompactBumpFiniteBoxLambdaOne_positive
          index)))
      hNegative

def scalarLapseCompactBumpFiniteBoxSpectrumStatus : String :=
  "FIVE_FINITE_BOX_FLOATING_POINT_ROWS_RECORDED_AS_EXACT_RATIONAL_DATA_RECORDED_LOWEST_VALUES_POSITIVE_AND_STRICTLY_DECREASING"

def scalarLapseCompactBumpFiniteBoxSpectrumBoundary : String :=
  "NO_INTERVAL_ARITHMETIC_NO_FINITE_ELEMENT_RESIDUAL_BOUND_NO_EXTERIOR_TRUNCATION_BOUND_NO_INFINITE_DOMAIN_SPECTRAL_CERTIFICATE"


end

end Chronos.Frontier
