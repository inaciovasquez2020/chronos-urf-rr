namespace Chronos
namespace Frontier

structure GravityVariationalFieldEquation where
  primitiveState : Type
  emergentMetric : Type
  matterSector : Type

  action : emergentMetric → matterSector → Real

  metricVariation :
    emergentMetric → emergentMetric

  fieldEquation :
    emergentMetric → matterSector → Prop

axiom stationarity_implies_field_equation :
  ∀ (G : GravityVariationalFieldEquation) (g : G.emergentMetric) (m : G.matterSector),
    G.fieldEquation g m

structure TGO (G : GravityVariationalFieldEquation) where
  Scalar : Type
  T : G.emergentMetric → Scalar
  Gm : G.emergentMetric
  O : G.matterSector → Scalar

end Frontier
end Chronos
