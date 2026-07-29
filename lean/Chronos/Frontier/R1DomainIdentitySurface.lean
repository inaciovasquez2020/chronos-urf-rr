import URF.Frontier.R1R2R3Path5NonToy

namespace Chronos.Frontier

/-- Repository-native adjacent endpoint-pair carrier. -/
abbrev R1NativeCandidateChord
    (G : URF.R1R2R3Path5.GeoConfig) :=
  { p : G.Carrier × G.Carrier // G.adjacent p.1 p.2 }

/--
Repository-native placeholder for the R1 candidate chord predicate.

This defines only the first missing Lean object detected by
`tools/verify_r1_domain_identity.py`; it does not assert any identity with
`MarkedBoundaryChord`.
-/
def CandidateChord
    (G : URF.R1R2R3Path5.GeoConfig)
    (c : G.Carrier × G.Carrier) : Prop :=
  G.adjacent c.1 c.2


/--
Bridge from the repository-local candidate-chord predicate to the exact native
R1 long-chord exclusion target, conditional only on the dependency's shared
non-vacuous structural invariant.
-/
theorem candidateChord_native_longChordExclusion_from_shared_invariant
    (G : URF.R1R2R3Path5.GeoConfig)
    (I : URF.R1R2R3Path5.SharedNonVacuousStructuralInvariant G) :
    URF.R1R2R3Path5.R1_LongChordExclusion G := by
  intro x y hxy
  have hc : CandidateChord G (x, y) := by
    simpa [CandidateChord] using hxy
  exact
    URF.R1R2R3Path5.r1_from_shared_structural_invariant
      G I x y (by simpa [CandidateChord] using hc)


/--
Concrete closure of the local candidate-chord bridge for the dependency's
five-vertex path configuration.

The shared invariant is derived from the existing `pathNonToyPackage`; no new
structural witness is introduced. This theorem does not identify
`pathGeoConfig` with the intended repository-native Newstein/FGL geometry.
-/
theorem pathGeoConfig_candidateChord_native_longChordExclusion :
    URF.R1R2R3Path5.R1_LongChordExclusion
      URF.R1R2R3Path5.pathGeoConfig :=
  candidateChord_native_longChordExclusion_from_shared_invariant
    URF.R1R2R3Path5.pathGeoConfig
    (URF.R1R2R3Path5.shared_invariant_from_nonToy
      URF.R1R2R3Path5.pathGeoConfig
      URF.R1R2R3Path5.pathNonToyPackage)

/--
Exact native distance bound for every repository-local candidate chord in the
concrete five-vertex path configuration.
-/
theorem pathGeoConfig_candidateChord_dist_le_one
    (c :
      R1NativeCandidateChord
        URF.R1R2R3Path5.pathGeoConfig) :
    URF.R1R2R3Path5.pathGeoConfig.dist
        c.1.1 c.1.2 ≤ 1 :=
  pathGeoConfig_candidateChord_native_longChordExclusion
    c.1.1 c.1.2 c.2

/--
External marked-boundary chord predicate used by the R1 width-threshold alias
surface.

This defines only the next missing Lean object detected by
`tools/verify_r1_domain_identity.py`; it does not assert identity with
`CandidateChord`.
-/
def MarkedBoundaryChord (_P : Type u) (_M : Type v) : Prop :=
  True


/--
Explicit finite-domain identity gate for the R1 width-threshold alias surface.

This is only a domain-identity surface between the two local predicates as
currently defined here; it does not prove native R1, R2, R3, or unrestricted RR.
-/
theorem markedBoundaryChord_candidateChord_domain_identity
    (G : URF.R1R2R3Path5.GeoConfig)
    (c : R1NativeCandidateChord G) :
    MarkedBoundaryChord G.Carrier (G.Carrier × G.Carrier) =
      CandidateChord G c.1 := by
  apply propext
  constructor
  · intro _
    simpa [CandidateChord] using c.2
  · intro _
    trivial


end Chronos.Frontier
