import Chronos.Frontier.PrizcarbonOddParityVacuumCPMLinearizedScalarCurvature

namespace Chronos.Frontier

noncomputable section

/--
The explicit Schwarzschild Ricci contraction derived from the repository's
coordinate connection and Riemann tensor vanishes componentwise.
-/
theorem prizcarbonSchwarzschildRicciContraction_ofFrame_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (left right : ReggeWheelerSpacetimeCoordinate) :
    prizcarbonSchwarzschildRicciContraction
        frame
        (reggeWheelerSchwarzschildConnectionFirstJetOfFrame frame)
        left
        right =
      0 := by
  have hRadiusPos :
      0 < frame.background.radius :=
    reggeWheelerSchwarzschildBackground_radius_pos
      frame.background

  have hRadius :
      frame.background.radius ≠ 0 :=
    ne_of_gt hRadiusPos

  have hGapPos :
      0 <
        frame.background.radius -
          2 * frame.background.mass :=
    sub_pos.mpr frame.background.exterior

  have hGap :
      frame.background.radius -
          2 * frame.background.mass ≠
        0 :=
    ne_of_gt hGapPos

  have hGapLeft :
      -(frame.background.mass * 2) +
          frame.background.radius ≠
        0 := by
    nlinarith [frame.background.exterior]

  have hGapRight :
      frame.background.radius -
          frame.background.mass * 2 ≠
        0 := by
    nlinarith [frame.background.exterior]

  have hSin :
      Real.sin frame.polarAngle ≠ 0 :=
    frame.sinPolarAngle_ne_zero

  have hFactor :
      reggeWheelerSchwarzschildExteriorFactor
          frame.background ≠
        0 :=
    reggeWheelerSchwarzschildExteriorFactor_ne_zero
      frame.background

  have hQuadraticA :
      -(
          frame.background.mass *
            frame.background.radius *
            frame.background.radius⁻¹ ^ 2 *
            4
        ) +
          frame.background.mass ^ 2 *
            frame.background.radius⁻¹ ^ 2 *
            4 +
          frame.background.radius ^ 2 *
            frame.background.radius⁻¹ ^ 2 =
        (
          frame.background.radius -
            2 * frame.background.mass
        ) ^ 2 *
          frame.background.radius⁻¹ ^ 2 := by
    ring

  have hQuadraticB :
      -(
          frame.background.radius *
            frame.background.mass *
            frame.background.radius⁻¹ ^ 2 *
            4
        ) +
          frame.background.radius ^ 2 *
            frame.background.radius⁻¹ ^ 2 +
          frame.background.mass ^ 2 *
            frame.background.radius⁻¹ ^ 2 *
            4 =
        (
          frame.background.radius -
            2 * frame.background.mass
        ) ^ 2 *
          frame.background.radius⁻¹ ^ 2 := by
    ring

  have hQuadraticA_ne :
      -(
          frame.background.mass *
            frame.background.radius *
            frame.background.radius⁻¹ ^ 2 *
            4
        ) +
          frame.background.mass ^ 2 *
            frame.background.radius⁻¹ ^ 2 *
            4 +
          frame.background.radius ^ 2 *
            frame.background.radius⁻¹ ^ 2 ≠
        0 := by
    rw [hQuadraticA]
    exact
      mul_ne_zero
        (pow_ne_zero 2 hGap)
        (pow_ne_zero 2 (inv_ne_zero hRadius))

  have hQuadraticB_ne :
      -(
          frame.background.radius *
            frame.background.mass *
            frame.background.radius⁻¹ ^ 2 *
            4
        ) +
          frame.background.radius ^ 2 *
            frame.background.radius⁻¹ ^ 2 +
          frame.background.mass ^ 2 *
            frame.background.radius⁻¹ ^ 2 *
            4 ≠
        0 := by
    rw [hQuadraticB]
    exact
      mul_ne_zero
        (pow_ne_zero 2 hGap)
        (pow_ne_zero 2 (inv_ne_zero hRadius))

  have hTrig :
      Real.sin frame.polarAngle ^ 2 +
          Real.cos frame.polarAngle ^ 2 =
        1 :=
    Real.sin_sq_add_cos_sq frame.polarAngle

  cases left <;>
    cases right <;>
      simp [
        prizcarbonSchwarzschildRicciContraction,
        reggeWheelerSpacetimeCoordinateContraction,
        reggeWheelerSchwarzschildConnectionFirstJetOfFrame,
        reggeWheelerSchwarzschildRiemann,
        reggeWheelerSchwarzschildRiemannSummand,
        reggeWheelerSchwarzschildChristoffel,
        reggeWheelerSchwarzschildChristoffelPartial,
        reggeWheelerSchwarzschildConnectionKernel,
        reggeWheelerSchwarzschildConnectionKernelPartial,
        reggeWheelerSchwarzschildInverseMetricDiagonal,
        reggeWheelerSchwarzschildInverseMetricComponentPartial,
        reggeWheelerSchwarzschildMetricComponent,
        reggeWheelerSchwarzschildMetricPartial,
        reggeWheelerSchwarzschildMetricSecondPartial,
        reggeWheelerSchwarzschildExteriorFactor,
        reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative,
        reggeWheelerSchwarzschildExteriorFactorRadialDerivative,
        reggeWheelerSchwarzschildExteriorFactorSecondRadialDerivative,
        hRadius,
        hGap,
        hGapLeft,
        hGapRight,
        hSin,
        hFactor,
        hQuadraticA,
        hQuadraticB,
        hQuadraticA_ne,
        hQuadraticB_ne
      ] <;>
      field_simp [
        hRadius,
        hGap,
        hGapLeft,
        hGapRight,
        hSin,
        hFactor,
        hQuadraticA_ne,
        hQuadraticB_ne
      ] <;>
      ring_nf at * <;>
      nlinarith [hTrig]

/--
The inverse-metric/background-Ricci contribution in the concrete vacuum CPM
scalar-curvature variation vanishes.
-/
theorem
    prizcarbonOddParityVacuumCPMInverseMetricBackgroundRicciContribution_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMInverseMetricBackgroundRicciContribution
        frame
        cpmJet
        harmonicJet =
      0 := by
  unfold
    prizcarbonOddParityVacuumCPMInverseMetricBackgroundRicciContribution
  unfold
    prizcarbonOddParityInverseMetricBackgroundRicciContribution
  simp [
    prizcarbonSchwarzschildRicciContraction_ofFrame_eq_zero,
    reggeWheelerSpacetimeCoordinateContraction
  ]

/--
After removing the background-Ricci product-rule term, the specialized CPM
scalar-curvature variation is exactly its linearized-Ricci contraction.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedScalarCurvature_eq_linearizedRicciContribution
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMLinearizedScalarCurvature
        frame
        cpmJet
        harmonicJet =
      prizcarbonOddParityVacuumCPMBackgroundMetricLinearizedRicciContribution
        frame
        cpmJet
        harmonicJet := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedScalarCurvature_eq_contributions,
    prizcarbonOddParityVacuumCPMInverseMetricBackgroundRicciContribution_eq_zero,
    zero_add
  ]

def prizcarbonSchwarzschildRicciContractionZeroBoundary : String :=
  "SCHWARZSCHILD_RICCI_CONTRACTION_ZERO_PROVED_CPM_LINEARIZED_RICCI_CONTRACTION_REMAINS"

end

end Chronos.Frontier
