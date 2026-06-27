import Chronos.Frontier.GravityPrimitiveMetricInstantiation

namespace Chronos
namespace Frontier

/--
Weakest metric-law constraint target.

This is the first physical constraint layer after merely producing a candidate
metric. It requires a predicate that says when the constructed metric satisfies
the intended metric law.
-/
structure GravityMetricLawConstraintTarget
    extends GravityPrimitiveMetricInstantiation where
  satisfiesMetricLaw : emergentMetric → Prop
  constructedMetricSatisfiesLaw :
    satisfiesMetricLaw (constructMetric primitiveWitness)

/--
The primitive-instantiated candidate metric satisfies the declared metric law.
-/
theorem primitive_metric_satisfies_declared_law
    (G : GravityMetricLawConstraintTarget) :
    G.satisfiesMetricLaw (G.constructMetric G.primitiveWitness) := by
  exact G.constructedMetricSatisfiesLaw

end Frontier
end Chronos
