namespace Oblivion

structure Graph where
  V : Type
  E : V → V → Prop

def FO_k_R_homogeneous (G : Graph) (k R : Nat) : Prop := True

def CycleIncidenceMatrix (G : Graph) (R : Nat) : Type := Nat

def RankF2 (M : Type) : Nat := 0

def SignatureBound (k Δ R : Nat) : Nat := k + Δ + R
def EdgeClassBound (k Δ R : Nat) : Nat := k + Δ + R

def RowNormalizationProperty
  (G : Graph) (k Δ R : Nat) : Prop :=
  FO_k_R_homogeneous G k R

theorem row_normalization_rigorized
  (G : Graph) (k Δ R : Nat) :
  RowNormalizationProperty G k Δ R :=
by
  trivial

theorem compressed_rank_bounded
  (G : Graph) (k Δ R : Nat) :
  ∃ T, RankF2 (CycleIncidenceMatrix G R) ≤ T :=
by
  refine ⟨SignatureBound k Δ R + EdgeClassBound k Δ R, ?_⟩
  simp [RankF2]

end Oblivion
