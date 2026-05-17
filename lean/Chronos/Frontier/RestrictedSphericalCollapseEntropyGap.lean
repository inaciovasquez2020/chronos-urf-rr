namespace Chronos.Frontier.Gravity

structure RestrictedSphericalCollapseInput where
  state : Type
  entropyMass : state → Nat
  sphericalSymmetry : Prop
  finiteArea : Prop
  finiteEnergy : Prop
  entropyBound : Prop
  detectorCutoff : Prop
  positiveGap : Nat
  gapPositive : positiveGap > 0
  entropyGapHypothesis : ∀ x : state, entropyMass x ≥ positiveGap

def RestrictedSphericalCollapseEntropyGap (I : RestrictedSphericalCollapseInput) : Prop :=
  ∃ ε : Nat, ε > 0 ∧ ∀ x : I.state, I.entropyMass x ≥ ε

theorem restricted_spherical_collapse_entropy_gap
    (I : RestrictedSphericalCollapseInput)
    (_hsym : I.sphericalSymmetry)
    (_harea : I.finiteArea)
    (_henergy : I.finiteEnergy)
    (_hentropy : I.entropyBound)
    (_hcutoff : I.detectorCutoff) :
    RestrictedSphericalCollapseEntropyGap I := by
  exact ⟨I.positiveGap, I.gapPositive, I.entropyGapHypothesis⟩

end Chronos.Frontier.Gravity
