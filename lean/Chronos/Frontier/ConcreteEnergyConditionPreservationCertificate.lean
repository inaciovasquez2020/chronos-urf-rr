/-
Concrete energy-condition preservation certificate.

This module records only the bootstrap energy-condition preservation interface:
if the concrete evolution has the required pointwise sign data and bootstrap
pointwise bounds, then the selected energy condition holds on the verified slab.

Boundary:
This does not prove analytic Einstein-matter bootstrap package,
matter-coupling compatibility, constraint propagation,
continuation until collapse threshold, restricted collapse-gate trigger,
gravity closure, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
-/

universe u v

namespace Chronos
namespace Frontier

structure ConcreteEnergyConditionDatum where
  Time : Type u
  State : Type v
  le : Time → Time → Prop
  zeroTime : Time
  finalTime : Time
  evolvesOn : State → Prop
  pointwiseSignCondition : Time → State → Prop
  bootstrapPointwiseBounds : Time → State → Prop
  energyCondition : Time → State → Prop

def EnergyConditionPreserved
    (D : ConcreteEnergyConditionDatum) : Prop :=
  ∀ s : D.State,
    D.evolvesOn s →
    ∀ t : D.Time,
      D.le D.zeroTime t →
      D.le t D.finalTime →
      D.pointwiseSignCondition t s →
      D.bootstrapPointwiseBounds t s →
      D.energyCondition t s

structure ConcreteEnergyConditionPreservationCertificate
    (D : ConcreteEnergyConditionDatum) where
  preservation : EnergyConditionPreserved D

theorem concrete_energy_condition_preservation_certificate
    {D : ConcreteEnergyConditionDatum}
    (cert : ConcreteEnergyConditionPreservationCertificate D) :
    EnergyConditionPreserved D :=
  cert.preservation

theorem energy_condition_at_time_of_certificate
    {D : ConcreteEnergyConditionDatum}
    (cert : ConcreteEnergyConditionPreservationCertificate D)
    (s : D.State)
    (hs : D.evolvesOn s)
    (t : D.Time)
    (ht0 : D.le D.zeroTime t)
    (htT : D.le t D.finalTime)
    (hsign : D.pointwiseSignCondition t s)
    (hboot : D.bootstrapPointwiseBounds t s) :
    D.energyCondition t s :=
  cert.preservation s hs t ht0 htT hsign hboot

end Frontier
end Chronos
