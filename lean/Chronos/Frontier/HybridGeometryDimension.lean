import Mathlib.Data.Real.Basic

namespace Chronos
namespace Frontier

structure HybridGeometryDimension where
  Space : Type
  dimension : Space → Nat
  separation : Space → Space → Real

def HybridGeometryDimension.same_dimension
    (H : HybridGeometryDimension)
    (x y : H.Space) : Prop :=
  H.dimension x = H.dimension y

def HybridGeometryDimension.symmetric_separation
    (H : HybridGeometryDimension) : Prop :=
  ∀ x y : H.Space, H.separation x y = H.separation y x

def HybridGeometryDimension.nonnegative_separation
    (H : HybridGeometryDimension) : Prop :=
  ∀ x y : H.Space, 0 ≤ H.separation x y

def HybridGeometryDimension.zero_separation
    (H : HybridGeometryDimension)
    (x : H.Space) : Prop :=
  H.separation x x = 0

def HybridGeometryDimension.dimension_potential
    (H : HybridGeometryDimension)
    (x y : H.Space) : Real :=
  H.separation x y + (H.dimension x : Real)

theorem HybridGeometryDimension.dimension_potential_eq
    (H : HybridGeometryDimension)
    (x y : H.Space) :
    H.dimension_potential x y =
      H.separation x y + (H.dimension x : Real) :=
  rfl

def HybridGeometryDimension.gravity_test_surface
    (H : HybridGeometryDimension)
    (x y : H.Space) : Real :=
  H.dimension_potential x y

theorem HybridGeometryDimension.gravity_test_surface_eq
    (H : HybridGeometryDimension)
    (x y : H.Space) :
    H.gravity_test_surface x y =
      H.dimension_potential x y :=
  rfl

theorem HybridGeometryDimension.gravity_test_surface_expanded_eq
    (H : HybridGeometryDimension)
    (x y : H.Space) :
    H.gravity_test_surface x y =
      H.separation x y + (H.dimension x : Real) :=
  rfl

theorem HybridGeometryDimension.same_dimension_gravity_test_dimension_term_eq
    (H : HybridGeometryDimension)
    {x y z : H.Space}
    (h : H.same_dimension x z) :
    H.separation x y + (H.dimension x : Real) =
      H.separation x y + (H.dimension z : Real) := by
  rw [h]

theorem HybridGeometryDimension.same_dimension_refl
    (H : HybridGeometryDimension)
    (x : H.Space) :
    H.same_dimension x x :=
  rfl

theorem HybridGeometryDimension.same_dimension_symm
    (H : HybridGeometryDimension)
    {x y : H.Space} :
    H.same_dimension x y → H.same_dimension y x :=
  Eq.symm

theorem HybridGeometryDimension.same_dimension_trans
    (H : HybridGeometryDimension)
    {x y z : H.Space} :
    H.same_dimension x y →
    H.same_dimension y z →
    H.same_dimension x z :=
  Eq.trans

end Frontier
end Chronos
