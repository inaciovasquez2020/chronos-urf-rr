# Selected-Domain H4.1/FGL to Admissible H4.1/FGL

Status: `SELECTED_DOMAIN_H41_FGL_TO_ADMISSIBLE_H41_FGL_CLOSED`

## Closed surface

```lean
structure SelectedDomainAdmissibleH41FGLEmbedding
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass) : Prop
theorem admissible_h41_fgl_from_selected_domain_h41_fgl
    (rankRate : RankRate)
    (fiberMass : FiberEntropyMass)
    (hSelected : SelectedDomainH41FGL rankRate fiberMass)
    (hEmbed : SelectedDomainAdmissibleH41FGLEmbedding rankRate fiberMass) :
    AdmissibleH41FGL
Boundary
selected-domain to admissible bridge only.
requires explicit admissible embedding data.
does not construct the embedding.
does not prove unrestricted H4.1/FGL.
does not prove P vs NP.
does not prove any Clay problem.
No admissible unrestricted step.
