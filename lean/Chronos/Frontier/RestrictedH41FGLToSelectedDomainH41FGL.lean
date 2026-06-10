import Chronos.Frontier.RestrictedChronosRRToRestrictedH41FGL
import Chronos.Frontier.SelectedDomainH41FGLFromChronosRR

namespace Chronos
namespace Frontier

structure RestrictedH41FGLSelectedDomainEmbedding
    (D : RestrictedChronosRRData)
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass) where
  carrier_gap : RestrictedCarrierFiberEntropyGap rankRate fiberMass
  boundary_lock : True := by trivial

theorem selected_domain_h41fgl_from_restricted_h41_fgl
    (D : RestrictedChronosRRData)
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass)
    (_hRestricted : RestrictedH41FGL D)
    (hEmbed : RestrictedH41FGLSelectedDomainEmbedding D rankRate fiberMass) :
    SelectedDomainH41FGL rankRate fiberMass := by
  exact selected_domain_h41_fgl_from_chronos_rr rankRate fiberMass
    (selected_domain_chronos_rr_from_universal_gap rankRate fiberMass
      (selected_domain_universal_gap_from_restricted_carrier rankRate fiberMass
        hEmbed.carrier_gap))

end Frontier
end Chronos
