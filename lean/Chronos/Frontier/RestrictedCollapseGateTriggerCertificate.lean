/-
Restricted collapse-gate trigger certificate.

This module records only the restricted collapse-gate trigger interface:
monotone concentration plus threshold crossing plus previously certified
constraint, energy, and continuation inputs imply the restricted gate.

Boundary:
This does not prove analytic Einstein-matter bootstrap package,
matter-coupling compatibility, constraint propagation,
energy-condition preservation, continuation until collapse threshold,
gravity closure, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
-/

universe u v

namespace Chronos
namespace Frontier

structure RestrictedCollapseGateTriggerDatum where
  Time : Type u
  State : Type v
  triggerTime : Time
  evolvesOn : State → Prop
  concentrationInitiallyBelowThreshold : State → Prop
  concentrationMonotone : State → Prop
  thresholdCrossing : Time → State → Prop
  constraintsPropagate : State → Prop
  energyConditionPreserved : State → Prop
  continuationUntilThreshold : State → Prop
  restrictedCollapseGate : Time → State → Prop

def RestrictedCollapseGateTriggers
    (D : RestrictedCollapseGateTriggerDatum) : Prop :=
  ∀ s : D.State,
    D.evolvesOn s →
    D.concentrationInitiallyBelowThreshold s →
    D.concentrationMonotone s →
    D.thresholdCrossing D.triggerTime s →
    D.constraintsPropagate s →
    D.energyConditionPreserved s →
    D.continuationUntilThreshold s →
    D.restrictedCollapseGate D.triggerTime s

structure RestrictedCollapseGateTriggerCertificate
    (D : RestrictedCollapseGateTriggerDatum) where
  trigger : RestrictedCollapseGateTriggers D

theorem restricted_collapse_gate_trigger_certificate
    {D : RestrictedCollapseGateTriggerDatum}
    (cert : RestrictedCollapseGateTriggerCertificate D) :
    RestrictedCollapseGateTriggers D :=
  cert.trigger

theorem collapse_gate_at_trigger_time_of_certificate
    {D : RestrictedCollapseGateTriggerDatum}
    (cert : RestrictedCollapseGateTriggerCertificate D)
    (s : D.State)
    (hs : D.evolvesOn s)
    (hbelow : D.concentrationInitiallyBelowThreshold s)
    (hmono : D.concentrationMonotone s)
    (hcross : D.thresholdCrossing D.triggerTime s)
    (hconstraint : D.constraintsPropagate s)
    (henergy : D.energyConditionPreserved s)
    (hcontinue : D.continuationUntilThreshold s) :
    D.restrictedCollapseGate D.triggerTime s :=
  cert.trigger s hs hbelow hmono hcross hconstraint henergy hcontinue

end Frontier
end Chronos
