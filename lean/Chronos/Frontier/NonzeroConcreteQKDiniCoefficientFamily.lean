import Chronos.Frontier.QKDiniUniformCoefficientBounds

namespace Chronos
namespace Frontier

def NonzeroConcreteQKDiniCoefficientFamily : QKDiniCoefficientFamily where
  Index := Unit
  coefficient := fun _ _ => 1

theorem nonzeroConcreteQKDiniCoefficientFamily_nonzero :
    ∃ i : NonzeroConcreteQKDiniCoefficientFamily.Index,
      ∃ n : Nat,
        NonzeroConcreteQKDiniCoefficientFamily.coefficient i n ≠ 0 := by
  exact ⟨(), 0, by decide⟩

def NonzeroConcreteQKDiniCoefficientFamilyBoundWitness :
    QKDiniUniformCoefficientBounds NonzeroConcreteQKDiniCoefficientFamily where
  bound := 1
  coefficient_le_bound := by
    intro _ _
    exact Nat.le_refl 1

theorem nonzeroConcreteQKDiniCoefficientFamily_uniform_bound :
    ∀ i : NonzeroConcreteQKDiniCoefficientFamily.Index,
      ∀ n : Nat,
        NonzeroConcreteQKDiniCoefficientFamily.coefficient i n
          ≤ NonzeroConcreteQKDiniCoefficientFamilyBoundWitness.bound :=
  NonzeroConcreteQKDiniCoefficientFamilyBoundWitness.coefficient_le_bound

def NonzeroConcreteQKDiniCoefficientFamilyStatus : String :=
  "NONZERO_CONCRETE_CONSTANT_ONE_FAMILY_BOUND_WITNESS_ONLY"

end Frontier
end Chronos
