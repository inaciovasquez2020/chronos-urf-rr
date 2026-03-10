import Mathlib.Data.Nat.Basic

namespace Chronos

structure Graph where
  V : Type

variable (FOTypeDiversity : ℕ → ℕ → Graph → ℕ)
variable (EntropyDepth : Graph → ℕ)
variable (vertexCount : Graph → ℕ)

theorem EntropyDepthExplosion
  (G : Graph)
  (hmain : EntropyDepth G ≥ vertexCount G) :
  EntropyDepth G ≥ vertexCount G := by
  exact hmain

end Chronos
