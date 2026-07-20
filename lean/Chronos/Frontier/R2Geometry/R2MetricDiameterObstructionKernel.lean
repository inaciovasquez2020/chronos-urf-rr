import Chronos.Frontier.R2Geometry.R2BoundarySupportMonotonicity

/-!
# The metric diameter obstruction kernel

For any `R2FillingGeometry`, if every admissible filling has support diameter
at most `D`, then a boundary whose support contains two points farther apart
than `D` cannot have an admissible filling.

This proof uses no finite enumeration, `native_decide`, or packet-specific
constructors.
-/

noncomputable section

namespace Chronos
namespace Frontier

open R2FillingGeometry

variable
  (G : R2FillingGeometry)
  (Adm : (G.Face2 →₀ F2) → Prop)
  (D : ℝ)

/--
Every admissible filling has metric support diameter at most `D`, expressed
pointwise.
-/
def AdmissibleLocalized : Prop :=
  ∀ F,
    Adm F →
    ∀ x ∈ G.supp2 F,
      ∀ y ∈ G.supp2 F,
        dist x y ≤ D

/--
If a boundary contains two support points farther apart than the localization
bound for admissible fillings, then it has no admissible filling.
-/
theorem diameter_separation_filling_obstruction
    (hLoc : AdmissibleLocalized G Adm D)
    (c : G.Face1 →₀ F2)
    (hSep : G.Separated c D) :
    ¬ G.Fillable Adm c := by
  rintro ⟨F, hBoundary, hAdm⟩
  obtain
    ⟨xLeft, hxLeft, xRight, hxRight, hSeparated⟩ :=
    hSep

  have hBoundarySupport :
      G.supp1 c ⊆ G.supp2 F := by
    rw [← hBoundary]
    exact supp1_boundary_subset_supp2 G F

  have hxLeftFilling :
      xLeft ∈ G.supp2 F :=
    hBoundarySupport hxLeft

  have hxRightFilling :
      xRight ∈ G.supp2 F :=
    hBoundarySupport hxRight

  have hLocalized :
      dist xLeft xRight ≤ D :=
    hLoc F hAdm
      xLeft hxLeftFilling
      xRight hxRightFilling

  exact (not_le.mpr hSeparated) hLocalized

end Frontier
end Chronos
