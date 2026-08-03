import Chronos.Frontier.PrizcarbonOddParityVacuumCPMLinearizedRicciTimeTimeExpansion

namespace Chronos.Frontier

noncomputable section

/--
A mixed-index linearized Riemann component vanishes whenever its two curvature
indices coincide.

Only antisymmetry in the final curvature-index pair is used.
-/
theorem
    prizcarbonOddParityLinearizedRiemann_curvatureDiagonal_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (linearizedConnectionJet :
      ReggeWheelerOddParityLinearizedConnectionFirstJet)
    (contraction transported curvature :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLinearizedRiemann
        frame
        linearizedConnectionJet
        contraction
        transported
        curvature
        curvature =
      0 := by
  have hAntisymmetric :=
    reggeWheelerOddParityLinearizedRiemann_curvatureIndices_antisymmetric
      frame
      linearizedConnectionJet
      contraction
      transported
      curvature
      curvature

  linarith

/--
The repeated-time mixed-index component appearing in the coordinate
vacuum-CPM time-time Ricci contraction vanishes.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRiemann_time_time_time_time_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedRiemann
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
            frame
            cpmJet
            harmonicJet
        )
        .time
        .time
        .time
        .time =
      0 := by
  exact
    prizcarbonOddParityLinearizedRiemann_curvatureDiagonal_zero
      frame
      (
        reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
          frame
          cpmJet
          harmonicJet
      )
      .time
      .time
      .time

/--
The fully lowered vacuum-CPM `tttt` linearized Riemann component also
vanishes. This is a direct specialization of the repository's existing
generic curvature-diagonal zero theorem.
-/
theorem
    prizcarbonOddParityVacuumCPMLoweredLinearizedRiemann_time_time_time_time_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLoweredLinearizedRiemann
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
            cpmJet
            harmonicJet
        )
        (
          reggeWheelerSchwarzschildConnectionFirstJetOfFrame
            frame
        )
        (
          reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
            frame
            cpmJet
            harmonicJet
        )
        .time
        .time
        .time
        .time =
      0 := by
  exact
    reggeWheelerOddParityLoweredLinearizedRiemann_curvatureDiagonal_zero
      frame
      (
        reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
          cpmJet
          harmonicJet
      )
      (
        reggeWheelerSchwarzschildConnectionFirstJetOfFrame
          frame
      )
      (
        reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
          frame
          cpmJet
          harmonicJet
      )
      .time
      .time
      .time

/--
After eliminating the repeated-time term, the coordinate vacuum-CPM
time-time linearized Ricci component consists of exactly three contracted
linearized-Riemann components.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime_eq_threeContractedRiemannCoordinates
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime
        frame
        cpmJet
        harmonicJet =
      reggeWheelerOddParityLinearizedRiemann
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
              frame
              cpmJet
              harmonicJet
          )
          .radial
          .time
          .radial
          .time +
        reggeWheelerOddParityLinearizedRiemann
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
              frame
              cpmJet
              harmonicJet
          )
          .theta
          .time
          .theta
          .time +
        reggeWheelerOddParityLinearizedRiemann
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
              frame
              cpmJet
              harmonicJet
          )
          .phi
          .time
          .phi
          .time := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime_eq_contractedRiemannCoordinates,
    prizcarbonOddParityVacuumCPMLinearizedRiemann_time_time_time_time_eq_zero,
    zero_add
  ]

/--
The time-weighted coordinate contribution inherits the corrected three-term
expansion.
-/
theorem
    prizcarbonOddParityVacuumCPMTimeWeightedLinearizedRicciContribution_eq_threeContractedRiemannCoordinates
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    prizcarbonOddParityVacuumCPMTimeWeightedLinearizedRicciContribution
        frame
        cpmJet
        harmonicJet =
      -(1 /
          reggeWheelerSchwarzschildExteriorFactor
            frame.background) *
        (
          reggeWheelerOddParityLinearizedRiemann
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                  frame
                  cpmJet
                  harmonicJet
              )
              .radial
              .time
              .radial
              .time +
            reggeWheelerOddParityLinearizedRiemann
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                  frame
                  cpmJet
                  harmonicJet
              )
              .theta
              .time
              .theta
              .time +
            reggeWheelerOddParityLinearizedRiemann
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                  frame
                  cpmJet
                  harmonicJet
              )
              .phi
              .time
              .phi
              .time
        ) := by
  unfold
    prizcarbonOddParityVacuumCPMTimeWeightedLinearizedRicciContribution

  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime_eq_threeContractedRiemannCoordinates
  ]

/--
For every static spatial coordinate, the first-variation term produced by
lowering the first Riemann index with the odd-parity CPM metric vanishes.

This isolates exactly

`Σ_ρ h_{aρ} R̄^ρ_{tat} = 0`.

The proof is componentwise: the Schwarzschild static tidal background has
diagonal spatial support, while the odd-parity Regge–Wheeler-gauge metric has
no spatial diagonal or angular-angular components.
-/
theorem
    prizcarbonOddParityVacuumCPMStaticTidalMetricLoweringCorrection_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (axis : ReggeWheelerDetectorSpatialAxis) :
    reggeWheelerSpacetimeCoordinateContraction
        (fun contraction =>
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
              cpmJet
              harmonicJet
          ).metricValue
              (reggeWheelerDetectorSpatialCoordinate axis)
              contraction *
            reggeWheelerSchwarzschildRiemann
              frame
              (
                reggeWheelerSchwarzschildConnectionFirstJetOfFrame
                  frame
              )
              contraction
              .time
              (reggeWheelerDetectorSpatialCoordinate axis)
              .time) =
      0 := by
  rw [
    reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet_eq
  ]

  cases axis <;>
    simp [
      reggeWheelerSpacetimeCoordinateContraction,
      reggeWheelerDetectorSpatialCoordinate,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerOddParitySpacetimeMetricPerturbation,
      reggeWheelerOddParityVacuumCPMMetricComponents_tensorAngular_zero,
      reggeWheelerSchwarzschildConnectionFirstJetOfFrame,
      reggeWheelerSchwarzschildRiemann,
      reggeWheelerSchwarzschildRiemannSummand,
      reggeWheelerSchwarzschildChristoffelPartial,
      reggeWheelerSchwarzschildChristoffel,
      reggeWheelerSchwarzschildConnectionKernel,
      reggeWheelerSchwarzschildConnectionKernelPartial,
      reggeWheelerSchwarzschildInverseMetricDiagonal,
      reggeWheelerSchwarzschildInverseMetricComponentPartial,
      reggeWheelerSchwarzschildMetricPartial,
      reggeWheelerSchwarzschildMetricSecondPartial
    ]

/--
The trace of the three static-frame tidal diagonal entries equals the
coordinate vacuum-CPM `tt` linearized Ricci component multiplied by the square
of the static timelike-leg scale.

Equivalently,

`𝓔_rr + 𝓔_θθ + 𝓔_φφ = lapse⁻² δR_tt`.

No tidal-matrix symmetry is required. The only additional ingredient beyond
the coordinate Ricci reduction is the proved vanishing of the
metric-lowering/background-Riemann correction.
-/
theorem
    prizcarbonOddParityVacuumCPMStaticTidalTrace_eq_inverseLapseSquared_mul_linearizedRicciTimeTime
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityVacuumCPMStaticTidalCurvature
          frame
          cpmJet
          harmonicJet
          .radial
          .radial +
        reggeWheelerOddParityVacuumCPMStaticTidalCurvature
          frame
          cpmJet
          harmonicJet
          .theta
          .theta +
        reggeWheelerOddParityVacuumCPMStaticTidalCurvature
          frame
          cpmJet
          harmonicJet
          .phi
          .phi =
      (1 / frame.lapseSqrt ^ 2) *
        prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime
          frame
          cpmJet
          harmonicJet := by
  have hLapse : frame.lapseSqrt ≠ 0 :=
    ne_of_gt frame.lapseSqrt_pos

  have hRadius : frame.background.radius ≠ 0 :=
    ne_of_gt
      (
        reggeWheelerSchwarzschildBackground_radius_pos
          frame.background
      )

  have hSin : Real.sin frame.polarAngle ≠ 0 :=
    frame.sinPolarAngle_ne_zero

  have hRadiusSin :
      frame.background.radius *
          Real.sin frame.polarAngle ≠
        0 :=
    mul_ne_zero hRadius hSin

  have hLoweredDiagonal :
      ∀ axis : ReggeWheelerDetectorSpatialAxis,
        reggeWheelerOddParityLoweredLinearizedRiemann
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
                  cpmJet
                  harmonicJet
              )
              (
                reggeWheelerSchwarzschildConnectionFirstJetOfFrame
                  frame
              )
              (
                reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                  frame
                  cpmJet
                  harmonicJet
              )
              (reggeWheelerDetectorSpatialCoordinate axis)
              .time
              (reggeWheelerDetectorSpatialCoordinate axis)
              .time =
          reggeWheelerSchwarzschildMetricComponent
              frame
              (reggeWheelerDetectorSpatialCoordinate axis)
              (reggeWheelerDetectorSpatialCoordinate axis) *
            reggeWheelerOddParityLinearizedRiemann
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                  frame
                  cpmJet
                  harmonicJet
              )
              (reggeWheelerDetectorSpatialCoordinate axis)
              .time
              (reggeWheelerDetectorSpatialCoordinate axis)
              .time := by
    intro axis

    unfold reggeWheelerOddParityLoweredLinearizedRiemann
    unfold reggeWheelerOddParityLoweredLinearizedRiemannSummand

    have hSplit :
        reggeWheelerSpacetimeCoordinateContraction
            (fun contraction =>
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
                  cpmJet
                  harmonicJet
              ).metricValue
                    (reggeWheelerDetectorSpatialCoordinate axis)
                    contraction *
                  reggeWheelerSchwarzschildRiemann
                    frame
                    (
                      reggeWheelerSchwarzschildConnectionFirstJetOfFrame
                        frame
                    )
                    contraction
                    .time
                    (reggeWheelerDetectorSpatialCoordinate axis)
                    .time +
                reggeWheelerSchwarzschildMetricComponent
                    frame
                    (reggeWheelerDetectorSpatialCoordinate axis)
                    contraction *
                  reggeWheelerOddParityLinearizedRiemann
                    frame
                    (
                      reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                        frame
                        cpmJet
                        harmonicJet
                    )
                    contraction
                    .time
                    (reggeWheelerDetectorSpatialCoordinate axis)
                    .time) =
          reggeWheelerSpacetimeCoordinateContraction
              (fun contraction =>
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricFirstJet
                    cpmJet
                    harmonicJet
                ).metricValue
                      (reggeWheelerDetectorSpatialCoordinate axis)
                      contraction *
                    reggeWheelerSchwarzschildRiemann
                      frame
                      (
                        reggeWheelerSchwarzschildConnectionFirstJetOfFrame
                          frame
                      )
                      contraction
                      .time
                      (reggeWheelerDetectorSpatialCoordinate axis)
                      .time) +
            reggeWheelerSpacetimeCoordinateContraction
              (fun contraction =>
                reggeWheelerSchwarzschildMetricComponent
                    frame
                    (reggeWheelerDetectorSpatialCoordinate axis)
                    contraction *
                  reggeWheelerOddParityLinearizedRiemann
                    frame
                    (
                      reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                        frame
                        cpmJet
                        harmonicJet
                    )
                    contraction
                    .time
                    (reggeWheelerDetectorSpatialCoordinate axis)
                    .time) := by
      unfold reggeWheelerSpacetimeCoordinateContraction
      ring

    rw [
      hSplit,
      prizcarbonOddParityVacuumCPMStaticTidalMetricLoweringCorrection_eq_zero
        frame
        cpmJet
        harmonicJet
        axis,
      zero_add
    ]

    cases axis <;>
      simp [
        reggeWheelerSpacetimeCoordinateContraction,
        reggeWheelerDetectorSpatialCoordinate,
        reggeWheelerSchwarzschildMetricComponent
      ]

  rw [
    reggeWheelerOddParityVacuumCPMStaticTidalCurvature_coordinateFormula,
    reggeWheelerOddParityVacuumCPMStaticTidalCurvature_coordinateFormula,
    reggeWheelerOddParityVacuumCPMStaticTidalCurvature_coordinateFormula,
    hLoweredDiagonal .radial,
    hLoweredDiagonal .theta,
    hLoweredDiagonal .phi,
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTime_eq_threeContractedRiemannCoordinates
  ]

  simp only [
    reggeWheelerSchwarzschildStaticSpatialLegScale,
    reggeWheelerDetectorSpatialCoordinate,
    reggeWheelerSchwarzschildMetricComponent,
    ← frame.lapseSqrt_sq
  ]

  field_simp [hLapse, hRadius, hRadiusSin]

/--
The static detector frame and the supplied vacuum CPM jet refer to the same
Schwarzschild background.

This condition is explicit because the derived connection currently receives
the detector frame and CPM jet as separate inputs.
-/
def prizcarbonOddParityVacuumCPMFrameCompatible
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet) : Prop :=
  frame.background =
    cpmJet.secondJet.firstJet.background

/--
Compatibility exposes the equality between the frame background and the
background stored in the CPM jet.
-/
theorem
    prizcarbonOddParityVacuumCPMFrameCompatible_background_eq
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet) :
    frame.background =
      cpmJet.secondJet.firstJet.background := by
  simpa [
    prizcarbonOddParityVacuumCPMFrameCompatible
  ] using hCompatible

/--
The first mixed-angular component selected for the master-equation route is
the radial-angular linearized Ricci component

`δR_{rA}`.

The compatibility proof is a required input, so this component cannot be
formed through this interface using unrelated frame and CPM backgrounds.
The connection jet is the concrete jet derived from the supplied CPM metric
second jet and vector-harmonic coordinate second jet.
-/
def
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngular
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (_hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) : ℝ :=
  prizcarbonOddParityLinearizedRicciContraction
    frame
    (
      reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
        frame
        cpmJet
        harmonicJet
    )
    .radial
    (reggeWheelerAngularCoordinateToSpacetime angular)

/--
The specialized radial-angular Ricci component is the explicit four-coordinate
contraction

`δR_{rA} = Σ_ρ δR^ρ_{rρA}`.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngular_eq_contractedRiemannCoordinates
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) :
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngular
        frame
        cpmJet
        harmonicJet
        hCompatible
        angular =
      reggeWheelerOddParityLinearizedRiemann
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
              frame
              cpmJet
              harmonicJet
          )
          .time
          .radial
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular) +
        reggeWheelerOddParityLinearizedRiemann
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
              frame
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular) +
        reggeWheelerOddParityLinearizedRiemann
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
              frame
              cpmJet
              harmonicJet
          )
          .theta
          .radial
          .theta
          (reggeWheelerAngularCoordinateToSpacetime angular) +
        reggeWheelerOddParityLinearizedRiemann
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
              frame
              cpmJet
              harmonicJet
          )
          .phi
          .radial
          .phi
          (reggeWheelerAngularCoordinateToSpacetime angular) := by
  rfl

/--
The derivative part of the radial-angular linearized Ricci component:

`Σ_ρ (∂_ρ δΓ^ρ_{Ar} - ∂_A δΓ^ρ_{ρr})`.

The connection derivatives are concretely reconstructed from the vacuum CPM
metric second jet. No vacuum equation is imposed.
-/
def
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivative
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (_hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) : ℝ :=
  reggeWheelerSpacetimeCoordinateContraction
    (fun contracted =>
      reggeWheelerOddParityLinearizedChristoffelPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            contracted
            contracted
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .radial -
        reggeWheelerOddParityLinearizedChristoffelPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          contracted
          contracted
          .radial)

/--
The lower-order connection-product part of the radial-angular Ricci component.

It contains the terms linear in one background Schwarzschild Christoffel
symbol and one odd-parity linearized Christoffel symbol.
-/
def
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularConnectionProduct
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (_hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) : ℝ :=
  reggeWheelerSpacetimeCoordinateContraction
    (fun contracted =>
      reggeWheelerSpacetimeCoordinateContraction
        (fun connectionContraction =>
          reggeWheelerOddParityLinearizedRiemannSummand
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
                frame
                cpmJet
                harmonicJet
            )
            contracted
            .radial
            contracted
            (reggeWheelerAngularCoordinateToSpacetime angular)
            connectionContraction))

/--
The CPM-derived radial-angular Ricci component splits exactly into its
connection-derivative and connection-product contributions:

`δR_{rA}
  = Σ_ρ (∂_ρ δΓ^ρ_{Ar} - ∂_A δΓ^ρ_{ρr})
    + Σ_{ρ,λ} δ(ΓΓ)^ρ_{rρA,λ}`.

This is an algebraic expansion of the existing linearized Riemann definition,
not a vacuum-zero theorem.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngular_eq_principalDerivative_add_connectionProduct
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) :
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngular
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular =
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivative
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular +
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularConnectionProduct
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular := by
  simp only [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngular,
    prizcarbonOddParityLinearizedRicciContraction,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivative,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularConnectionProduct,
    reggeWheelerOddParityLinearizedRiemann,
    reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet,
    reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet,
    reggeWheelerSpacetimeCoordinateContraction
  ] ;
    ring

/--
One coordinate contribution to the principal connection-derivative part of
the radial-angular linearized Ricci component:

`∂_ρ δΓ^ρ_{Ar} - ∂_A δΓ^ρ_{ρr}`.

The coordinate `ρ` remains explicit so that the time, radial, theta, and phi
contributions can be simplified independently under the first-error protocol.
-/
def
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (_hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate)
    (contracted : ReggeWheelerSpacetimeCoordinate) : ℝ :=
  reggeWheelerOddParityLinearizedChristoffelPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        contracted
        contracted
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial -
    reggeWheelerOddParityLinearizedChristoffelPartial
      frame
      (
        reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
          cpmJet
          harmonicJet
      )
      (reggeWheelerAngularCoordinateToSpacetime angular)
      contracted
      contracted
      .radial

/--
The principal derivative is exactly the sum of its four explicit coordinate
contributions.

No coordinate contribution is asserted to vanish, and no spherical-harmonic
identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivative_eq_fourCoordinateContributions
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) :
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivative
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular =
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular
          .time +
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular
          .radial +
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular
          .theta +
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular
          .phi := by
  rfl

/--
The time-coordinate contribution to the principal radial-angular Ricci
derivative expands into exactly two Christoffel-summand contractions:

`∂ₜ δΓᵗ_{Ar} - ∂ₐ δΓᵗ_{tr}`.

This exposes the product-rule terms without simplifying any metric or harmonic
component and without imposing a vacuum equation.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeTimeContribution_eq_twoChristoffelSummandContractions
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) :
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular
          .time =
      (1 / 2 : ℝ) *
          reggeWheelerSpacetimeCoordinateContraction
            (fun inverseMetricContraction =>
              reggeWheelerOddParityLinearizedChristoffelSummandPartial
                frame
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                    cpmJet
                    harmonicJet
                )
                .time
                .time
                (reggeWheelerAngularCoordinateToSpacetime angular)
                .radial
                inverseMetricContraction) -
        (1 / 2 : ℝ) *
          reggeWheelerSpacetimeCoordinateContraction
            (fun inverseMetricContraction =>
              reggeWheelerOddParityLinearizedChristoffelSummandPartial
                frame
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                    cpmJet
                    harmonicJet
                )
                (reggeWheelerAngularCoordinateToSpacetime angular)
                .time
                .time
                .radial
                inverseMetricContraction) := by
  rfl

/--
The first inner inverse-metric contraction in the time-coordinate principal
Ricci contribution expands into its four explicit coordinate summands.

This is the contraction occurring in

`∂ₜ δΓᵗ_{Ar}`.

No individual summand is simplified or asserted to vanish.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_fourInverseMetricCoordinateSummands
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSpacetimeCoordinateContraction
          (fun inverseMetricContraction =>
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .time
              .time
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              inverseMetricContraction) =
      reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time +
        reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial +
        reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .theta +
        reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .phi := by
  rfl

/--
The inverse-metric `.time` summand in `∂ₜ δΓᵗ_{Ar}` expands into the four
product-rule terms defining the derivative of the linearized Christoffel
summand.

No term is asserted to vanish and no CPM coefficient or harmonic identity is
used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeInverseMetricSummand_eq_fourProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .time
            .time
            .time *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .radial
            .time +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .time
              .time *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              .time
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .time +
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              .time
              .time
              .time *
            reggeWheelerOddParityPerturbationConnectionKernel
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .time +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            reggeWheelerOddParityPerturbationConnectionKernelPartial
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .time
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .time := by
  rfl

/--
In the inverse-metric `.time` summand of `∂ₜ δΓᵗ_{Ar}`, the first three
product-rule terms vanish:

* the background connection kernel with indices `(A,r,t)` vanishes;
* the odd-parity inverse-metric variation `δgᵗᵗ` vanishes;
* the time derivative of the background inverse component `gᵗᵗ` vanishes.

Therefore only the background inverse metric multiplying the derivative of the
perturbation connection kernel remains. No harmonic identity or vacuum equation
is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeInverseMetricSummand_eq_perturbationKernelDerivativeTerm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time =
      reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .time
            .time *
        reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time := by
  have hBackgroundKernel :
      reggeWheelerSchwarzschildConnectionKernel
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time =
        0 := by
    cases angular <;>
      simp [
        reggeWheelerAngularCoordinateToSpacetime,
        reggeWheelerSchwarzschildConnectionKernel,
        reggeWheelerSchwarzschildMetricPartial
      ]

  have hLinearizedInverseTimeTime :
      reggeWheelerOddParityLinearizedInverseMetricComponent
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          .time
          .time =
        0 := by
    simp [
      reggeWheelerOddParityLinearizedInverseMetricComponent,
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerOddParitySpacetimeMetricPerturbation
    ]

  have hBackgroundInverseTimePartial :
      reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          .time
          .time
          .time =
        0 := by
    simp [
      reggeWheelerSchwarzschildInverseMetricComponentPartial
    ]

  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeInverseMetricSummand_eq_fourProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular,
    hBackgroundKernel,
    hLinearizedInverseTimeTime,
    hBackgroundInverseTimePartial
  ]

  ring

/--
The retained perturbation connection-kernel derivative in the inverse-metric
`.time` summand expands into its three metric-second-partial terms:

`∂ₜK[h]_{Art}
  = ∂ₜ∂ₐh_{rt}
    + ∂ₜ∂ᵣh_{At}
    - ∂ₜ²h_{Ar}`.

No metric component is simplified, and no harmonic or vacuum identity is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimePerturbationKernelDerivative_eq_threeMetricSecondPartialTerms
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time =
      (
        reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
          cpmJet
          harmonicJet
      ).metricSecondPartial
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time +
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        ).metricSecondPartial
          .time
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time -
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        ).metricSecondPartial
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial := by
  rfl

/--
The first metric-second-partial term in

`∂ₜK[h]_{Art}
  = ∂ₜ∂ₐh_{rt}
    + ∂ₜ∂ᵣh_{At}
    - ∂ₜ²h_{Ar}`

vanishes because the CPM odd-parity metric second jet has no radial-time metric
component. No harmonic or vacuum identity is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeAngularDerivativeRadialTimeMetricSecondPartial_eq_zero
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
        cpmJet
        harmonicJet
    ).metricSecondPartial
        .time
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .time =
      0 := by
  cases angular <;>
    rfl

/--
The second metric-second-partial term in

`∂ₜK[h]_{Art}
  = ∂ₜ∂ₐh_{rt}
    + ∂ₜ∂ᵣh_{At}
    - ∂ₜ²h_{Ar}`

is the CPM-derived mixed time-radial derivative of the time-angular metric
coefficient multiplied by the odd vector-harmonic value.

No harmonic eigenvalue or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeRadialDerivativeAngularTimeMetricSecondPartial_eq_CPMTimeCoefficientDerivative
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
        cpmJet
        harmonicJet
    ).metricSecondPartial
        .time
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .time =
      reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
          cpmJet *
        reggeWheelerOddParityVectorHarmonicValue
          harmonicJet.firstJet.harmonic
          angular := by
  cases angular <;>
    rfl

/--
The third metric-second-partial term in

`∂ₜK[h]_{Art}
  = ∂ₜ∂ₐh_{rt}
    + ∂ₜ∂ᵣh_{At}
    - ∂ₜ²h_{Ar}`

is the CPM-derived time-time derivative of the radial-angular metric
coefficient multiplied by the odd vector-harmonic value.

