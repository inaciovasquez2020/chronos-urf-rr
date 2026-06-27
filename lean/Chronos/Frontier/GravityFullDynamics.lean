namespace Chronos
namespace Frontier

structure GravityFullDynamics where
  primitiveState : Type
  emergentMetric : Type
  matterSector : Type

  action : primitiveState → Real

  metricEquation :
    emergentMetric → matterSector → Prop

  deriveMetric :
    primitiveState →
    emergentMetric

  predict :
    emergentMetric →
    matterSector →
    Real

axiom metric_is_dynamical :
  ∀ (G : GravityFullDynamics),
    Nonempty G.emergentMetric

axiom prediction_well_defined :
  ∀ (G : GravityFullDynamics) (g : G.emergentMetric) (m : G.matterSector),
    ∃ (_ : Real), True

structure TGO (G : GravityFullDynamics) where
  T : G.primitiveState → G.emergentMetric
  Gm : G.primitiveState → G.emergentMetric
  O : G.emergentMetric → G.matterSector → G.emergentMetric

end Frontier
end Chronos
