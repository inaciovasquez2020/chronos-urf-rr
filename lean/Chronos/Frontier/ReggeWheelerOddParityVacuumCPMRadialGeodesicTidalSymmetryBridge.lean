import Mathlib
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMMetricSecondJetCommutation
import Chronos.Frontier.ReggeWheelerOddParityVacuumCPMRadialGeodesicDeviation

namespace Chronos.Frontier

noncomputable section

set_option maxRecDepth 100000
set_option maxHeartbeats 4000000

/--
Exchange the two coordinate pairs of a covariant rank-four tensor:

`Tᵖ_{αβγδ} = T_{γδαβ}`.
-/
def reggeWheelerSpacetimeRankFourPairExchange
    (tensor :
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ReggeWheelerSpacetimeCoordinate →
              ℝ) :
    ReggeWheelerSpacetimeCoordinate →
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ℝ :=
  fun first second third fourth =>
    tensor third fourth first second

/--
A pointwise pair-exchange theorem gives equality with the pair-exchanged
rank-four tensor.
-/
theorem reggeWheelerSpacetimeRankFour_eq_pairExchange
    (tensor :
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ReggeWheelerSpacetimeCoordinate →
              ℝ)
    (pairExchange :
      ∀ first second third fourth,
        tensor first second third fourth =
          tensor third fourth first second) :
    tensor =
      reggeWheelerSpacetimeRankFourPairExchange tensor := by
  funext first second third fourth
  exact pairExchange first second third fourth

/--
Projection of the pair-exchanged tensor swaps the first and third vectors
when the same vector occupies the second and fourth positions.

The proof expands both finite-contraction layers before polynomial
normalization.
-/
theorem
    reggeWheelerSpacetimeRankFourProjection_pairExchange
    (tensor :
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ReggeWheelerSpacetimeCoordinate →
              ℝ)
    (left time right : ReggeWheelerSpacetimeVectorValue) :
    reggeWheelerSpacetimeRankFourProjection
        (reggeWheelerSpacetimeRankFourPairExchange tensor)
        left
        time
        right
        time =
      reggeWheelerSpacetimeRankFourProjection
        tensor
        right
        time
        left
        time := by
  unfold reggeWheelerSpacetimeRankFourPairExchange
  unfold reggeWheelerSpacetimeRankFourProjection
  unfold reggeWheelerSpacetimeVectorContraction
  unfold reggeWheelerSpacetimeCoordinateContraction
  ring_nf

/--
Pair-exchange symmetry of a covariant rank-four tensor implies symmetry of
its tidal projection:

`T(e_a,u,e_b,u) = T(e_b,u,e_a,u)`.
-/
theorem
    reggeWheelerSpacetimeRankFourProjection_symmetric_of_pairExchange
    (tensor :
      ReggeWheelerSpacetimeCoordinate →
        ReggeWheelerSpacetimeCoordinate →
          ReggeWheelerSpacetimeCoordinate →
            ReggeWheelerSpacetimeCoordinate →
              ℝ)
    (pairExchange :
      ∀ first second third fourth,
        tensor first second third fourth =
          tensor third fourth first second)
    (left time right : ReggeWheelerSpacetimeVectorValue) :
    reggeWheelerSpacetimeRankFourProjection
        tensor
        left
        time
        right
        time =
      reggeWheelerSpacetimeRankFourProjection
        tensor
        right
        time
        left
        time := by
  calc
    reggeWheelerSpacetimeRankFourProjection
          tensor
          left
          time
          right
          time =
        reggeWheelerSpacetimeRankFourProjection
          (reggeWheelerSpacetimeRankFourPairExchange tensor)
          left
          time
          right
          time := by
            exact
              congrArg
                (
                  fun currentTensor =>
                    reggeWheelerSpacetimeRankFourProjection
                      currentTensor
                      left
                      time
                      right
                      time
                )
                (
                  reggeWheelerSpacetimeRankFour_eq_pairExchange
                    tensor
                    pairExchange
                )

    _ =
        reggeWheelerSpacetimeRankFourProjection
          tensor
          right
          time
          left
          time := by
            exact
              reggeWheelerSpacetimeRankFourProjection_pairExchange
                tensor
                left
                time
                right

/--
Pair exchange of the complete CPM-derived lowered linearized Riemann tensor
implies symmetry of the radial-geodesic tidal-curvature matrix.
-/
theorem
    reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature_symmetric_of_loweredRiemann_pairExchange
    (observer : ReggeWheelerSchwarzschildRadialGeodesicPointData)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (pairExchange :
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
  unfold
    reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature

  exact
    reggeWheelerSpacetimeRankFourProjection_symmetric_of_pairExchange
      (
        reggeWheelerOddParityVacuumCPMRadialGeodesicLoweredRiemann
          observer
          cpmJet
          harmonicJet
      )
      pairExchange
      (
        reggeWheelerSchwarzschildRadialGeodesicSpatialLeg
          observer
          left
      )
      (
        reggeWheelerSchwarzschildRadialGeodesicTimeLeg
          observer
      )
      (
        reggeWheelerSchwarzschildRadialGeodesicSpatialLeg
          observer
          right
      )

/--
Under lowered-Riemann pair exchange, every entry of the radial-geodesic
tidal matrix is symmetric.
-/
theorem
    reggeWheelerOddParityVacuumCPMRadialGeodesicTidalMatrix_symmetric
    (observer : ReggeWheelerSchwarzschildRadialGeodesicPointData)
    (cpmJet : ReggeWheelerOddParityVacuumCPMThirdJet)
    (harmonicJet :
      ReggeWheelerOddParityVectorHarmonicCoordinateSecondJet)
    (pairExchange :
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
              second) :
    ∀ left right,
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
  intro left right

  exact
    reggeWheelerOddParityVacuumCPMRadialGeodesicTidalCurvature_symmetric_of_loweredRiemann_pairExchange
      observer
      cpmJet
      harmonicJet
      pairExchange
      left
      right

def
    reggeWheelerOddParityVacuumCPMRadialGeodesicTidalSymmetryBridgeBoundary :
    String :=
  "LOWERED_RIEMANN_PAIR_EXCHANGE_IMPLIES_RADIAL_GEODESIC_TIDAL_MATRIX_SYMMETRY_BY_PAIR_EXCHANGED_FUNCTION_EQUALITY_AND_FULLY_EXPANDED_FINITE_COORDINATE_CONTRACTION_REINDEXING_TIDAL_SYMMETRY_IS_NO_LONGER_AN_INDEPENDENT_OBLIGATION_THE_REMAINING_ALGEBRAIC_CURVATURE_TARGET_IS_PAIR_EXCHANGE_FOR_THE_CPM_DERIVED_LOWERED_LINEARIZED_RIEMANN_UNDER_THE_EXPLICIT_ANGULAR_HARMONIC_SECOND_PARTIAL_COMMUTATION_HYPOTHESIS_GLOBAL_GEODESIC_EVOLUTION_FRAME_TRANSPORT_AND_INTEGRATED_PHYSICAL_STRAIN_REMAIN_UNPROVED"

end

end Chronos.Frontier
