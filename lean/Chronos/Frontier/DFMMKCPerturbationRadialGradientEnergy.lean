import Chronos.Frontier.DFMMKCChargeReducedRadialMomentumSourceBinding

namespace Chronos.Frontier

/--
Quadratic radial gradient energy for the scalar/phase perturbation variables
appearing in the charge-reduced DFM-MKC momentum source.

This is the action-derived positive quadratic form before any comparison with
the curvature-energy carrier E_grav. It is deliberately local and makes no
Einstein-matter evolution or energy-control claim.
-/
noncomputable def dfmMkcPerturbationRadialGradientEnergy
    (x : RestrictedDFMMKCEnergyState)
    (deltaScalarFieldPrime deltaPhaseFieldPrime : ℝ) : ℝ :=
  x.alpha / (2 * x.scaleFactor ^ 2) * deltaScalarFieldPrime ^ 2
    + x.beta * x.phi ^ 2 / (2 * x.scaleFactor ^ 2) *
        deltaPhaseFieldPrime ^ 2

/-- The action-derived radial perturbation gradient energy is nonnegative. -/
theorem dfmMkcPerturbationRadialGradientEnergy_nonneg
    (x : RestrictedDFMMKCEnergyState)
    (deltaScalarFieldPrime deltaPhaseFieldPrime : ℝ) :
    0 ≤ dfmMkcPerturbationRadialGradientEnergy
      x deltaScalarFieldPrime deltaPhaseFieldPrime := by
  unfold dfmMkcPerturbationRadialGradientEnergy
  positivity

/--
Weighted quadratic control of the exact charge-reduced momentum-source
combination by the radial gradient energy.  The constant is explicit and
depends only on the background coefficients.
-/
theorem dfmMkcChargeReducedMomentumSource_abs_le_gradientEnergy
    (x : RestrictedDFMMKCEnergyState)
    (deltaScalarFieldPrime deltaPhaseFieldPrime : ℝ) :
    |x.alpha * x.phiDot / x.scaleFactor * deltaScalarFieldPrime
        + x.qTheta / x.scaleFactor ^ 4 * deltaPhaseFieldPrime| ≤
      (4 * x.alpha * x.phiDot ^ 2
        + 4 * x.qTheta ^ 2 /
            (x.beta * x.phi ^ 2 * x.scaleFactor ^ 6)) *
        dfmMkcPerturbationRadialGradientEnergy
          x deltaScalarFieldPrime deltaPhaseFieldPrime := by
  let E := dfmMkcPerturbationRadialGradientEnergy
    x deltaScalarFieldPrime deltaPhaseFieldPrime
  have hE : 0 ≤ E := by
    dsimp [E]
    exact dfmMkcPerturbationRadialGradientEnergy_nonneg
      x deltaScalarFieldPrime deltaPhaseFieldPrime
  have hsq :
      (x.alpha * x.phiDot / x.scaleFactor * deltaScalarFieldPrime
        + x.qTheta / x.scaleFactor ^ 4 * deltaPhaseFieldPrime) ^ 2 ≤
      ((4 * x.alpha * x.phiDot ^ 2
        + 4 * x.qTheta ^ 2 /
            (x.beta * x.phi ^ 2 * x.scaleFactor ^ 6)) * E) ^ 2 := by
    dsimp [E, dfmMkcPerturbationRadialGradientEnergy]
    field_simp [ne_of_gt x.alpha_pos, ne_of_gt x.beta_pos,
      ne_of_gt x.scaleFactor_pos, ne_of_ne x.phi_ne_zero]
    nlinarith [sq_nonneg
      (x.beta * x.phi ^ 2 * x.scaleFactor ^ 3 * deltaScalarFieldPrime *
          x.alpha * x.phiDot
        - x.alpha * x.scaleFactor ^ 3 * deltaPhaseFieldPrime *
          x.qTheta * x.phi)]
  have hR :
      0 ≤
        (4 * x.alpha * x.phiDot ^ 2
          + 4 * x.qTheta ^ 2 /
              (x.beta * x.phi ^ 2 * x.scaleFactor ^ 6)) * E := by
    positivity
  exact abs_le_of_sq_le_sq hsq hR


