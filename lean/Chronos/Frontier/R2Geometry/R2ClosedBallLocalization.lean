import Chronos.Frontier.R2Geometry.R2MetricDiameterObstructionKernel

/-!
# Closed-ball localization for genuine R2 fillings

This module derives the localization hypothesis used by the metric diameter
obstruction kernel from a more primitive geometric condition:

every admissible filling support is contained in some metric closed ball of
radius `R`.

The triangle inequality then gives support diameter at most `2 * R`.
-/

noncomputable section

namespace Chronos
namespace Frontier

open R2FillingGeometry

variable
  (G : R2FillingGeometry)
  (Adm : (G.Face2 →₀ F2) → Prop)
  (R : ℝ)

/--
Every admissible filling support is contained in a metric closed ball of
radius `R`. The center may depend on the filling.
-/
def AdmissibleContainedInClosedBall : Prop :=
  ∀ F,
    Adm F →
    ∃ center : G.Point,
      G.supp2 F ⊆ Metric.closedBall center R

/--
Closed-ball containment of radius `R` implies that every admissible filling
has support diameter at most `2 * R`.
-/
theorem admissibleLocalized_of_closedBall
    (hBall : AdmissibleContainedInClosedBall G Adm R) :
    AdmissibleLocalized G Adm (2 * R) := by
  intro F hAdm x hx y hy

  obtain ⟨center, hSupport⟩ := hBall F hAdm

  have hxBall :
      x ∈ Metric.closedBall center R :=
    hSupport hx

  have hyBall :
      y ∈ Metric.closedBall center R :=
    hSupport hy

  have hxBound :
      dist x center ≤ R := by
    simpa [Metric.mem_closedBall, dist_comm] using hxBall

  have hyBound :
      dist center y ≤ R := by
    simpa [Metric.mem_closedBall, dist_comm] using hyBall

  calc
    dist x y
        ≤ dist x center + dist center y :=
      dist_triangle x center y
    _ ≤ R + R :=
      add_le_add hxBound hyBound
    _ = 2 * R := by
      ring

/--
A boundary separated by more than twice the admissible closed-ball radius
cannot be filled by an admissible two-chain.
-/
theorem diameter_separation_filling_obstruction_of_closedBall
    (hBall : AdmissibleContainedInClosedBall G Adm R)
    (c : G.Face1 →₀ F2)
    (hSeparated : G.Separated c (2 * R)) :
    ¬ G.Fillable Adm c :=
  diameter_separation_filling_obstruction
    G
    Adm
    (2 * R)
    (admissibleLocalized_of_closedBall G Adm R hBall)
    c
    hSeparated

end Frontier
end Chronos