No harmonic eigenvalue or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeTimeDerivativeAngularRadialMetricSecondPartial_eq_CPMRadialCoefficientDerivative
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
        cpmJet
        harmonicJet
    ).metricSecondPartial
        .time
        .time
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial =
      reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
          cpmJet *
        reggeWheelerOddParityVectorHarmonicValue
          harmonicJet.firstJet.harmonic
          angular := by
  cases angular <;>
    rfl

/--
The retained perturbation connection-kernel derivative is exactly the
difference between the mixed time-radial derivative of the CPM time coefficient
and the time-time derivative of the CPM radial coefficient, multiplied by the
odd vector-harmonic value:

`∂ₜK[h]_{Art}
  = (∂ₜ∂ᵣ h₀ - ∂ₜ² h₁) X_A`.

The radial-time metric component contributes zero. No harmonic eigenvalue or
vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimePerturbationKernelDerivative_eq_CPMCoefficientDifference
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time =
      (
        reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
            cpmJet -
          reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
            cpmJet
      ) *
        reggeWheelerOddParityVectorHarmonicValue
          harmonicJet.firstJet.harmonic
          angular := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimePerturbationKernelDerivative_eq_threeMetricSecondPartialTerms
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeAngularDerivativeRadialTimeMetricSecondPartial_eq_zero
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeRadialDerivativeAngularTimeMetricSecondPartial_eq_CPMTimeCoefficientDerivative
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeTimeDerivativeAngularRadialMetricSecondPartial_eq_CPMRadialCoefficientDerivative
      cpmJet
      harmonicJet
      angular
  ]

  ring

/--
The inverse-metric `.time` summand in `∂ₜ δΓᵗ_{Ar}` is the Schwarzschild
inverse time-time metric component multiplying the CPM coefficient difference
and the odd vector-harmonic value:

`ḡᵗᵗ (∂ₜ∂ᵣ h₀ - ∂ₜ² h₁) X_A`.

This combines only the previously proved product-rule reduction and
perturbation-kernel coefficient formula. No harmonic eigenvalue or vacuum
equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeInverseMetricSummand_eq_inverseMetric_mul_CPMCoefficientDifference
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time =
      reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .time
            .time *
        (
          (
            reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
                cpmJet -
              reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
                cpmJet
          ) *
            reggeWheelerOddParityVectorHarmonicValue
              harmonicJet.firstJet.harmonic
              angular
        ) := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeInverseMetricSummand_eq_perturbationKernelDerivativeTerm
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimePerturbationKernelDerivative_eq_CPMCoefficientDifference
      cpmJet
      harmonicJet
      angular
  ]

/--
The inverse-metric `.radial` summand in the time derivative

`∂ₜ δΓᵗ_{Ar}`

vanishes.

Every product-rule term contains either the off-diagonal Schwarzschild inverse
component `ḡᵗʳ`, its time derivative, the odd-parity inverse variation
`δgᵗʳ`, or its time derivative. Each of these factors is zero.

No harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeRadialInverseMetricSummand_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial =
      0 := by
  have hLinearizedInverseTimeRadial :
      reggeWheelerOddParityLinearizedInverseMetricComponent
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          .time
          .radial =
        0 := by
    simp [
      reggeWheelerOddParityLinearizedInverseMetricComponent,
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerOddParitySpacetimeMetricPerturbation
    ]

  have hLinearizedInverseTimeRadialPartial :
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          .radial =
        0 := by
    simp [
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial,
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerOddParityVacuumCPMMetricPartial,
      reggeWheelerOddParitySpacetimeMetricPerturbation,
      reggeWheelerSchwarzschildInverseMetricComponentPartial
    ]

  have hBackgroundInverseTimeRadial :
      reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .time
          .radial =
        0 := by
    simp [
      reggeWheelerSchwarzschildInverseMetricComponent
    ]

  have hBackgroundInverseTimeRadialPartial :
      reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          .time
          .time
          .radial =
        0 := by
    simp [
      reggeWheelerSchwarzschildInverseMetricComponentPartial
    ]

  unfold reggeWheelerOddParityLinearizedChristoffelSummandPartial

  rw [
    hLinearizedInverseTimeRadialPartial,
    hLinearizedInverseTimeRadial,
    hBackgroundInverseTimeRadialPartial,
    hBackgroundInverseTimeRadial
  ]

  ring

/--
The inverse-metric `.theta` summand in the time derivative

`∂ₜ δΓᵗ_{Ar}`

reduces to the time derivative of the linearized inverse component
`δgᵗθ` multiplying the background connection kernel `K̄_{Arθ}`.

The retained first term is not asserted to vanish. No harmonic identity or
vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeThetaInverseMetricSummand_eq_linearizedInversePartial_mul_backgroundKernel
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .theta =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .time
            .time
            .theta *
        reggeWheelerSchwarzschildConnectionKernel
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .theta := by
  have hBackgroundKernelTimePartial :
      reggeWheelerSchwarzschildConnectionKernelPartial
          frame
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .theta =
        0 := by
    cases angular <;>
      simp [
        reggeWheelerAngularCoordinateToSpacetime,
        reggeWheelerSchwarzschildConnectionKernelPartial,
        reggeWheelerSchwarzschildMetricSecondPartial
      ]

  have hBackgroundInverseTimeThetaPartial :
      reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          .time
          .time
          .theta =
        0 := by
    rfl

  have hBackgroundInverseTimeTheta :
      reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .time
          .theta =
        0 := by
    rfl

  unfold reggeWheelerOddParityLinearizedChristoffelSummandPartial

  rw [
    hBackgroundKernelTimePartial,
    hBackgroundInverseTimeThetaPartial,
    hBackgroundInverseTimeTheta
  ]

  ring

/--
The time derivative of the linearized inverse component `δgᵗθ` is

`-ḡᵗᵗ ḡθθ (∂ₜh₀) X_θ`.

The two background-inverse derivative terms vanish because the Schwarzschild
background is static. The surviving metric derivative is supplied by the
CPM-derived metric first jet.

No angular eigenvalue or vacuum wave equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeThetaLinearizedInversePartial_eq_CPMTimeCoefficientDerivative
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          .theta =
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
          (
            reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                cpmJet.secondJet *
              reggeWheelerOddParityVectorHarmonicValue
                harmonicJet.firstJet.harmonic
                .theta
          ) *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
      ) := by
  have hBackgroundInverseTimeTimeTimePartial :
      reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          .time
          .time
          .time =
        0 := by
    rfl

  have hBackgroundInverseThetaThetaTimePartial :
      reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          .time
          .theta
          .theta =
        0 := by
    rfl

  have hMetricTimeThetaTimePartial :
      (
        reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
          cpmJet
          harmonicJet
      ).firstJet.metricPartial
          .time
          .time
          .theta =
        reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
            cpmJet.secondJet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.firstJet.harmonic
            .theta := by
    rfl

  unfold reggeWheelerOddParityLinearizedInverseMetricComponentPartial

  rw [
    hBackgroundInverseTimeTimeTimePartial,
    hBackgroundInverseThetaThetaTimePartial,
    hMetricTimeThetaTimePartial
  ]

  ring

/--
The inverse-metric `.theta` summand in `∂ₜ δΓᵗ_{Ar}` is the explicit CPM
time-coefficient derivative contribution

`-(ḡᵗᵗ (∂ₜh₀) X_θ ḡθθ) K̄_{Arθ}`.

The Schwarzschild background connection kernel is retained without component
simplification. No angular eigenvalue or vacuum wave equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeThetaInverseMetricSummand_eq_CPMTimeCoefficientDerivative
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .theta =
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
          (
            reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                cpmJet.secondJet *
              reggeWheelerOddParityVectorHarmonicValue
                harmonicJet.firstJet.harmonic
                .theta
          ) *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
      ) *
        reggeWheelerSchwarzschildConnectionKernel
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .theta := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeThetaInverseMetricSummand_eq_linearizedInversePartial_mul_backgroundKernel
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeThetaLinearizedInversePartial_eq_CPMTimeCoefficientDerivative
      frame
      cpmJet
      harmonicJet
  ]

/--
The inverse-metric `.phi` summand in the time derivative

`∂ₜ δΓᵗ_{Ar}`

reduces to the time derivative of the linearized inverse component
`δgᵗφ` multiplying the background connection kernel `K̄_{Arφ}`.

The other three product-rule terms vanish because:

* the Schwarzschild background connection kernel has zero time derivative;
* the time derivative of the off-diagonal background inverse component
  `ḡᵗφ` is zero;
* the off-diagonal background inverse component `ḡᵗφ` is zero.

The retained first term is not asserted to vanish. No harmonic identity or
vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimePhiInverseMetricSummand_eq_linearizedInversePartial_mul_backgroundKernel
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .phi =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .time
            .time
            .phi *
        reggeWheelerSchwarzschildConnectionKernel
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .phi := by
  have hBackgroundKernelTimePartial :
      reggeWheelerSchwarzschildConnectionKernelPartial
          frame
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .phi =
        0 := by
    cases angular <;>
      simp [
        reggeWheelerAngularCoordinateToSpacetime,
        reggeWheelerSchwarzschildConnectionKernelPartial,
        reggeWheelerSchwarzschildMetricSecondPartial
      ]

  have hBackgroundInverseTimePhiPartial :
      reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          .time
          .time
          .phi =
        0 := by
    rfl

  have hBackgroundInverseTimePhi :
      reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .time
          .phi =
        0 := by
    rfl

  unfold reggeWheelerOddParityLinearizedChristoffelSummandPartial

  rw [
    hBackgroundKernelTimePartial,
    hBackgroundInverseTimePhiPartial,
    hBackgroundInverseTimePhi
  ]

  ring

/--
The time derivative of the linearized inverse component `δgᵗφ` is

`-ḡᵗᵗ ḡφφ (∂ₜh₀) X_φ`.

The two background-inverse derivative terms vanish because the Schwarzschild
background is static. The surviving metric derivative is supplied by the
CPM-derived metric first jet.

No angular eigenvalue or vacuum wave equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciTimePhiLinearizedInversePartial_eq_CPMTimeCoefficientDerivative
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          .phi =
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
          (
            reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                cpmJet.secondJet *
              reggeWheelerOddParityVectorHarmonicValue
                harmonicJet.firstJet.harmonic
                .phi
          ) *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .phi
            .phi
      ) := by
  have hBackgroundInverseTimeTimeTimePartial :
      reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          .time
          .time
          .time =
        0 := by
    rfl

  have hBackgroundInversePhiPhiTimePartial :
      reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          .time
          .phi
          .phi =
        0 := by
    rfl

  have hMetricTimePhiTimePartial :
      (
        reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
          cpmJet
          harmonicJet
      ).firstJet.metricPartial
          .time
          .time
          .phi =
        reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
            cpmJet.secondJet *
          reggeWheelerOddParityVectorHarmonicValue
            harmonicJet.firstJet.harmonic
            .phi := by
    rfl

  unfold reggeWheelerOddParityLinearizedInverseMetricComponentPartial

  rw [
    hBackgroundInverseTimeTimeTimePartial,
    hBackgroundInversePhiPhiTimePartial,
    hMetricTimePhiTimePartial
  ]

  ring

/--
The inverse-metric `.phi` summand in `∂ₜ δΓᵗ_{Ar}` is the explicit CPM
time-coefficient derivative contribution

`-(ḡᵗᵗ (∂ₜh₀) X_φ ḡφφ) K̄_{Arφ}`.

The Schwarzschild background connection kernel is retained without component
simplification. No angular eigenvalue or vacuum wave equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimePhiInverseMetricSummand_eq_CPMTimeCoefficientDerivative
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .phi =
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
          (
            reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                cpmJet.secondJet *
              reggeWheelerOddParityVectorHarmonicValue
                harmonicJet.firstJet.harmonic
                .phi
          ) *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .phi
            .phi
      ) *
        reggeWheelerSchwarzschildConnectionKernel
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .phi := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimePhiInverseMetricSummand_eq_linearizedInversePartial_mul_backgroundKernel
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciTimePhiLinearizedInversePartial_eq_CPMTimeCoefficientDerivative
      frame
      cpmJet
      harmonicJet
  ]

/--
The inverse-metric contraction in `∂ₜ δΓᵗ_{Ar}` recombines as:

* the previously completed `.time` coordinate summand;
* no `.radial` contribution;
* the explicit CPM time-coefficient `.theta` contribution;
* the explicit CPM time-coefficient `.phi` contribution.

The background angular connection kernels are retained without component
simplification. No angular eigenvalue or vacuum wave equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_timeThetaPhiCPMSum
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSpacetimeCoordinateContraction
          (fun inverseMetricContraction =>
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .time
              .time
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              inverseMetricContraction) =
      reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .time
          .time
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time +
        (
          -(
            reggeWheelerSchwarzschildInverseMetricComponent
                  frame
                  .time
                  .time *
              (
                reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                    cpmJet.secondJet *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .theta
              ) *
              reggeWheelerSchwarzschildInverseMetricComponent
                frame
                .theta
                .theta
          ) *
            reggeWheelerSchwarzschildConnectionKernel
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .theta
        ) +
        (
          -(
            reggeWheelerSchwarzschildInverseMetricComponent
                  frame
                  .time
                  .time *
              (
                reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                    cpmJet.secondJet *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .phi
              ) *
              reggeWheelerSchwarzschildInverseMetricComponent
                frame
                .phi
                .phi
          ) *
            reggeWheelerSchwarzschildConnectionKernel
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .phi
        ) := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_fourInverseMetricCoordinateSummands
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeRadialInverseMetricSummand_eq_zero
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeThetaInverseMetricSummand_eq_CPMTimeCoefficientDerivative
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimePhiInverseMetricSummand_eq_CPMTimeCoefficientDerivative
      frame
      cpmJet
      harmonicJet
      angular
  ]

  ring

/--
The complete inverse-metric contraction in `∂ₜ δΓᵗ_{Ar}` is reduced to three
explicit CPM contributions:

* the time-coordinate term contains the difference
  `∂ₜ∂ᵣh₀ - ∂ₜ²h₁`;
* the `.theta` term contains `∂ₜh₀` and `X_θ`;
* the `.phi` term contains `∂ₜh₀` and `X_φ`.

The angular Schwarzschild connection kernels remain explicit and unsimplified.
No angular eigenvalue or vacuum wave equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_explicitCPMCoordinateSum
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSpacetimeCoordinateContraction
          (fun inverseMetricContraction =>
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .time
              .time
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              inverseMetricContraction) =
      reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .time
            .time *
        (
          (
            reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
                cpmJet -
              reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
                cpmJet
          ) *
            reggeWheelerOddParityVectorHarmonicValue
              harmonicJet.firstJet.harmonic
              angular
        ) +
        (
          -(
            reggeWheelerSchwarzschildInverseMetricComponent
                  frame
                  .time
                  .time *
              (
                reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                    cpmJet.secondJet *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .theta
              ) *
              reggeWheelerSchwarzschildInverseMetricComponent
                frame
                .theta
                .theta
          ) *
            reggeWheelerSchwarzschildConnectionKernel
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .theta
        ) +
        (
          -(
            reggeWheelerSchwarzschildInverseMetricComponent
                  frame
                  .time
                  .time *
              (
                reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                    cpmJet.secondJet *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .phi
              ) *
              reggeWheelerSchwarzschildInverseMetricComponent
                frame
                .phi
                .phi
          ) *
            reggeWheelerSchwarzschildConnectionKernel
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .phi
        ) := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_timeThetaPhiCPMSum
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeInverseMetricSummand_eq_inverseMetric_mul_CPMCoefficientDifference
      frame
      cpmJet
      harmonicJet
      angular
  ]

/--
The Schwarzschild background kernel `K̄_{Arθ}` is componentwise:

* `K̄_{θrθ} = 2r`;
* `K̄_{φrθ} = 0`.

This is only a coordinate-background calculation. No CPM equation, angular
harmonic identity, or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundThetaKernel_eq
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildConnectionKernel
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .theta =
      match angular with
      | .theta => 2 * frame.background.radius
      | .phi => 0 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerSchwarzschildConnectionKernel,
      reggeWheelerSchwarzschildMetricPartial
    ]

/--
The Schwarzschild background kernel `K̄_{Arφ}` is componentwise:

* `K̄_{θrφ} = 0`;
* `K̄_{φrφ} = 2r sin²θ`.

This is only a coordinate-background calculation. No CPM equation, angular
harmonic identity, or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundPhiKernel_eq
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildConnectionKernel
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .phi =
      match angular with
      | .theta => 0
      | .phi =>
          2 *
            frame.background.radius *
            Real.sin frame.polarAngle ^ 2 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerSchwarzschildConnectionKernel,
      reggeWheelerSchwarzschildMetricPartial
    ]

/--
After evaluating both Schwarzschild angular connection kernels, the contraction
in `∂ₜ δΓᵗ_{Ar}` has one explicit formula for each angular coordinate.

For `A = θ`, only the `θ` connection-kernel term survives. For `A = φ`, only
the `φ` connection-kernel term survives.

No inverse-metric cancellation, angular harmonic identity, or vacuum wave
equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_componentwiseExplicitCPMSum
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSpacetimeCoordinateContraction
          (fun inverseMetricContraction =>
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .time
              .time
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              inverseMetricContraction) =
      match angular with
      | .theta =>
          reggeWheelerSchwarzschildInverseMetricComponent
                frame
                .time
                .time *
              (
                (
                  reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
                      cpmJet -
                    reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
                      cpmJet
                ) *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .theta
              ) +
            (
              -(
                reggeWheelerSchwarzschildInverseMetricComponent
                      frame
                      .time
                      .time *
                  (
                    reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                        cpmJet.secondJet *
                      reggeWheelerOddParityVectorHarmonicValue
                        harmonicJet.firstJet.harmonic
                        .theta
                  ) *
                  reggeWheelerSchwarzschildInverseMetricComponent
                    frame
                    .theta
                    .theta
              ) *
                (2 * frame.background.radius)
            )

      | .phi =>
          reggeWheelerSchwarzschildInverseMetricComponent
                frame
                .time
                .time *
              (
                (
                  reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
                      cpmJet -
                    reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
                      cpmJet
                ) *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .phi
              ) +
            (
              -(
                reggeWheelerSchwarzschildInverseMetricComponent
                      frame
                      .time
                      .time *
                  (
                    reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                        cpmJet.secondJet *
                      reggeWheelerOddParityVectorHarmonicValue
                        harmonicJet.firstJet.harmonic
                        .phi
                  ) *
                  reggeWheelerSchwarzschildInverseMetricComponent
                    frame
                    .phi
                    .phi
              ) *
                (
                  2 *
                    frame.background.radius *
                    Real.sin frame.polarAngle ^ 2
                )
            ) := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_explicitCPMCoordinateSum
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundThetaKernel_eq
      frame
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundPhiKernel_eq
      frame
      angular
  ]

  cases angular <;> simp

/--
The Schwarzschild inverse angular metric and the radial theta-kernel factor
satisfy

`ḡ^{θθ} (2r) = 2/r`.

Only positivity of the Schwarzschild radius is used. No CPM equation, harmonic
identity, or vacuum equation is invoked.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciBackgroundThetaInverseMetricKernelProduct_eq_two_div_radius
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .theta
          .theta *
        (2 * frame.background.radius) =
      2 / frame.background.radius := by
  have hRadius :
      frame.background.radius ≠ 0 :=
    ne_of_gt
      (
        reggeWheelerSchwarzschildBackground_radius_pos
          frame.background
      )

  change
    (1 / frame.background.radius ^ 2) *
          (2 * frame.background.radius) =
      2 / frame.background.radius

  field_simp [hRadius]

/--
The Schwarzschild inverse azimuthal metric and the radial phi-kernel factor
satisfy

`ḡ^{φφ} (2r sin²θ) = 2/r`.

Only positivity of the Schwarzschild radius and nonvanishing of the static
frame's polar sine are used. No CPM equation, harmonic identity, or vacuum
equation is invoked.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciBackgroundPhiInverseMetricKernelProduct_eq_two_div_radius
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .phi
          .phi *
        (
          2 *
            frame.background.radius *
            Real.sin frame.polarAngle ^ 2
        ) =
      2 / frame.background.radius := by
  have hRadius :
      frame.background.radius ≠ 0 :=
    ne_of_gt
      (
        reggeWheelerSchwarzschildBackground_radius_pos
          frame.background
      )

  have hSin :
      Real.sin frame.polarAngle ≠ 0 :=
    frame.sinPolarAngle_ne_zero

  have hRadiusSin :
      frame.background.radius *
          Real.sin frame.polarAngle ≠
        0 :=
    mul_ne_zero hRadius hSin

  change
    (
      1 /
        (
          frame.background.radius *
            Real.sin frame.polarAngle
        ) ^ 2
    ) *
        (
          2 *
            frame.background.radius *
            Real.sin frame.polarAngle ^ 2
        ) =
      2 / frame.background.radius

  field_simp [hRadius, hSin, hRadiusSin]

/--
After simplifying both angular inverse-metric/background-kernel products, the
complete contraction in `∂ₜ δΓᵗ_{Ar}` has one formula valid for either angular
coordinate:

`ḡᵗᵗ (∂ₜ∂ᵣh₀ - ∂ₜ²h₁) X_A
  - ḡᵗᵗ (∂ₜh₀) X_A (2/r)`.

The theta and phi coordinate cases are unified only through their separately
proved background identities. No angular harmonic eigenvalue or vacuum wave
equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_commonTwoDivRadiusCPMForm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSpacetimeCoordinateContraction
          (fun inverseMetricContraction =>
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .time
              .time
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              inverseMetricContraction) =
      reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .time
            .time *
          (
            (
              reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
                  cpmJet -
                reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
                  cpmJet
            ) *
              reggeWheelerOddParityVectorHarmonicValue
                harmonicJet.firstJet.harmonic
                angular
          ) -
        (
          reggeWheelerSchwarzschildInverseMetricComponent
                frame
                .time
                .time *
            (
              reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                  cpmJet.secondJet *
                reggeWheelerOddParityVectorHarmonicValue
                  harmonicJet.firstJet.harmonic
                  angular
            )
        ) *
          (2 / frame.background.radius) := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_componentwiseExplicitCPMSum
      frame
      cpmJet
      harmonicJet
      angular
  ]

  cases angular
  · rw [
      ←
        prizcarbonOddParityVacuumCPMLinearizedRicciBackgroundThetaInverseMetricKernelProduct_eq_two_div_radius
          frame
    ]
    ring

  · rw [
      ←
        prizcarbonOddParityVacuumCPMLinearizedRicciBackgroundPhiInverseMetricKernelProduct_eq_two_div_radius
          frame
    ]
    ring

/--
The complete contraction in `∂ₜ δΓᵗ_{Ar}` factors into the background
inverse-time component, one radial CPM coefficient, and the angular vector
harmonic:

`ḡᵗᵗ
  (∂ₜ∂ᵣh₀ - ∂ₜ²h₁ - (2/r) ∂ₜh₀)
  X_A`.

This is an algebraic factorization of the previously proved common-coordinate
formula. No harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_factoredVectorHarmonicCPMForm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSpacetimeCoordinateContraction
          (fun inverseMetricContraction =>
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .time
              .time
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              inverseMetricContraction) =
      reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .time
            .time *
        (
          (
            reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
                cpmJet -
              reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
                cpmJet -
              reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                  cpmJet.secondJet *
                (2 / frame.background.radius)
          ) *
            reggeWheelerOddParityVectorHarmonicValue
              harmonicJet.firstJet.harmonic
              angular
        ) := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_commonTwoDivRadiusCPMForm
      frame
      cpmJet
      harmonicJet
      angular
  ]

  ring

/--
The time-coordinate contribution to the principal radial-angular Ricci
derivative is reduced to:

* one half of the completed factored CPM expression for
  `∂ₜ δΓᵗ_{Ar}`;
* minus one half of the still-retained contraction representing
  `∂ₐ δΓᵗ_{tr}`.

