import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMMetricSecondJetCommutation
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMRadialGeodesicTidalSymmetryBridge

namespace Chronos.Frontier

noncomputable section

/--
The principal, second-coordinate-derivative contribution to the fully
covariant linearized Riemann tensor:

`P_abcd =
  1/2 (
      ∂_c∂_b h_ad
    + ∂_d∂_a h_bc
    - ∂_d∂_b h_ac
    - ∂_c∂_a h_bd
  )`.

This separates the highest-derivative curvature content from the lower-order
background-connection terms.
-/
def reggeWheelerOddParityMetricSecondJetPrincipalLoweredRiemann
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (first second third fourth : ReggeWheelerSpacetimeCoordinate) : ℝ :=
  (1 / 2 : ℝ) *
    (
      jet.metricSecondPartial
          third
          second
          first
          fourth +
        jet.metricSecondPartial
          fourth
          first
          second
          third -
        jet.metricSecondPartial
          fourth
          second
          first
          third -
        jet.metricSecondPartial
          third
          first
          second
          fourth
    )

/--
The principal linearized-curvature contribution satisfies pair exchange when:

* the two derivative coordinates commute;
* the two metric coordinates are symmetric.
-/
theorem
    reggeWheelerOddParityMetricSecondJetPrincipalLoweredRiemann_pairExchange
    (jet : ReggeWheelerOddParityMetricPerturbationSecondJet)
    (hDerivativeCommutes :
      ∀ derivativeOuter derivativeInner metricLeft metricRight,
        jet.metricSecondPartial
            derivativeOuter
            derivativeInner
            metricLeft
            metricRight =
          jet.metricSecondPartial
            derivativeInner
            derivativeOuter
            metricLeft
            metricRight)
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
    (first second third fourth : ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityMetricSecondJetPrincipalLoweredRiemann
        jet
        first
        second
        third
        fourth =
      reggeWheelerOddParityMetricSecondJetPrincipalLoweredRiemann
        jet
        third
        fourth
        first
        second := by
  have hFirst :
      jet.metricSecondPartial
          third
          second
          first
          fourth =
        jet.metricSecondPartial
          second
          third
          fourth
          first := by
    calc
      jet.metricSecondPartial
          third
          second
          first
          fourth =
        jet.metricSecondPartial
          second
          third
          first
          fourth := by
            exact
              hDerivativeCommutes
                third
                second
                first
                fourth

      _ =
        jet.metricSecondPartial
          second
          third
          fourth
          first := by
            exact
              hMetricIndicesSymmetric
                second
                third
                first
                fourth

  have hSecond :
      jet.metricSecondPartial
          fourth
          first
          second
          third =
        jet.metricSecondPartial
          first
          fourth
          third
          second := by
    calc
      jet.metricSecondPartial
          fourth
          first
          second
          third =
        jet.metricSecondPartial
          first
          fourth
          second
          third := by
            exact
              hDerivativeCommutes
                fourth
                first
                second
                third

      _ =
        jet.metricSecondPartial
          first
          fourth
          third
          second := by
            exact
              hMetricIndicesSymmetric
                first
                fourth
                second
                third

  have hThird :
      jet.metricSecondPartial
          fourth
          second
          first
          third =
        jet.metricSecondPartial
          second
          fourth
          third
          first := by
    calc
      jet.metricSecondPartial
          fourth
          second
          first
          third =
        jet.metricSecondPartial
          second
          fourth
          first
          third := by
            exact
              hDerivativeCommutes
                fourth
                second
                first
                third

      _ =
        jet.metricSecondPartial
          second
          fourth
          third
          first := by
            exact
              hMetricIndicesSymmetric
                second
                fourth
                first
                third

  have hFourth :
      jet.metricSecondPartial
          third
          first
          second
          fourth =
        jet.metricSecondPartial
          first
          third
          fourth
          second := by
    calc
      jet.metricSecondPartial
          third
          first
          second
          fourth =
        jet.metricSecondPartial
          first
          third
          second
          fourth := by
            exact
              hDerivativeCommutes
                third
                first
                second
                fourth

      _ =
        jet.metricSecondPartial
          first
          third
          fourth
          second := by
            exact
              hMetricIndicesSymmetric
                first
                third
                second
                fourth

  unfold
    reggeWheelerOddParityMetricSecondJetPrincipalLoweredRiemann

  rw [
    hFirst,
    hSecond,
    hThird,
    hFourth
  ]

  ring

/--
The complete CPM-reconstructed metric second partial is symmetric in its two
metric coordinates.

This property is definitional for the existing odd-parity metric
reconstruction and introduces no additional hypothesis.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricSecondPartial_metricIndices_symmetric
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (derivativeOuter derivativeInner metricLeft metricRight :
      ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityVacuumCPMMetricSecondPartial
        cpmJet
        harmonicJet
        derivativeOuter
        derivativeInner
        metricLeft
        metricRight =
      reggeWheelerOddParityVacuumCPMMetricSecondPartial
        cpmJet
        harmonicJet
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
The concrete CPM metric second jet inherits symmetry in its two metric
coordinates.
-/
theorem
    reggeWheelerOddParityVacuumCPMMetricSecondJet_metricIndices_symmetric
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (derivativeOuter derivativeInner metricLeft metricRight :
      ReggeWheelerSpacetimeCoordinate) :
    (
      reggeWheelerOddParityVacuumCPMMetricSecondJet
        cpmJet
        harmonicJet
    ).metricSecondPartial
        derivativeOuter
        derivativeInner
        metricLeft
        metricRight =
      (
        reggeWheelerOddParityVacuumCPMMetricSecondJet
          cpmJet
          harmonicJet
      ).metricSecondPartial
        derivativeOuter
        derivativeInner
        metricRight
        metricLeft := by
  exact
    reggeWheelerOddParityVacuumCPMMetricSecondPartial_metricIndices_symmetric
      cpmJet
      harmonicJet
      derivativeOuter
      derivativeInner
      metricLeft
      metricRight

/--
The principal second-derivative part of the CPM-derived lowered linearized
Riemann tensor satisfies pair exchange under the explicit angular harmonic
mixed-partial commutation hypothesis.
-/
theorem
    reggeWheelerOddParityVacuumCPMPrincipalLoweredRiemann_pairExchange
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hHarmonicSymm :
      ∀ derivativeLeft derivativeRight angularCoordinate,
        harmonicJet.vectorCoordinateSecondPartial
            derivativeLeft
            derivativeRight
            angularCoordinate =
          harmonicJet.vectorCoordinateSecondPartial
            derivativeRight
            derivativeLeft
            angularCoordinate)
    (first second third fourth : ReggeWheelerSpacetimeCoordinate) :
    reggeWheelerOddParityMetricSecondJetPrincipalLoweredRiemann
        (
          reggeWheelerOddParityVacuumCPMMetricSecondJet
            cpmJet
            harmonicJet
        )
        first
        second
        third
        fourth =
      reggeWheelerOddParityMetricSecondJetPrincipalLoweredRiemann
        (
          reggeWheelerOddParityVacuumCPMMetricSecondJet
            cpmJet
            harmonicJet
        )
        third
        fourth
        first
        second := by
  exact
    reggeWheelerOddParityMetricSecondJetPrincipalLoweredRiemann_pairExchange
      (
        reggeWheelerOddParityVacuumCPMMetricSecondJet
          cpmJet
          harmonicJet
      )
      (
        reggeWheelerOddParityVacuumCPMMetricSecondJet_derivatives_commute
          cpmJet
          harmonicJet
          hHarmonicSymm
      )
      (
        reggeWheelerOddParityVacuumCPMMetricSecondJet_metricIndices_symmetric
          cpmJet
          harmonicJet
      )
      first
      second
      third
      fourth

/--
The exact residual after subtracting the manifestly pair-symmetric principal
second-derivative contribution from the complete CPM-derived lowered
linearized Riemann tensor.
-/
def reggeWheelerOddParityVacuumCPMRadialGeodesicPairExchangeResidual
    (observer : ReggeWheelerSchwarzschildRadialGeodesicPointData)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (first second third fourth : ReggeWheelerSpacetimeCoordinate) : ℝ :=
  reggeWheelerOddParityVacuumCPMRadialGeodesicLoweredRiemann
      observer
      cpmJet
      harmonicJet
      first
      second
      third
      fourth -
    reggeWheelerOddParityMetricSecondJetPrincipalLoweredRiemann
      (
        reggeWheelerOddParityVacuumCPMMetricSecondJet
          cpmJet
          harmonicJet
      )
      first
      second
      third
      fourth

/--
Once the principal second-derivative contribution is proved pair symmetric,
full pair exchange is exactly equivalent to pair exchange of the remaining
lower-order residual.
-/
theorem
    reggeWheelerOddParityVacuumCPMRadialGeodesicLoweredRiemann_pairExchange_iff_residualPairExchange
    (observer : ReggeWheelerSchwarzschildRadialGeodesicPointData)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hHarmonicSymm :
      ∀ derivativeLeft derivativeRight angularCoordinate,
        harmonicJet.vectorCoordinateSecondPartial
            derivativeLeft
            derivativeRight
            angularCoordinate =
          harmonicJet.vectorCoordinateSecondPartial
            derivativeRight
            derivativeLeft
            angularCoordinate)
    (first second third fourth : ReggeWheelerSpacetimeCoordinate) :
    (
      reggeWheelerOddParityVacuumCPMRadialGeodesicLoweredRiemann
          observer
          cpmJet
          harmonicJet
          first
          second
          third
          fourth =
        reggeWheelerOddParityVacuumCPMRadialGeodesicLoweredRiemann
          observer
          cpmJet
          harmonicJet
          third
          fourth
          first
          second
    ) ↔
    (
      reggeWheelerOddParityVacuumCPMRadialGeodesicPairExchangeResidual
          observer
          cpmJet
          harmonicJet
          first
          second
          third
          fourth =
        reggeWheelerOddParityVacuumCPMRadialGeodesicPairExchangeResidual
          observer
          cpmJet
          harmonicJet
          third
          fourth
          first
          second
    ) := by
  have hPrincipal :
      reggeWheelerOddParityMetricSecondJetPrincipalLoweredRiemann
          (
            reggeWheelerOddParityVacuumCPMMetricSecondJet
              cpmJet
              harmonicJet
          )
          first
          second
          third
          fourth =
        reggeWheelerOddParityMetricSecondJetPrincipalLoweredRiemann
          (
            reggeWheelerOddParityVacuumCPMMetricSecondJet
              cpmJet
              harmonicJet
          )
          third
          fourth
          first
          second := by
    exact
      reggeWheelerOddParityVacuumCPMPrincipalLoweredRiemann_pairExchange
        cpmJet
        harmonicJet
        hHarmonicSymm
        first
        second
        third
        fourth

  unfold
    reggeWheelerOddParityVacuumCPMRadialGeodesicPairExchangeResidual

  constructor
  · intro hFull
    rw [
      hFull,
      hPrincipal
    ]

  · intro hResidual
    linarith

