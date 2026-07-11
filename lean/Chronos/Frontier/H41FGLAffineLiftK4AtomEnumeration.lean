import Mathlib

namespace Chronos
namespace Frontier

/--
The fifteen nonconstant squarefree face monomials on the four vertices of
the tetrahedral clique complex of `K₄`.

The constant monomial is intentionally excluded because the FGL formulation
handles the constant line `⟨1⟩` separately.

This is a concrete bounded coordinate model. No theorem in this file identifies
it with the repository's external admissible-history space.
-/
inductive H41FGLK4AffineAtom where
  | vertex0
  | vertex1
  | vertex2
  | vertex3
  | edge01
  | edge02
  | edge03
  | edge12
  | edge13
  | edge23
  | triangle012
  | triangle013
  | triangle023
  | triangle123
  | tetrahedron
  deriving DecidableEq, Fintype, Repr

namespace H41FGLK4AffineAtom

/-- The local `K₄` vertices touched by one affine-lift atom. -/
def localVertices : H41FGLK4AffineAtom → Finset (Fin 4)
  | .vertex0 => {0}
  | .vertex1 => {1}
  | .vertex2 => {2}
  | .vertex3 => {3}
  | .edge01 => {0, 1}
  | .edge02 => {0, 2}
  | .edge03 => {0, 3}
  | .edge12 => {1, 2}
  | .edge13 => {1, 3}
  | .edge23 => {2, 3}
  | .triangle012 => {0, 1, 2}
  | .triangle013 => {0, 1, 3}
  | .triangle023 => {0, 2, 3}
  | .triangle123 => {1, 2, 3}
  | .tetrahedron => {0, 1, 2, 3}

/-- The concrete local atom enumeration has exactly fifteen elements. -/
theorem card_eq_fifteen :
    Fintype.card H41FGLK4AffineAtom = 15 := by
  native_decide

/-- Every enumerated atom has nonempty local support. -/
theorem localVertices_nonempty
    (a : H41FGLK4AffineAtom) :
    (localVertices a).Nonempty := by
  cases a <;> simp [localVertices]

/-- Every enumerated atom touches at most the four vertices of `K₄`. -/
theorem localVertices_card_le_four
    (a : H41FGLK4AffineAtom) :
    (localVertices a).card ≤ 4 := by
  cases a <;> native_decide

end H41FGLK4AffineAtom

/--
A global vertex is a local `K₄` vertex at one radius layer of one selected
rooted patch.
-/
structure H41FGLAffineLiftK4Vertex (R B : Nat) where
  patch : Fin B
  layer : Fin (R + 1)
  localVertex : Fin 4
  deriving DecidableEq, Fintype, Repr

/--
A global affine-lift atom is one of the fifteen nonconstant `K₄` face
monomials at one radius layer of one selected rooted patch.
-/
structure H41FGLAffineLiftK4Atom (R B : Nat) where
  patch : Fin B
  layer : Fin (R + 1)
  face : H41FGLK4AffineAtom
  deriving DecidableEq, Fintype, Repr

/--
The concrete finite coordinate set `E_{k,R,B}`.

The coordinate enumeration depends on `R` and `B`; the parameter `k` controls
which finite supports are admissible.
-/
abbrev H41FGLAffineLiftK4E
    (_k R B : Nat) : Type :=
  H41FGLAffineLiftK4Atom R B

namespace H41FGLAffineLiftK4Atom

/-- The global vertices touched by one concrete affine-lift atom. -/
def vertices
    {R B : Nat}
    (a : H41FGLAffineLiftK4Atom R B) :
    Finset (H41FGLAffineLiftK4Vertex R B) :=
  (H41FGLK4AffineAtom.localVertices a.face).image
    (fun v =>
      { patch := a.patch
        layer := a.layer
        localVertex := v })

/-- Membership in an atom support preserves its patch, layer, and local face. -/
theorem mem_vertices_characterization
    {R B : Nat}
    (a : H41FGLAffineLiftK4Atom R B)
    (v : H41FGLAffineLiftK4Vertex R B)
    (hv : v ∈ vertices a) :
    v.patch = a.patch ∧
      v.layer = a.layer ∧
      v.localVertex ∈ H41FGLK4AffineAtom.localVertices a.face := by
  rcases Finset.mem_image.mp hv with ⟨q, hq, hqv⟩
  subst v
  exact ⟨rfl, rfl, hq⟩

end H41FGLAffineLiftK4Atom

/-- All global vertices touched by a finite parity support. -/
def H41FGLAffineLiftK4SupportVertices
    {k R B : Nat}
    (support : Finset (H41FGLAffineLiftK4E k R B)) :
    Finset (H41FGLAffineLiftK4Vertex R B) :=
  support.biUnion H41FGLAffineLiftK4Atom.vertices

/--
The exact concrete admissibility predicate:

a parity support is admissible when its atoms collectively touch at most `k`
global vertices. Patch count and radius are bounded by the finite index types
`Fin B` and `Fin (R + 1)`.
-/
def H41FGLAffineLiftK4AdmissibleSupport
    (k R B : Nat)
    (support : Finset (H41FGLAffineLiftK4E k R B)) : Prop :=
  (H41FGLAffineLiftK4SupportVertices support).card ≤ k

/-- The concrete finite family `D_{k,R,B}` of admissible parity supports. -/
abbrev H41FGLAffineLiftK4D
    (k R B : Nat) : Type :=
  {support : Finset (H41FGLAffineLiftK4E k R B) //
    H41FGLAffineLiftK4AdmissibleSupport k R B support}

/-- Admissibility exposes exactly the `k`-vertex support bound. -/
theorem h41FGLAffineLiftK4AdmissibleSupport_card_le
    {k R B : Nat}
    {support : Finset (H41FGLAffineLiftK4E k R B)}
    (hsupport :
      H41FGLAffineLiftK4AdmissibleSupport k R B support) :
    (H41FGLAffineLiftK4SupportVertices support).card ≤ k :=
  hsupport

/-- Every encoded radius layer lies within the selected radius `R`. -/
theorem h41FGLAffineLiftK4Vertex_layer_le
    {R B : Nat}
    (v : H41FGLAffineLiftK4Vertex R B) :
    v.layer.val ≤ R := by
  omega

/-- A concrete radius-zero, one-patch tetrahedral atom. -/
def h41FGLAffineLiftK4TetrahedronExample :
    H41FGLAffineLiftK4E 4 0 1 :=
  { patch := 0
    layer := 0
    face := .tetrahedron }

/-- The singleton tetrahedral support touches exactly four vertices. -/
theorem h41FGLAffineLiftK4TetrahedronExample_support_card :
    (H41FGLAffineLiftK4SupportVertices
      ({h41FGLAffineLiftK4TetrahedronExample} :
        Finset (H41FGLAffineLiftK4E 4 0 1))).card = 4 := by
  native_decide

/-- The singleton tetrahedral support is admissible at vertex budget four. -/
theorem h41FGLAffineLiftK4TetrahedronExample_admissible :
    H41FGLAffineLiftK4AdmissibleSupport
      4
      0
      1
      ({h41FGLAffineLiftK4TetrahedronExample} :
        Finset (H41FGLAffineLiftK4E 4 0 1)) := by
  unfold H41FGLAffineLiftK4AdmissibleSupport
  exact h41FGLAffineLiftK4TetrahedronExample_support_card.le

end Frontier
end Chronos