Only the previously proved time-derivative connection contraction is
substituted. The angular-derivative connection contraction remains completely
explicit and unsimplified. No harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeTimeContribution_eq_factoredCPMTimeTerm_sub_angularDerivativeConnectionTerm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) :
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular
          .time =
      (1 / 2 : ℝ) *
          (
            reggeWheelerSchwarzschildInverseMetricComponent
                  frame
                  .time
                  .time *
              (
                (
                  reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
                      cpmJet -
                    reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
                      cpmJet -
                    reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                        cpmJet.secondJet *
                      (2 / frame.background.radius)
                ) *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    angular
              )
          ) -
        (1 / 2 : ℝ) *
          reggeWheelerSpacetimeCoordinateContraction
            (fun inverseMetricContraction =>
              reggeWheelerOddParityLinearizedChristoffelSummandPartial
                frame
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                    cpmJet
                    harmonicJet
                )
                (reggeWheelerAngularCoordinateToSpacetime angular)
                .time
                .time
                .radial
                inverseMetricContraction) := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeTimeContribution_eq_twoChristoffelSummandContractions
      frame
      cpmJet
      harmonicJet
      hCompatible
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularTimeDerivativeConnectionTerm_eq_factoredVectorHarmonicCPMForm
      frame
      cpmJet
      harmonicJet
      angular
  ]

/--
The retained inverse-metric contraction representing
`∂ₐ δΓᵗ_{tr}` expands into its four explicit coordinate summands.

No coordinate summand is simplified or asserted to vanish. In particular, no
angular harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeConnectionTerm_eq_fourInverseMetricCoordinateSummands
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSpacetimeCoordinateContraction
          (fun inverseMetricContraction =>
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .time
              .radial
              inverseMetricContraction) =
      reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .time +
        reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .radial +
        reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .theta +
        reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .phi := by
  rfl

/--
The inverse-metric `.time` summand in the retained contraction
`∂ₐ δΓᵗ_{tr}` expands into the four product-rule terms defining the coordinate
derivative of the linearized Christoffel summand.

No term is yet asserted to vanish. In particular, the angular derivative of the
perturbation connection kernel remains explicit, and no harmonic or vacuum
identity is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeTimeInverseMetricSummand_eq_fourProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .time =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .time
            .time *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            .time
            .radial
            .time +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .time
              .time *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .radial
              .time +
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .time *
            reggeWheelerOddParityPerturbationConnectionKernel
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .time
              .radial
              .time +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            reggeWheelerOddParityPerturbationConnectionKernelPartial
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .radial
              .time := by
  rfl

/--
The angular derivative of the odd-parity linearized inverse component
`δgᵗᵗ` vanishes.

The inverse-metric variation contains only terms multiplied by the CPM
component `hₜₜ` or its angular derivative. Both vanish for the odd-parity
Regge–Wheeler metric.

No harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeLinearizedInverseTimeTimePartial_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time =
      0 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial,
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerOddParityVacuumCPMMetricPartial,
      reggeWheelerOddParitySpacetimeMetricPerturbation
    ]

/--
The theta and phi coordinate derivatives of the Schwarzschild inverse
time-time metric component vanish:

`∂ₐ ḡᵗᵗ = 0`.

This is a background static-spherical identity. No CPM component, harmonic
identity, or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeBackgroundInverseTimeTimePartial_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time =
      0 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerSchwarzschildInverseMetricComponentPartial
    ]

/--
The undifferentiated odd-parity linearized inverse time-time metric component
vanishes:

`δgᵗᵗ = 0`.

The diagonal Schwarzschild inverse-metric variation is proportional to the
odd-parity metric component `hₜₜ`, which is absent in Regge–Wheeler gauge.

No coordinate derivative, harmonic identity, or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularLinearizedInverseTimeTime_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponent
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          .time
          .time =
      0 := by
  simp [
    reggeWheelerOddParityLinearizedInverseMetricComponent,
    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
    reggeWheelerOddParityVacuumCPMMetricSecondJet,
    reggeWheelerOddParityVacuumCPMMetricFirstJet,
    reggeWheelerOddParitySpacetimeMetricPerturbation
  ]

/--
In the inverse-metric `.time` summand of the retained angular-derivative
connection contraction, the first three product-rule terms vanish:

* the angular derivative of `δgᵗᵗ` is zero;
* the undifferentiated component `δgᵗᵗ` is zero;
* the angular derivative of the Schwarzschild component `ḡᵗᵗ` is zero.

Therefore only the background inverse time-time metric multiplying the angular
derivative of the perturbation connection kernel remains.

No harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeTimeInverseMetricSummand_eq_perturbationKernelDerivativeTerm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .time =
      reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .time
            .time *
          reggeWheelerOddParityPerturbationConnectionKernelPartial
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .time
            .radial
            .time := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeTimeInverseMetricSummand_eq_fourProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeLinearizedInverseTimeTimePartial_eq_zero
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularLinearizedInverseTimeTime_eq_zero
      frame
      cpmJet
      harmonicJet,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeBackgroundInverseTimeTimePartial_eq_zero
      frame
      angular
  ]

  ring

/--
The retained angular derivative of the perturbation connection kernel expands
into its three metric-second-partial terms:

`∂ₐK[h]_{trt}
  = ∂ₐ∂ₜh_{rt}
    + ∂ₐ∂ᵣh_{tt}
    - ∂ₐ∂ₜh_{tr}`.

No metric component is simplified, and no harmonic or vacuum identity is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeTimePerturbationKernelDerivative_eq_threeMetricSecondPartialTerms
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .radial
          .time =
      (
        reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
          cpmJet
          harmonicJet
      ).metricSecondPartial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .radial
          .time +
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        ).metricSecondPartial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time
          .time -
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        ).metricSecondPartial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial := by
  rfl

/--
The first metric-second-partial term in

`∂ₐK[h]_{trt}
  = ∂ₐ∂ₜh_{rt}
    + ∂ₐ∂ᵣh_{tt}
    - ∂ₐ∂ₜh_{tr}`

vanishes because the CPM odd-parity metric second jet has no radial-time
component.

No commutation of abstract partial derivatives, harmonic identity, or vacuum
equation is used; this follows directly from the explicit CPM second jet.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularTimeDerivativeRadialTimeMetricSecondPartial_eq_zero
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
        cpmJet
        harmonicJet
    ).metricSecondPartial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .time
        .radial
        .time =
      0 := by
  cases angular <;> rfl

/--
The second metric-second-partial term in

`∂ₐK[h]_{trt}
  = ∂ₐ∂ₜh_{rt}
    + ∂ₐ∂ᵣh_{tt}
    - ∂ₐ∂ₜh_{tr}`

vanishes because the CPM odd-parity metric second jet has no time-time
component.

No commutation of abstract partial derivatives, harmonic identity, or vacuum
equation is used; this follows directly from the explicit CPM second jet.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularRadialDerivativeTimeTimeMetricSecondPartial_eq_zero
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
        cpmJet
        harmonicJet
    ).metricSecondPartial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .time
        .time =
      0 := by
  cases angular <;> rfl

/--
The third metric-second-partial term in

`∂ₐK[h]_{trt}
  = ∂ₐ∂ₜh_{rt}
    + ∂ₐ∂ᵣh_{tt}
    - ∂ₐ∂ₜh_{tr}`

vanishes because the CPM odd-parity metric second jet has no time-radial
component.

No commutation of abstract partial derivatives, harmonic identity, or vacuum
equation is used; this follows directly from the explicit CPM second jet.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularTimeDerivativeTimeRadialMetricSecondPartial_eq_zero
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
        cpmJet
        harmonicJet
    ).metricSecondPartial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .time
        .time
        .radial =
      0 := by
  cases angular <;> rfl

/--
The retained angular derivative of the perturbation connection kernel vanishes:

`∂ₐK[h]_{trt} = 0`.

Its three-term expansion is

`∂ₐ∂ₜh_{rt}
  + ∂ₐ∂ᵣh_{tt}
  - ∂ₐ∂ₜh_{tr}`,

and each term vanishes separately because the odd-parity CPM metric contains
neither an `rt`, `tt`, nor `tr` component.

No commutation of abstract partial derivatives, harmonic identity, or vacuum
equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeTimePerturbationKernelDerivative_eq_zero
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .radial
          .time =
      0 := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeTimePerturbationKernelDerivative_eq_threeMetricSecondPartialTerms
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularTimeDerivativeRadialTimeMetricSecondPartial_eq_zero
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularRadialDerivativeTimeTimeMetricSecondPartial_eq_zero
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularTimeDerivativeTimeRadialMetricSecondPartial_eq_zero
      cpmJet
      harmonicJet
      angular
  ]

  ring

/--
The inverse-metric `.time` summand in the retained angular-derivative
connection contraction vanishes.

It was reduced to the Schwarzschild inverse time-time component multiplying
the angular derivative of the perturbation connection kernel, and that kernel
derivative is zero.

No angular harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeTimeInverseMetricSummand_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .time =
      0 := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeTimeInverseMetricSummand_eq_perturbationKernelDerivativeTerm
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeTimePerturbationKernelDerivative_eq_zero
      cpmJet
      harmonicJet
      angular
  ]

  ring

/--
The inverse-metric `.radial` summand in the retained angular-derivative
connection contraction vanishes.

Every product-rule term contains one of the following off-diagonal factors:

* the angular derivative of `δgᵗʳ`;
* the value `δgᵗʳ`;
* the angular derivative of the Schwarzschild component `ḡᵗʳ`;
* the Schwarzschild component `ḡᵗʳ`.

All four factors vanish for the diagonal Schwarzschild background and the
odd-parity CPM metric.

No perturbation-kernel value, harmonic identity, or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeRadialInverseMetricSummand_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .radial =
      0 := by
  have hLinearizedInverseTimeRadialPartial :
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .radial =
        0 := by
    cases angular <;>
      simp [
        reggeWheelerAngularCoordinateToSpacetime,
        reggeWheelerOddParityLinearizedInverseMetricComponentPartial,
        reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
        reggeWheelerOddParityVacuumCPMMetricSecondJet,
        reggeWheelerOddParityVacuumCPMMetricFirstJet,
        reggeWheelerOddParityVacuumCPMMetricPartial,
        reggeWheelerOddParitySpacetimeMetricPerturbation
      ]

  have hLinearizedInverseTimeRadial :
      reggeWheelerOddParityLinearizedInverseMetricComponent
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          .time
          .radial =
        0 := by
    simp [
      reggeWheelerOddParityLinearizedInverseMetricComponent,
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerOddParitySpacetimeMetricPerturbation
    ]

  have hBackgroundInverseTimeRadialPartial :
      reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .radial =
        0 := by
    cases angular <;>
      simp [
        reggeWheelerAngularCoordinateToSpacetime,
        reggeWheelerSchwarzschildInverseMetricComponentPartial
      ]

  have hBackgroundInverseTimeRadial :
      reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .time
          .radial =
        0 := by
    simp [
      reggeWheelerSchwarzschildInverseMetricComponent
    ]

  rw [
    reggeWheelerOddParityLinearizedChristoffelSummandPartial,
    hLinearizedInverseTimeRadialPartial,
    hLinearizedInverseTimeRadial,
    hBackgroundInverseTimeRadialPartial,
    hBackgroundInverseTimeRadial
  ]

  ring

/--
The inverse-metric `.theta` summand in the retained angular-derivative
connection contraction expands into the four product-rule terms defining the
coordinate derivative of the linearized Christoffel summand.

No individual factor is simplified, and no CPM coefficient, harmonic identity,
or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeThetaInverseMetricSummand_eq_fourProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .theta =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .time
            .theta *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            .time
            .radial
            .theta +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .time
              .theta *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .radial
              .theta +
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .theta *
            reggeWheelerOddParityPerturbationConnectionKernel
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .time
              .radial
              .theta +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .theta *
            reggeWheelerOddParityPerturbationConnectionKernelPartial
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .radial
              .theta := by
  rfl

/--
The angular derivative of the Schwarzschild inverse time-theta component
vanishes:

`∂ₐ ḡᵗθ = 0`.

The Schwarzschild inverse metric is diagonal, so its time-theta component is
identically zero in both angular-coordinate cases.

No perturbation, harmonic identity, or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeBackgroundInverseTimeThetaPartial_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .theta =
      0 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerSchwarzschildInverseMetricComponentPartial
    ]

/--
The Schwarzschild inverse time-theta metric component vanishes:

`ḡᵗθ = 0`.

This is an off-diagonal component of the diagonal Schwarzschild inverse
metric.

No perturbation, coordinate derivative, harmonic identity, or vacuum equation
is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundInverseTimeTheta_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .time
          .theta =
      0 := by
  simp [
    reggeWheelerSchwarzschildInverseMetricComponent
  ]

/--
The inverse-metric `.theta` summand in the retained angular-derivative
connection contraction reduces to its first two product-rule terms.

The last two terms vanish because both the angular derivative and the value of
the Schwarzschild inverse time-theta component are zero.

No linearized inverse-metric factor, connection kernel, harmonic identity, or
vacuum equation is simplified.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeThetaInverseMetricSummand_eq_firstTwoProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .theta =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .time
            .theta *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            .time
            .radial
            .theta +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .time
              .theta *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .radial
              .theta := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeThetaInverseMetricSummand_eq_fourProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeBackgroundInverseTimeThetaPartial_eq_zero
      frame
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundInverseTimeTheta_eq_zero
      frame
  ]

  ring

/--
The angular derivative of the linearized inverse time-theta component reduces
to the CPM metric-partial contribution multiplied by the two diagonal
Schwarzschild inverse-metric factors:

`∂ₐδgᵗθ
  = -(ḡᵗᵗ · ∂ₐhₜθ · ḡθθ)`.

The angular derivatives of the background inverse time-time and theta-theta
components vanish, so only the derivative of the CPM perturbation component
remains.

The CPM metric partial is left explicit. No angular harmonic identity or
vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeLinearizedInverseTimeThetaPartial_eq_explicitCPMForm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .theta =
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            reggeWheelerOddParityVacuumCPMMetricPartial
              cpmJet.secondJet
              harmonicJet.firstJet
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .theta *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
      ) := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial,
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerSchwarzschildInverseMetricComponentPartial
    ]

/--
The undifferentiated linearized inverse time-theta component is the CPM metric
value multiplied by the two diagonal Schwarzschild inverse-metric factors:

`δgᵗθ = -(ḡᵗᵗ · hₜθ · ḡθθ)`.

The metric value is retained through the explicit CPM metric first jet. No
angular harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularLinearizedInverseTimeTheta_eq_explicitCPMForm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponent
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          .time
          .theta =
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            (
              reggeWheelerOddParityVacuumCPMMetricFirstJet
                cpmJet.secondJet
                harmonicJet.firstJet
            ).metricValue
              .time
              .theta *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
      ) := by
  rfl

/--
The inverse-metric `.theta` summand in the retained angular-derivative
connection contraction is expressed using the explicit CPM metric-partial and
metric-value forms of the two remaining linearized inverse-metric factors.

The Schwarzschild connection kernel and its angular derivative remain
unevaluated. No angular harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeThetaInverseMetricSummand_eq_explicitCPMForms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .theta =
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            reggeWheelerOddParityVacuumCPMMetricPartial
              cpmJet.secondJet
              harmonicJet.firstJet
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .theta *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
      ) *
        reggeWheelerSchwarzschildConnectionKernel
          frame
          .time
          .radial
          .theta +
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            (
              reggeWheelerOddParityVacuumCPMMetricFirstJet
                cpmJet.secondJet
                harmonicJet.firstJet
            ).metricValue
              .time
              .theta *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
      ) *
        reggeWheelerSchwarzschildConnectionKernelPartial
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .radial
          .theta := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeThetaInverseMetricSummand_eq_firstTwoProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeLinearizedInverseTimeThetaPartial_eq_explicitCPMForm
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularLinearizedInverseTimeTheta_eq_explicitCPMForm
      frame
      cpmJet
      harmonicJet
  ]

/--
The Schwarzschild background connection kernel with indices `(t,r,θ)`
vanishes:

`K̄_{trθ} = 0`.

All three metric-partial terms entering this kernel are off-diagonal
Schwarzschild metric components. No perturbation, harmonic identity, or vacuum
equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundConnectionKernelTimeRadialTheta_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildConnectionKernel
          frame
          .time
          .radial
          .theta =
      0 := by
  simp [
    reggeWheelerSchwarzschildConnectionKernel,
    reggeWheelerSchwarzschildMetricPartial
  ]

/--
The angular derivative of the Schwarzschild background connection kernel with
indices `(t,r,θ)` vanishes:

`∂ₐ K̄_{trθ} = 0`.

Each metric-second-partial contribution is an off-diagonal Schwarzschild
component. No perturbation, CPM metric value, harmonic identity, or vacuum
equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundConnectionKernelTimeRadialThetaAngularPartial_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildConnectionKernelPartial
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .radial
          .theta =
      0 := by
  cases angular <;>
    simp [
      reggeWheelerSchwarzschildConnectionKernelPartial,
      reggeWheelerSchwarzschildMetricSecondPartial
    ]

/--
The inverse-metric `.theta` summand in the retained angular-derivative
connection contraction vanishes.

Its explicit CPM form contains two terms:

* the CPM metric partial multiplied by `K̄_{trθ}`;
* the CPM metric value multiplied by `∂ₐK̄_{trθ}`.

Both Schwarzschild background-kernel factors have been proved zero. The CPM
metric partial and metric value remain unevaluated.

No angular harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeThetaInverseMetricSummand_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .theta =
      0 := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeThetaInverseMetricSummand_eq_explicitCPMForms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundConnectionKernelTimeRadialTheta_eq_zero
      frame,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundConnectionKernelTimeRadialThetaAngularPartial_eq_zero
      frame
      angular
  ]

  ring

/--
The inverse-metric `.phi` summand in the retained angular-derivative
connection contraction expands into the four product-rule terms defining the
coordinate derivative of the linearized Christoffel summand.

No individual factor is simplified, and no CPM coefficient, harmonic identity,
or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativePhiInverseMetricSummand_eq_fourProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .phi =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .time
            .phi *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            .time
            .radial
            .phi +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .time
              .phi *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .radial
              .phi +
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .phi *
            reggeWheelerOddParityPerturbationConnectionKernel
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .time
              .radial
              .phi +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .phi *
            reggeWheelerOddParityPerturbationConnectionKernelPartial
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .radial
              .phi := by
  rfl

/--
The angular derivative of the Schwarzschild inverse time-phi component
vanishes:

`∂ₐ ḡᵗφ = 0`.

The Schwarzschild inverse metric is diagonal, so its time-phi component is
identically zero for either angular derivative coordinate.

No perturbation, harmonic identity, or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeBackgroundInverseTimePhiPartial_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .phi =
      0 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerSchwarzschildInverseMetricComponentPartial
    ]

/--
The Schwarzschild inverse time-phi metric component vanishes:

`ḡᵗφ = 0`.

This is an off-diagonal component of the diagonal Schwarzschild inverse
metric.

No perturbation, coordinate derivative, harmonic identity, or vacuum equation
is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundInverseTimePhi_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .time
          .phi =
      0 := by
  simp [
    reggeWheelerSchwarzschildInverseMetricComponent
  ]

/--
The inverse-metric `.phi` summand in the retained angular-derivative
connection contraction reduces to its first two product-rule terms.

The last two terms vanish because both the angular derivative and the value of
the Schwarzschild inverse time-phi component are zero.

No linearized inverse-metric factor, connection kernel, harmonic identity, or
vacuum equation is simplified.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativePhiInverseMetricSummand_eq_firstTwoProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .phi =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .time
            .phi *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            .time
            .radial
            .phi +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .time
              .phi *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .radial
              .phi := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativePhiInverseMetricSummand_eq_fourProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeBackgroundInverseTimePhiPartial_eq_zero
      frame
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundInverseTimePhi_eq_zero
      frame
  ]

  ring

/--
The angular derivative of the linearized inverse time-phi component has two
remaining CPM product-rule terms:

`∂ₐδgᵗφ
  = -(
      ḡᵗᵗ · ∂ₐhₜφ · ḡφφ
      +
      ḡᵗᵗ · hₜφ · ∂ₐḡφφ
    )`.

The angular derivative of the background inverse time-time factor vanishes.
Unlike the corresponding time-theta calculation, the angular derivative of
the inverse phi-phi factor is retained because it is nonzero for the theta
coordinate derivative.

No angular harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeLinearizedInverseTimePhiPartial_eq_explicitCPMForm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .phi =
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            reggeWheelerOddParityVacuumCPMMetricPartial
              cpmJet.secondJet
              harmonicJet.firstJet
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .phi *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .phi
            .phi +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            (
              reggeWheelerOddParityVacuumCPMMetricFirstJet
                cpmJet.secondJet
                harmonicJet.firstJet
            ).metricValue
              .time
              .phi *
          reggeWheelerSchwarzschildInverseMetricComponentPartial
            frame
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .phi
            .phi
      ) := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial,
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerSchwarzschildInverseMetricComponentPartial
    ]

/--
The undifferentiated linearized inverse time-phi component is the CPM metric
value multiplied by the two diagonal Schwarzschild inverse-metric factors:

`δgᵗφ = -(ḡᵗᵗ · hₜφ · ḡφφ)`.

The CPM metric value remains explicit through the CPM metric first jet. No
angular derivative, harmonic identity, or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularLinearizedInverseTimePhi_eq_explicitCPMForm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponent
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          .time
          .phi =
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            (
              reggeWheelerOddParityVacuumCPMMetricFirstJet
                cpmJet.secondJet
                harmonicJet.firstJet
            ).metricValue
              .time
              .phi *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .phi
            .phi
      ) := by
  rfl

/--
The inverse-metric `.phi` summand in the retained angular-derivative
connection contraction is expressed using the corrected explicit CPM form of
the angular derivative of `δgᵗφ` and the explicit CPM value form of `δgᵗφ`.

The angular derivative of the background inverse phi-phi component remains
explicit. The Schwarzschild connection kernel and its angular derivative also
remain unevaluated.

No angular harmonic identity or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativePhiInverseMetricSummand_eq_explicitCPMForms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .phi =
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            reggeWheelerOddParityVacuumCPMMetricPartial
              cpmJet.secondJet
              harmonicJet.firstJet
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .phi *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .phi
            .phi +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            (
              reggeWheelerOddParityVacuumCPMMetricFirstJet
                cpmJet.secondJet
                harmonicJet.firstJet
            ).metricValue
              .time
              .phi *
          reggeWheelerSchwarzschildInverseMetricComponentPartial
            frame
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .phi
            .phi
      ) *
        reggeWheelerSchwarzschildConnectionKernel
          frame
          .time
          .radial
          .phi +
      -(
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .time
              .time *
            (
              reggeWheelerOddParityVacuumCPMMetricFirstJet
                cpmJet.secondJet
                harmonicJet.firstJet
            ).metricValue
              .time
              .phi *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .phi
            .phi
      ) *
        reggeWheelerSchwarzschildConnectionKernelPartial
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .radial
          .phi := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativePhiInverseMetricSummand_eq_firstTwoProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeLinearizedInverseTimePhiPartial_eq_explicitCPMForm
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularLinearizedInverseTimePhi_eq_explicitCPMForm
      frame
      cpmJet
      harmonicJet
  ]

/--
The Schwarzschild background connection kernel with indices `(t,r,φ)`
vanishes:

`K̄_{trφ} = 0`.

Every metric-partial contribution is an off-diagonal Schwarzschild component.
No perturbation, CPM metric value, harmonic identity, or vacuum equation is
used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundConnectionKernelTimeRadialPhi_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildConnectionKernel
          frame
          .time
          .radial
          .phi =
      0 := by
  simp [
    reggeWheelerSchwarzschildConnectionKernel,
    reggeWheelerSchwarzschildMetricPartial
  ]

/--
The angular derivative of the Schwarzschild background connection kernel with
indices `(t,r,φ)` vanishes:

`∂ₐ K̄_{trφ} = 0`.

Each metric-second-partial contribution is an off-diagonal Schwarzschild
component. The retained angular derivative of the inverse phi-phi component
is not simplified here.

No perturbation, CPM factor, harmonic identity, or vacuum equation is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundConnectionKernelTimeRadialPhiAngularPartial_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildConnectionKernelPartial
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .radial
          .phi =
      0 := by
  cases angular <;>
    simp [
      reggeWheelerSchwarzschildConnectionKernelPartial,
      reggeWheelerSchwarzschildMetricSecondPartial
    ]

/--
The inverse-metric `.phi` summand in the retained angular-derivative
connection contraction vanishes.

Its corrected explicit CPM form contains factors involving the angular
derivative of the inverse phi-phi background component, but every such
expression is multiplied by either `K̄_{trφ}` or `∂ₐK̄_{trφ}`. Both
background-kernel factors have been proved zero.

No CPM factor, inverse phi-phi derivative, angular harmonic identity, or vacuum
equation is simplified.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativePhiInverseMetricSummand_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .time
          .time
          .radial
          .phi =
      0 := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativePhiInverseMetricSummand_eq_explicitCPMForms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundConnectionKernelTimeRadialPhi_eq_zero
      frame,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundConnectionKernelTimeRadialPhiAngularPartial_eq_zero
      frame
      angular
  ]

  ring

