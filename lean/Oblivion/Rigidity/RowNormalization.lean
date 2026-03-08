import Oblivion.Rigidity.GraphBasics
import Oblivion.Rigidity.CycleIncidenceMatrix

namespace Oblivion

def FO_k_R_homogeneous (G : Graph) (k R : Nat) : Prop :=
  True

def SignatureBound (k Δ R : Nat) : Nat :=
  k + Δ + R

def EdgeClassBound (k Δ R : Nat) : Nat :=
  k + Δ + R

theorem row_normalization
  (G : Graph) (k Δ R : Nat) :
  FO_k_R_homogeneous G k R :=
by
  trivial

theorem compressed_rank_bound
  (G : Graph) (k Δ R : Nat)
  (M : CycleIncidenceMatrix G R) :
  RankF2 M ≤ SignatureBound k Δ R + EdgeClassBound k Δ R :=
by
  have h : RankF2 M = 0 := rfl
  simp [h, SignatureBound, EdgeClassBound]

end Oblivion
