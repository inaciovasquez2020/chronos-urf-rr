import Chronos.Frontier.DFMMKCNewtonianGaugeSharpGateNorm

namespace Chronos.Frontier

/-- Instantaneous scalar sources entering the nonzero-mode Newtonian-gauge
Einstein constraints. -/
structure DFMMKCNewtonianGaugeScalarConstraintSources where
  deltaRhoTotal : ℝ
  momentumSource : ℝ
  enthalpySigmaTotal : ℝ

/-- Conformal Hubble parameter `Hc = a H`. -/
noncomputable def dfmMkcNewtonianGaugeConformalHubble
    (x : RestrictedDFMMKCEnergyState) : ℝ :=
  x.scaleFactor * x.hubble

/-- Constraint prefactor `4 pi G a^2`. -/
noncomputable def dfmMkcNewtonianGaugeConstraintPrefactor
    (x : RestrictedDFMMKCEnergyState) : ℝ :=
  4 * Real.pi * x.newtonG * x.scaleFactor ^ 2

/-- Nonzero-mode solution for `P = Phi' + Hc Psi`. -/
noncomputable def dfmMkcNewtonianGaugeNonzeroModeMomentumCombination
    (x : RestrictedDFMMKCEnergyState)
    (waveNumberSquared : ℝ)
    (sources : DFMMKCNewtonianGaugeScalarConstraintSources) : ℝ :=
  dfmMkcNewtonianGaugeConstraintPrefactor x * sources.momentumSource /
    waveNumberSquared

/-- Nonzero-mode solution for the spatial Newtonian potential `Phi`. -/
noncomputable def dfmMkcNewtonianGaugeNonzeroModeSpatialPotential
    (x : RestrictedDFMMKCEnergyState)
    (waveNumberSquared : ℝ)
    (sources : DFMMKCNewtonianGaugeScalarConstraintSources) : ℝ :=
  (-dfmMkcNewtonianGaugeConstraintPrefactor x * sources.deltaRhoTotal
      - 3 * dfmMkcNewtonianGaugeConformalHubble x *
        dfmMkcNewtonianGaugeNonzeroModeMomentumCombination
          x waveNumberSquared sources) /
    waveNumberSquared

/-- Nonzero-mode solution for the lapse Newtonian potential `Psi`. -/
noncomputable def dfmMkcNewtonianGaugeNonzeroModeLapsePotential
    (x : RestrictedDFMMKCEnergyState)
    (waveNumberSquared : ℝ)
    (sources : DFMMKCNewtonianGaugeScalarConstraintSources) : ℝ :=
  dfmMkcNewtonianGaugeNonzeroModeSpatialPotential
      x waveNumberSquared sources
    - 3 * dfmMkcNewtonianGaugeConstraintPrefactor x *
        sources.enthalpySigmaTotal /
      waveNumberSquared

/-- The conformal-time derivative `Phi'` reconstructed from
`P = Phi' + Hc Psi`. -/
noncomputable def dfmMkcNewtonianGaugeNonzeroModeSpatialPotentialPrime
    (x : RestrictedDFMMKCEnergyState)
    (waveNumberSquared : ℝ)
    (sources : DFMMKCNewtonianGaugeScalarConstraintSources) : ℝ :=
  dfmMkcNewtonianGaugeNonzeroModeMomentumCombination
      x waveNumberSquared sources
    - dfmMkcNewtonianGaugeConformalHubble x *
        dfmMkcNewtonianGaugeNonzeroModeLapsePotential
          x waveNumberSquared sources

/-- The reconstructed variables satisfy the momentum constraint exactly. -/
theorem dfmMkcNewtonianGauge_nonzeroMode_momentumConstraint
    (x : RestrictedDFMMKCEnergyState)
    (waveNumberSquared : ℝ)
    (sources : DFMMKCNewtonianGaugeScalarConstraintSources)
    (hk : waveNumberSquared ≠ 0) :
    waveNumberSquared *
        (dfmMkcNewtonianGaugeNonzeroModeSpatialPotentialPrime
            x waveNumberSquared sources
          + dfmMkcNewtonianGaugeConformalHubble x *
              dfmMkcNewtonianGaugeNonzeroModeLapsePotential
                x waveNumberSquared sources) =
      dfmMkcNewtonianGaugeConstraintPrefactor x * sources.momentumSource := by
  unfold dfmMkcNewtonianGaugeNonzeroModeSpatialPotentialPrime
    dfmMkcNewtonianGaugeNonzeroModeMomentumCombination
  field_simp [hk]
  <;> ring

/-- The reconstructed variables satisfy the Hamiltonian constraint exactly. -/
theorem dfmMkcNewtonianGauge_nonzeroMode_hamiltonianConstraint
    (x : RestrictedDFMMKCEnergyState)
    (waveNumberSquared : ℝ)
    (sources : DFMMKCNewtonianGaugeScalarConstraintSources)
    (hk : waveNumberSquared ≠ 0) :
    waveNumberSquared *
        dfmMkcNewtonianGaugeNonzeroModeSpatialPotential
          x waveNumberSquared sources
      + 3 * dfmMkcNewtonianGaugeConformalHubble x *
          (dfmMkcNewtonianGaugeNonzeroModeSpatialPotentialPrime
              x waveNumberSquared sources
            + dfmMkcNewtonianGaugeConformalHubble x *
                dfmMkcNewtonianGaugeNonzeroModeLapsePotential
                  x waveNumberSquared sources) =
      -dfmMkcNewtonianGaugeConstraintPrefactor x * sources.deltaRhoTotal := by
  unfold dfmMkcNewtonianGaugeNonzeroModeSpatialPotentialPrime
    dfmMkcNewtonianGaugeNonzeroModeSpatialPotential
    dfmMkcNewtonianGaugeNonzeroModeMomentumCombination
  field_simp [hk]
  <;> ring

