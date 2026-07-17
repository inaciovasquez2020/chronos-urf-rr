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

end

end Chronos.Frontier
