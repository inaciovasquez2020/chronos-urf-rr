import Chronos.Frontier.RestrictedH41FGLToSelectedDomainH41FGL

namespace Chronos
namespace Frontier

/--
Opaque admissible H4.1/FGL target.

This introduces the admissible target proposition only as an abstract
frontier surface. It does not prove unrestricted H4.1/FGL.
-/
opaque AdmissibleH41FGL : Prop := False

/--
Explicit embedding data from the selected-domain H4.1/FGL surface
to the admissible H4.1/FGL surface.

This is data only. It does not construct the embedding.
-/
structure SelectedDomainAdmissibleH41FGLEmbedding
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass) : Prop where
  to_admissible :
    SelectedDomainH41FGL rankRate fiberMass → AdmissibleH41FGL

/--
Selected-domain H4.1/FGL promotes to admissible H4.1/FGL
only when explicit admissible embedding data is supplied.
-/
theorem admissible_h41_fgl_from_selected_domain_h41_fgl
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass)
    (hSelected : SelectedDomainH41FGL rankRate fiberMass)
    (hEmbed : SelectedDomainAdmissibleH41FGLEmbedding rankRate fiberMass) :
    AdmissibleH41FGL := by
  exact hEmbed.to_admissible hSelected

end Frontier
end Chronos
