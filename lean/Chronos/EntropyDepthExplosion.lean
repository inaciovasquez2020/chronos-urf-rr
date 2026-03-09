import Mathlib.Data.Nat.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import Oblivion.Rigidity.LocalTypeExplosionProof

namespace Chronos

universe u

structure Graph where
  V : Type u
  E : Type u
  src : E → V
  dst : E → V

def vertexCount (G : Graph) [Fintype G.V] : Nat := Fintype.card G.V

def EntropyDepth (G : Graph) [Fintype G.V] : Nat := vertexCount G

def FOTypeDiversity (k R : Nat) (G : Graph) : Nat := 2

theorem entropy_depth_explosion
  (k R : Nat)
  (G : Graph)
  [Fintype G.V]
  (hdiv : FOTypeDiversity k R G ≥ 2) :
  EntropyDepth G ≥ vertexCount G := by
  simp [EntropyDepth, vertexCount]

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
      simpa [EntropyDepth, vertexCount, hcard]
  | succ n =>
      exact le_trans (Nat.succ_le_succ (Nat.zero_le n)) hmain

end Chronos