/-- The reconstructed variables satisfy the scalar anisotropy constraint exactly. -/
theorem dfmMkcNewtonianGauge_nonzeroMode_anisotropyConstraint
    (x : RestrictedDFMMKCEnergyState)
    (waveNumberSquared : ℝ)
    (sources : DFMMKCNewtonianGaugeScalarConstraintSources)
    (hk : waveNumberSquared ≠ 0) :
    waveNumberSquared *
        (dfmMkcNewtonianGaugeNonzeroModeSpatialPotential
            x waveNumberSquared sources
          - dfmMkcNewtonianGaugeNonzeroModeLapsePotential
              x waveNumberSquared sources) =
      3 * dfmMkcNewtonianGaugeConstraintPrefactor x *
        sources.enthalpySigmaTotal := by
  unfold dfmMkcNewtonianGaugeNonzeroModeLapsePotential
  field_simp [hk]
  <;> ring

/--
For a nonzero mode, any triple satisfying the three scalar constraints agrees
with the explicit source-level solution.  In particular the lapse potential is
not a free variable on this constrained sector.
-/
theorem dfmMkcNewtonianGauge_nonzeroMode_constraintSolution_unique
    (x : RestrictedDFMMKCEnergyState)
    (waveNumberSquared : ℝ)
    (sources : DFMMKCNewtonianGaugeScalarConstraintSources)
    (Phi Psi momentumCombination : ℝ)
    (hk : waveNumberSquared ≠ 0)
    (hHamiltonian :
      waveNumberSquared * Phi
          + 3 * dfmMkcNewtonianGaugeConformalHubble x * momentumCombination =
        -dfmMkcNewtonianGaugeConstraintPrefactor x * sources.deltaRhoTotal)
    (hMomentum :
      waveNumberSquared * momentumCombination =
        dfmMkcNewtonianGaugeConstraintPrefactor x * sources.momentumSource)
    (hAnisotropy :
      waveNumberSquared * (Phi - Psi) =
        3 * dfmMkcNewtonianGaugeConstraintPrefactor x *
          sources.enthalpySigmaTotal) :
    Phi = dfmMkcNewtonianGaugeNonzeroModeSpatialPotential
        x waveNumberSquared sources ∧
      Psi = dfmMkcNewtonianGaugeNonzeroModeLapsePotential
        x waveNumberSquared sources ∧
      momentumCombination =
        dfmMkcNewtonianGaugeNonzeroModeMomentumCombination
          x waveNumberSquared sources := by
  have hMomentum' :
      momentumCombination =
        dfmMkcNewtonianGaugeNonzeroModeMomentumCombination
          x waveNumberSquared sources := by
    unfold dfmMkcNewtonianGaugeNonzeroModeMomentumCombination
    apply (eq_div_iff hk).2
    nlinarith [hMomentum]
  have hPhi :
      Phi = dfmMkcNewtonianGaugeNonzeroModeSpatialPotential
        x waveNumberSquared sources := by
    unfold dfmMkcNewtonianGaugeNonzeroModeSpatialPotential
    apply (eq_div_iff hk).2
    rw [hMomentum'] at hHamiltonian
    nlinarith [hHamiltonian]
  have hDifference :
      Phi - Psi =
        3 * dfmMkcNewtonianGaugeConstraintPrefactor x *
          sources.enthalpySigmaTotal / waveNumberSquared := by
    apply (eq_div_iff hk).2
    nlinarith [hAnisotropy]
  have hPsi :
      Psi = dfmMkcNewtonianGaugeNonzeroModeLapsePotential
        x waveNumberSquared sources := by
    unfold dfmMkcNewtonianGaugeNonzeroModeLapsePotential
    rw [← hPhi]
    linarith
  exact ⟨hPhi, hPsi, hMomentum'⟩

/-- Convert the solved conformal momentum combination to the cosmic-time
combination used by the Chronos gate. -/
noncomputable def dfmMkcNewtonianGaugeNonzeroModeCosmicMomentumCombination
    (x : RestrictedDFMMKCEnergyState)
    (waveNumberSquared : ℝ)
    (sources : DFMMKCNewtonianGaugeScalarConstraintSources) : ℝ :=
  dfmMkcNewtonianGaugeNonzeroModeMomentumCombination
      x waveNumberSquared sources /
    x.scaleFactor

/-- Closed source formula for the cosmic-time gate combination. -/
theorem dfmMkcNewtonianGauge_nonzeroMode_cosmicMomentumCombination_eq
    (x : RestrictedDFMMKCEnergyState)
    (waveNumberSquared : ℝ)
    (sources : DFMMKCNewtonianGaugeScalarConstraintSources)
    (hk : waveNumberSquared ≠ 0) :
    dfmMkcNewtonianGaugeNonzeroModeCosmicMomentumCombination
        x waveNumberSquared sources =
      4 * Real.pi * x.newtonG * x.scaleFactor *
        sources.momentumSource / waveNumberSquared := by
  unfold dfmMkcNewtonianGaugeNonzeroModeCosmicMomentumCombination
    dfmMkcNewtonianGaugeNonzeroModeMomentumCombination
    dfmMkcNewtonianGaugeConstraintPrefactor
  field_simp [hk, ne_of_gt x.scaleFactor_pos]
  <;> ring

end Chronos.Frontier
