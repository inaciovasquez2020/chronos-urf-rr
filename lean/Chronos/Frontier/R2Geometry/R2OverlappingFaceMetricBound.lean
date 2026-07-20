import Chronos.Frontier.R2Geometry.R2MetricFillingGeometry

/-!
# Metric bound across overlapping two-faces

This module introduces two primitive geometric conditions:

* every two-face has metric diameter at most `ε`;
* two faces are adjacent when their metric supports overlap.

It then proves that points lying in two overlapping faces are at distance at
most `2 * ε`. This is the first local metric estimate needed to derive a
global filling-support localization bound from a bounded dual face path.
-/

noncomputable section

namespace Chronos
namespace Frontier

open R2FillingGeometry

variable
  (G : R2FillingGeometry)
  (ε : ℝ)

/--
Every two-face support has metric diameter at most `ε`.
-/
def FaceDiameterBound : Prop :=
  ∀ face,
    ∀ x ∈ G.face2Support face,
      ∀ y ∈ G.face2Support face,
        dist x y ≤ ε

/--
Two two-faces overlap when their metric supports contain a common point.
-/
def FacesOverlap
    (first second : G.Face2) :
    Prop :=
  ∃ point : G.Point,
    point ∈ G.face2Support first ∧
    point ∈ G.face2Support second

/--
Points in two overlapping faces are at distance at most twice the uniform
face-diameter bound.
-/
theorem overlapping_faces_metric_bound
    (hDiameter : FaceDiameterBound G ε)
    {first second : G.Face2}
    (hOverlap : FacesOverlap G first second)
    {x y : G.Point}
    (hx : x ∈ G.face2Support first)
    (hy : y ∈ G.face2Support second) :
    dist x y ≤ 2 * ε := by
  obtain ⟨middle, hMiddleFirst, hMiddleSecond⟩ :=
    hOverlap

  have hFirst :
      dist x middle ≤ ε :=
    hDiameter first x hx middle hMiddleFirst

  have hSecond :
      dist middle y ≤ ε :=
    hDiameter second middle hMiddleSecond y hy

  calc
    dist x y
        ≤ dist x middle + dist middle y :=
      dist_triangle x middle y
    _ ≤ ε + ε :=
      add_le_add hFirst hSecond
    _ = 2 * ε := by
      ring

end Frontier
end Chronos
