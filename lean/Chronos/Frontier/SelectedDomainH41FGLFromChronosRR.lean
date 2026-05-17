import Chronos.Frontier.SelectedDomainChronosRRFromUniversalGap

namespace Chronos
namespace Frontier

/--
SelectedDomainH41FGL is the selected-domain H4.1/FGL interface obtained from
the selected-domain Chronos-RR interface.

This is not unrestricted H4.1/FGL.
-/
def SelectedDomainH41FGL
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass) : Prop :=
  SelectedDomainChronosRR rankRate fiberMass

/--
Closed bridge: selected-domain Chronos-RR supplies the selected-domain H4.1/FGL
interface.
-/
theorem selected_domain_h41_fgl_from_chronos_rr
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass)
    (hrr : SelectedDomainChronosRR rankRate fiberMass) :
    SelectedDomainH41FGL rankRate fiberMass := by
  exact hrr

end Frontier
end Chronos
