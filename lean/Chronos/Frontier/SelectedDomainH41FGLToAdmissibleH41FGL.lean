import Chronos.Frontier.RestrictedH41FGLToSelectedDomainH41FGL

namespace Chronos
namespace Frontier

/--
Admissible H4.1/FGL selected-domain target.

This is the admissible target induced by the selected-domain surface.
It is not unrestricted H4.1/FGL and it does not range over arbitrary
`FiberMassData`.
-/
def AdmissibleH41FGL (rankRate : RankRate) (fiberMass : FiberEntropyMass) : Prop :=
  SelectedDomainH41FGL rankRate fiberMass

/--
Explicit selected-domain-to-admissible embedding data.

The embedding is data, not an open assumption.  The repository-native
construction below supplies the identity/transport embedding for the
selected-domain admissible target.
-/
structure SelectedDomainAdmissibleH41FGLEmbedding
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass) where
  to_admissible :
    SelectedDomainH41FGL rankRate fiberMass →
      AdmissibleH41FGL rankRate fiberMass
  boundary_lock : True := by trivial

/--
Repository-native identity embedding from selected-domain H4.1/FGL into
the admissible selected-domain target.
-/
def selected_domain_admissible_h41_fgl_identity_embedding
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass) :
    SelectedDomainAdmissibleH41FGLEmbedding rankRate fiberMass :=
  { to_admissible := fun hSelected => hSelected
    boundary_lock := trivial }

/--
Selected-domain H4.1/FGL promotes to admissible selected-domain H4.1/FGL
using explicit embedding data.
-/
theorem admissible_h41_fgl_from_selected_domain_h41_fgl
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass)
    (hSelected : SelectedDomainH41FGL rankRate fiberMass)
    (hEmbed : SelectedDomainAdmissibleH41FGLEmbedding rankRate fiberMass) :
    AdmissibleH41FGL rankRate fiberMass := by
  exact hEmbed.to_admissible hSelected

/--
Closed construction: selected-domain H4.1/FGL supplies admissible
selected-domain H4.1/FGL through the repository-native identity embedding.
-/
theorem admissible_h41_fgl_from_selected_domain_h41_fgl_constructed
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass)
    (hSelected : SelectedDomainH41FGL rankRate fiberMass) :
    AdmissibleH41FGL rankRate fiberMass := by
  exact admissible_h41_fgl_from_selected_domain_h41_fgl
    rankRate
    fiberMass
    hSelected
    (selected_domain_admissible_h41_fgl_identity_embedding rankRate fiberMass)

/--
Composed restricted-to-admissible selected-domain H4.1/FGL bridge.

The remaining carrier-gap input is the already-restricted selected-domain
carrier gap.  This does not construct any unrestricted arbitrary-fiber-mass
object.
-/
theorem admissible_h41_fgl_from_restricted_h41_fgl_constructed
    (D : RestrictedChronosRRData)
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass)
    (hRestricted : RestrictedH41FGL D)
    (hCarrier : RestrictedCarrierFiberEntropyGap rankRate fiberMass) :
    AdmissibleH41FGL rankRate fiberMass := by
  let hRestrictedEmbed :
      RestrictedH41FGLSelectedDomainEmbedding D rankRate fiberMass :=
    { carrier_gap := hCarrier
      boundary_lock := trivial }
  exact admissible_h41_fgl_from_selected_domain_h41_fgl_constructed
    rankRate
    fiberMass
    (selected_domain_h41fgl_from_restricted_h41_fgl
      D
      rankRate
      fiberMass
      hRestricted
      hRestrictedEmbed)

end Frontier
end Chronos
