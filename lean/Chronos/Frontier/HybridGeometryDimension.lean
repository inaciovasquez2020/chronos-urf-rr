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

def HybridGeometryDimension.zero_separation
    (H : HybridGeometryDimension)
    (x : H.Space) : Prop :=
  H.separation x x = 0

theorem HybridGeometryDimension.same_dimension_refl
    (H : HybridGeometryDimension)
    (x : H.Space) :
    H.same_dimension x x :=
  rfl

end Frontier
end Chronos
