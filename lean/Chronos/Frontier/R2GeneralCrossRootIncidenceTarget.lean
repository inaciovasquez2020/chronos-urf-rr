import Chronos.Frontier.R2CrossRootFaceIncidenceObstruction

namespace Chronos
namespace Frontier

structure R2GeneralCrossRootIncidenceSystem where
  Root : Type
  Face : Type
  Chain : Type
  boundaryMatches : Chain → Prop
  contains : Face → Chain → Prop
  adjacent : Face → Face → Prop
  touchesRoot : Face → Root → Prop

namespace R2GeneralCrossRootIncidenceSystem

def CrossRootWitness
    (S : R2GeneralCrossRootIncidenceSystem)
    (chain : S.Chain) : Prop :=
  ∃ left right : S.Face,
    ∃ leftRoot rightRoot : S.Root,
      S.contains left chain ∧
      S.contains right chain ∧
      S.adjacent left right ∧
      S.touchesRoot left leftRoot ∧
      S.touchesRoot right rightRoot ∧
      leftRoot ≠ rightRoot

def NonvacuousTarget
    (S : R2GeneralCrossRootIncidenceSystem) : Prop :=
  (∃ chain : S.Chain, S.boundaryMatches chain) ∧
  ∀ chain : S.Chain,
    S.boundaryMatches chain →
    S.CrossRootWitness chain

end R2GeneralCrossRootIncidenceSystem

def r2IncidenceGeneralCrossRootSystem :
    R2GeneralCrossRootIncidenceSystem where
  Root := R2IncidenceRoot
  Face := R2IncidenceFace
  Chain := R2IncidenceFaceChain
  boundaryMatches := fun chain =>
    r2IncidenceBoundary2 chain = r2IncidenceCrossRootBoundary
  contains := fun face chain => face ∈ chain
  adjacent := r2IncidenceFaceAdjacent
  touchesRoot := fun face root =>
    root ∈ r2IncidenceFaceRoots face

theorem r2_incidence_all_faces_matches_cross_root_boundary :
    r2IncidenceBoundary2 r2IncidenceAllFaces =
      r2IncidenceCrossRootBoundary := by
  native_decide

theorem r2_incidence_boundary_match_eq_all_faces
    (chain : R2IncidenceFaceChain)
    (hBoundary :
      r2IncidenceBoundary2 chain = r2IncidenceCrossRootBoundary) :
    chain = r2IncidenceAllFaces := by
  have hmem : chain ∈ r2IncidenceCrossRootSolutions := by
    simp [r2IncidenceCrossRootSolutions, hBoundary]
  rw [r2_incidence_cross_root_solution_unique] at hmem
  simpa using hmem

theorem r2_incidence_all_faces_has_cross_root_witness :
    r2IncidenceGeneralCrossRootSystem.CrossRootWitness
      r2IncidenceAllFaces := by
  refine
    ⟨R2IncidenceFace.f0a,
      R2IncidenceFace.f0b,
      R2IncidenceRoot.top,
      R2IncidenceRoot.bottom,
      ?_, ?_, ?_, ?_, ?_, ?_⟩
  · change R2IncidenceFace.f0a ∈ r2IncidenceAllFaces
    native_decide
  · change R2IncidenceFace.f0b ∈ r2IncidenceAllFaces
    native_decide
  · change r2IncidenceFaceAdjacent R2IncidenceFace.f0a R2IncidenceFace.f0b
    native_decide
  · change
      R2IncidenceRoot.top ∈
        r2IncidenceFaceRoots R2IncidenceFace.f0a
    native_decide
  · change
      R2IncidenceRoot.bottom ∈
        r2IncidenceFaceRoots R2IncidenceFace.f0b
    native_decide
  · intro h
    cases h

theorem r2_incidence_general_cross_root_target :
    r2IncidenceGeneralCrossRootSystem.NonvacuousTarget := by
  constructor
  · exact
      ⟨r2IncidenceAllFaces,
        r2_incidence_all_faces_matches_cross_root_boundary⟩
  · intro chain hBoundary
    have hChain :
        chain = r2IncidenceAllFaces :=
      r2_incidence_boundary_match_eq_all_faces chain hBoundary
    subst chain
    exact r2_incidence_all_faces_has_cross_root_witness

end Frontier
end Chronos
