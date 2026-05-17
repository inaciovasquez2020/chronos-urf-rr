import Chronos.Frontier.SelectedDomainUniversalGapFromRestrictedCarrier

namespace Chronos
namespace Frontier

/--
SelectedDomainChronosRR is the selected-domain Chronos-RR target obtained
from the selected-domain universal fiber entropy gap interface.

This is not unrestricted Chronos-RR.
-/
def SelectedDomainChronosRR
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass) : Prop :=
  SelectedDomainUniversalFiberEntropyGap rankRate fiberMass

/--
Closed bridge: the selected-domain universal fiber entropy gap supplies the
selected-domain Chronos-RR interface.
-/
theorem selected_domain_chronos_rr_from_universal_gap
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass)
    (hgap : SelectedDomainUniversalFiberEntropyGap rankRate fiberMass) :
    SelectedDomainChronosRR rankRate fiberMass := by
  exact hgap

end Frontier
end Chronos
