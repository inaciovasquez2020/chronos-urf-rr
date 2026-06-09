import Chronos.Frontier.QKDiniUniformCoefficientBounds

namespace Chronos
namespace Frontier

structure QKDiniSourceObject where
  Index : Type
  coefficient : Index → Nat → Nat
  bound : Nat
  nonzero : ∃ i : Index, ∃ n : Nat, coefficient i n ≠ 0
  uniform_bound : ∀ i : Index, ∀ n : Nat, coefficient i n ≤ bound

def QKDiniSourceObject.toCoefficientFamily
    (S : QKDiniSourceObject) : QKDiniCoefficientFamily where
  Index := S.Index
  coefficient := S.coefficient

def QKDiniSourceObject.toUniformCoefficientBounds
    (S : QKDiniSourceObject) :
    QKDiniUniformCoefficientBounds S.toCoefficientFamily where
  bound := S.bound
  coefficient_le_bound := S.uniform_bound

theorem qkDiniSourceObject_extracted_coefficient_nonzero
    (S : QKDiniSourceObject) :
    ∃ i : S.toCoefficientFamily.Index,
      ∃ n : Nat,
        S.toCoefficientFamily.coefficient i n ≠ 0 :=
  S.nonzero

theorem qkDiniSourceObject_extracted_uniform_bound
    (S : QKDiniSourceObject) :
    ∀ i : S.toCoefficientFamily.Index,
      ∀ n : Nat,
        S.toCoefficientFamily.coefficient i n
          ≤ (S.toUniformCoefficientBounds).bound :=
  S.uniform_bound

def QKDiniSourceDerivedCoefficientFamilyInterfaceStatus : String :=
  "SOURCE_DERIVED_COEFFICIENT_FAMILY_INTERFACE_ONLY"

end Frontier
end Chronos
