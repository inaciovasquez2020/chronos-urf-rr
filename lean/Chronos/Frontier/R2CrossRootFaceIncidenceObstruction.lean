import Mathlib.Tactic

namespace Chronos
namespace Frontier

inductive R2IncidenceRoot where
  | top
  | bottom
  deriving DecidableEq, Fintype, Repr

inductive R2IncidenceVertex where
  | t0 | t1 | t2
  | b0 | b1 | b2
  deriving DecidableEq, Fintype, Repr

inductive R2IncidenceEdge where
  | t01 | t12 | t20
  | b01 | b12 | b20
  | v0 | v1 | v2
  | d0 | d1 | d2
  deriving DecidableEq, Fintype, Repr

inductive R2IncidenceFace where
  | f0a | f0b
  | f1a | f1b
  | f2a | f2b
  deriving DecidableEq, Fintype, Repr

abbrev R2IncidenceEdgeChain := Finset R2IncidenceEdge
abbrev R2IncidenceFaceChain := Finset R2IncidenceFace

/-- Endpoint map ε for the finite witness-layer incidence packet. -/
def r2IncidenceEndpoints : R2IncidenceEdge → Finset R2IncidenceVertex
  | .t01 => {.t0, .t1}
  | .t12 => {.t1, .t2}
  | .t20 => {.t2, .t0}
  | .b01 => {.b0, .b1}
  | .b12 => {.b1, .b2}
  | .b20 => {.b2, .b0}
  | .v0 => {.t0, .b0}
  | .v1 => {.t1, .b1}
  | .v2 => {.t2, .b2}
  | .d0 => {.t0, .b1}
  | .d1 => {.t1, .b2}
  | .d2 => {.t2, .b0}

/-- Admissible 2-faces and their three-edge boundaries. -/
def r2IncidenceFaceBoundary : R2IncidenceFace → Finset R2IncidenceEdge
  | .f0a => {.t01, .v1, .d0}
  | .f0b => {.d0, .b01, .v0}
  | .f1a => {.t12, .v2, .d1}
  | .f1b => {.d1, .b12, .v1}
  | .f2a => {.t20, .v0, .d2}
  | .f2b => {.d2, .b20, .v2}

/-- Rooted boundary regions B(top) and B(bottom). -/
def r2IncidenceRootEdges : R2IncidenceRoot → Finset R2IncidenceEdge
  | .top => {.t01, .t12, .t20}
  | .bottom => {.b01, .b12, .b20}

/-- Face-root incidence ρ. Top-facing and bottom-facing cylinder triangles alternate. -/
def r2IncidenceFaceRoots : R2IncidenceFace → Finset R2IncidenceRoot
  | .f0a | .f1a | .f2a => {.top}
  | .f0b | .f1b | .f2b => {.bottom}

/-- Boundary D₁ over F₂, represented by odd endpoint incidence. -/
def r2IncidenceBoundary1 (chain : R2IncidenceEdgeChain) : Finset R2IncidenceVertex :=
  Finset.univ.filter fun vertex =>
    (chain.filter fun edge => vertex ∈ r2IncidenceEndpoints edge).card % 2 = 1

/-- Boundary D₂ over F₂, represented by odd face incidence. -/
def r2IncidenceBoundary2 (chain : R2IncidenceFaceChain) : R2IncidenceEdgeChain :=
  Finset.univ.filter fun edge =>
    (chain.filter fun face => edge ∈ r2IncidenceFaceBoundary face).card % 2 = 1

/-- The packet is a chain complex: D₁D₂ = 0 for every 2-chain. -/
theorem r2_incidence_boundary_squared_zero :
    ∀ chain : R2IncidenceFaceChain,
      r2IncidenceBoundary1 (r2IncidenceBoundary2 chain) = ∅ := by
  native_decide

/-- Local 1-cycles in a rooted region. -/
def r2IncidenceLocalCycles (root : R2IncidenceRoot) : Finset R2IncidenceEdgeChain :=
  Finset.univ.filter fun chain =>
    chain ⊆ r2IncidenceRootEdges root ∧ r2IncidenceBoundary1 chain = ∅

/-- Local face chains are generated exclusively by faces whose full boundary lies in B(root). -/
def r2IncidenceLocalFaceChains (root : R2IncidenceRoot) : Finset R2IncidenceFaceChain :=
  Finset.univ.filter fun chain =>
    ∀ face ∈ chain, r2IncidenceFaceBoundary face ⊆ r2IncidenceRootEdges root

/-- Wᵤ is computed as the image of the local D₂ map. -/
def r2IncidenceLocalBoundaries (root : R2IncidenceRoot) : Finset R2IncidenceEdgeChain :=
  (r2IncidenceLocalFaceChains root).image r2IncidenceBoundary2

