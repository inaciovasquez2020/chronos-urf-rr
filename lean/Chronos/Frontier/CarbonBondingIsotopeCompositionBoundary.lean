import Chronos.Frontier.KnownGravityLimitInterface
import Chronos.Frontier.CarbonBondingMetricBackreactionBoundary

namespace Chronos.Frontier

/--
Composition boundary from carbon bonding non-realization to the existing
same-radius Newtonian isotope mass-ratio bound.

This theorem does not derive metric backreaction, Einstein limit, stress-energy
realization, or solved gravity. It only proves that the carbon bonding boundary
remains non-realized while the field comparison stays inside the already
verified Newtonian same-radius mass-ratio bound.
-/
theorem carbonBondingBoundary_composes_with_carbon14_carbon12_gravity_ratio_bound
    (boundary : CarbonBondingMetricBackreactionBoundary)
    (cb : CarbonBondingStructure)
    (gHeavy gLight mHeavy mLight radius G : Real)
    (hradius : radius > 0)
    (hG : G > 0)
    (hmLight : mLight > 0)
    (hgLight : gLight = (G * mLight) / (radius ^ 2))
    (hgHeavy : gHeavy = (G * mHeavy) / (radius ^ 2))
    (hmassBound : mHeavy / mLight ≤ carbonIsotopeMassRatioBound) :
    boundary.bonding_to_metric_map cb = none ∧
      gHeavy / gLight ≤ carbonIsotopeMassRatioBound := by
  exact ⟨boundary.no_metric_backreaction_realization cb,
    carbon14_carbon12_gravity_ratio_bound
      gHeavy gLight mHeavy mLight radius G
      hradius hG hmLight hgLight hgHeavy hmassBound⟩

end Chronos.Frontier
