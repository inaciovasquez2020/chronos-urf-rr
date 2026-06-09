import Chronos.Frontier.QKDiniUniformCoefficientBounds

namespace Chronos
namespace Frontier

def ConcreteQKDiniCoefficientFamily : QKDiniCoefficientFamily where
  Index := Unit
  coefficient := fun _ _ => 0

def ConcreteQKDiniCoefficientFamilyBoundWitness :
    QKDiniUniformCoefficientBounds ConcreteQKDiniCoefficientFamily where
  bound := 0
  coefficient_le_bound := by
    intro _ _
    exact Nat.le_refl 0

theorem concreteQKDiniCoefficientFamilyBoundWitness_closed :
    ∀ i : ConcreteQKDiniCoefficientFamily.Index,
      ∀ n : Nat,
        ConcreteQKDiniCoefficientFamily.coefficient i n
          ≤ ConcreteQKDiniCoefficientFamilyBoundWitness.bound :=
  ConcreteQKDiniCoefficientFamilyBoundWitness.coefficient_le_bound

def ConcreteQKDiniCoefficientFamilyBoundWitnessStatus : String :=
  "CONCRETE_ZERO_FAMILY_BOUND_WITNESS_ONLY"

end Frontier
end Chronos
