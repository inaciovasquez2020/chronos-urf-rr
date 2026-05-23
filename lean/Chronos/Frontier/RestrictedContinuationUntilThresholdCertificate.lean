/-
Restricted continuation-until-threshold certificate.

This module records only the restricted continuation interface:
finite continuation norm plus bootstrap bounds plus below-threshold status
imply extension past the selected time.

Boundary:
This does not prove analytic Einstein-matter bootstrap package,
matter-coupling compatibility, constraint propagation,
energy-condition preservation, restricted collapse-gate trigger,
gravity closure, Chronos-RR, H4.1/FGL, P vs NP, or any Clay problem.
-/

universe u v

namespace Chronos
namespace Frontier

structure RestrictedContinuationDatum where
  Time : Type u
  State : Type v
  le : Time → Time → Prop
  zeroTime : Time
  finalTime : Time
  evolvesOn : State → Prop
  bootstrapBounds : Time → State → Prop
  finiteContinuationNorm : Time → State → Prop
  belowCollapseThreshold : Time → State → Prop
  extendsPast : Time → State → Prop

def ContinuationUntilThreshold
    (D : RestrictedContinuationDatum) : Prop :=
  ∀ s : D.State,
    D.evolvesOn s →
    ∀ t : D.Time,
      D.le D.zeroTime t →
      D.le t D.finalTime →
      D.bootstrapBounds t s →
      D.finiteContinuationNorm t s →
      D.belowCollapseThreshold t s →
      D.extendsPast t s

structure RestrictedContinuationUntilThresholdCertificate
    (D : RestrictedContinuationDatum) where
  continuation : ContinuationUntilThreshold D

theorem restricted_continuation_until_threshold_certificate
    {D : RestrictedContinuationDatum}
    (cert : RestrictedContinuationUntilThresholdCertificate D) :
    ContinuationUntilThreshold D :=
  cert.continuation

theorem extends_past_of_restricted_continuation_certificate
    {D : RestrictedContinuationDatum}
    (cert : RestrictedContinuationUntilThresholdCertificate D)
    (s : D.State)
    (hs : D.evolvesOn s)
    (t : D.Time)
    (ht0 : D.le D.zeroTime t)
    (htT : D.le t D.finalTime)
    (hboot : D.bootstrapBounds t s)
    (hnorm : D.finiteContinuationNorm t s)
    (hbelow : D.belowCollapseThreshold t s) :
    D.extendsPast t s :=
  cert.continuation s hs t ht0 htT hboot hnorm hbelow

end Frontier
end Chronos