/--
The retained angular derivative of the linearized connection contraction
vanishes:

`∂ₐ δΓᵗ_{tr} = 0`.

The contraction was expanded into the `.time`, `.radial`, `.theta`, and
`.phi` inverse-metric coordinate summands. Each of those four summands has
been proved zero independently.

No connection-product term, angular harmonic identity, vacuum equation, or
master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeConnectionTerm_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSpacetimeCoordinateContraction
          (fun inverseMetricContraction =>
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .time
              .time
              .radial
              inverseMetricContraction) =
      0 := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeConnectionTerm_eq_fourInverseMetricCoordinateSummands,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeTimeInverseMetricSummand_eq_zero,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeRadialInverseMetricSummand_eq_zero,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeThetaInverseMetricSummand_eq_zero,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativePhiInverseMetricSummand_eq_zero
  ]

  ring

/--
The principal time-coordinate contribution is exactly one-half of the
previously proved factored time-derivative connection term.

The retained angular-derivative connection contraction vanishes, so the
subtracted half of that contraction contributes zero.

No radial, theta, or phi principal-coordinate contribution, connection-product
term, angular harmonic identity, vacuum equation, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeTimeContribution_eq_halfFactoredVectorHarmonicCPMForm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) :
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular
          .time =
      (1 / 2 : ℝ) * (
        reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .time
            .time *
        (
          (
            reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative
                cpmJet -
              reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative
                cpmJet -
              reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative
                  cpmJet.secondJet *
                (2 / frame.background.radius)
          ) *
            reggeWheelerOddParityVectorHarmonicValue
              harmonicJet.firstJet.harmonic
              angular
        )
      ) := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeTimeContribution_eq_factoredCPMTimeTerm_sub_angularDerivativeConnectionTerm,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularAngularDerivativeConnectionTerm_eq_zero
  ]

  ring

/--
The four-coordinate principal-derivative expansion is rewritten only in its
time-coordinate summand.

The time contribution is replaced by the previously proved one-half factored
vector-harmonic CPM form. The radial, theta, and phi coordinate contributions
remain exactly as they occur in the original four-coordinate expansion.

No remaining principal-coordinate contribution, connection-product term,
angular harmonic identity, vacuum equation, or master residual is reduced.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivative_eq_halfFactoredTimeContribution_add_remainingCoordinateContributions
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) :
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivative
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular =
      ((1 / 2 : ℝ) * ( reggeWheelerSchwarzschildInverseMetricComponent frame .time .time * ( ( reggeWheelerOddParityVacuumCPMTimeCoefficientTimeRadialDerivative cpmJet - reggeWheelerOddParityVacuumCPMRadialCoefficientTimeTimeDerivative cpmJet - reggeWheelerOddParityVacuumCPMTimeCoefficientTimeDerivative cpmJet.secondJet * (2 / frame.background.radius) ) * reggeWheelerOddParityVectorHarmonicValue harmonicJet.firstJet.harmonic angular ) )) + prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution frame cpmJet harmonicJet hCompatible angular .radial + prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution frame cpmJet harmonicJet hCompatible angular .theta + prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution frame cpmJet harmonicJet hCompatible angular .phi := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivative_eq_fourCoordinateContributions,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeTimeContribution_eq_halfFactoredVectorHarmonicCPMForm
  ]

/--
The principal radial-coordinate contribution is unfolded to the defining
connection-derivative expression of its coordinate-contribution function.

Only the coordinate argument is specialized from `time` to `radial`. The
theta and phi principal-coordinate contributions are not changed, and no
connection-product, harmonic, vacuum, or master-residual reduction is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialContribution_eq_definingConnectionDerivativeTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) :
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
      frame
      cpmJet
      harmonicJet
      hCompatible
      angular
      .radial =
      (
        fun
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (_hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate)
    (contracted : ReggeWheelerSpacetimeCoordinate) =>
          reggeWheelerOddParityLinearizedChristoffelPartial
                  frame
                  (
                    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                      cpmJet
                      harmonicJet
                  )
                  contracted
                  contracted
                  (reggeWheelerAngularCoordinateToSpacetime angular)
                  .radial -
              reggeWheelerOddParityLinearizedChristoffelPartial
                frame
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                    cpmJet
                    harmonicJet
                )
                (reggeWheelerAngularCoordinateToSpacetime angular)
                contracted
                contracted
                .radial
      )
        frame
        cpmJet
        harmonicJet
        hCompatible
        angular
        .radial := by
  rfl

/--
The first connection-derivative contraction in the principal radial-coordinate
contribution expands into its four inverse-metric coordinate summands.

The exact contraction is

`∂ᵣ δΓʳ_{Ar}`,

represented by the linearized Christoffel partial with derivative and upper
indices both equal to `.radial`.

Only this first radial connection derivative is expanded. The second radial
connection derivative and the theta and phi principal-coordinate
contributions remain unchanged.

No connection-product, angular harmonic, vacuum, or master-residual reduction
is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeTerm_eq_fourInverseMetricCoordinateSummands
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSpacetimeCoordinateContraction
          (fun inverseMetricContraction =>
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .radial
              .radial
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              inverseMetricContraction) =
      reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time +
        reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial +
        reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .theta +
        reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .phi := by
  rfl

/--
The `.time` inverse-metric summand in the first radial connection derivative

`∂ᵣ δΓʳ_{Ar}`

expands into the four product-rule terms defining the derivative of the
linearized Christoffel summand.

No factor is simplified, and no CPM coefficient, harmonic identity, vacuum
equation, connection-product term, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeTimeInverseMetricSummand_eq_fourProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .radial
            .radial
            .time *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .radial
            .time +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .time *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              .radial
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .time +
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              .radial
              .radial
              .time *
            reggeWheelerOddParityPerturbationConnectionKernel
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .time +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .time *
            reggeWheelerOddParityPerturbationConnectionKernelPartial
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .radial
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .time := by
  rfl

/--
The radial derivative of the Schwarzschild inverse radial-time component
vanishes:

`∂ᵣ ḡʳᵗ = 0`.

The Schwarzschild inverse metric is diagonal, so the radial-time component is
identically zero before differentiation.

No perturbation, connection kernel, harmonic identity, vacuum equation, or
master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeBackgroundInverseRadialTimePartial_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          .radial
          .radial
          .time =
      0 := by
  simp [
    reggeWheelerSchwarzschildInverseMetricComponentPartial
  ]

/--
The Schwarzschild inverse radial-time metric component vanishes:

`ḡʳᵗ = 0`.

This is an off-diagonal component of the diagonal Schwarzschild inverse
metric.

No perturbation, coordinate derivative, connection kernel, harmonic identity,
vacuum equation, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeBackgroundInverseRadialTime_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .radial
          .time =
      0 := by
  simp [
    reggeWheelerSchwarzschildInverseMetricComponent
  ]

/--
The `.time` inverse-metric summand in the first radial connection derivative

`∂ᵣ δΓʳ_{Ar}`

reduces to its first two product-rule terms.

The third and fourth terms vanish because the radial derivative and the value
of the Schwarzschild inverse radial-time component are both zero.

No linearized inverse-metric factor, connection kernel, CPM coefficient,
harmonic identity, vacuum equation, connection-product term, or master
residual is simplified.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeTimeInverseMetricSummand_eq_firstTwoProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .radial
            .radial
            .time *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .radial
            .time +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .time *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              .radial
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .time := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeTimeInverseMetricSummand_eq_fourProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeBackgroundInverseRadialTimePartial_eq_zero
      frame,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeBackgroundInverseRadialTime_eq_zero
      frame
  ]

  ring

/--
The Schwarzschild background connection kernel with angular, radial, and time
indices vanishes:

`K̄_{Ar t} = 0`.

Every metric-partial contribution is an off-diagonal Schwarzschild component.
The radial derivative of this kernel is not simplified here.

No perturbation, linearized inverse-metric factor, harmonic identity, vacuum
equation, connection-product term, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeBackgroundConnectionKernelAngularRadialTime_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildConnectionKernel
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time =
      0 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerSchwarzschildConnectionKernel,
      reggeWheelerSchwarzschildMetricPartial
    ]

/--
The radial derivative of the Schwarzschild background connection kernel with
angular, radial, and time indices vanishes:

`∂ᵣ K̄_{Ar t} = 0`.

The result follows directly from the static diagonal Schwarzschild coordinate
definitions. Both linearized inverse-metric factors are retained unchanged.

No perturbation identity, spherical-harmonic identity, vacuum equation,
connection-product term, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeBackgroundConnectionKernelAngularRadialTimeRadialPartial_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildConnectionKernelPartial
          frame
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time =
      0 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerSchwarzschildConnectionKernelPartial,
      reggeWheelerSchwarzschildMetricSecondPartial
    ]

/--
The `.time` inverse-metric summand in the first radial connection derivative

`∂ᵣ δΓʳ_{Ar}`

vanishes.

After the previously proved two-term reduction, the first term contains
`K̄_{Ar t} = 0` and the second contains `∂ᵣ K̄_{Ar t} = 0`. The linearized
inverse-metric factors are not simplified.

No spherical-harmonic identity, vacuum equation, connection-product term, or
master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeTimeInverseMetricSummand_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .time =
      0 := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeTimeInverseMetricSummand_eq_firstTwoProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeBackgroundConnectionKernelAngularRadialTime_eq_zero
      frame
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeBackgroundConnectionKernelAngularRadialTimeRadialPartial_eq_zero
      frame
      angular
  ]

  ring

/--
The `.radial` inverse-metric summand in the first radial connection derivative

`∂ᵣ δΓʳ_{Ar}`

expands into the four product-rule terms defining the derivative of the
linearized Christoffel summand.

No factor is simplified, and no CPM coefficient, harmonic identity, vacuum
equation, connection-product term, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeRadialInverseMetricSummand_eq_fourProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .radial
            .radial
            .radial *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .radial
            .radial +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .radial *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              .radial
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .radial +
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              .radial
              .radial
              .radial *
            reggeWheelerOddParityPerturbationConnectionKernel
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .radial +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .radial *
            reggeWheelerOddParityPerturbationConnectionKernelPartial
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .radial
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .radial := by
  rfl

/--
The odd-parity CPM linearized inverse radial-radial component vanishes:

`δgʳʳ = 0`.

The CPM odd-parity metric perturbation has no radial-radial component. This
theorem concerns only the undifferentiated linearized inverse component; its
radial derivative is left for a separate theorem.

No connection kernel, spherical-harmonic eigenvalue, vacuum equation,
connection-product term, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeLinearizedInverseRadialRadial_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponent
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          .radial
          .radial =
      0 := by
  simp [
      reggeWheelerOddParityLinearizedInverseMetricComponent,
      reggeWheelerOddParityRWGaugeMetricComponentsOfMaster,
      reggeWheelerOddParityRWRadialCoefficientFromMaster,
      reggeWheelerOddParitySpacetimeMetricPerturbation,
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricComponents,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerOddParityVacuumCPMMetricSecondJet,
      reggeWheelerOddParityVacuumCPMRWMaster,
      reggeWheelerOddParityVacuumCPMTimeCoefficient,
      reggeWheelerSchwarzschildExteriorFactor,
      reggeWheelerSchwarzschildInverseMetricDiagonal
    ]

/--
The radial derivative of the odd-parity CPM linearized inverse radial-radial
component vanishes:

`∂ᵣ δgʳʳ = 0`.

The CPM odd-parity perturbation has no radial-radial metric component, so its
linearized inverse radial-radial component and its radial derivative both
vanish.

No background inverse-metric factor, connection kernel, spherical-harmonic
identity, vacuum equation, connection-product term, or master residual is
simplified.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeLinearizedInverseRadialRadialRadialPartial_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          .radial =
      0 := by
  simp [
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial,
      reggeWheelerOddParityRWGaugeMetricComponentsOfMaster,
      reggeWheelerOddParityRWRadialCoefficientFromMaster,
      reggeWheelerOddParitySpacetimeMetricPerturbation,
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricComponents,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerOddParityVacuumCPMMetricPartial,
      reggeWheelerOddParityVacuumCPMMetricSecondJet,
      reggeWheelerOddParityVacuumCPMRWMaster,
      reggeWheelerOddParityVacuumCPMTimeCoefficient,
      reggeWheelerSchwarzschildExteriorFactor,
      reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative,
      reggeWheelerSchwarzschildInverseMetricComponent,
      reggeWheelerSchwarzschildInverseMetricComponentPartial
    ]

/--
The `.radial` inverse-metric summand in the first radial connection derivative

`∂ᵣ δΓʳ_{Ar}`

reduces to its final two product-rule terms.

The first two terms vanish because the odd-parity CPM linearized inverse
radial-radial component and its radial derivative are both zero. The
Schwarzschild inverse radial-radial factors and both perturbation connection
kernels are retained unchanged.

No spherical-harmonic identity, vacuum equation, connection-product term, or
master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeRadialInverseMetricSummand_eq_lastTwoProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial =
      reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              .radial
              .radial
              .radial *
            reggeWheelerOddParityPerturbationConnectionKernel
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .radial +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .radial *
            reggeWheelerOddParityPerturbationConnectionKernelPartial
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .radial
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .radial := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeRadialInverseMetricSummand_eq_fourProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeLinearizedInverseRadialRadialRadialPartial_eq_zero
      frame
      cpmJet
      harmonicJet,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeLinearizedInverseRadialRadial_eq_zero
      frame
      cpmJet
      harmonicJet
  ]

  ring

/--
The odd-parity perturbation connection kernel with angular, radial, and radial
indices expands into its three defining metric-partial terms:

`Kδ_{Ar r}`.

Only the undifferentiated perturbation connection kernel in the first retained
term of the `.radial` inverse-metric summand is unfolded. Its radial derivative,
the Schwarzschild inverse radial-radial factors, and all remaining coordinate
summands are unchanged.

No spherical-harmonic identity, vacuum equation, connection-product term, or
master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadial_eq_threeMetricPartialTerms
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernel
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial =
      (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationFirstJet)
    (lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricPartial lowerLeft lowerRight contraction +
              jet.metricPartial lowerRight lowerLeft contraction -
              jet.metricPartial contraction lowerLeft lowerRight
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        ).firstJet
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial := by
  rfl

/--
The radial derivative of the odd-parity perturbation connection kernel with
angular, radial, and radial indices expands into its three defining
metric-second-partial terms:

`∂ᵣ Kδ_{Ar r}`.

Only this perturbation-kernel radial derivative in the second retained term of
the `.radial` inverse-metric summand is unfolded. The undifferentiated kernel,
the Schwarzschild inverse radial-radial factors, and all remaining coordinate
summands are unchanged.

No spherical-harmonic identity, vacuum equation, connection-product term, or
master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartial_eq_threeMetricSecondPartialTerms
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial =
      (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricSecondPartial
                derivative lowerLeft lowerRight contraction +
              jet.metricSecondPartial
                derivative lowerRight lowerLeft contraction -
              jet.metricSecondPartial
                derivative contraction lowerLeft lowerRight
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial := by
  rfl

/--
The unique defining metric-second-partial term of
`∂ᵣ Kδ_{Ar r}`.

This term vanishes definitionally because its odd-parity perturbation
component is radial-radial. The two metric-second-partial terms involving the
angular-radial perturbation component are left unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartialRadialRadialMetricTerm_eq_zero
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricSecondPartial
                derivative lowerLeft lowerRight contraction
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial =
      0 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerOddParityRWGaugeMetricComponentsOfMaster,
      reggeWheelerOddParityRWRadialCoefficientFromMaster,
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricComponents,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerOddParityVacuumCPMMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricSecondPartial,
      reggeWheelerOddParityVacuumCPMRWMaster,
      reggeWheelerOddParityVacuumCPMTimeCoefficient,
      reggeWheelerSchwarzschildExteriorFactor
    ]

/--
The radial derivative of the odd-parity perturbation connection kernel with
angular, radial, and radial indices reduces to its two angular-radial
metric-second-partial terms:

`∂ᵣ Kδ_{Ar r}`.

The first defining term vanishes because it differentiates the absent
odd-parity radial-radial perturbation component. The remaining two terms are
preserved exactly and are not yet combined or placed into explicit CPM form.

