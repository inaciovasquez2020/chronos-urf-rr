namespace Chronos
namespace Frontier

structure QKDiniCoefficientFamily where
  Index : Type
  coefficient : Index → Nat → Nat

structure QKDiniUniformCoefficientBounds
    (F : QKDiniCoefficientFamily) where
  bound : Nat
  coefficient_le_bound :
    ∀ i : F.Index, ∀ n : Nat, F.coefficient i n ≤ bound

def QKDiniUniformCoefficientBoundsStatus : String :=
  "UNIFORM_COEFFICIENT_BOUNDS_INTERFACE_ONLY"

theorem qkDiniUniformCoefficientBounds_boundary
    (F : QKDiniCoefficientFamily)
    (B : QKDiniUniformCoefficientBounds F) :
    ∀ i : F.Index, ∀ n : Nat, F.coefficient i n ≤ B.bound :=
  B.coefficient_le_bound

end Frontier
end Chronos
