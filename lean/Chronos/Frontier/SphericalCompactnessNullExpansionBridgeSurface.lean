import Chronos.Frontier.SphericalCollapseGateThresholdSurface
import Chronos.Frontier.SphericalNullExpansionCriterionSurface
import Chronos.Frontier.ConcreteGravityAnalyticEstimateReadiness

namespace Chronos
namespace Frontier

/--
Real-valued Hawking mass of a round symmetry sphere in the null-normal
normalization `g(l,n) = -2`.
-/
def sphericalHawkingMassGlnNegTwo
    (areaRadius outgoingExpansion ingoingExpansion : ℝ) : ℝ :=
  areaRadius / 2 *
    (1 + areaRadius ^ 2 * outgoingExpansion * ingoingExpansion / 4)

/--
Binding from the previously free `S.hawkingMass` scalar to the real round-sphere
Hawking formula in the fixed `g(l,n) = -2` normalization.  This records the
chosen normalization and round-sphere formula only; it does not yet derive the
expansions from an areal-radius gradient.
-/
structure RealSphericalHawkingMassBinding
    {data : SelectedEinsteinMatterCauchyData}
    (S : AdmissibleQuasiLocalSurface data)
    (roundSymmetrySphere : Prop) where
  outgoingExpansion : ℝ
  ingoingExpansion : ℝ
  round : roundSymmetrySphere
  hawkingMass_eq :
    S.hawkingMass =
      sphericalHawkingMassGlnNegTwo
        S.areaRadius outgoingExpansion ingoingExpansion

/--
Repository-native bridge input from the spherical compactness threshold
`arealRadius <= 2 * misnerSharpMass` to the null-expansion sign condition.

The bridge field is explicit: this file records the interface-level bridge and
does not derive the geometric threshold-to-expansion theorem from Einstein
geometry.
-/
structure SphericalCompactnessNullExpansionBridgeInput where
  thresholdInput : SphericalCollapseGateInput
  expansionInput : SphericalNullExpansionInput
  threshold_to_outer_marginal :
    SphericalCollapseGate thresholdInput ->
      FutureOuterMarginalSphericalSurface expansionInput

def SphericalCompactnessToNullExpansionBridge
    (B : SphericalCompactnessNullExpansionBridgeInput) : Prop :=
  SphericalCollapseGate B.thresholdInput ->
    FutureOuterMarginalSphericalSurface B.expansionInput

theorem spherical_compactness_threshold_implies_outer_marginal_by_bridge
    (B : SphericalCompactnessNullExpansionBridgeInput) :
    SphericalCompactnessToNullExpansionBridge B := by
  intro h
  exact B.threshold_to_outer_marginal h

theorem spherical_compactness_threshold_implies_trapped_or_marginal_by_bridge
    (B : SphericalCompactnessNullExpansionBridgeInput) :
    SphericalCollapseGate B.thresholdInput ->
      TrappedOrMarginalByNullExpansions B.expansionInput := by
  intro h
  exact marginal_spherical_null_expansions_imply_trapped_or_marginal
    B.expansionInput
    (B.threshold_to_outer_marginal h)

/--
Boundary marker.

This file closes only the repository-native conditional bridge interface from
the spherical compactness gate to the spherical null-expansion criterion.
It does not prove the geometric threshold-to-expansion theorem, nonspherical
collapse exclusion, Cosmic Censorship, the Hoop Conjecture, or unrestricted
UniversalBoundaryCompactness.
-/
def SphericalCompactnessNullExpansionBridgeBoundary : Prop := True

theorem spherical_compactness_null_expansion_bridge_boundary_verified :
    SphericalCompactnessNullExpansionBridgeBoundary := by
  trivial

end Frontier
end Chronos
