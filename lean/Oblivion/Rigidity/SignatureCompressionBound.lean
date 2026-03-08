import Mathlib.Combinatorics.SimpleGraph.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.LinearAlgebra.FiniteDimensional
import Oblivion.Rigidity.FiniteGraphModel
import Oblivion.Rigidity.CycleRowSpace
import Oblivion.Rigidity.CompressionArchitecture
import Oblivion.Rigidity.FokNeighborhoodType
import Oblivion.Rigidity.BoundedRadiusCycleRows

namespace Oblivion

universe u

variable {V α : Type u}

def SignatureClassBound (k Δ R : Nat) : Nat := k + Δ + R + 1

def EdgeClassBound' (k Δ R : Nat) : Nat := k + Δ + R + 1

theorem rowRank_le_card_rows
    {ι β : Type u} [Fintype β] [Fintype ι] (rows : ι → β → ZMod 2) :
    rowRank rows ≤ Fintype.card ι := by
  classical
  simpa [rowRank, rowSpace] using
    FiniteDimensional.finrank_span_le_card (K := ZMod 2) (s := Set.range rows)

theorem compressedRank_le_card_classes
    {ι β : Type u} [Fintype β] [Fintype ι] [DecidableEq β]
    (rows : ι → β → ZMod 2) :
    rowRank rows ≤ Fintype.card ι := by
  exact rowRank_le_card_rows rows

theorem signatureCompressionBound
    {V α ι : Type u}
    [Fintype (Edge V)] [DecidableEq (Edge V)]
    [Fintype α] [DecidableEq α] [Fintype ι]
    (π : EdgeCompression V α) (C : CycleFamily ι V) :
    compressedRank π C ≤ Fintype.card ι := by
  simpa [compressedRank] using
    compressedRank_le_card_classes (rowBySignature π C)

end Oblivion
