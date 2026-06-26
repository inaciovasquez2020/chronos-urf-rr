import Chronos.Frontier.NewsteinR1R2R3NativeBindingSpec
namespace Chronos.Frontier

universe u

structure CanonicalWitnessInput (α : Type u) where
  r1w : R1SemanticData
  r2w : R2SemanticData
  r3w : R3SemanticData

end Chronos.Frontier
