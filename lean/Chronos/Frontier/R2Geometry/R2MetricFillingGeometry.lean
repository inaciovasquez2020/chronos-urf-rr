import Mathlib.Data.Finsupp.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Topology.MetricSpace.Basic

/-!
# Metric filling geometry for the genuine R2 obstruction

This module introduces actual metric points, one- and two-dimensional faces,
chain supports, a boundary operator, admissible filling, and metric boundary
separation.

`Fillable` is defined independently as the existence of a two-chain whose
boundary is the supplied one-chain. The obstruction is not included as a field.
-/

noncomputable section

namespace Chronos
namespace Frontier

abbrev F2 := ZMod 2

/--
A metric two-dimensional filling geometry.

`boundary_face_support` records the primitive compatibility needed to derive
boundary-support monotonicity: every nonzero boundary face of a two-chain is
supported inside some nonzero two-face of that chain.
-/
structure R2FillingGeometry where
  Point : Type
  Face1 : Type
  Face2 : Type

  pointMetric : MetricSpace Point
  face1DecidableEq : DecidableEq Face1
  face2DecidableEq : DecidableEq Face2

  face1Support : Face1 → Set Point
  face2Support : Face2 → Set Point

  boundary2 : (Face2 →₀ F2) → Face1 →₀ F2

  boundary_face_support :
    ∀ F e,
      boundary2 F e ≠ 0 →
      ∃ f,
        F f ≠ 0 ∧
        face1Support e ⊆ face2Support f

attribute [instance] R2FillingGeometry.pointMetric
attribute [instance] R2FillingGeometry.face1DecidableEq
attribute [instance] R2FillingGeometry.face2DecidableEq

namespace R2FillingGeometry

/-- Metric support of a one-chain. -/
def supp1
    (G : R2FillingGeometry)
    (c : G.Face1 →₀ F2) :
    Set G.Point :=
  {x | ∃ e, c e ≠ 0 ∧ x ∈ G.face1Support e}

/-- Metric support of a two-chain. -/
def supp2
    (G : R2FillingGeometry)
    (F : G.Face2 →₀ F2) :
    Set G.Point :=
  {x | ∃ f, F f ≠ 0 ∧ x ∈ G.face2Support f}

/--
A one-chain is fillable when it is the actual boundary of an admissible
two-chain.
-/
def Fillable
    (G : R2FillingGeometry)
    (Adm : (G.Face2 →₀ F2) → Prop)
    (c : G.Face1 →₀ F2) :
    Prop :=
  ∃ F, G.boundary2 F = c ∧ Adm F

/--
A boundary is separated beyond `D` when its metric support contains two points
whose distance is strictly larger than `D`.
-/
def Separated
    (G : R2FillingGeometry)
    (c : G.Face1 →₀ F2)
    (D : ℝ) :
    Prop :=
  ∃ xLeft ∈ G.supp1 c,
    ∃ xRight ∈ G.supp1 c,
      D < dist xLeft xRight

end R2FillingGeometry

end Frontier
end Chronos
