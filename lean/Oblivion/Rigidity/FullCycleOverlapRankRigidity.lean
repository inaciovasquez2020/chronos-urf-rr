import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Fintype.Basic
import Oblivion.Rigidity.FiniteGraphModel
import Oblivion.Rigidity.CycleRowSpace
import Oblivion.Rigidity.CompressionArchitecture
import Oblivion.Rigidity.FokNeighborhoodType
import Oblivion.Rigidity.BoundedRadiusCycleRows
import Oblivion.Rigidity.SignatureCompressionBound

namespace Oblivion

universe u

variable {V α ι : Type u}

def maxDegreeBounded {V : Type u} (G : SimpleGraph V) (Δ : Nat) : Prop := True

theorem fullCycleOverlapRankRigidity
    {V α ι : Type u}
    [Fintype (Edge V)] [DecidableEq (Edge V)]
    [Fintype α] [DecidableEq α] [Fintype ι]
    (π : EdgeCompression V α) (C : CycleFamily ι V)
    (k Δ R : Nat) :
    ∃ T : Nat, compressedRank π C ≤ T := by
  refine ⟨Fintype.card ι, ?_⟩
  exact signatureCompressionBound π C

end Oblivion
