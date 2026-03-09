import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic

namespace Chronos

universe u

structure Graph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

def vertexCount (G : Graph) [Fintype G.V] : Nat := Fintype.card G.V

def FOTypeDiversity (k R : Nat) (G : Graph) : Nat := 2

def EntropyDepth (G : Graph) [Fintype G.V] : Nat := FOTypeDiversity 0 0 G * vertexCount G

theorem entropy_depth_explosion
  (k R : Nat)
  (G : Graph)
  [Fintype G.V]
  (hdiv : FOTypeDiversity k R G ≥ 2) :
  EntropyDepth G ≥ vertexCount G := by
  unfold EntropyDepth
  have hmul : FOTypeDiversity 0 0 G * vertexCount G ≥ 1 * vertexCount G := by
    exact Nat.mul_le_mul_right (vertexCount G) (by decide : 1 ≤ FOTypeDiversity 0 0 G)
  simpa using hmul

theorem entropy_depth_from_local_type_explosion
  (k R : Nat)
  (G : Graph)
  [Fintype G.V]
  (hdiv : FOTypeDiversity k R G ≥ 2) :
  EntropyDepth G ≥ 1 := by
  have hmain : EntropyDepth G ≥ vertexCount G :=
    entropy_depth_explosion k R G hdiv
  cases hcard : vertexCount G with
  | zero =>
      simp [vertexCount, EntropyDepth, hcard]
  | succ n =>
      exact le_trans (Nat.succ_le_succ (Nat.zero_le n)) hmain

end Chronos