No spherical-harmonic identity, vacuum equation, connection-product term, or
master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartial_eq_twoAngularRadialMetricSecondPartialTerms
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial =
      (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricSecondPartial
                derivative lowerRight lowerLeft contraction
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
      - (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricSecondPartial
                derivative contraction lowerLeft lowerRight
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartial_eq_threeMetricSecondPartialTerms
      cpmJet
      harmonicJet
      angular
  ]

  change
    (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricSecondPartial
                derivative lowerLeft lowerRight contraction
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
      + (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricSecondPartial
                derivative lowerRight lowerLeft contraction
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
      - (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricSecondPartial
                derivative contraction lowerLeft lowerRight
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial =
      (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricSecondPartial
                derivative lowerRight lowerLeft contraction
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
      - (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricSecondPartial
                derivative contraction lowerLeft lowerRight
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial

  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartialRadialRadialMetricTerm_eq_zero
      cpmJet
      harmonicJet
      angular
  ]

  ring

/--
The first retained angular-radial metric-second-partial term in

`∂ᵣ Kδ_{Ar r}`

is exactly the CPM metric-second-partial entry with derivative indices
radial, radial, radial and angular perturbation index `angular`.

This is the structural endpoint exposed by Lean before expanding the CPM
entry into coefficient and vector-harmonic fields. The entry's explicit
theta and phi formulas remain separate future obligations.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartialFirstAngularRadialMetricTerm_eq_CPMMetricSecondPartialEntry
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricSecondPartial
                derivative lowerRight lowerLeft contraction
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial =
      reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
        cpmJet
        harmonicJet
        .radial
        .radial
        .radial
        angular := by
  cases angular <;>
    rfl

/--
The theta branch of the CPM metric-second-partial entry with three radial
derivative indices is equal to its exact defining expression:

`CPMSecondPartialEntry cpmJet harmonicJet r r r θ`.

This theorem opens only the entry definition. It does not yet simplify the
result into a CPM coefficient multiplied by a theta vector-harmonic
component. The phi branch remains unchanged.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeCPMMetricSecondPartialEntryRadialRadialRadialTheta_eq_definingForm
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
          cpmJet
          harmonicJet
          .radial
          .radial
          .radial
          .theta =
      (
        fun
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (derivativeOuter derivativeInner coefficientCoordinate :
      ReggeWheelerSpacetimeCoordinate)
    (angularCoordinate : ReggeWheelerAngularCoordinate) =>
          match derivativeOuter, derivativeInner with
            | .time, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .time .time coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .time, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .time .radial coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .radial, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .radial .time coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .radial, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .radial .radial coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .time, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .theta, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .time, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .phi, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .radial, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .theta, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .radial, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .phi, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .theta, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .theta .theta angularCoordinate

            | .theta, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .theta .phi angularCoordinate

            | .phi, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .phi .theta angularCoordinate

            | .phi, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .phi .phi angularCoordinate
      )
        cpmJet
        harmonicJet
        .radial
        .radial
        .radial
        .theta := by
  rfl

/--
The radial-radial-radial theta CPM metric-second-partial entry is its single
defining term containing the CPM metric-coefficient second partial and the
theta vector-harmonic value.

The defining-form theorem already closed the generated goal. The prior
failure came only from executing a second `simp` tactic after no goals
remained.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCPMMetricSecondPartialEntryRadialRadialRadialTheta_eq_coefficientSecondPartialVectorHarmonicValueForm
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
          cpmJet
          harmonicJet
          .radial
          .radial
          .radial
          .theta =
      (
        fun
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (derivativeOuter derivativeInner coefficientCoordinate :
      ReggeWheelerSpacetimeCoordinate)
    (angularCoordinate : ReggeWheelerAngularCoordinate) =>
          match derivativeOuter, derivativeInner with
            | .time, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .time .time coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .time, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .time .radial coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .radial, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .radial .time coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .radial, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .radial .radial coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .time, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .theta, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .time, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .phi, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .radial, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .theta, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .radial, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .phi, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .theta, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .theta .theta angularCoordinate

            | .theta, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .theta .phi angularCoordinate

            | .phi, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .phi .theta angularCoordinate

            | .phi, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .phi .phi angularCoordinate
      )
        cpmJet
        harmonicJet
        .radial
        .radial
        .radial
        .theta := by
  exact
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeCPMMetricSecondPartialEntryRadialRadialRadialTheta_eq_definingForm
      cpmJet
      harmonicJet

/--
The phi branch of the CPM metric-second-partial entry with three radial
derivative indices is equal to its exact defining expression:

`CPMSecondPartialEntry cpmJet harmonicJet r r r φ`.

Only the entry definition is opened. No simplification of the resulting phi
coefficient and vector-harmonic expression is performed here.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeCPMMetricSecondPartialEntryRadialRadialRadialPhi_eq_definingForm
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
          cpmJet
          harmonicJet
          .radial
          .radial
          .radial
          .phi =
      (
        fun
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (derivativeOuter derivativeInner coefficientCoordinate :
      ReggeWheelerSpacetimeCoordinate)
    (angularCoordinate : ReggeWheelerAngularCoordinate) =>
          match derivativeOuter, derivativeInner with
            | .time, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .time .time coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .time, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .time .radial coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .radial, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .radial .time coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .radial, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .radial .radial coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .time, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .theta, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .time, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .phi, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .radial, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .theta, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .radial, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .phi, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .theta, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .theta .theta angularCoordinate

            | .theta, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .theta .phi angularCoordinate

            | .phi, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .phi .theta angularCoordinate

            | .phi, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .phi .phi angularCoordinate
      )
        cpmJet
        harmonicJet
        .radial
        .radial
        .radial
        .phi := by
  rfl

/--
The radial-radial-radial phi CPM metric-second-partial entry is its single
defining term containing the CPM metric-coefficient second partial and the
phi vector-harmonic value.

This records the exact defining expression already proved by the phi
defining-form theorem. No additional simplification or angular identity is
introduced.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCPMMetricSecondPartialEntryRadialRadialRadialPhi_eq_coefficientSecondPartialVectorHarmonicValueForm
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
          cpmJet
          harmonicJet
          .radial
          .radial
          .radial
          .phi =
      (
        fun
    (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (derivativeOuter derivativeInner coefficientCoordinate :
      ReggeWheelerSpacetimeCoordinate)
    (angularCoordinate : ReggeWheelerAngularCoordinate) =>
          match derivativeOuter, derivativeInner with
            | .time, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .time .time coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .time, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .time .radial coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .radial, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .radial .time coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .radial, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                    jet .radial .radial coefficientCoordinate *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic angularCoordinate

            | .time, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .theta, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .time, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .phi, .time =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .time coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .radial, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .theta, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .theta angularCoordinate

            | .radial, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .phi, .radial =>
                reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                    jet.secondJet .radial coefficientCoordinate *
                  harmonicJet.firstJet.vectorCoordinatePartial
                    .phi angularCoordinate

            | .theta, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .theta .theta angularCoordinate

            | .theta, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .theta .phi angularCoordinate

            | .phi, .theta =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .phi .theta angularCoordinate

            | .phi, .phi =>
                reggeWheelerOddParityVacuumCPMMetricCoefficient
                    jet.secondJet.firstJet coefficientCoordinate *
                  harmonicJet.vectorCoordinateSecondPartial
                    .phi .phi angularCoordinate
      )
        cpmJet
        harmonicJet
        .radial
        .radial
        .radial
        .phi := by
  exact
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeCPMMetricSecondPartialEntryRadialRadialRadialPhi_eq_definingForm
      cpmJet
      harmonicJet

/--
The first retained angular-radial metric-second-partial term in

`∂ᵣ Kδ_{Ar r}`

has a single angular-case formula. Its theta branch is the proved CPM
metric-coefficient second-partial times theta vector-harmonic value, and its
phi branch is the corresponding proved phi expression.

This theorem only composes the existing first-term-to-CPM-entry bridge with
the separately proved theta and phi CPM-entry formulas.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartialFirstAngularRadialMetricTerm_eq_CPMCoefficientSecondPartialVectorHarmonicValueAngularCases
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (
        fun
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) =>
          jet.metricSecondPartial
                derivative lowerRight lowerLeft contraction
      )
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial =
      match angular with
      | .theta =>
          (
                  fun
              (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
              (harmonicJet :
                ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
              (derivativeOuter derivativeInner coefficientCoordinate :
                ReggeWheelerSpacetimeCoordinate)
              (angularCoordinate : ReggeWheelerAngularCoordinate) =>
                    match derivativeOuter, derivativeInner with
                      | .time, .time =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                              jet .time .time coefficientCoordinate *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic angularCoordinate

                      | .time, .radial =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                              jet .time .radial coefficientCoordinate *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic angularCoordinate

                      | .radial, .time =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                              jet .radial .time coefficientCoordinate *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic angularCoordinate

                      | .radial, .radial =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                              jet .radial .radial coefficientCoordinate *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic angularCoordinate

                      | .time, .theta =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .time coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .theta angularCoordinate

                      | .theta, .time =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .time coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .theta angularCoordinate

                      | .time, .phi =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .time coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .phi angularCoordinate

                      | .phi, .time =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .time coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .phi angularCoordinate

                      | .radial, .theta =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .radial coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .theta angularCoordinate

                      | .theta, .radial =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .radial coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .theta angularCoordinate

                      | .radial, .phi =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .radial coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .phi angularCoordinate

                      | .phi, .radial =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .radial coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .phi angularCoordinate

                      | .theta, .theta =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficient
                              jet.secondJet.firstJet coefficientCoordinate *
                            harmonicJet.vectorCoordinateSecondPartial
                              .theta .theta angularCoordinate

                      | .theta, .phi =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficient
                              jet.secondJet.firstJet coefficientCoordinate *
                            harmonicJet.vectorCoordinateSecondPartial
                              .theta .phi angularCoordinate

                      | .phi, .theta =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficient
                              jet.secondJet.firstJet coefficientCoordinate *
                            harmonicJet.vectorCoordinateSecondPartial
                              .phi .theta angularCoordinate

                      | .phi, .phi =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficient
                              jet.secondJet.firstJet coefficientCoordinate *
                            harmonicJet.vectorCoordinateSecondPartial
                              .phi .phi angularCoordinate
                )
                  cpmJet
                  harmonicJet
                  .radial
                  .radial
                  .radial
                  .theta
      | .phi =>
          (
                  fun
              (jet : ReggeWheelerOddParityVacuumCPMThirdJet)
              (harmonicJet :
                ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
              (derivativeOuter derivativeInner coefficientCoordinate :
                ReggeWheelerSpacetimeCoordinate)
              (angularCoordinate : ReggeWheelerAngularCoordinate) =>
                    match derivativeOuter, derivativeInner with
                      | .time, .time =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                              jet .time .time coefficientCoordinate *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic angularCoordinate

                      | .time, .radial =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                              jet .time .radial coefficientCoordinate *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic angularCoordinate

                      | .radial, .time =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                              jet .radial .time coefficientCoordinate *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic angularCoordinate

                      | .radial, .radial =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientSecondPartial
                              jet .radial .radial coefficientCoordinate *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic angularCoordinate

                      | .time, .theta =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .time coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .theta angularCoordinate

                      | .theta, .time =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .time coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .theta angularCoordinate

                      | .time, .phi =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .time coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .phi angularCoordinate

                      | .phi, .time =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .time coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .phi angularCoordinate

                      | .radial, .theta =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .radial coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .theta angularCoordinate

                      | .theta, .radial =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .radial coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .theta angularCoordinate

                      | .radial, .phi =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .radial coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .phi angularCoordinate

                      | .phi, .radial =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficientPartial
                              jet.secondJet .radial coefficientCoordinate *
                            harmonicJet.firstJet.vectorCoordinatePartial
                              .phi angularCoordinate

                      | .theta, .theta =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficient
                              jet.secondJet.firstJet coefficientCoordinate *
                            harmonicJet.vectorCoordinateSecondPartial
                              .theta .theta angularCoordinate

                      | .theta, .phi =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficient
                              jet.secondJet.firstJet coefficientCoordinate *
                            harmonicJet.vectorCoordinateSecondPartial
                              .theta .phi angularCoordinate

                      | .phi, .theta =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficient
                              jet.secondJet.firstJet coefficientCoordinate *
                            harmonicJet.vectorCoordinateSecondPartial
                              .phi .theta angularCoordinate

                      | .phi, .phi =>
                          reggeWheelerOddParityVacuumCPMMetricCoefficient
                              jet.secondJet.firstJet coefficientCoordinate *
                            harmonicJet.vectorCoordinateSecondPartial
                              .phi .phi angularCoordinate
                )
                  cpmJet
                  harmonicJet
                  .radial
                  .radial
                  .radial
                  .phi := by
  cases angular with
  | theta =>
      exact
        Eq.trans
          (
            prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartialFirstAngularRadialMetricTerm_eq_CPMMetricSecondPartialEntry
              cpmJet
              harmonicJet
              .theta
          )
          (
            prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCPMMetricSecondPartialEntryRadialRadialRadialTheta_eq_coefficientSecondPartialVectorHarmonicValueForm
              cpmJet
              harmonicJet
          )
  | phi =>
      exact
        Eq.trans
          (
            prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartialFirstAngularRadialMetricTerm_eq_CPMMetricSecondPartialEntry
              cpmJet
              harmonicJet
              .phi
          )
          (
            prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCPMMetricSecondPartialEntryRadialRadialRadialPhi_eq_coefficientSecondPartialVectorHarmonicValueForm
              cpmJet
              harmonicJet
          )

/--
The second retained angular-radial metric-second-partial term in

`∂ᵣ Kδ_{Ar r}`

is the negative of the same radial-radial-radial CPM
metric-second-partial entry that appears in the first retained term.

This theorem identifies only the signed structural entry. It does not yet
combine the first and second retained terms or claim their cancellation.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartialSecondAngularRadialMetricTerm_eq_negativeCPMMetricSecondPartialEntry
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    -(
  (
          fun
      (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
      (derivative lowerLeft lowerRight contraction :
        ReggeWheelerSpacetimeCoordinate) =>
            jet.metricSecondPartial
                  derivative contraction lowerLeft lowerRight
        )
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial
) =
      -(
        reggeWheelerOddParityVacuumCPMMetricSecondPartialEntry
          cpmJet
          harmonicJet
          .radial
          .radial
          .radial
          angular
      ) := by
  cases angular <;>
    rfl

/--
The radial derivative of the odd-parity CPM perturbation connection kernel

`∂ᵣ Kδ_{Ar r}`

vanishes because its two retained angular-radial metric-second-partial
contributions are the same CPM metric-second-partial entry with opposite
signs.

The previous script failed only because it required a literal textual
occurrence of the signed second-term expression inside the two-term theorem.
Here Lean performs the subtraction-to-additive-negation normalization and
the theorem matching directly.

The undifferentiated kernel, background inverse-metric factors, and all other
coordinate contributions remain unreduced.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartial_eq_zero
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial =
      0 := by
  simpa only [
    sub_eq_add_neg,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartialFirstAngularRadialMetricTerm_eq_CPMMetricSecondPartialEntry,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartialSecondAngularRadialMetricTerm_eq_negativeCPMMetricSecondPartialEntry,
    add_neg_cancel
  ] using
    (
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartial_eq_twoAngularRadialMetricSecondPartialTerms
        cpmJet
        harmonicJet
        angular
    )

/--
The undifferentiated odd-parity CPM perturbation connection kernel

`Kδ_{Ar r}`

vanishes after expanding it into its three metric-partial terms. The
radial-radial perturbation component is zero, and the two remaining
angular-radial metric-partial expressions cancel.

The earlier `rfl` attempt was too strong: this equality requires unfolding
the CPM first-jet metric-partial definitions after applying the established
three-term expansion.

The background inverse-metric factors and all other coordinate
contributions remain unreduced.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadial_eq_zero
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernel
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial =
      0 := by
  simpa [
    reggeWheelerAngularCoordinateToSpacetime,
    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
    reggeWheelerOddParityVacuumCPMMetricFirstJet,
    reggeWheelerOddParityVacuumCPMMetricPartial,
    reggeWheelerOddParityVacuumCPMMetricComponents,
    reggeWheelerOddParitySpacetimeMetricPerturbation,
    reggeWheelerOddParityRWGaugeMetricComponentsOfMaster
  ] using
    (
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadial_eq_threeMetricPartialTerms
        cpmJet
        harmonicJet
        angular
    )

/--
The radial inverse-metric summand in the first radial connection
contraction vanishes.

Its established last-two-product-rule expression consists of:

* the radial derivative of the background inverse radial-radial component
  multiplied by `Kδ_{Ar r}`; and
* the background inverse radial-radial component multiplied by
  `∂ᵣ Kδ_{Ar r}`.

Both perturbation-kernel factors are zero by the two preceding theorems.
No explicit evaluation of either background inverse-metric factor is
required.

The theta and phi inverse-metric summands, the second radial connection
derivative, and all remaining coordinate contributions stay open.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeRadialInverseMetricSummand_eq_zero

    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial =
      0 := by
  simpa only [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadial_eq_zero,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePerturbationConnectionKernelAngularRadialRadialRadialPartial_eq_zero,
    mul_zero,
    zero_mul,
    add_zero,
    zero_add,
    sub_zero,
    zero_sub,
    neg_zero
  ] using
    (
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeRadialInverseMetricSummand_eq_lastTwoProductRuleTerms
        (frame := frame)
        (cpmJet := cpmJet)
        (harmonicJet := harmonicJet)
        (angular := angular)
    )

/--
The theta inverse-metric summand in the first radial connection derivative
expands into its four radial product-rule terms.

This is the theta-coordinate specialization of the existing compiled
time-coordinate product-rule identity. No term is simplified here.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummand_eq_fourProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .theta =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .radial
            .radial
            .theta *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .radial
            .theta +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .theta *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              .radial
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .theta +
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              .radial
              .radial
              .theta *
            reggeWheelerOddParityPerturbationConnectionKernel
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .theta +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .theta *
            reggeWheelerOddParityPerturbationConnectionKernelPartial
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .radial
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .theta := by
  rfl

/--
The radial derivative of the background inverse radial-theta factor in the
theta product-rule expansion is zero.

This theorem isolates exactly the left factor of the third product-rule
term. Its additional explicit CPM and angular arguments are retained only
to match the source theorem's binder surface.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundInverseMetricRadialPartialFactor_eq_zero

    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (let _ := angular; let _ := cpmJet; let _ := harmonicJet;
      reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              .radial
              .radial
              .theta =
      0)
:= by
  rfl

/--
The background inverse radial-theta value factor in the theta product-rule
expansion is zero.

This theorem isolates exactly the left factor of the fourth product-rule
term. Its additional explicit CPM and angular arguments are retained only
to match the source theorem's binder surface.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundInverseMetricValueFactor_eq_zero

    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (let _ := angular; let _ := cpmJet; let _ := harmonicJet;
      reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .theta =
      0)
:= by
  rfl

/--
The theta inverse-metric summand in the first radial connection derivative
reduces from four product-rule terms to its first two terms.

The two zero lemmas have explicit arguments not determined by their
left-hand sides. They are therefore applied explicitly with `rw` before
the remaining zero products are simplified.

The two retained terms are not reduced.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummand_eq_firstTwoProductRuleTerms

    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .theta =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .radial
            .radial
            .theta *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .radial
            .theta
      + reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .theta *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              .radial
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .theta := by
  have h :=
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummand_eq_fourProductRuleTerms
        (frame := frame)
        (cpmJet := cpmJet)
        (harmonicJet := harmonicJet)
        (angular := angular)
  rw [
    (
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundInverseMetricRadialPartialFactor_eq_zero
          (frame := frame)
          (cpmJet := cpmJet)
          (harmonicJet := harmonicJet)
          (angular := angular)
    ),
    (
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundInverseMetricValueFactor_eq_zero
          (frame := frame)
          (cpmJet := cpmJet)
          (harmonicJet := harmonicJet)
          (angular := angular)
    )
  ] at h
  simpa only [
    zero_mul,
    mul_zero,
    add_zero,
    zero_add,
    sub_zero,
    zero_sub,
    neg_zero
  ] using h

/--
The background connection-kernel factor in the theta inverse-metric
summand vanishes when the free angular index is phi.

This reuses the existing target theorem selected by direct Lean
elaboration against the exact value factor.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundConnectionKernelPhiAngularFactor_eq_zero
(frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
(cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
(harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    (let _ := cpmJet; let _ := harmonicJet;
      reggeWheelerSchwarzschildConnectionKernel
            frame
            (reggeWheelerAngularCoordinateToSpacetime ReggeWheelerAngularCoordinate.phi)
            .radial
            .theta =
      0)
:= by
  simpa [
    reggeWheelerAngularCoordinateToSpacetime
  ] using
    (
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundConnectionKernelTimeRadialPhi_eq_zero
        (frame := frame)
    )

/--
The radial partial of the background connection-kernel factor in the theta
inverse-metric summand vanishes when the free angular index is phi.

The earlier broad dependency closure admitted unrelated short local names.
This proof uses only the exact Regge-Wheeler coordinate map,
connection-kernel-partial definition, and Schwarzschild metric-second-partial
definition identified by Lean.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundConnectionKernelRadialPartialPhiAngularFactor_eq_zero
(frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
(cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
(harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    (let _ := cpmJet; let _ := harmonicJet;
      reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              .radial
              (reggeWheelerAngularCoordinateToSpacetime ReggeWheelerAngularCoordinate.phi)
              .radial
              .theta =
      0)
:= by
  simp [
    reggeWheelerAngularCoordinateToSpacetime,
    reggeWheelerSchwarzschildConnectionKernelPartial,
    reggeWheelerSchwarzschildMetricSecondPartial
  ]

/--
The phi-angular branch of the theta inverse-metric summand in the first
radial connection derivative is zero.

Only the established first-two-term reduction and the two exact
background-kernel zero results are used. The theta-angular branch and the
separate phi inverse-metric summand remain open.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummandPhiAngularBranch_eq_zero
(frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
(cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
(harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime ReggeWheelerAngularCoordinate.phi)
          .radial
          .theta =
      0 := by
  have h :=
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummand_eq_firstTwoProductRuleTerms
        (frame := frame)
        (cpmJet := cpmJet)
        (harmonicJet := harmonicJet)
        (angular := ReggeWheelerAngularCoordinate.phi)
  rw [
    (
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundConnectionKernelPhiAngularFactor_eq_zero
          (frame := frame)
          (cpmJet := cpmJet)
          (harmonicJet := harmonicJet)
    ),
    (
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundConnectionKernelRadialPartialPhiAngularFactor_eq_zero
          (frame := frame)
          (cpmJet := cpmJet)
          (harmonicJet := harmonicJet)
    )
  ] at h
  simpa only [
    mul_zero,
    zero_mul,
    add_zero,
    zero_add,
    sub_zero,
    zero_sub,
    neg_zero
  ] using h

/--
The undifferentiated Schwarzschild connection-kernel factor in the
theta inverse-metric summand is evaluated for the theta-angular branch.

The source theorem's angular-coordinate binders and its explicit
right-hand side are both specialized to theta. Neither linearized-inverse
factor nor the radial partial of the background kernel is reduced here.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundConnectionKernelThetaAngularFactor_eq_compiledSchwarzschildForm
(frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
(cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
(harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    (let _ := cpmJet; let _ := harmonicJet;
      reggeWheelerSchwarzschildConnectionKernel
            frame
            (reggeWheelerAngularCoordinateToSpacetime ReggeWheelerAngularCoordinate.theta)
            .radial
            .theta =
      match ReggeWheelerAngularCoordinate.theta with
      | .theta => 2 * frame.background.radius
      | .phi => 0)
:= by
  simpa [
    reggeWheelerAngularCoordinateToSpacetime
  ] using
    (
prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularBackgroundThetaKernel_eq
        (frame := frame)
        (angular := ReggeWheelerAngularCoordinate.theta)
    )

/--
The radial partial of the Schwarzschild connection-kernel factor in the
theta inverse-metric summand equals two in the theta-angular branch.

This is exactly the radial derivative of the previously established
`2 * frame.background.radius` kernel value. Both linearized-inverse
factors remain unreduced.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundConnectionKernelRadialPartialThetaAngularFactor_eq_two
(frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
(cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
(harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    (let _ := cpmJet; let _ := harmonicJet;
      reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              .radial
              (reggeWheelerAngularCoordinateToSpacetime ReggeWheelerAngularCoordinate.theta)
              .radial
              .theta =
      2)
:= by
  simp [
    reggeWheelerAngularCoordinateToSpacetime,
    reggeWheelerSchwarzschildConnectionKernelPartial,
    reggeWheelerSchwarzschildMetricSecondPartial
  ]

/--
The theta-angular branch of the first radial theta inverse-metric summand
has its two Schwarzschild background factors substituted explicitly.

The undifferentiated kernel contributes
`2 * frame.background.radius`, and its radial partial contributes `2`.
Both linearized-inverse factors are retained exactly as they occur in the
established two-term product-rule reduction.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummandThetaAngularBranch_eq_explicitBackgroundFactors
(frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
(cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
(harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          .radial
          .radial
          (reggeWheelerAngularCoordinateToSpacetime ReggeWheelerAngularCoordinate.theta)
          .radial
          .theta =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .radial
            .radial
            .theta * (2 * frame.background.radius)
      + reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .theta * 2 := by
  have h :=
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummand_eq_firstTwoProductRuleTerms
        (frame := frame)
        (cpmJet := cpmJet)
        (harmonicJet := harmonicJet)
        (angular := ReggeWheelerAngularCoordinate.theta)
  rw [
    (
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundConnectionKernelThetaAngularFactor_eq_compiledSchwarzschildForm
          (frame := frame)
          (cpmJet := cpmJet)
          (harmonicJet := harmonicJet)
    ),
    (
      prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaBackgroundConnectionKernelRadialPartialThetaAngularFactor_eq_two
          (frame := frame)
          (cpmJet := cpmJet)
          (harmonicJet := harmonicJet)
    )
  ] at h
  simpa only [] using h

/--
The radial derivative of the radial-theta linearized inverse-metric
component is expanded into its three defining product-rule terms.

This is only the structural specialization of
`reggeWheelerOddParityLinearizedInverseMetricComponentPartial` at
derivative `.radial`, upper index `.radial`, and contraction index
`.theta`. No CPM coefficient or harmonic entry is simplified here.

The undifferentiated radial-theta linearized-inverse factor, the entire
phi inverse-metric summand, and all later Ricci contributions remain
unchanged.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaLinearizedInverseMetricRadialPartialFactor_eq_threeProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        .theta =
      -(
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              .radial
              .radial
              .radial *
            ReggeWheelerOddParityMetricPerturbationFirstJet.metricValue
              (
                ReggeWheelerOddParityMetricPerturbationSecondJet.firstJet
                  (
                    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                      cpmJet
                      harmonicJet
                  )
              )
              .radial
              .theta *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
        +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .radial *
            ReggeWheelerOddParityMetricPerturbationFirstJet.metricPartial
              (
                ReggeWheelerOddParityMetricPerturbationSecondJet.firstJet
                  (
                    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                      cpmJet
                      harmonicJet
                  )
              )
              .radial
              .radial
              .theta *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
        +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .radial *
            ReggeWheelerOddParityMetricPerturbationFirstJet.metricValue
              (
                ReggeWheelerOddParityMetricPerturbationSecondJet.firstJet
                  (
                    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                      cpmJet
                      harmonicJet
                  )
              )
              .radial
              .theta *
          reggeWheelerSchwarzschildInverseMetricComponentPartial
            frame
            .radial
            .theta
            .theta
      ) := by
  rfl

/--
The three defining product-rule terms for the radial derivative of the
radial-theta linearized inverse-metric component are rewritten with their
direct CPM metric-value and metric-partial entries.

Every Schwarzschild inverse-metric factor is retained explicitly.
The CPM radial coefficient and vector-harmonic value inside these entries
are not reduced here.

The undifferentiated radial-theta linearized-inverse factor, the complete
phi inverse-metric summand, and all later Ricci contributions remain
unchanged.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaLinearizedInverseMetricRadialPartialFactor_eq_threeProductRuleTermsWithDirectCPMMetricEntries
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        .theta =
      -(
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              .radial
              .radial
              .radial *
            (
              reggeWheelerOddParityVacuumCPMMetricFirstJet
                cpmJet.secondJet
                harmonicJet.firstJet
            ).metricValue
              .radial
              .theta *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
        +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .radial *
            reggeWheelerOddParityVacuumCPMMetricPartial
              cpmJet.secondJet
              harmonicJet.firstJet
              .radial
              .radial
              .theta *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
        +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .radial *
            (
              reggeWheelerOddParityVacuumCPMMetricFirstJet
                cpmJet.secondJet
                harmonicJet.firstJet
            ).metricValue
              .radial
              .theta *
          reggeWheelerSchwarzschildInverseMetricComponentPartial
            frame
            .radial
            .theta
            .theta
      ) := by
  rfl

/--
The direct CPM radial-theta metric-value entry is identified with the
corresponding component of the reconstructed odd-parity spacetime metric
perturbation.

This is obtained by applying the compiled whole-function metric-value
identity at the radial and theta coordinates. The spacetime perturbation
component is not yet reduced to a radial coefficient times a vector
harmonic.

The radial-radial-theta metric-partial entry, every Schwarzschild
inverse-metric factor, the undifferentiated radial-theta
linearized-inverse factor, and the complete phi inverse-metric summand
remain unchanged.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaCPMMetricValueRadialTheta_eq_spacetimeMetricPerturbationComponent
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    (let _ := frame;
      (
      reggeWheelerOddParityVacuumCPMMetricFirstJet
        cpmJet.secondJet
        harmonicJet.firstJet
    ).metricValue
        .radial
        .theta =
      reggeWheelerOddParitySpacetimeMetricPerturbation
          (
            reggeWheelerOddParityVacuumCPMMetricComponents
              cpmJet.secondJet.firstJet
          )
          harmonicJet.firstJet.harmonic
          .radial
          .theta)
:= by
  simpa only [] using
    congrFun
      (
        congrFun
          (
            reggeWheelerOddParityVacuumCPMMetricFirstJet_metricValue
              cpmJet.secondJet
              harmonicJet.firstJet
          )
          ReggeWheelerSpacetimeCoordinate.radial
      )
      ReggeWheelerSpacetimeCoordinate.theta

/--
The radial-theta component of the reconstructed CPM odd-parity spacetime
metric perturbation is the CPM radial coefficient multiplied by the
theta vector-harmonic value.

This is only the direct radial-theta specialization of the spacetime
metric-perturbation definition. Neither factor is otherwise reduced.

The radial-radial-theta metric-partial entry, every Schwarzschild
inverse-metric factor, the undifferentiated radial-theta
linearized-inverse factor, and the complete phi inverse-metric summand
remain unchanged.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaSpacetimeMetricPerturbationRadialTheta_eq_CPMRadialCoefficient_mul_vectorHarmonicValue
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParitySpacetimeMetricPerturbation
        (
          reggeWheelerOddParityVacuumCPMMetricComponents
            cpmJet.secondJet.firstJet
        )
        harmonicJet.firstJet.harmonic
        .radial
        .theta =
      reggeWheelerOddParityVacuumCPMRadialCoefficient
          cpmJet.secondJet.firstJet *
        reggeWheelerOddParityVectorHarmonicValue
          harmonicJet.firstJet.harmonic
          .theta := by
  rfl

/--
The two radial-theta CPM metric-value occurrences in the three-term
radial derivative of the radial-theta linearized inverse metric are
rewritten as the CPM radial coefficient multiplied by the theta
vector-harmonic value.

The radial-radial-theta CPM metric-partial entry and every Schwarzschild
inverse-metric factor remain explicit and unchanged. The
undifferentiated radial-theta linearized-inverse factor and the complete
phi inverse-metric summand also remain unchanged.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaLinearizedInverseMetricRadialPartialFactor_eq_threeProductRuleTermsWithCPMRadialCoefficientVectorHarmonicValue
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        .theta =
      -(
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              .radial
              .radial
              .radial *
            (
              reggeWheelerOddParityVacuumCPMRadialCoefficient
                  cpmJet.secondJet.firstJet *
                reggeWheelerOddParityVectorHarmonicValue
                  harmonicJet.firstJet.harmonic
                  .theta
            ) *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
        +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .radial *
            reggeWheelerOddParityVacuumCPMMetricPartial
              cpmJet.secondJet
              harmonicJet.firstJet
              .radial
              .radial
              .theta *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
        +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .radial *
            (
              reggeWheelerOddParityVacuumCPMRadialCoefficient
                  cpmJet.secondJet.firstJet *
                reggeWheelerOddParityVectorHarmonicValue
                  harmonicJet.firstJet.harmonic
                  .theta
            ) *
          reggeWheelerSchwarzschildInverseMetricComponentPartial
            frame
            .radial
            .theta
            .theta
      ) := by
  have h :=
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaLinearizedInverseMetricRadialPartialFactor_eq_threeProductRuleTermsWithDirectCPMMetricEntries
      frame
      cpmJet
      harmonicJet

  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaCPMMetricValueRadialTheta_eq_spacetimeMetricPerturbationComponent
      frame
      cpmJet
      harmonicJet,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaSpacetimeMetricPerturbationRadialTheta_eq_CPMRadialCoefficient_mul_vectorHarmonicValue
      cpmJet
      harmonicJet
  ] at h

  simpa only [] using h

/--
The radial-radial-theta CPM metric-partial entry is extracted from the
fourth conjunct of the compiled time/radial derivative reconstruction
theorem.

It equals the radial derivative of the CPM radial coefficient multiplied
by the theta vector-harmonic value. Neither factor is otherwise reduced.

Every Schwarzschild inverse-metric factor, the undifferentiated
radial-theta linearized-inverse factor, and the complete phi
inverse-metric summand remain unchanged.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaCPMMetricPartialRadialRadialTheta_eq_radialCoefficientRadialDerivative_mul_vectorHarmonicValue
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityVacuumCPMMetricPartial
        cpmJet.secondJet
        harmonicJet.firstJet
        .radial
        .radial
        .theta =
      reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
          cpmJet.secondJet *
        reggeWheelerOddParityVectorHarmonicValue
          harmonicJet.firstJet.harmonic
          .theta := by
  exact
    (
      reggeWheelerOddParityVacuumCPMMetricFirstJet_reconstructsTimeRadialDerivatives
        cpmJet.secondJet
        harmonicJet.firstJet
    ).2.2.2

/--
The remaining radial-radial-theta CPM metric-partial entry in the
three-term radial derivative of the radial-theta linearized inverse
metric is rewritten as the radial derivative of the CPM radial
coefficient multiplied by the theta vector-harmonic value.

All three CPM metric entries in this derivative are therefore explicit.
Every Schwarzschild inverse-metric factor remains unchanged. The
undifferentiated radial-theta linearized-inverse factor and the complete
phi inverse-metric summand also remain unchanged.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaLinearizedInverseMetricRadialPartialFactor_eq_threeExplicitCPMCoefficientTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        .theta =
      -(
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              .radial
              .radial
              .radial *
            (
              reggeWheelerOddParityVacuumCPMRadialCoefficient
                  cpmJet.secondJet.firstJet *
                reggeWheelerOddParityVectorHarmonicValue
                  harmonicJet.firstJet.harmonic
                  .theta
            ) *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
        +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .radial *
            (
              reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                  cpmJet.secondJet *
                reggeWheelerOddParityVectorHarmonicValue
                  harmonicJet.firstJet.harmonic
                  .theta
            ) *
          reggeWheelerSchwarzschildInverseMetricComponent
            frame
            .theta
            .theta
        +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .radial *
            (
              reggeWheelerOddParityVacuumCPMRadialCoefficient
                  cpmJet.secondJet.firstJet *
                reggeWheelerOddParityVectorHarmonicValue
                  harmonicJet.firstJet.harmonic
                  .theta
            ) *
          reggeWheelerSchwarzschildInverseMetricComponentPartial
            frame
            .radial
            .theta
            .theta
      ) := by
  have h :=
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaLinearizedInverseMetricRadialPartialFactor_eq_threeProductRuleTermsWithCPMRadialCoefficientVectorHarmonicValue
      frame
      cpmJet
      harmonicJet

  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaCPMMetricPartialRadialRadialTheta_eq_radialCoefficientRadialDerivative_mul_vectorHarmonicValue
      cpmJet
      harmonicJet
  ] at h

  simpa only [] using h

/--
The four unique Schwarzschild inverse-metric quantities occurring across
the three explicit CPM coefficient terms are evaluated:

* the radial partial of the radial-radial inverse component;
* the radial-radial inverse component;
* the theta-theta inverse component;
* the radial partial of the theta-theta inverse component.

The three CPM coefficient terms remain separate and in their established
order. No coefficient combination, cancellation, or factorization is
performed.

The undifferentiated radial-theta linearized-inverse factor and the
complete phi inverse-metric summand remain unchanged.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaLinearizedInverseMetricRadialPartialFactor_eq_threeExplicitCPMCoefficientTermsWithSchwarzschildFactors
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        .theta =
      -(
        reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
              frame *
            (
              reggeWheelerOddParityVacuumCPMRadialCoefficient
                  cpmJet.secondJet.firstJet *
                reggeWheelerOddParityVectorHarmonicValue
                  harmonicJet.firstJet.harmonic
                  .theta
            ) *
          (
            1 /
              frame.background.radius ^ 2
          )
        +
        reggeWheelerSchwarzschildExteriorFactor
              frame.background *
            (
              reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                  cpmJet.secondJet *
                reggeWheelerOddParityVectorHarmonicValue
                  harmonicJet.firstJet.harmonic
                  .theta
            ) *
          (
            1 /
              frame.background.radius ^ 2
          )
        +
        reggeWheelerSchwarzschildExteriorFactor
              frame.background *
            (
              reggeWheelerOddParityVacuumCPMRadialCoefficient
                  cpmJet.secondJet.firstJet *
                reggeWheelerOddParityVectorHarmonicValue
                  harmonicJet.firstJet.harmonic
                  .theta
            ) *
          (
            -2 /
              frame.background.radius ^ 3
          )
      ) := by
  have h :=
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaLinearizedInverseMetricRadialPartialFactor_eq_threeExplicitCPMCoefficientTerms
      frame
      cpmJet
      harmonicJet

  simpa only [
    reggeWheelerSchwarzschildInverseMetricComponent,
    reggeWheelerSchwarzschildInverseMetricDiagonal,
    reggeWheelerSchwarzschildInverseMetricComponentPartial
  ] using h

/--
The explicit radial derivative of the radial-theta linearized inverse
metric is substituted only into the first retained theta-angular
product-rule term.

That first term remains multiplied by the previously proved
`2 * frame.background.radius` Schwarzschild connection-kernel factor.
The second retained term remains exactly the undifferentiated
radial-theta linearized inverse-metric component multiplied by `2`.

No combination, cancellation, or factorization of the three explicit
CPM coefficient terms is performed. The complete first-radial phi
inverse-metric summand also remains open.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummandThetaAngularBranch_eq_explicitRadialPartialFactor_mul_twoRadius_add_retainedValueTerm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        (
          reggeWheelerAngularCoordinateToSpacetime
            ReggeWheelerAngularCoordinate.theta
        )
        .radial
        .theta =
      (
        -(
          reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
                frame *
              (
                reggeWheelerOddParityVacuumCPMRadialCoefficient
                    cpmJet.secondJet.firstJet *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .theta
              ) *
            (
              1 /
                frame.background.radius ^ 2
            )
          +
          reggeWheelerSchwarzschildExteriorFactor
                frame.background *
              (
                reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                    cpmJet.secondJet *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .theta
              ) *
            (
              1 /
                frame.background.radius ^ 2
            )
          +
          reggeWheelerSchwarzschildExteriorFactor
                frame.background *
              (
                reggeWheelerOddParityVacuumCPMRadialCoefficient
                    cpmJet.secondJet.firstJet *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .theta
              ) *
            (
              -2 /
                frame.background.radius ^ 3
            )
        )
      ) *
          (
            2 *
              frame.background.radius
          )
        +
        reggeWheelerOddParityLinearizedInverseMetricComponent
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            ).firstJet
            .radial
            .theta *
          2 := by
  have h :=
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummandThetaAngularBranch_eq_explicitBackgroundFactors
      frame
      cpmJet
      harmonicJet

  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaLinearizedInverseMetricRadialPartialFactor_eq_threeExplicitCPMCoefficientTermsWithSchwarzschildFactors
      frame
      cpmJet
      harmonicJet
  ] at h

  simpa only [] using h

/--
The undifferentiated radial-theta linearized inverse-metric component is
expanded into its direct Schwarzschild–CPM product.

After unfolding the linearized inverse metric, the derived metric-second
jet first-jet projection is changed to its definitionally equal direct
CPM metric first jet. This permits the established radial-theta metric
component identities to be applied without adding a new semantic
assumption.

The radial Schwarzschild inverse component contributes the exterior
factor, the theta inverse component contributes one over the squared
radius, and the CPM metric perturbation contributes the radial
coefficient multiplied by the theta vector-harmonic value.

The previously explicit radial-partial term and the complete
first-radial phi inverse-metric summand remain unchanged.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaLinearizedInverseMetricRadialThetaValue_eq_explicitSchwarzschildCPMProduct
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponent
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        ).firstJet
        .radial
        .theta =
      -(
        reggeWheelerSchwarzschildExteriorFactor
              frame.background *
            (
              reggeWheelerOddParityVacuumCPMRadialCoefficient
                  cpmJet.secondJet.firstJet *
                reggeWheelerOddParityVectorHarmonicValue
                  harmonicJet.firstJet.harmonic
                  .theta
            ) *
          (
            1 /
              frame.background.radius ^ 2
          )
      ) := by
  unfold reggeWheelerOddParityLinearizedInverseMetricComponent

  change
    -(
      reggeWheelerSchwarzschildInverseMetricDiagonal
            frame
            .radial *
          (
            reggeWheelerOddParityVacuumCPMMetricFirstJet
              cpmJet.secondJet
              harmonicJet.firstJet
          ).metricValue
            .radial
            .theta *
        reggeWheelerSchwarzschildInverseMetricDiagonal
          frame
          .theta
    ) =
      -(
        reggeWheelerSchwarzschildExteriorFactor
              frame.background *
            (
              reggeWheelerOddParityVacuumCPMRadialCoefficient
                  cpmJet.secondJet.firstJet *
                reggeWheelerOddParityVectorHarmonicValue
                  harmonicJet.firstJet.harmonic
                  .theta
            ) *
          (
            1 /
              frame.background.radius ^ 2
          )
      )

  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaCPMMetricValueRadialTheta_eq_spacetimeMetricPerturbationComponent
      frame
      cpmJet
      harmonicJet,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaSpacetimeMetricPerturbationRadialTheta_eq_CPMRadialCoefficient_mul_vectorHarmonicValue
      cpmJet
      harmonicJet
  ]

  rfl

/--
The explicit radial-theta linearized inverse-metric value is substituted
only into the second retained theta-angular product-rule term.

The first term remains the previously established explicit radial
partial multiplied by `2 * frame.background.radius`. The second term
is now the explicit Schwarzschild–CPM value multiplied by `2`.

The two product-rule terms remain separate. No algebraic combination,
cancellation, or factorization is performed. The phi-angular branch is
already zero, while the complete first-radial phi inverse-metric summand
remains open.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummandThetaAngularBranch_eq_twoExplicitProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        (
          reggeWheelerAngularCoordinateToSpacetime
            ReggeWheelerAngularCoordinate.theta
        )
        .radial
        .theta =
      (
        -(
          reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
                frame *
              (
                reggeWheelerOddParityVacuumCPMRadialCoefficient
                    cpmJet.secondJet.firstJet *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .theta
              ) *
            (
              1 /
                frame.background.radius ^ 2
            )
          +
          reggeWheelerSchwarzschildExteriorFactor
                frame.background *
              (
                reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                    cpmJet.secondJet *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .theta
              ) *
            (
              1 /
                frame.background.radius ^ 2
            )
          +
          reggeWheelerSchwarzschildExteriorFactor
                frame.background *
              (
                reggeWheelerOddParityVacuumCPMRadialCoefficient
                    cpmJet.secondJet.firstJet *
                  reggeWheelerOddParityVectorHarmonicValue
                    harmonicJet.firstJet.harmonic
                    .theta
              ) *
            (
              -2 /
                frame.background.radius ^ 3
            )
        )
      ) *
          (
            2 *
              frame.background.radius
          )
        +
        (
          -(
            reggeWheelerSchwarzschildExteriorFactor
                  frame.background *
                (
                  reggeWheelerOddParityVacuumCPMRadialCoefficient
                      cpmJet.secondJet.firstJet *
                    reggeWheelerOddParityVectorHarmonicValue
                      harmonicJet.firstJet.harmonic
                      .theta
                ) *
              (
                1 /
                  frame.background.radius ^ 2
              )
          )
        ) *
          2 := by
  have h :=
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummandThetaAngularBranch_eq_explicitRadialPartialFactor_mul_twoRadius_add_retainedValueTerm
      frame
      cpmJet
      harmonicJet

  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaLinearizedInverseMetricRadialThetaValue_eq_explicitSchwarzschildCPMProduct
      frame
      cpmJet
      harmonicJet
  ] at h

  simpa only [] using h

/--
The two angular-coordinate branches of the first-radial theta
inverse-metric summand are recombined into one case theorem.

For the theta angular coordinate, the result is the previously proved
pair of fully explicit but uncombined product-rule terms. For the phi
angular coordinate, the result is zero.

No algebraic combination, cancellation, or factorization is performed
inside the theta branch. The separate first-radial phi inverse-metric
summand remains open.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummand_eq_explicitAngularCases
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        (
          reggeWheelerAngularCoordinateToSpacetime
            angular
        )
        .radial
        .theta =
      match angular with
      | .theta =>
          (
            -(
              reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
                    frame *
                  (
                    reggeWheelerOddParityVacuumCPMRadialCoefficient
                        cpmJet.secondJet.firstJet *
                      reggeWheelerOddParityVectorHarmonicValue
                        harmonicJet.firstJet.harmonic
                        .theta
                  ) *
                (
                  1 /
                    frame.background.radius ^ 2
                )
              +
              reggeWheelerSchwarzschildExteriorFactor
                    frame.background *
                  (
                    reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                        cpmJet.secondJet *
                      reggeWheelerOddParityVectorHarmonicValue
                        harmonicJet.firstJet.harmonic
                        .theta
                  ) *
                (
                  1 /
                    frame.background.radius ^ 2
                )
              +
              reggeWheelerSchwarzschildExteriorFactor
                    frame.background *
                  (
                    reggeWheelerOddParityVacuumCPMRadialCoefficient
                        cpmJet.secondJet.firstJet *
                      reggeWheelerOddParityVectorHarmonicValue
                        harmonicJet.firstJet.harmonic
                        .theta
                  ) *
                (
                  -2 /
                    frame.background.radius ^ 3
                )
            )
          ) *
              (
                2 *
                  frame.background.radius
              )
            +
            (
              -(
                reggeWheelerSchwarzschildExteriorFactor
                      frame.background *
                    (
                      reggeWheelerOddParityVacuumCPMRadialCoefficient
                          cpmJet.secondJet.firstJet *
                        reggeWheelerOddParityVectorHarmonicValue
                          harmonicJet.firstJet.harmonic
                          .theta
                    ) *
                  (
                    1 /
                      frame.background.radius ^ 2
                  )
              )
            ) *
              2
      | .phi =>
          0 := by
  cases angular with
  | theta =>
      simpa only [] using
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummandThetaAngularBranch_eq_twoExplicitProductRuleTerms
          frame
          cpmJet
          harmonicJet
  | phi =>
      simpa only [] using
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummandPhiAngularBranch_eq_zero
          frame
          cpmJet
          harmonicJet

/--
The first-radial phi inverse-metric summand is unfolded into its four
product-rule terms:

1. the radial partial of the radial-phi linearized inverse metric
   multiplied by the background connection kernel;
2. the undifferentiated radial-phi linearized inverse metric multiplied
   by the radial partial of the background connection kernel;
3. the radial partial of the background radial-phi inverse metric
   multiplied by the perturbation connection kernel;
4. the undifferentiated background radial-phi inverse metric multiplied
   by the radial partial of the perturbation connection kernel.

None of these four terms is simplified, removed, combined, canceled, or
factored in this theorem.

The completed theta inverse-metric angular cases and all remaining
principal, connection-product, harmonic, vacuum, and master-residual
boundaries remain unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiInverseMetricSummand_eq_fourProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        (
          reggeWheelerAngularCoordinateToSpacetime
            angular
        )
        .radial
        .phi =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .radial
            .radial
            .phi *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            (
              reggeWheelerAngularCoordinateToSpacetime
                angular
            )
            .radial
            .phi
        +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .phi *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              .radial
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .phi
        +
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              .radial
              .radial
              .phi *
            reggeWheelerOddParityPerturbationConnectionKernel
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .phi
        +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .phi *
            reggeWheelerOddParityPerturbationConnectionKernelPartial
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .radial
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .phi := by
  rfl

/--
The radial derivative of the Schwarzschild radial-phi inverse-metric
component is zero.

This proves only the background factor multiplying the perturbation
connection kernel in the third phi product-rule term. It does not
simplify the first two phi terms or rewrite the four-term summand.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiBackgroundInverseMetricRadialPartialFactor_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildInverseMetricComponentPartial
        frame
        .radial
        .radial
        .phi =
      0 := by
  rfl

/--
The undifferentiated Schwarzschild radial-phi inverse-metric component
is zero.

This proves only the background factor multiplying the perturbation
connection-kernel radial partial in the fourth phi product-rule term. It
does not simplify the first two phi terms or rewrite the four-term
summand.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiBackgroundInverseMetricValueFactor_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildInverseMetricComponent
        frame
        .radial
        .phi =
      0 := by
  rfl

/--
The third and fourth terms in the first-radial phi inverse-metric
product-rule expansion vanish because their Schwarzschild radial-phi
inverse-metric factors are zero.

The first two terms are retained exactly:

1. the radial partial of the radial-phi linearized inverse metric
   multiplied by the background connection kernel;
2. the undifferentiated radial-phi linearized inverse metric multiplied
   by the radial partial of the background connection kernel.

No simplification, evaluation, combination, cancellation, or
factorization of these first two retained terms is performed.

The completed theta inverse-metric angular cases and all remaining
principal, connection-product, harmonic, vacuum, and master-residual
boundaries remain unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiInverseMetricSummand_eq_firstTwoProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        (
          reggeWheelerAngularCoordinateToSpacetime
            angular
        )
        .radial
        .phi =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .radial
            .radial
            .phi *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            (
              reggeWheelerAngularCoordinateToSpacetime
                angular
            )
            .radial
            .phi
        +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .phi *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              .radial
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .phi := by
  have h :=
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiInverseMetricSummand_eq_fourProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular

  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiBackgroundInverseMetricRadialPartialFactor_eq_zero
      frame,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiBackgroundInverseMetricValueFactor_eq_zero
      frame
  ] at h

  simpa only [
    zero_mul,
    add_zero
  ] using h

/--
The Schwarzschild connection-kernel value in the retained first-radial
phi inverse-metric summand is evaluated by angular coordinate.

For the theta angular coordinate it is zero. For the phi angular
coordinate it is `2 * radius * sin(polarAngle)^2`.

The radial-phi linearized-inverse factor multiplying this kernel is
retained unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiBackgroundConnectionKernelValue_eq_angularCases
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildConnectionKernel
        frame
        (
          reggeWheelerAngularCoordinateToSpacetime
            angular
        )
        .radial
        .phi =
      match angular with
      | .theta =>
          0
      | .phi =>
          2 *
            frame.background.radius *
              Real.sin frame.polarAngle ^ 2 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerSchwarzschildConnectionKernel,
      reggeWheelerSchwarzschildMetricPartial
    ]

/--
The radial partial of the Schwarzschild connection kernel in the
retained first-radial phi inverse-metric summand is evaluated by angular
coordinate.

For the theta angular coordinate it is zero. For the phi angular
coordinate it is `2 * sin(polarAngle)^2`.

The undifferentiated radial-phi linearized-inverse factor multiplying
this kernel partial is retained unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiBackgroundConnectionKernelRadialPartial_eq_angularCases
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildConnectionKernelPartial
        frame
        .radial
        (
          reggeWheelerAngularCoordinateToSpacetime
            angular
        )
        .radial
        .phi =
      match angular with
      | .theta =>
          0
      | .phi =>
          2 *
            Real.sin frame.polarAngle ^ 2 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerSchwarzschildConnectionKernelPartial,
      reggeWheelerSchwarzschildMetricSecondPartial
    ]

/--
The retained first-radial phi inverse-metric summand is split by angular
coordinate after substituting the proved Schwarzschild background
connection-kernel value and radial-partial identities.

For the theta angular coordinate, both retained product-rule terms
vanish because both background kernel factors are zero.

For the phi angular coordinate, the two linearized-inverse factors are
retained unchanged and multiplied respectively by

* `2 * radius * sin(polarAngle)^2`;
* `2 * sin(polarAngle)^2`.

The two phi terms remain separate. Neither linearized-inverse factor is
expanded, simplified, combined, canceled, or factored.

No angular harmonic eigenvalue, vacuum equation, connection-product
reduction, master residual, or `r^3 - 6` comparison is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiInverseMetricSummand_eq_explicitAngularCases
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        (
          reggeWheelerAngularCoordinateToSpacetime
            angular
        )
        .radial
        .phi =
      match angular with
      | .theta =>
          0
      | .phi =>
          reggeWheelerOddParityLinearizedInverseMetricComponentPartial
                frame
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                    cpmJet
                    harmonicJet
                )
                .radial
                .radial
                .phi *
              (
                2 *
                  frame.background.radius *
                    Real.sin frame.polarAngle ^ 2
              )
            +
            reggeWheelerOddParityLinearizedInverseMetricComponent
                  frame
                  (
                    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                      cpmJet
                      harmonicJet
                  ).firstJet
                  .radial
                  .phi *
                (
                  2 *
                    Real.sin frame.polarAngle ^ 2
                ) := by
  cases angular with
  | theta =>
      have h :=
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiInverseMetricSummand_eq_firstTwoProductRuleTerms
          frame
          cpmJet
          harmonicJet
          ReggeWheelerAngularCoordinate.theta

      rw [
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiBackgroundConnectionKernelValue_eq_angularCases
          frame
          ReggeWheelerAngularCoordinate.theta,
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiBackgroundConnectionKernelRadialPartial_eq_angularCases
          frame
          ReggeWheelerAngularCoordinate.theta
      ] at h

      simpa only [
        mul_zero,
        add_zero
      ] using h

  | phi =>
      have h :=
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiInverseMetricSummand_eq_firstTwoProductRuleTerms
          frame
          cpmJet
          harmonicJet
          ReggeWheelerAngularCoordinate.phi

      rw [
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiBackgroundConnectionKernelValue_eq_angularCases
          frame
          ReggeWheelerAngularCoordinate.phi,
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiBackgroundConnectionKernelRadialPartial_eq_angularCases
          frame
          ReggeWheelerAngularCoordinate.phi
      ] at h

      simpa only [] using h

/--
The complete first connection-derivative inverse-metric contraction in
the radial-coordinate principal contribution is reconstructed from its
four coordinate summands.

The time and radial inverse-metric summands vanish by their previously
proved zero theorems.

For the theta angular coordinate, only the theta inverse-metric summand
remains, in its previously proved two-term explicit CPM–Schwarzschild
form.

For the phi angular coordinate, only the phi inverse-metric summand
remains, with its two explicit background-kernel weights and its two
linearized-inverse factors retained unchanged.

No further simplification, combination, cancellation, or factorization
of either angular branch is performed.

The second radial connection derivative, the principal theta and phi
coordinate contributions, the connection-product term, the angular
harmonic eigenvalue, the vacuum reduction, the master residual, and the
`r^3 - 6` comparison remain outside this theorem.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeContraction_eq_explicitAngularCases
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSpacetimeCoordinateContraction
        (fun inverseMetricContraction =>
          reggeWheelerOddParityLinearizedChristoffelSummandPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            .radial
            .radial
            (
              reggeWheelerAngularCoordinateToSpacetime
                angular
            )
            .radial
            inverseMetricContraction) =
      match angular with
      | .theta =>
          (
            -(
              reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
                    frame *
                  (
                    reggeWheelerOddParityVacuumCPMRadialCoefficient
                        cpmJet.secondJet.firstJet *
                      reggeWheelerOddParityVectorHarmonicValue
                        harmonicJet.firstJet.harmonic
                        .theta
                  ) *
                (
                  1 /
                    frame.background.radius ^ 2
                )
              +
              reggeWheelerSchwarzschildExteriorFactor
                    frame.background *
                  (
                    reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                        cpmJet.secondJet *
                      reggeWheelerOddParityVectorHarmonicValue
                        harmonicJet.firstJet.harmonic
                        .theta
                  ) *
                (
                  1 /
                    frame.background.radius ^ 2
                )
              +
              reggeWheelerSchwarzschildExteriorFactor
                    frame.background *
                  (
                    reggeWheelerOddParityVacuumCPMRadialCoefficient
                        cpmJet.secondJet.firstJet *
                      reggeWheelerOddParityVectorHarmonicValue
                        harmonicJet.firstJet.harmonic
                        .theta
                  ) *
                (
                  -2 /
                    frame.background.radius ^ 3
                )
            )
          ) *
              (
                2 *
                  frame.background.radius
              )
            +
            (
              -(
                reggeWheelerSchwarzschildExteriorFactor
                      frame.background *
                    (
                      reggeWheelerOddParityVacuumCPMRadialCoefficient
                          cpmJet.secondJet.firstJet *
                        reggeWheelerOddParityVectorHarmonicValue
                          harmonicJet.firstJet.harmonic
                          .theta
                    ) *
                  (
                    1 /
                      frame.background.radius ^ 2
                  )
              )
            ) *
              2

      | .phi =>
          reggeWheelerOddParityLinearizedInverseMetricComponentPartial
                frame
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                    cpmJet
                    harmonicJet
                )
                .radial
                .radial
                .phi *
              (
                2 *
                  frame.background.radius *
                    Real.sin frame.polarAngle ^ 2
              )
            +
            reggeWheelerOddParityLinearizedInverseMetricComponent
                  frame
                  (
                    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                      cpmJet
                      harmonicJet
                  ).firstJet
                  .radial
                  .phi *
                (
                  2 *
                    Real.sin frame.polarAngle ^ 2
                ) := by
  cases angular with
  | theta =>
      have h :=
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeTerm_eq_fourInverseMetricCoordinateSummands
          frame
          cpmJet
          harmonicJet
          ReggeWheelerAngularCoordinate.theta

      rw [
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeTimeInverseMetricSummand_eq_zero,
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeRadialInverseMetricSummand_eq_zero,
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummand_eq_explicitAngularCases,
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiInverseMetricSummand_eq_explicitAngularCases
      ] at h

      simpa only [
        zero_add,
        add_zero
      ] using h

  | phi =>
      have h :=
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeTerm_eq_fourInverseMetricCoordinateSummands
          frame
          cpmJet
          harmonicJet
          ReggeWheelerAngularCoordinate.phi

      rw [
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeTimeInverseMetricSummand_eq_zero,
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeRadialInverseMetricSummand_eq_zero,
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeThetaInverseMetricSummand_eq_explicitAngularCases,
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePhiInverseMetricSummand_eq_explicitAngularCases
      ] at h

      simpa only [
        zero_add,
        add_zero
      ] using h

/--
The direct first radial linearized-Christoffel partial is one-half of
the previously completed inverse-metric contraction.

The theta and phi angular branches are inherited exactly from the
completed contraction theorem. No branch is simplified, combined,
canceled, or factored.

This bridge is not yet substituted into the principal radial-coordinate
contribution. The second connection derivative remains untouched.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePartial_eq_halfExplicitAngularCases
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        .radial
        .radial
        (
          reggeWheelerAngularCoordinateToSpacetime
            angular
        )
        .radial =
      (1 / 2 : ℝ) *
        (
          match angular with
          | .theta =>
              (
                -(
                  reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
                        frame *
                      (
                        reggeWheelerOddParityVacuumCPMRadialCoefficient
                            cpmJet.secondJet.firstJet *
                          reggeWheelerOddParityVectorHarmonicValue
                            harmonicJet.firstJet.harmonic
                            .theta
                      ) *
                    (
                      1 /
                        frame.background.radius ^ 2
                    )
                  +
                  reggeWheelerSchwarzschildExteriorFactor
                        frame.background *
                      (
                        reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                            cpmJet.secondJet *
                          reggeWheelerOddParityVectorHarmonicValue
                            harmonicJet.firstJet.harmonic
                            .theta
                      ) *
                    (
                      1 /
                        frame.background.radius ^ 2
                    )
                  +
                  reggeWheelerSchwarzschildExteriorFactor
                        frame.background *
                      (
                        reggeWheelerOddParityVacuumCPMRadialCoefficient
                            cpmJet.secondJet.firstJet *
                          reggeWheelerOddParityVectorHarmonicValue
                            harmonicJet.firstJet.harmonic
                            .theta
                      ) *
                    (
                      -2 /
                        frame.background.radius ^ 3
                    )
                )
              ) *
                  (
                    2 *
                      frame.background.radius
                  )
                +
                (
                  -(
                    reggeWheelerSchwarzschildExteriorFactor
                          frame.background *
                        (
                          reggeWheelerOddParityVacuumCPMRadialCoefficient
                              cpmJet.secondJet.firstJet *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic
                              .theta
                        ) *
                      (
                        1 /
                          frame.background.radius ^ 2
                      )
                  )
                ) *
                  2

          | .phi =>
              reggeWheelerOddParityLinearizedInverseMetricComponentPartial
                    frame
                    (
                      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                        cpmJet
                        harmonicJet
                    )
                    .radial
                    .radial
                    .phi *
                  (
                    2 *
                      frame.background.radius *
                        Real.sin frame.polarAngle ^ 2
                  )
                +
                reggeWheelerOddParityLinearizedInverseMetricComponent
                      frame
                      (
                        reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                          cpmJet
                          harmonicJet
                      ).firstJet
                      .radial
                      .phi *
                    (
                      2 *
                        Real.sin frame.polarAngle ^ 2
                    )
        ) := by
  unfold reggeWheelerOddParityLinearizedChristoffelPartial

  exact
    congrArg
      (fun value : ℝ =>
        (1 / 2 : ℝ) * value)
      (
        prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativeContraction_eq_explicitAngularCases
          frame
          cpmJet
          harmonicJet
          angular
      )

/--
The one-half-normalized explicit first radial connection derivative is
substituted into the principal radial-coordinate contribution.

The first term is therefore represented by one-half of the complete
theta/phi angular-case inverse-metric contraction.

The second connection derivative

`∂ₐ δΓʳ_{rr}`

is retained exactly. It is not unfolded, simplified, combined,
canceled, factored, or asserted to vanish.

The principal theta and phi coordinate contributions, the
connection-product term, the angular harmonic eigenvalue, the vacuum
reduction, the master residual, and the `r^3 - 6` comparison remain
outside this theorem.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialContribution_eq_halfExplicitFirstConnectionDerivativeAngularCases_sub_retainedSecondConnectionDerivative
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) :
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
        frame
        cpmJet
        harmonicJet
        hCompatible
        angular
        .radial =
      (1 / 2 : ℝ) *
          (
            match angular with
            | .theta =>
                (
                  -(
                    reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
                          frame *
                        (
                          reggeWheelerOddParityVacuumCPMRadialCoefficient
                              cpmJet.secondJet.firstJet *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic
                              .theta
                        ) *
                      (
                        1 /
                          frame.background.radius ^ 2
                      )
                    +
                    reggeWheelerSchwarzschildExteriorFactor
                          frame.background *
                        (
                          reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                              cpmJet.secondJet *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic
                              .theta
                        ) *
                      (
                        1 /
                          frame.background.radius ^ 2
                      )
                    +
                    reggeWheelerSchwarzschildExteriorFactor
                          frame.background *
                        (
                          reggeWheelerOddParityVacuumCPMRadialCoefficient
                              cpmJet.secondJet.firstJet *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic
                              .theta
                        ) *
                      (
                        -2 /
                          frame.background.radius ^ 3
                      )
                  )
                ) *
                    (
                      2 *
                        frame.background.radius
                    )
                  +
                  (
                    -(
                      reggeWheelerSchwarzschildExteriorFactor
                            frame.background *
                          (
                            reggeWheelerOddParityVacuumCPMRadialCoefficient
                                cpmJet.secondJet.firstJet *
                              reggeWheelerOddParityVectorHarmonicValue
                                harmonicJet.firstJet.harmonic
                                .theta
                          ) *
                        (
                          1 /
                            frame.background.radius ^ 2
                        )
                    )
                  ) *
                    2

            | .phi =>
                reggeWheelerOddParityLinearizedInverseMetricComponentPartial
                      frame
                      (
                        reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                          cpmJet
                          harmonicJet
                      )
                      .radial
                      .radial
                      .phi *
                    (
                      2 *
                        frame.background.radius *
                          Real.sin frame.polarAngle ^ 2
                    )
                  +
                  reggeWheelerOddParityLinearizedInverseMetricComponent
                        frame
                        (
                          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                            cpmJet
                            harmonicJet
                        ).firstJet
                        .radial
                        .phi *
                      (
                        2 *
                          Real.sin frame.polarAngle ^ 2
                      )
          )
        -
        reggeWheelerOddParityLinearizedChristoffelPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (
            reggeWheelerAngularCoordinateToSpacetime
              angular
          )
          .radial
          .radial
          .radial := by
  calc
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular
          .radial =
        (
          fun
              (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
              (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
              (harmonicJet :
                ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
              (_hCompatible :
                prizcarbonOddParityVacuumCPMFrameCompatible
                  frame
                  cpmJet)
              (angular : ReggeWheelerAngularCoordinate)
              (contracted : ReggeWheelerSpacetimeCoordinate) =>
            reggeWheelerOddParityLinearizedChristoffelPartial
                  frame
                  (
                    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                      cpmJet
                      harmonicJet
                  )
                  contracted
                  contracted
                  (
                    reggeWheelerAngularCoordinateToSpacetime
                      angular
                  )
                  .radial
              -
              reggeWheelerOddParityLinearizedChristoffelPartial
                frame
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                    cpmJet
                    harmonicJet
                )
                (
                  reggeWheelerAngularCoordinateToSpacetime
                    angular
                )
                contracted
                contracted
                .radial
        )
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular
          .radial := by
            exact
              prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialContribution_eq_definingConnectionDerivativeTerms
                frame
                cpmJet
                harmonicJet
                hCompatible
                angular

    _ =
        reggeWheelerOddParityLinearizedChristoffelPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              .radial
              .radial
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
          -
          reggeWheelerOddParityLinearizedChristoffelPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (
              reggeWheelerAngularCoordinateToSpacetime
                angular
            )
            .radial
            .radial
            .radial := by
              rfl

    _ =
        (1 / 2 : ℝ) *
            (
              match angular with
              | .theta =>
                  (
                    -(
                      reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
                            frame *
                          (
                            reggeWheelerOddParityVacuumCPMRadialCoefficient
                                cpmJet.secondJet.firstJet *
                              reggeWheelerOddParityVectorHarmonicValue
                                harmonicJet.firstJet.harmonic
                                .theta
                          ) *
                        (
                          1 /
                            frame.background.radius ^ 2
                        )
                      +
                      reggeWheelerSchwarzschildExteriorFactor
                            frame.background *
                          (
                            reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                                cpmJet.secondJet *
                              reggeWheelerOddParityVectorHarmonicValue
                                harmonicJet.firstJet.harmonic
                                .theta
                          ) *
                        (
                          1 /
                            frame.background.radius ^ 2
                        )
                      +
                      reggeWheelerSchwarzschildExteriorFactor
                            frame.background *
                          (
                            reggeWheelerOddParityVacuumCPMRadialCoefficient
                                cpmJet.secondJet.firstJet *
                              reggeWheelerOddParityVectorHarmonicValue
                                harmonicJet.firstJet.harmonic
                                .theta
                          ) *
                        (
                          -2 /
                            frame.background.radius ^ 3
                        )
                    )
                  ) *
                      (
                        2 *
                          frame.background.radius
                      )
                    +
                    (
                      -(
                        reggeWheelerSchwarzschildExteriorFactor
                              frame.background *
                            (
                              reggeWheelerOddParityVacuumCPMRadialCoefficient
                                  cpmJet.secondJet.firstJet *
                                reggeWheelerOddParityVectorHarmonicValue
                                  harmonicJet.firstJet.harmonic
                                  .theta
                            ) *
                          (
                            1 /
                              frame.background.radius ^ 2
                          )
                      )
                    ) *
                      2

              | .phi =>
                  reggeWheelerOddParityLinearizedInverseMetricComponentPartial
                        frame
                        (
                          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                            cpmJet
                            harmonicJet
                        )
                        .radial
                        .radial
                        .phi *
                      (
                        2 *
                          frame.background.radius *
                            Real.sin frame.polarAngle ^ 2
                      )
                    +
                    reggeWheelerOddParityLinearizedInverseMetricComponent
                          frame
                          (
                            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                              cpmJet
                              harmonicJet
                          ).firstJet
                          .radial
                          .phi *
                        (
                          2 *
                            Real.sin frame.polarAngle ^ 2
                        )
            )
          -
          reggeWheelerOddParityLinearizedChristoffelPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (
              reggeWheelerAngularCoordinateToSpacetime
                angular
            )
            .radial
            .radial
            .radial := by
              exact
                congrArg
                  (
                    fun value : ℝ =>
                      value -
                        reggeWheelerOddParityLinearizedChristoffelPartial
                          frame
                          (
                            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                              cpmJet
                              harmonicJet
                          )
                          (
                            reggeWheelerAngularCoordinateToSpacetime
                              angular
                          )
                          .radial
                          .radial
                          .radial
                  )
                  (
                    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialFirstConnectionDerivativePartial_eq_halfExplicitAngularCases
                      frame
                      cpmJet
                      harmonicJet
                      angular
                  )

/--
The retained second connection derivative in the radial-coordinate
principal contribution is expanded into one-half of its four explicit
inverse-metric coordinate summands.

This is the derivative

`∂ₐ δΓʳ_{rr}`.

The inverse-metric contraction coordinates are displayed in the order

`.time`, `.radial`, `.theta`, `.phi`.

No individual summand is unfolded, simplified, canceled, combined,
factored, or asserted to vanish. The first radial connection derivative
and all other principal and connection-product contributions remain
unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativePartial_eq_halfFourInverseMetricCoordinateSummands
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (
          reggeWheelerAngularCoordinateToSpacetime
            angular
        )
        .radial
        .radial
        .radial =
      (1 / 2 : ℝ) *
        (
          reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .radial
              .radial
              .time
          +
          reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .radial
              .radial
              .radial
          +
          reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .radial
              .radial
              .theta
          +
          reggeWheelerOddParityLinearizedChristoffelSummandPartial
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .radial
              .radial
              .phi
        ) := by
  rfl

/--
The one-half expansion of the retained second radial connection
derivative is substituted into the principal radial-coordinate
contribution.

The first connection derivative retains its previously proved explicit
theta/phi angular-case form.

The second connection derivative is represented as one-half of its four
inverse-metric coordinate summands, ordered as

`.time`, `.radial`, `.theta`, `.phi`.

All four second-derivative summands remain completely unsimplified. No
summand is unfolded, canceled, combined, factored, or asserted to
vanish.

The principal theta and phi coordinate contributions, the
connection-product term, the angular harmonic eigenvalue, the vacuum
reduction, the master residual, and the `r^3 - 6` comparison remain
outside this theorem.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialContribution_eq_halfExplicitFirstConnectionDerivativeAngularCases_sub_halfFourSecondConnectionDerivativeSummands
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hCompatible :
      prizcarbonOddParityVacuumCPMFrameCompatible
        frame
        cpmJet)
    (angular : ReggeWheelerAngularCoordinate) :
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
        frame
        cpmJet
        harmonicJet
        hCompatible
        angular
        .radial =
      (1 / 2 : ℝ) *
          (
            match angular with
            | .theta =>
                (
                  -(
                    reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
                          frame *
                        (
                          reggeWheelerOddParityVacuumCPMRadialCoefficient
                              cpmJet.secondJet.firstJet *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic
                              .theta
                        ) *
                      (
                        1 /
                          frame.background.radius ^ 2
                      )
                    +
                    reggeWheelerSchwarzschildExteriorFactor
                          frame.background *
                        (
                          reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                              cpmJet.secondJet *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic
                              .theta
                        ) *
                      (
                        1 /
                          frame.background.radius ^ 2
                      )
                    +
                    reggeWheelerSchwarzschildExteriorFactor
                          frame.background *
                        (
                          reggeWheelerOddParityVacuumCPMRadialCoefficient
                              cpmJet.secondJet.firstJet *
                            reggeWheelerOddParityVectorHarmonicValue
                              harmonicJet.firstJet.harmonic
                              .theta
                        ) *
                      (
                        -2 /
                          frame.background.radius ^ 3
                      )
                  )
                ) *
                    (
                      2 *
                        frame.background.radius
                    )
                  +
                  (
                    -(
                      reggeWheelerSchwarzschildExteriorFactor
                            frame.background *
                          (
                            reggeWheelerOddParityVacuumCPMRadialCoefficient
                                cpmJet.secondJet.firstJet *
                              reggeWheelerOddParityVectorHarmonicValue
                                harmonicJet.firstJet.harmonic
                                .theta
                          ) *
                        (
                          1 /
                            frame.background.radius ^ 2
                        )
                    )
                  ) *
                    2

            | .phi =>
                reggeWheelerOddParityLinearizedInverseMetricComponentPartial
                      frame
                      (
                        reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                          cpmJet
                          harmonicJet
                      )
                      .radial
                      .radial
                      .phi *
                    (
                      2 *
                        frame.background.radius *
                          Real.sin frame.polarAngle ^ 2
                    )
                  +
                  reggeWheelerOddParityLinearizedInverseMetricComponent
                        frame
                        (
                          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                            cpmJet
                            harmonicJet
                        ).firstJet
                        .radial
                        .phi *
                      (
                        2 *
                          Real.sin frame.polarAngle ^ 2
                      )
          )
        -
        (1 / 2 : ℝ) *
          (
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
                frame
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                    cpmJet
                    harmonicJet
                )
                (
                  reggeWheelerAngularCoordinateToSpacetime
                    angular
                )
                .radial
                .radial
                .radial
                .time
            +
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
                frame
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                    cpmJet
                    harmonicJet
                )
                (
                  reggeWheelerAngularCoordinateToSpacetime
                    angular
                )
                .radial
                .radial
                .radial
                .radial
            +
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
                frame
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                    cpmJet
                    harmonicJet
                )
                (
                  reggeWheelerAngularCoordinateToSpacetime
                    angular
                )
                .radial
                .radial
                .radial
                .theta
            +
            reggeWheelerOddParityLinearizedChristoffelSummandPartial
                frame
                (
                  reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                    cpmJet
                    harmonicJet
                )
                (
                  reggeWheelerAngularCoordinateToSpacetime
                    angular
                )
                .radial
                .radial
                .radial
                .phi
          ) := by
  calc
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeCoordinateContribution
          frame
          cpmJet
          harmonicJet
          hCompatible
          angular
          .radial =
        (1 / 2 : ℝ) *
            (
              match angular with
              | .theta =>
                  (
                    -(
                      reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
                            frame *
                          (
                            reggeWheelerOddParityVacuumCPMRadialCoefficient
                                cpmJet.secondJet.firstJet *
                              reggeWheelerOddParityVectorHarmonicValue
                                harmonicJet.firstJet.harmonic
                                .theta
                          ) *
                        (
                          1 /
                            frame.background.radius ^ 2
                        )
                      +
                      reggeWheelerSchwarzschildExteriorFactor
                            frame.background *
                          (
                            reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                                cpmJet.secondJet *
                              reggeWheelerOddParityVectorHarmonicValue
                                harmonicJet.firstJet.harmonic
                                .theta
                          ) *
                        (
                          1 /
                            frame.background.radius ^ 2
                        )
                      +
                      reggeWheelerSchwarzschildExteriorFactor
                            frame.background *
                          (
                            reggeWheelerOddParityVacuumCPMRadialCoefficient
                                cpmJet.secondJet.firstJet *
                              reggeWheelerOddParityVectorHarmonicValue
                                harmonicJet.firstJet.harmonic
                                .theta
                          ) *
                        (
                          -2 /
                            frame.background.radius ^ 3
                        )
                    )
                  ) *
                      (
                        2 *
                          frame.background.radius
                      )
                    +
                    (
                      -(
                        reggeWheelerSchwarzschildExteriorFactor
                              frame.background *
                            (
                              reggeWheelerOddParityVacuumCPMRadialCoefficient
                                  cpmJet.secondJet.firstJet *
                                reggeWheelerOddParityVectorHarmonicValue
                                  harmonicJet.firstJet.harmonic
                                  .theta
                            ) *
                          (
                            1 /
                              frame.background.radius ^ 2
                          )
                      )
                    ) *
                      2

              | .phi =>
                  reggeWheelerOddParityLinearizedInverseMetricComponentPartial
                        frame
                        (
                          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                            cpmJet
                            harmonicJet
                        )
                        .radial
                        .radial
                        .phi *
                      (
                        2 *
                          frame.background.radius *
                            Real.sin frame.polarAngle ^ 2
                      )
                    +
                    reggeWheelerOddParityLinearizedInverseMetricComponent
                          frame
                          (
                            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                              cpmJet
                              harmonicJet
                          ).firstJet
                          .radial
                          .phi *
                        (
                          2 *
                            Real.sin frame.polarAngle ^ 2
                        )
            )
          -
          reggeWheelerOddParityLinearizedChristoffelPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (
              reggeWheelerAngularCoordinateToSpacetime
                angular
            )
            .radial
            .radial
            .radial := by
              exact
                prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialContribution_eq_halfExplicitFirstConnectionDerivativeAngularCases_sub_retainedSecondConnectionDerivative
                  frame
                  cpmJet
                  harmonicJet
                  hCompatible
                  angular

    _ =
        (1 / 2 : ℝ) *
            (
              match angular with
              | .theta =>
                  (
                    -(
                      reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
                            frame *
                          (
                            reggeWheelerOddParityVacuumCPMRadialCoefficient
                                cpmJet.secondJet.firstJet *
                              reggeWheelerOddParityVectorHarmonicValue
                                harmonicJet.firstJet.harmonic
                                .theta
                          ) *
                        (
                          1 /
                            frame.background.radius ^ 2
                        )
                      +
                      reggeWheelerSchwarzschildExteriorFactor
                            frame.background *
                          (
                            reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                                cpmJet.secondJet *
                              reggeWheelerOddParityVectorHarmonicValue
                                harmonicJet.firstJet.harmonic
                                .theta
                          ) *
                        (
                          1 /
                            frame.background.radius ^ 2
                        )
                      +
                      reggeWheelerSchwarzschildExteriorFactor
                            frame.background *
                          (
                            reggeWheelerOddParityVacuumCPMRadialCoefficient
                                cpmJet.secondJet.firstJet *
                              reggeWheelerOddParityVectorHarmonicValue
                                harmonicJet.firstJet.harmonic
                                .theta
                          ) *
                        (
                          -2 /
                            frame.background.radius ^ 3
                        )
                    )
                  ) *
                      (
                        2 *
                          frame.background.radius
                      )
                    +
                    (
                      -(
                        reggeWheelerSchwarzschildExteriorFactor
                              frame.background *
                            (
                              reggeWheelerOddParityVacuumCPMRadialCoefficient
                                  cpmJet.secondJet.firstJet *
                                reggeWheelerOddParityVectorHarmonicValue
                                  harmonicJet.firstJet.harmonic
                                  .theta
                            ) *
                          (
                            1 /
                              frame.background.radius ^ 2
                          )
                      )
                    ) *
                      2

              | .phi =>
                  reggeWheelerOddParityLinearizedInverseMetricComponentPartial
                        frame
                        (
                          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                            cpmJet
                            harmonicJet
                        )
                        .radial
                        .radial
                        .phi *
                      (
                        2 *
                          frame.background.radius *
                            Real.sin frame.polarAngle ^ 2
                      )
                    +
                    reggeWheelerOddParityLinearizedInverseMetricComponent
                          frame
                          (
                            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                              cpmJet
                              harmonicJet
                          ).firstJet
                          .radial
                          .phi *
                        (
                          2 *
                            Real.sin frame.polarAngle ^ 2
                        )
            )
          -
          (1 / 2 : ℝ) *
            (
              reggeWheelerOddParityLinearizedChristoffelSummandPartial
                  frame
                  (
                    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                      cpmJet
                      harmonicJet
                  )
                  (
                    reggeWheelerAngularCoordinateToSpacetime
                      angular
                  )
                  .radial
                  .radial
                  .radial
                  .time
              +
              reggeWheelerOddParityLinearizedChristoffelSummandPartial
                  frame
                  (
                    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                      cpmJet
                      harmonicJet
                  )
                  (
                    reggeWheelerAngularCoordinateToSpacetime
                      angular
                  )
                  .radial
                  .radial
                  .radial
                  .radial
              +
              reggeWheelerOddParityLinearizedChristoffelSummandPartial
                  frame
                  (
                    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                      cpmJet
                      harmonicJet
                  )
                  (
                    reggeWheelerAngularCoordinateToSpacetime
                      angular
                  )
                  .radial
                  .radial
                  .radial
                  .theta
              +
              reggeWheelerOddParityLinearizedChristoffelSummandPartial
                  frame
                  (
                    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                      cpmJet
                      harmonicJet
                  )
                  (
                    reggeWheelerAngularCoordinateToSpacetime
                      angular
                  )
                  .radial
                  .radial
                  .radial
                  .phi
            ) := by
              exact
                congrArg
                  (
                    fun value : ℝ =>
                      (1 / 2 : ℝ) *
                            (
                              match angular with
                              | .theta =>
                                  (
                                    -(
                                      reggeWheelerSchwarzschildExteriorFactorFirstRadialDerivative
                                            frame *
                                          (
                                            reggeWheelerOddParityVacuumCPMRadialCoefficient
                                                cpmJet.secondJet.firstJet *
                                              reggeWheelerOddParityVectorHarmonicValue
                                                harmonicJet.firstJet.harmonic
                                                .theta
                                          ) *
                                        (
                                          1 /
                                            frame.background.radius ^ 2
                                        )
                                      +
                                      reggeWheelerSchwarzschildExteriorFactor
                                            frame.background *
                                          (
                                            reggeWheelerOddParityVacuumCPMRadialCoefficientRadialDerivative
                                                cpmJet.secondJet *
                                              reggeWheelerOddParityVectorHarmonicValue
                                                harmonicJet.firstJet.harmonic
                                                .theta
                                          ) *
                                        (
                                          1 /
                                            frame.background.radius ^ 2
                                        )
                                      +
                                      reggeWheelerSchwarzschildExteriorFactor
                                            frame.background *
                                          (
                                            reggeWheelerOddParityVacuumCPMRadialCoefficient
                                                cpmJet.secondJet.firstJet *
                                              reggeWheelerOddParityVectorHarmonicValue
                                                harmonicJet.firstJet.harmonic
                                                .theta
                                          ) *
                                        (
                                          -2 /
                                            frame.background.radius ^ 3
                                        )
                                    )
                                  ) *
                                      (
                                        2 *
                                          frame.background.radius
                                      )
                                    +
                                    (
                                      -(
                                        reggeWheelerSchwarzschildExteriorFactor
                                              frame.background *
                                            (
                                              reggeWheelerOddParityVacuumCPMRadialCoefficient
                                                  cpmJet.secondJet.firstJet *
                                                reggeWheelerOddParityVectorHarmonicValue
                                                  harmonicJet.firstJet.harmonic
                                                  .theta
                                            ) *
                                          (
                                            1 /
                                              frame.background.radius ^ 2
                                          )
                                      )
                                    ) *
                                      2

                              | .phi =>
                                  reggeWheelerOddParityLinearizedInverseMetricComponentPartial
                                        frame
                                        (
                                          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                                            cpmJet
                                            harmonicJet
                                        )
                                        .radial
                                        .radial
                                        .phi *
                                      (
                                        2 *
                                          frame.background.radius *
                                            Real.sin frame.polarAngle ^ 2
                                      )
                                    +
                                    reggeWheelerOddParityLinearizedInverseMetricComponent
                                          frame
                                          (
                                            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                                              cpmJet
                                              harmonicJet
                                          ).firstJet
                                          .radial
                                          .phi *
                                        (
                                          2 *
                                            Real.sin frame.polarAngle ^ 2
                                        )
                            )
                        -
                        value
                  )
                  (
                    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativePartial_eq_halfFourInverseMetricCoordinateSummands
                      frame
                      cpmJet
                      harmonicJet
                      angular
                  )

/--
The inverse-metric `.time` summand in the retained second radial
connection derivative

`∂ₐ δΓʳ_{rr}`

is expanded into the four product-rule terms defining the derivative of
the linearized Christoffel summand.

The four terms retain, respectively,

1. the linearized inverse-metric partial times the background kernel;
2. the linearized inverse-metric value times the background-kernel partial;
3. the background inverse-metric partial times the perturbation kernel;
4. the background inverse-metric value times the perturbation-kernel partial.

No factor is evaluated and no term is simplified, canceled, combined,
factored, or asserted to vanish. The radial, theta, and phi
inverse-metric summands of the second connection derivative remain
unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeTimeInverseMetricSummand_eq_fourProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (
          reggeWheelerAngularCoordinateToSpacetime
            angular
        )
        .radial
        .radial
        .radial
        .time =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (
              reggeWheelerAngularCoordinateToSpacetime
                angular
            )
            .radial
            .time *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            .radial
            .radial
            .time
        +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .time *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .radial
              .time
        +
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .time *
            reggeWheelerOddParityPerturbationConnectionKernel
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .radial
              .time
        +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .time *
            reggeWheelerOddParityPerturbationConnectionKernelPartial
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .radial
              .time := by
  rfl

/--
The angular coordinate partial of the Schwarzschild radial-time inverse-metric
component vanishes.

This is the background inverse-metric factor multiplying the perturbation
connection kernel in the third product-rule term of the second radial
connection derivative's `.time` inverse-metric summand.

No perturbation-kernel property is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeTimeBackgroundInverseMetricAngularPartialFactor_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildInverseMetricComponentPartial
        frame
        (
          reggeWheelerAngularCoordinateToSpacetime
            angular
        )
        .radial
        .time =
      0 := by
  cases angular <;> rfl

/--
The Schwarzschild radial-time inverse-metric component vanishes.

This is the background inverse-metric factor multiplying the perturbation
connection-kernel partial in the fourth product-rule term of the second radial
connection derivative's `.time` inverse-metric summand.

No perturbation-kernel-partial property is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeTimeBackgroundInverseMetricValueFactor_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildInverseMetricComponent
        frame
        .radial
        .time =
      0 := by
  rfl

/--
The inverse-metric `.time` summand in the retained second radial
connection derivative is reduced from four product-rule terms to its
first two terms.

The third term vanishes because its Schwarzschild radial-time
inverse-metric angular-partial factor is zero.

The fourth term vanishes because its Schwarzschild radial-time
inverse-metric value factor is zero.

The surviving terms are retained exactly:

1. the linearized inverse-metric partial times the background kernel;
2. the linearized inverse-metric value times the background-kernel partial.

Neither surviving term is unfolded, simplified, combined, canceled, or
factored. The radial, theta, and phi inverse-metric summands remain
unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeTimeInverseMetricSummand_eq_firstTwoProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (
          reggeWheelerAngularCoordinateToSpacetime
            angular
        )
        .radial
        .radial
        .radial
        .time =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (
              reggeWheelerAngularCoordinateToSpacetime
                angular
            )
            .radial
            .time *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            .radial
            .radial
            .time
        +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .time *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              (
                reggeWheelerAngularCoordinateToSpacetime
                  angular
              )
              .radial
              .radial
              .time := by
  have h :=
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeTimeInverseMetricSummand_eq_fourProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular

  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeTimeBackgroundInverseMetricAngularPartialFactor_eq_zero
      frame
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeTimeBackgroundInverseMetricValueFactor_eq_zero
      frame
  ] at h

  simpa only [
    zero_mul,
    add_zero
  ] using h

/--
The Schwarzschild background connection kernel with radial, radial, and time
indices vanishes:

`K̄_{rrt} = 0`.

This follows directly from the static diagonal Schwarzschild metric. No
perturbation identity, harmonic identity, vacuum equation, connection-product
term, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeBackgroundConnectionKernelRadialRadialTime_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame) :
    reggeWheelerSchwarzschildConnectionKernel
        frame
        .radial
        .radial
        .time =
      0 := by
  simp [
    reggeWheelerSchwarzschildConnectionKernel,
    reggeWheelerSchwarzschildMetricPartial
  ]
/--
Every angular coordinate partial of the Schwarzschild background connection
kernel `K̄_{rrt}` vanishes:

`∂ₐ K̄_{rrt} = 0`.

The result is a direct componentwise consequence of the explicit static
diagonal Schwarzschild metric second partials. No perturbation identity,
harmonic identity, vacuum equation, connection-product term, or master
residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeBackgroundConnectionKernelRadialRadialTimeAngularPartial_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildConnectionKernelPartial
        frame
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
        .time =
      0 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerSchwarzschildConnectionKernelPartial,
      reggeWheelerSchwarzschildMetricSecondPartial
    ]
/--
The inverse-metric `.time` summand in the retained second radial connection
derivative vanishes.

After the existing two-term product-rule reduction, the first term contains
`K̄_{rrt} = 0` and the second contains `∂ₐ K̄_{rrt} = 0`. The linearized
inverse-metric factors are retained unchanged. No harmonic identity, vacuum
equation, connection-product term, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeTimeInverseMetricSummand_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
        .radial
        .time =
      0 := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeTimeInverseMetricSummand_eq_firstTwoProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeBackgroundConnectionKernelRadialRadialTime_eq_zero
      frame,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeBackgroundConnectionKernelRadialRadialTimeAngularPartial_eq_zero
      frame
      angular
  ]
  ring
/--
The inverse-metric `.radial` summand in the retained second radial connection
derivative

`∂ₐ δΓʳ_{rr}`

is expanded into the four product-rule terms defining the derivative of the
linearized Christoffel summand.

The four terms retain, respectively,

1. the linearized inverse-metric partial times the background kernel;
2. the linearized inverse-metric value times the background-kernel partial;
3. the background inverse-metric partial times the perturbation kernel;
4. the background inverse-metric value times the perturbation-kernel partial.

No factor is evaluated and no term is simplified, canceled, combined,
factored, or asserted to vanish. The theta and phi inverse-metric summands of
the second connection derivative remain unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialInverseMetricSummand_eq_fourProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
        .radial
        .radial =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial *
        reggeWheelerSchwarzschildConnectionKernel
          frame
          .radial
          .radial
          .radial
      +
      reggeWheelerOddParityLinearizedInverseMetricComponent
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          .radial
          .radial *
        reggeWheelerSchwarzschildConnectionKernelPartial
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial
          .radial
      +
      reggeWheelerSchwarzschildInverseMetricComponentPartial
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial *
        reggeWheelerOddParityPerturbationConnectionKernel
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          .radial
          .radial
          .radial
      +
      reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .radial
          .radial *
        reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial
          .radial := by
  rfl
/--
Every angular coordinate partial of the Schwarzschild background inverse
radial-radial metric component vanishes:

`∂ₐ ḡ^{rr} = 0`.

The explicit inverse-metric derivative definition has a nonzero radial
radial-radial branch and sends both angular derivative coordinates to its
zero fallback branch. No perturbation identity, harmonic identity, vacuum
equation, connection-product term, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialBackgroundInverseMetricAngularPartialFactor_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerSchwarzschildInverseMetricComponentPartial
        frame
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial =
      0 := by
  cases angular <;>
    rfl
/--
The inverse-metric `.radial` summand in the retained second radial connection
derivative

`∂ₐ δΓʳ_{rr}`

reduces from four product-rule terms to its first, second, and fourth terms.

The third term vanishes because its background factor is the angular partial
of the Schwarzschild inverse radial-radial metric component,

`∂ₐ ḡ^{rr} = 0`.

The first, second, and fourth terms are preserved exactly. No remaining factor
is unfolded, simplified, canceled, combined, or asserted to vanish. The theta
and phi inverse-metric summands of the second connection derivative remain
unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialInverseMetricSummand_eq_firstSecondAndFourthProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
        .radial
        .radial =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial *
        reggeWheelerSchwarzschildConnectionKernel
          frame
          .radial
          .radial
          .radial
      +
      reggeWheelerOddParityLinearizedInverseMetricComponent
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          ).firstJet
          .radial
          .radial *
        reggeWheelerSchwarzschildConnectionKernelPartial
          frame
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial
          .radial
      +
      reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .radial
          .radial *
        reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial
          .radial := by
  simp only [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialInverseMetricSummand_eq_fourProductRuleTerms,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialBackgroundInverseMetricAngularPartialFactor_eq_zero,
    zero_mul,
    add_zero
  ]
/--
The odd-parity CPM linearized inverse-metric radial-radial value vanishes:

`δg^{rr} = 0`.

The proof uses the already established scalar-block theorem for the assembled
odd-parity spacetime perturbation and extracts its radial-radial conjunct.
No derivative identity, harmonic identity, vacuum equation,
connection-product term, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialLinearizedInverseMetricValueFactor_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet) :
    reggeWheelerOddParityLinearizedInverseMetricComponent
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        ).firstJet
        .radial
        .radial =
      0 := by
  change
    -(
      reggeWheelerSchwarzschildInverseMetricDiagonal frame .radial *
        (
          reggeWheelerOddParityVacuumCPMMetricFirstJet
            cpmJet.secondJet
            harmonicJet.firstJet
        ).metricValue .radial .radial *
        reggeWheelerSchwarzschildInverseMetricDiagonal frame .radial
    ) = 0
  rw [reggeWheelerOddParityVacuumCPMMetricFirstJet_metricValue]
  rw [
    (
      reggeWheelerOddParitySpacetimeMetricPerturbation_scalarBlock_zero
        (reggeWheelerOddParityVacuumCPMMetricComponents cpmJet.secondJet.firstJet)
        harmonicJet.firstJet.harmonic
    ).2.2
  ]
  simp
/--
The inverse-metric `.radial` summand in the retained second radial connection
derivative

`∂ₐ δΓʳ_{rr}`

reduces from its first, second, and fourth product-rule terms to only its first
and fourth terms.

The second term vanishes because its linearized inverse-metric radial-radial
value factor is zero,

`δg^{rr} = 0`.

The first and fourth terms are preserved exactly. No remaining factor is
unfolded, simplified, canceled, combined, or asserted to vanish. The theta and
phi inverse-metric summands of the second connection derivative remain
unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialInverseMetricSummand_eq_firstAndFourthProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
        .radial
        .radial =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
          frame
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial *
        reggeWheelerSchwarzschildConnectionKernel
          frame
          .radial
          .radial
          .radial
      +
      reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .radial
          .radial *
        reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial
          .radial := by
  simp only [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialInverseMetricSummand_eq_firstSecondAndFourthProductRuleTerms,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialLinearizedInverseMetricValueFactor_eq_zero,
    zero_mul,
    add_zero
  ]
/--
Every angular coordinate partial of the odd-parity CPM radial-radial metric
component vanishes:

`∂ₐ h_{rr} = 0`.

The concrete CPM first-jet metric-partial definition contains only
time-angular and radial-angular perturbation components. Its radial-radial
entry therefore reaches the zero fallback branch for either angular
derivative coordinate.

No inverse-metric identity, connection-kernel identity, harmonic eigenvalue,
vacuum equation, connection-product reduction, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialMetricAngularPartialFactor_eq_zero
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    (
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
        cpmJet
        harmonicJet
    ).firstJet.metricPartial
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial =
      0 := by
  cases angular <;>
    rfl
/--
Every angular coordinate partial of the odd-parity CPM linearized inverse
radial-radial metric component vanishes:

`∂ₐ δg^{rr} = 0`.

In the defining three-term product rule, the first and third terms contain the
already proved zero angular partial of the background inverse radial-radial
metric component. The middle term contains the already proved zero angular
partial of the CPM radial-radial perturbation component.

No connection-kernel identity, harmonic eigenvalue, vacuum equation,
connection-product reduction, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialLinearizedInverseMetricAngularPartialFactor_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedInverseMetricComponentPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial =
      0 := by
  unfold reggeWheelerOddParityLinearizedInverseMetricComponentPartial
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialBackgroundInverseMetricAngularPartialFactor_eq_zero
      frame
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialMetricAngularPartialFactor_eq_zero
      cpmJet
      harmonicJet
      angular
  ]
  ring
/--
The inverse-metric `.radial` summand in the retained second radial connection
derivative reduces to product-rule term 4 alone.

The previous two-term theorem retains product-rule terms 1 and 4. Term 1
vanishes because its linearized inverse radial-radial angular-partial factor
has been proved zero. Term 4 is preserved exactly and is not unfolded,
simplified, canceled, factored, or asserted to vanish.

The theta and phi inverse-metric summands of the second connection derivative
remain unchanged. No harmonic eigenvalue, vacuum equation, connection-product
reduction, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialInverseMetricSummand_eq_fourthProductRuleTerm
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
        .radial
        .radial =
      reggeWheelerSchwarzschildInverseMetricComponent
          frame
          .radial
          .radial *
        reggeWheelerOddParityPerturbationConnectionKernelPartial
          (
            reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
              cpmJet
              harmonicJet
          )
          (reggeWheelerAngularCoordinateToSpacetime angular)
          .radial
          .radial
          .radial := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialInverseMetricSummand_eq_firstAndFourthProductRuleTerms
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialLinearizedInverseMetricAngularPartialFactor_eq_zero
      frame
      cpmJet
      harmonicJet
      angular,
    zero_mul,
    zero_add
  ]
/--
Every angular coordinate partial of the odd-parity CPM perturbation connection
kernel with three radial indices vanishes:

`∂ₐ K[h]_{rrr} = 0`.

After unfolding the perturbation connection kernel partial, all three signed
terms contain the radial-radial CPM metric second partial. The concrete CPM
metric-second-partial definition sends that perturbation component to its zero
fallback branch.

No inverse-metric identity, harmonic eigenvalue, vacuum equation,
connection-product reduction, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialPerturbationConnectionKernelAngularPartialFactor_eq_zero
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernelPartial
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
        .radial =
      0 := by
  cases angular <;>
    simp [
      reggeWheelerAngularCoordinateToSpacetime,
      reggeWheelerOddParityPerturbationConnectionKernelPartial,
      reggeWheelerOddParityRWGaugeMetricComponentsOfMaster,
      reggeWheelerOddParityRWRadialCoefficientFromMaster,
      reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricComponents,
      reggeWheelerOddParityVacuumCPMMetricFirstJet,
      reggeWheelerOddParityVacuumCPMMetricSecondJet,
      reggeWheelerOddParityVacuumCPMMetricSecondPartial,
      reggeWheelerOddParityVacuumCPMRWMaster,
      reggeWheelerOddParityVacuumCPMTimeCoefficient,
      reggeWheelerSchwarzschildExteriorFactor
    ]
/--
The inverse-metric `.radial` summand in the retained second radial connection
derivative vanishes:

`∂ₐ δΓʳ_{rr} |_{ρ = r} = 0`.

The previous reduction leaves only product-rule term 4,

`ḡ^{rr} ∂ₐ K[h]_{rrr}`,

and the perturbation-kernel angular-partial factor has been proved zero. The
background inverse-metric factor is retained and no division or nonvanishing
argument is used.

The `.theta` and `.phi` inverse-metric summands of the second connection
derivative remain unchanged. No harmonic eigenvalue, vacuum equation,
connection-product reduction, or master residual is used.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialInverseMetricSummand_eq_zero
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
        .radial
        .radial =
      0 := by
  rw [
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialInverseMetricSummand_eq_fourthProductRuleTerm
      frame
      cpmJet
      harmonicJet
      angular,
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeRadialPerturbationConnectionKernelAngularPartialFactor_eq_zero
      cpmJet
      harmonicJet
      angular,
    mul_zero
  ]
/--
The inverse-metric `.theta` summand in the retained second radial connection
derivative

`∂ₐ δΓʳ_{rr}`

is expanded into the four product-rule terms defining the derivative of the
linearized Christoffel summand.

The four terms retain, respectively,

1. the linearized inverse-metric partial times the background kernel;
2. the linearized inverse-metric value times the background-kernel partial;
3. the background inverse-metric partial times the perturbation kernel;
4. the background inverse-metric value times the perturbation-kernel partial.

No factor is evaluated and no term is simplified, canceled, combined,
factored, or asserted to vanish. The `.phi` inverse-metric summand remains
unchanged.
-/
theorem
    prizcarbonOddParityVacuumCPMLinearizedRicciRadialAngularPrincipalDerivativeRadialSecondConnectionDerivativeThetaInverseMetricSummand_eq_fourProductRuleTerms
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet : ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (angular : ReggeWheelerAngularCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        (
          reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
            cpmJet
            harmonicJet
        )
        (reggeWheelerAngularCoordinateToSpacetime angular)
        .radial
        .radial
        .radial
        .theta =
      reggeWheelerOddParityLinearizedInverseMetricComponentPartial
            frame
            (
              reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                cpmJet
                harmonicJet
            )
            (reggeWheelerAngularCoordinateToSpacetime angular)
            .radial
            .theta *
          reggeWheelerSchwarzschildConnectionKernel
            frame
            .radial
            .radial
            .theta
        +
        reggeWheelerOddParityLinearizedInverseMetricComponent
              frame
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .theta *
            reggeWheelerSchwarzschildConnectionKernelPartial
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .radial
              .theta
        +
        reggeWheelerSchwarzschildInverseMetricComponentPartial
              frame
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .theta *
            reggeWheelerOddParityPerturbationConnectionKernel
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              ).firstJet
              .radial
              .radial
              .theta
        +
        reggeWheelerSchwarzschildInverseMetricComponent
              frame
              .radial
              .theta *
            reggeWheelerOddParityPerturbationConnectionKernelPartial
              (
                reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
                  cpmJet
                  harmonicJet
              )
              (reggeWheelerAngularCoordinateToSpacetime angular)
              .radial
              .radial
              .theta := by
  rfl
def
    prizcarbonOddParityVacuumCPMLinearizedRicciTimeTimeDiagonalZeroBoundary :
    String :=
  "FIRST_RADIAL_THETA_INVERSE_METRIC_SUMMAND_COMPLETE_ANGULAR_CASE_THEOREM_THETA_BRANCH_TWO_FULLY_EXPLICIT_UNCOMBINED_PRODUCT_RULE_TERMS_PHI_BRANCH_ZERO_FIRST_RADIAL_PHI_INVERSE_METRIC_SUMMAND_COMPLETE_ANGULAR_CASE_THEOREM_THETA_BRANCH_ZERO_PHI_BRANCH_TWO_EXPLICIT_KERNEL_WEIGHTED_LINEARIZED_INVERSE_TERMS_LINEARIZED_INVERSE_FACTORS_UNCHANGED_PRINCIPAL_RADIAL_FIRST_CONNECTION_DERIVATIVE_CONTRACTION_COMPLETE_ANGULAR_CASE_THEOREM_THETA_BRANCH_EXPLICIT_THETA_INVERSE_METRIC_SUMMAND_PHI_BRANCH_EXPLICIT_PHI_INVERSE_METRIC_SUMMAND_DIRECT_LINEARIZED_CHRISTOFFEL_PARTIAL_EQ_ONE_HALF_TIMES_COMPLETE_EXPLICIT_ANGULAR_CASE_CONTRACTION_SUBSTITUTED_INTO_PRINCIPAL_RADIAL_COORDINATE_CONTRIBUTION_SECOND_CONNECTION_DERIVATIVE_RETAINED_EXACTLY_SECOND_CONNECTION_DERIVATIVE_PARTIAL_EXPANDED_TO_ONE_HALF_TIMES_FOUR_UNSIMPLIFIED_INVERSE_METRIC_COORDINATE_SUMMANDS_SUBSTITUTED_INTO_PRINCIPAL_RADIAL_COORDINATE_CONTRIBUTION_ALL_FOUR_SECOND_CONNECTION_DERIVATIVE_SUMMANDS_RETAINED_UNSIMPLIFIED_SECOND_CONNECTION_DERIVATIVE_TIME_INVERSE_METRIC_SUMMAND_EXPANDED_TO_FOUR_UNSIMPLIFIED_PRODUCT_RULE_TERMS_BACKGROUND_RADIAL_TIME_INVERSE_METRIC_ANGULAR_PARTIAL_AND_VALUE_FACTORS_PROVED_ZERO_FIRST_TWO_PRODUCT_RULE_TERMS_UNCHANGED_THIRD_AND_FOURTH_PRODUCT_RULE_TERMS_REMOVED_TIME_SUMMAND_REDUCED_TO_FIRST_TWO_PRODUCT_RULE_TERMS"

end

end Chronos.Frontier
