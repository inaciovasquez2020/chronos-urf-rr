import Oblivion.Rigidity.CompressionArchitecture

namespace Oblivion

variable {V α ι : Type _}

def FOHomogeneous (k R : Nat) : Prop := True

def SignatureBound (k Δ R : Nat) : Nat := k + Δ + R + 1

def EdgeClassBound (k Δ R : Nat) : Nat := k + Δ + R + 1

def CycleOverlapRankRigidityStatement
    [Fintype (Edge V)] [DecidableEq (Edge V)] [Fintype α] [DecidableEq α]
    (π : EdgeCompression V α) (C : CycleFamily ι V) (k Δ R T : Nat) : Prop :=
  FOHomogeneous k R → compressedRank π C ≤ T

theorem rigidity_statement_from_bound
    [Fintype (Edge V)] [DecidableEq (Edge V)] [Fintype α] [DecidableEq α]
    (π : EdgeCompression V α) (C : CycleFamily ι V) (k Δ R : Nat)
    (h : compressedRank π C ≤ SignatureBound k Δ R + EdgeClassBound k Δ R) :
    CycleOverlapRankRigidityStatement π C k Δ R
      (SignatureBound k Δ R + EdgeClassBound k Δ R) := by
  intro _
  exact h

end Oblivion
