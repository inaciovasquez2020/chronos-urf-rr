import Chronos.Frontier.GravityEmergentMetricConstruction

namespace Chronos
namespace Frontier

/--
Weakest primitive-state metric instantiation target.

This is the first nonempty instantiation layer after the abstract emergent
metric construction surface. It supplies one primitive state and therefore
one candidate emergent metric.
-/
structure GravityPrimitiveMetricInstantiation
    extends GravityEmergentMetricConstruction where
  primitiveWitness : primitiveState

/--
A primitive witness instantiates the emergent metric construction.
-/
theorem primitive_metric_instantiation_produces_candidate
    (G : GravityPrimitiveMetricInstantiation) :
    Nonempty G.emergentMetric := by
  exact ⟨G.constructMetric G.primitiveWitness⟩

end Frontier
end Chronos