/--
The exact radial derivative entering the charge-reduced momentum source is
controlled by the action-derived radial gradient energy once the scalar and
phase profiles realize the carrier's radial perturbation derivatives.
-/
theorem dfmMkcChargeReducedMomentumPotentialRadialDerivative_abs_le_gradientEnergy
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (Q : DFMMKCChargeReducedRadialMomentumSourceBinding S x P)
    (hscalar :
      HasDerivAt Q.deltaScalarProfile P.deltaScalarFieldPrime S.areaRadius)
    (hphase :
      HasDerivAt Q.deltaPhaseProfile P.deltaPhaseFieldPrime S.areaRadius) :
    |Q.momentumPotentialRadialDerivative| ≤
      (4 * x.alpha * x.phiDot ^ 2
        + 4 * x.qTheta ^ 2 /
            (x.beta * x.phi ^ 2 * x.scaleFactor ^ 6)) *
        dfmMkcPerturbationRadialGradientEnergy
          x P.deltaScalarFieldPrime P.deltaPhaseFieldPrime := by
  rw [dfmMkcChargeReducedMomentumPotentialRadialDerivative_eq_gradientSource
    S x P Q hscalar hphase]
  exact dfmMkcChargeReducedMomentumSource_abs_le_gradientEnergy
    x P.deltaScalarFieldPrime P.deltaPhaseFieldPrime


/--
Conditional surface source control.  The only additional input is an upper
bound on the positive projection normalization; no curvature-energy estimate
is used.
-/
theorem dfmMkcChargeReducedRadialMomentumSource_surface_abs_le_gradientEnergy
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (Q : DFMMKCChargeReducedRadialMomentumSourceBinding S x P)
    (B : DFMMKCChargeReducedRadialMomentumSourceIntervalBinding S x P Q)
    (hscalar :
      HasDerivAt Q.deltaScalarProfile P.deltaScalarFieldPrime S.areaRadius)
    (hphase :
      HasDerivAt Q.deltaPhaseProfile P.deltaPhaseFieldPrime S.areaRadius)
    (normalizationBound : ℝ)
    (hnorm : Q.projectionNormalization ≤ normalizationBound) :
    |B.radialSource S.areaRadius| ≤
      normalizationBound *
        (4 * x.alpha * x.phiDot ^ 2
          + 4 * x.qTheta ^ 2 /
              (x.beta * x.phi ^ 2 * x.scaleFactor ^ 6)) *
        dfmMkcPerturbationRadialGradientEnergy
          x P.deltaScalarFieldPrime P.deltaPhaseFieldPrime := by
  rw [dfmMkcChargeReducedRadialMomentumSourceIntervalBinding_abs_source_eq
    S x P Q B S.areaRadius
    ⟨B.anchor_le_surface, le_rfl⟩]
  have hderiv :=
    dfmMkcChargeReducedMomentumPotentialRadialDerivative_abs_le_gradientEnergy
      S x P Q hscalar hphase
  have henergy : 0 ≤
      (4 * x.alpha * x.phiDot ^ 2
        + 4 * x.qTheta ^ 2 /
            (x.beta * x.phi ^ 2 * x.scaleFactor ^ 6)) *
        dfmMkcPerturbationRadialGradientEnergy
          x P.deltaScalarFieldPrime P.deltaPhaseFieldPrime := by
    positivity
  exact mul_le_mul hnorm hderiv henergy
      (le_trans (le_of_lt Q.projectionNormalization_pos) hnorm)

/--
Smallest analytic target needed to connect the action-derived DFM-MKC radial
gradient energy to the selected Einstein-matter curvature-energy control.
This is a proof obligation only; no Einstein-matter coercivity estimate is
asserted here.
-/
def DFMMKCGradientToGravityCoerciveEstimate
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x)
    (C : ℝ) : Prop :=
  dfmMkcPerturbationRadialGradientEnergy
      x P.deltaScalarFieldPrime P.deltaPhaseFieldPrime ≤
    C * E_grav data + Flux_boundary data S

/--
Named status for the radial-gradient-to-gravity bridge.  The proposition above
is the exact inequality required before the source bound can be promoted from
a local gradient estimate to a curvature-energy estimate.
-/
def dfmMkcGradientToGravityProofObligation : Prop :=
  ∀ {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (x : RestrictedDFMMKCEnergyState)
    (P : DFMMKCPerturbedQuasiLocalSurfaceCarrier S x),
    ∃ C : ℝ, DFMMKCGradientToGravityCoerciveEstimate S x P C

end Chronos.Frontier
