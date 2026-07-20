import Chronos.Frontier.R2Geometry.R2OverlappingFaceMetricBound

/-!
# Metric bounds along overlapping face paths

This module derives a global endpoint-distance estimate from:

* a uniform metric diameter bound `ε` on every two-face; and
* a finite path of consecutively overlapping two-faces.

A path with `n` overlap steps has endpoint distance at most

`(2 * n + 1) * ε`.

This is the local-to-global metric estimate needed before a bounded dual-graph
diameter can imply localization of an entire admissible filling support.
-/

noncomputable section

namespace Chronos
namespace Frontier

open R2FillingGeometry

variable
  (G : R2FillingGeometry)
  (ε : ℝ)

/--
A face path of length `n` consists of `n` consecutive overlap steps.

Length zero is a single face. Extending a path adds one overlapping face at
its beginning.
-/
inductive FacePath :
    G.Face2 → G.Face2 → Nat → Prop
  | single (face : G.Face2) :
      FacePath face face 0
  | cons
      {first middle last : G.Face2}
      {length : Nat}
      (hOverlap : FacesOverlap G first middle)
      (tail : FacePath middle last length) :
      FacePath first last (length + 1)

/--
The closed-form metric bound associated with a face path of length `n`.
-/
def FacePathMetricBound
    (length : Nat) :
    ℝ :=
  (2 * (length : ℝ) + 1) * ε

/--
The face-path metric bound satisfies the recursion obtained by adding one
overlap step.
-/
theorem facePathMetricBound_succ
    (length : Nat) :
    2 * ε + FacePathMetricBound ε length =
      FacePathMetricBound ε (length + 1) := by
  simp only [
    FacePathMetricBound,
    Nat.cast_add,
    Nat.cast_one
  ]
  ring

/--
If every face has diameter at most `ε`, then points in the endpoint faces of
an overlap path of length `n` are at distance at most `(2 * n + 1) * ε`.
-/
theorem face_path_metric_bound
    (hDiameter : FaceDiameterBound G ε)
    {first last : G.Face2}
    {length : Nat}
    (hPath : FacePath G first last length)
    {x y : G.Point}
    (hx : x ∈ G.face2Support first)
    (hy : y ∈ G.face2Support last) :
    dist x y ≤ FacePathMetricBound ε length := by
  induction hPath generalizing x with
  | single face =>
      simpa [FacePathMetricBound] using
        hDiameter face x hx y hy

  | cons hOverlap tail ih =>
      obtain
        ⟨junction, hJunctionFirst, hJunctionMiddle⟩ :=
        hOverlap

      have hHead :
          dist x junction ≤ 2 * ε :=
        overlapping_faces_metric_bound
          G
          ε
          hDiameter
          ⟨junction, hJunctionFirst, hJunctionMiddle⟩
          hx
          hJunctionMiddle

      have hTail :
          dist junction y ≤ _ :=
        ih hJunctionMiddle hy

      calc
        dist x y
            ≤ dist x junction + dist junction y :=
          dist_triangle x junction y
        _ ≤ 2 * ε + _ :=
          add_le_add hHead hTail
        _ = _ := by
          simp only [
            FacePathMetricBound,
            Nat.cast_add,
            Nat.cast_one
          ]
          ring

end Frontier
end Chronos
