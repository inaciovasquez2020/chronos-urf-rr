/-
Concrete constraint-propagation certificate.

This module records only the homogeneous constraint-propagation interface:
if the concrete evolution has a homogeneous constraint propagation law, then
zero initial constraints remain zero on the verified propagation interval.

Boundary:
This does not prove analytic Einstein-matter bootstrap package,
matter-coupling compatibility, energy-condition preservation,
continuation until collapse threshold, restricted collapse-gate trigger,
gravity closure, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
-/

universe u v

namespace Chronos
namespace Frontier

structure ConcreteConstraintPropagationDatum where
  Time : Type u
  State : Type v
  le : Time → Time → Prop
  zeroTime : Time
  finalTime : Time
  constraint : Time → State → Prop
  evolvesOn : State → Prop
  initialConstraintZero : State → Prop

def ConstraintsPropagate
    (D : ConcreteConstraintPropagationDatum) : Prop :=
  ∀ s : D.State,
    D.evolvesOn s →
    D.initialConstraintZero s →
    ∀ t : D.Time,
      D.le D.zeroTime t →
      D.le t D.finalTime →
      D.constraint t s

structure HomogeneousConstraintPropagationCertificate
    (D : ConcreteConstraintPropagationDatum) where
  propagation : ConstraintsPropagate D

theorem concrete_constraint_propagation_certificate
    {D : ConcreteConstraintPropagationDatum}
    (cert : HomogeneousConstraintPropagationCertificate D) :
    ConstraintsPropagate D :=
  cert.propagation

theorem constraint_zero_at_time_of_certificate
    {D : ConcreteConstraintPropagationDatum}
    (cert : HomogeneousConstraintPropagationCertificate D)
    (s : D.State)
    (hs : D.evolvesOn s)
    (h0 : D.initialConstraintZero s)
    (t : D.Time)
    (ht0 : D.le D.zeroTime t)
    (htT : D.le t D.finalTime) :
    D.constraint t s :=
  cert.propagation s hs h0 t ht0 htT

end Frontier
end Chronos
