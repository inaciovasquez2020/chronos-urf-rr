namespace Chronos
namespace Frontier

/--
A restricted carrier state for the next closed bridge.

This object is intentionally abstract: it records only the local carrier
surface needed to compose rank soundness with rate-thick coercivity.
-/
structure RestrictedCarrierState where
  id : Nat

/--
RankRate is the local rank-rate observable on the restricted carrier.
-/
def RankRate := RestrictedCarrierState → Nat

/--
FiberEntropyMass is the local entropy-mass observable on the restricted carrier.
-/
def FiberEntropyMass := RestrictedCarrierState → Nat

/--
CarrierRankSoundness says positive rank-rate is certified on the restricted
carrier surface.
-/
def CarrierRankSoundness (rankRate : RankRate) : Prop :=
  ∀ X : RestrictedCarrierState, 0 < rankRate X → 0 < rankRate X

/--
RateThickFiberCoercivity says positive rank-rate forces positive entropy mass
on the restricted carrier surface.
-/
def RateThickFiberCoercivity
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass) : Prop :=
  ∀ X : RestrictedCarrierState, 0 < rankRate X → 0 < fiberMass X

/--
RestrictedCarrierFiberEntropyGap is the solved restricted target.

It is not the unrestricted UniversalFiberEntropyGap. It is only the local
positive-mass conclusion over `RestrictedCarrierState`.
-/
def RestrictedCarrierFiberEntropyGap
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass) : Prop :=
  ∀ X : RestrictedCarrierState, 0 < rankRate X → 0 < fiberMass X

/--
Closed bridge: rank soundness plus rate-thick coercivity yields the restricted
carrier fiber entropy gap.
-/
theorem restricted_carrier_rank_to_entropy_gap
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass)
    (_hsound : CarrierRankSoundness rankRate)
    (hcoercive : RateThickFiberCoercivity rankRate fiberMass) :
    RestrictedCarrierFiberEntropyGap rankRate fiberMass := by
  intro X h_rank
  exact hcoercive X h_rank

end Frontier
end Chronos