/--
Pair exchange of the isolated residual is sufficient to close symmetry of the
radial-geodesic CPM tidal matrix.
-/
theorem
    reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature_symmetric_of_residualPairExchange
    (observer : ReggeWheelerSchwarzschildRadialGeodesicPointData)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (hHarmonicSymm :
      ∀ derivativeLeft derivativeRight angularCoordinate,
        harmonicJet.vectorCoordinateSecondPartial
            derivativeLeft
            derivativeRight
            angularCoordinate =
          harmonicJet.vectorCoordinateSecondPartial
            derivativeRight
            derivativeLeft
            angularCoordinate)
    (hResidualPairExchange :
      ∀ first second third fourth,
        reggeWheelerOddParityVacuumCPMRadialGeodesicPairExchangeResidual
              observer
              cpmJet
              harmonicJet
              first
              second
              third
              fourth =
          reggeWheelerOddParityVacuumCPMRadialGeodesicPairExchangeResidual
              observer
              cpmJet
              harmonicJet
              third
              fourth
              first
              second)
    (left right : ReggeWheelerDetectorSpatialAxis) :
    reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature
        observer
        cpmJet
        harmonicJet
        left
        right =
      reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature
        observer
        cpmJet
        harmonicJet
        right
        left := by
  have hFullPairExchange :
      ∀ first second third fourth,
        reggeWheelerOddParityVacuumCPMRadialGeodesicLoweredRiemann
              observer
              cpmJet
              harmonicJet
              first
              second
              third
              fourth =
          reggeWheelerOddParityVacuumCPMRadialGeodesicLoweredRiemann
              observer
              cpmJet
              harmonicJet
              third
              fourth
              first
              second := by
    intro first second third fourth

    exact
      (
        reggeWheelerOddParityVacuumCPMRadialGeodesicLoweredRiemann_pairExchange_iff_residualPairExchange
          observer
          cpmJet
          harmonicJet
          hHarmonicSymm
          first
          second
          third
          fourth
      ).2
        (
          hResidualPairExchange
            first
            second
            third
            fourth
        )

  exact
    reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature_symmetric_of_loweredRiemann_pairExchange
      observer
      cpmJet
      harmonicJet
      hFullPairExchange
      left
      right

def
    reggeWheelerOddParityVacuumCPMLoweredRiemannPairExchangeResidualBoundary :
    String :=
  "THE_PRINCIPAL_SECOND_DERIVATIVE_PART_OF_THE_CPM_DERIVED_FULLY_LOWERED_LINEARIZED_RIEMANN_SATISFIES_PAIR_EXCHANGE_UNDER_THE_EXPLICIT_ANGULAR_HARMONIC_MIXED_PARTIAL_COMMUTATION_HYPOTHESIS_FULL_PAIR_EXCHANGE_IS_NOW_EXACTLY_EQUIVALENT_TO_PAIR_EXCHANGE_OF_AN_ISOLATED_LOWER_ORDER_BACKGROUND_CONNECTION_RESIDUAL_THE_RESIDUAL_PAIR_EXCHANGE_GLOBAL_GEODESIC_EVOLUTION_FRAME_TRANSPORT_AND_INTEGRATED_PHYSICAL_STRAIN_REMAIN_UNPROVED"

end

end Chronos.Frontier
