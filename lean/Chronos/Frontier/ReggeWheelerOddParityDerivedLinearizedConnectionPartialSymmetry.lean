import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMLoweredRiemannPairExchangeResidual

namespace Chronos.Frontier

noncomputable section

/--
The concrete Schwarzschild metric second partial is symmetric in its two
covariant metric indices.
-/
theorem
    reggeWheelerSchwarzschildMetricSecondPartial_metricIndices_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (derivativeOuter derivativeInner metricLeft metricRight :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerSchwarzschildMetricSecondPartial
        frame
        derivativeOuter
        derivativeInner
        metricLeft
        metricRight =
      reggeWheelerSchwarzschildMetricSecondPartial
        frame
        derivativeOuter
        derivativeInner
        metricRight
        metricLeft := by
  cases derivativeOuter <;>
    cases derivativeInner <;>
      cases metricLeft <;>
        cases metricRight <;>
          rfl

/--
The derivative of the Schwarzschild background connection kernel is
symmetric in its two connection-lower indices.
-/
theorem
    reggeWheelerSchwarzschildConnectionKernelPartial_lower_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerSchwarzschildConnectionKernelPartial
        frame
        derivative
        lowerLeft
        lowerRight
        contraction =
      reggeWheelerSchwarzschildConnectionKernelPartial
        frame
        derivative
        lowerRight
        lowerLeft
        contraction := by
  have hMetric :
      reggeWheelerSchwarzschildMetricSecondPartial
          frame
          derivative
          contraction
          lowerLeft
          lowerRight =
        reggeWheelerSchwarzschildMetricSecondPartial
          frame
          derivative
          contraction
          lowerRight
          lowerLeft := by
    exact
      reggeWheelerSchwarzschildMetricSecondPartial_metricIndices_symmetric
        frame
        derivative
        contraction
        lowerLeft
        lowerRight

  unfold reggeWheelerSchwarzschildConnectionKernelPartial
  rw [hMetric]
  ring

/--
The derivative of the perturbation connection kernel is symmetric in its two
connection-lower indices when the metric second partial is symmetric in its
two metric indices.
-/
theorem
    reggeWheelerOddParityPerturbationConnectionKernelPartial_lower_symmetric
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (hMetricIndicesSymmetric :
      ∀ derivativeOuter derivativeInner metricLeft metricRight,
        jet.metricSecondPartial
            derivativeOuter
            derivativeInner
            metricLeft
            metricRight =
          jet.metricSecondPartial
            derivativeOuter
            derivativeInner
            metricRight
            metricLeft)
    (derivative lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityPerturbationConnectionKernelPartial
        jet
        derivative
        lowerLeft
        lowerRight
        contraction =
      reggeWheelerOddParityPerturbationConnectionKernelPartial
        jet
        derivative
        lowerRight
        lowerLeft
        contraction := by
  have hMetric :
      jet.metricSecondPartial
          derivative
          contraction
          lowerLeft
          lowerRight =
        jet.metricSecondPartial
          derivative
          contraction
          lowerRight
          lowerLeft := by
    exact
      hMetricIndicesSymmetric
        derivative
        contraction
        lowerLeft
        lowerRight

  unfold reggeWheelerOddParityPerturbationConnectionKernelPartial
  rw [hMetric]
  ring

/--
Each product-rule summand in the derivative of the linearized Christoffel
symbol is symmetric in the two lower Christoffel indices.
-/
theorem
    reggeWheelerOddParityLinearizedChristoffelSummandPartial_lower_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (hMetricIndicesSymmetric :
      ∀ derivativeOuter derivativeInner metricLeft metricRight,
        jet.metricSecondPartial
            derivativeOuter
            derivativeInner
            metricLeft
            metricRight =
          jet.metricSecondPartial
            derivativeOuter
            derivativeInner
            metricRight
            metricLeft)
    (derivative upper lowerLeft lowerRight contraction :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        jet
        derivative
        upper
        lowerLeft
        lowerRight
        contraction =
      reggeWheelerOddParityLinearizedChristoffelSummandPartial
        frame
        jet
        derivative
        upper
        lowerRight
        lowerLeft
        contraction := by
  have hBackgroundKernel :
      reggeWheelerSchwarzschildConnectionKernel
          frame
          lowerLeft
          lowerRight
          contraction =
        reggeWheelerSchwarzschildConnectionKernel
          frame
          lowerRight
          lowerLeft
          contraction := by
    exact
      reggeWheelerSchwarzschildConnectionKernel_lower_symmetric
        frame
        lowerLeft
        lowerRight
        contraction

  have hBackgroundKernelPartial :
      reggeWheelerSchwarzschildConnectionKernelPartial
          frame
          derivative
          lowerLeft
          lowerRight
          contraction =
        reggeWheelerSchwarzschildConnectionKernelPartial
          frame
          derivative
          lowerRight
          lowerLeft
          contraction := by
    exact
      reggeWheelerSchwarzschildConnectionKernelPartial_lower_symmetric
        frame
        derivative
        lowerLeft
        lowerRight
        contraction

  have hPerturbationKernel :
      reggeWheelerOddParityPerturbationConnectionKernel
          jet.firstJet
          lowerLeft
          lowerRight
          contraction =
        reggeWheelerOddParityPerturbationConnectionKernel
          jet.firstJet
          lowerRight
          lowerLeft
          contraction := by
    exact
      reggeWheelerOddParityPerturbationConnectionKernel_lower_symmetric
        jet.firstJet
        lowerLeft
        lowerRight
        contraction

  have hPerturbationKernelPartial :
      reggeWheelerOddParityPerturbationConnectionKernelPartial
          jet
          derivative
          lowerLeft
          lowerRight
          contraction =
        reggeWheelerOddParityPerturbationConnectionKernelPartial
          jet
          derivative
          lowerRight
          lowerLeft
          contraction := by
    exact
      reggeWheelerOddParityPerturbationConnectionKernelPartial_lower_symmetric
        jet
        hMetricIndicesSymmetric
        derivative
        lowerLeft
        lowerRight
        contraction

  unfold reggeWheelerOddParityLinearizedChristoffelSummandPartial

  rw [
    hBackgroundKernel,
    hBackgroundKernelPartial,
    hPerturbationKernel,
    hPerturbationKernelPartial
  ]

/--
The full coordinate derivative of the metric-derived linearized Christoffel
symbol is symmetric in its two lower Christoffel indices.
-/
theorem
    reggeWheelerOddParityLinearizedChristoffelPartial_lower_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (hMetricIndicesSymmetric :
      ∀ derivativeOuter derivativeInner metricLeft metricRight,
        jet.metricSecondPartial
            derivativeOuter
            derivativeInner
            metricLeft
            metricRight =
          jet.metricSecondPartial
            derivativeOuter
            derivativeInner
            metricRight
            metricLeft)
    (derivative upper lowerLeft lowerRight :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityLinearizedChristoffelPartial
        frame
        jet
        derivative
        upper
        lowerLeft
        lowerRight =
      reggeWheelerOddParityLinearizedChristoffelPartial
        frame
        jet
        derivative
        upper
        lowerRight
        lowerLeft := by
  have hPointwise :
      ∀ contraction,
        reggeWheelerOddParityLinearizedChristoffelSummandPartial
            frame
            jet
            derivative
            upper
            lowerLeft
            lowerRight
            contraction =
          reggeWheelerOddParityLinearizedChristoffelSummandPartial
            frame
            jet
            derivative
            upper
            lowerRight
            lowerLeft
            contraction := by
    intro contraction

    exact
      reggeWheelerOddParityLinearizedChristoffelSummandPartial_lower_symmetric
        frame
        jet
        hMetricIndicesSymmetric
        derivative
        upper
        lowerLeft
        lowerRight
        contraction

  unfold reggeWheelerOddParityLinearizedChristoffelPartial

  apply congrArg (fun value : ℝ => (1 / 2 : ℝ) * value)

  exact
    reggeWheelerSpacetimeCoordinateContraction_congr
      (
        fun contraction =>
          reggeWheelerOddParityLinearizedChristoffelSummandPartial
            frame
            jet
            derivative
            upper
            lowerLeft
            lowerRight
            contraction
      )
      (
        fun contraction =>
          reggeWheelerOddParityLinearizedChristoffelSummandPartial
            frame
            jet
            derivative
            upper
            lowerRight
            lowerLeft
            contraction
      )
      hPointwise

/--
The connection-partial field of the metric-derived linearized connection
first jet is symmetric in its two lower connection indices.
-/
theorem
    reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet_connectionPartial_lower_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (hMetricIndicesSymmetric :
      ∀ derivativeOuter derivativeInner metricLeft metricRight,
        jet.metricSecondPartial
            derivativeOuter
            derivativeInner
            metricLeft
            metricRight =
          jet.metricSecondPartial
            derivativeOuter
            derivativeInner
            metricRight
            metricLeft)
    (derivative upper lowerLeft lowerRight :
      ReggeWheelerSpacetimeCoordinate) :
    (
      reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet
        frame
        jet
    ).connectionPartial
        derivative
        upper
        lowerLeft
        lowerRight =
      (
        reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet
          frame
          jet
      ).connectionPartial
        derivative
        upper
        lowerRight
        lowerLeft := by
  exact
    reggeWheelerOddParityLinearizedChristoffelPartial_lower_symmetric
      frame
      jet
      hMetricIndicesSymmetric
      derivative
      upper
      lowerLeft
      lowerRight

/--
The concrete CPM-derived linearized connection first jet has a
lower-index-symmetric connection-partial field.

This requires no angular mixed-partial commutation assumption.
-/
theorem
    reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet_connectionPartial_lower_symmetric
    (frame : ReggeWheelerSchwarzschildStaticDetectorFrame)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (derivative upper lowerLeft lowerRight :
      ReggeWheelerSpacetimeCoordinate) :
    (
      reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
        frame
        cpmJet
        harmonicJet
    ).connectionPartial
        derivative
        upper
        lowerLeft
        lowerRight =
      (
        reggeWheelerOddParityVacuumCPMDerivedLinearizedConnectionFirstJet
          frame
          cpmJet
          harmonicJet
      ).connectionPartial
        derivative
        upper
        lowerRight
        lowerLeft := by
  apply
    reggeWheelerOddParityLinearizedConnectionFirstJetOfMetricSecondJet_connectionPartial_lower_symmetric

  intro derivativeOuter derivativeInner metricLeft metricRight

  simpa [
    reggeWheelerOddParityVacuumCPMDerivedMetricSecondJet
  ] using
    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet_metricIndices_symmetric
        cpmJet
        harmonicJet
        derivativeOuter
        derivativeInner
        metricLeft
        metricRight
    )

def
    reggeWheelerOddParityDerivedLinearizedConnectionPartialSymmetryBoundary :
    String :=
  "THE_BACKGROUND_AND_PERTURBATION_CONNECTION_KERNEL_PARTIALS_THE_LINEARIZED_CHRISTOFFEL_PARTIAL_AND_THE_COMPLETE_CPM_DERIVED_LINEARIZED_CONNECTION_PARTIAL_ARE_NOW_PROVED_SYMMETRIC_IN_THE_TWO_LOWER_CONNECTION_INDICES_THIS_REMOVES_THE_CONNECTION_PARTIAL_LOWER_SYMMETRY_LAYER_FROM_THE_PAIR_EXCHANGE_RESIDUAL_FULL_RESIDUAL_PAIR_EXCHANGE_ANGULAR_HARMONIC_MIXED_PARTIAL_COMMUTATION_GLOBAL_GEODESIC_EVOLUTION_FRAME_TRANSPORT_AND_INTEGRATED_PHYSICAL_STRAIN_REMAIN_UNPROVED"

end

end Chronos.Frontier
