import Chronos.Frontier.RestrictedCarrierRankToEntropyGap

namespace Chronos
namespace Frontier

/--
SelectedDomainUniversalFiberEntropyGap is the selected-domain interface
obtained from the restricted carrier bridge.

This is not the unrestricted UniversalFiberEntropyGap.
-/
def SelectedDomainUniversalFiberEntropyGap
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass) : Prop :=
  RestrictedCarrierFiberEntropyGap rankRate fiberMass

/--
Closed bridge: the restricted carrier entropy gap immediately supplies the
selected-domain universal gap interface.
-/
theorem selected_domain_universal_gap_from_restricted_carrier
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass)
    (hgap : RestrictedCarrierFiberEntropyGap rankRate fiberMass) :
    SelectedDomainUniversalFiberEntropyGap rankRate fiberMass := by
  exact hgap

end Frontier
end Chronos