/-- Computed quotient size |Zᵤ| / |Wᵤ|. -/
def r2IncidenceLocalQuotientCard (root : R2IncidenceRoot) : Nat :=
  (r2IncidenceLocalCycles root).card / (r2IncidenceLocalBoundaries root).card

/-- Computed F₂ quotient dimension; no expected rank is stored in the definition. -/
def r2IncidenceLocalQuotientDimension (root : R2IncidenceRoot) : Nat :=
  Nat.log 2 (r2IncidenceLocalQuotientCard root)

/-- Both rooted boundary circles have a one-dimensional nonzero quotient. -/
theorem r2_incidence_local_quotient_dimensions :
    ∀ root : R2IncidenceRoot,
      r2IncidenceLocalQuotientDimension root = 1 := by
  native_decide

/-- The two nonzero local quotient representatives. -/
def r2IncidenceTopClass : R2IncidenceEdgeChain := {.t01, .t12, .t20}
def r2IncidenceBottomClass : R2IncidenceEdgeChain := {.b01, .b12, .b20}
def r2IncidenceCrossRootBoundary : R2IncidenceEdgeChain :=
  r2IncidenceTopClass ∪ r2IncidenceBottomClass

def r2IncidenceAllFaces : R2IncidenceFaceChain := Finset.univ

def r2IncidenceCrossRootSolutions : Finset R2IncidenceFaceChain :=
  Finset.univ.filter fun chain =>
    r2IncidenceBoundary2 chain = r2IncidenceCrossRootBoundary

/-- The triangulated cylinder is an actual cross-root filling. -/
theorem r2_incidence_cross_root_solution_exists :
    ∃ chain : R2IncidenceFaceChain,
      r2IncidenceBoundary2 chain = r2IncidenceCrossRootBoundary := by
  native_decide

/-- Exhaustive finite solve: the all-face cylinder chain is the unique solution. -/
theorem r2_incidence_cross_root_solution_unique :
    r2IncidenceCrossRootSolutions = {r2IncidenceAllFaces} := by
  native_decide

/-- Two faces are incidence-adjacent when their boundaries share an edge. -/
def r2IncidenceFaceAdjacent (left right : R2IncidenceFace) : Prop :=
  left ≠ right ∧ (r2IncidenceFaceBoundary left ∩ r2IncidenceFaceBoundary right).Nonempty

instance r2IncidenceFaceAdjacentDecidable :
    DecidableRel r2IncidenceFaceAdjacent := by
  intro left right
  unfold r2IncidenceFaceAdjacent
  infer_instance

/-- A fixed spanning tree inside the face-incidence graph of the cylinder. -/
def r2IncidenceSpanningTree : Finset (R2IncidenceFace × R2IncidenceFace) :=
  {(.f0a, .f0b), (.f0b, .f2a), (.f2a, .f2b), (.f2b, .f1a), (.f1a, .f1b)}

/-- Roots touched by a face chain through ρ. -/
def r2IncidenceRootsTouched (chain : R2IncidenceFaceChain) : Finset R2IncidenceRoot :=
  Finset.univ.filter fun root =>
    ∃ face ∈ chain, root ∈ r2IncidenceFaceRoots face

/-- Concrete cross-root component certificate: the chain contains the spanning incidence
    tree and touches both roots. -/
def R2CrossRootFaceIncidenceObstruction (chain : R2IncidenceFaceChain) : Prop :=
  (∀ pair ∈ r2IncidenceSpanningTree,
      pair.1 ∈ chain ∧ pair.2 ∈ chain ∧ r2IncidenceFaceAdjacent pair.1 pair.2) ∧
  r2IncidenceRootsTouched chain = Finset.univ

/-- Replacement R2 theorem for the nonvacuous finite packet. Every global filling of the
    two nonzero local classes contains a connected cross-root face-incidence component. -/
theorem r2_cross_root_face_incidence_obstruction :
    ∀ chain : R2IncidenceFaceChain,
      r2IncidenceBoundary2 chain = r2IncidenceCrossRootBoundary →
      R2CrossRootFaceIncidenceObstruction chain := by
  intro chain hboundary
  have hmem : chain ∈ r2IncidenceCrossRootSolutions := by
    simp [r2IncidenceCrossRootSolutions, hboundary]
  rw [r2_incidence_cross_root_solution_unique] at hmem
  have hchain : chain = r2IncidenceAllFaces := by
    simpa using hmem
  subst chain
  unfold R2CrossRootFaceIncidenceObstruction
  native_decide

end Frontier
end Chronos
