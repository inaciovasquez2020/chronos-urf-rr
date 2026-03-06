-- lean/oblivion/cor/PackingBound.lean  (APPEND at end)

import Mathlib.Data.Finset
import Mathlib.Data.Nat.Basic

namespace PackingBound

variable {α : Type} [DecidableEq α]

lemma packing_bound_union
(S : Finset (Finset α))
(L : Nat)
(hpair : S.Pairwise (fun A B => Disjoint A B))
(hlen : ∀ A ∈ S, A.card ≤ L) :
(S.biUnion id).card ≤ S.card * L :=
by
  classical
  -- Uses Mathlib lemma: card_biUnion + sum_le_card_nsmul
  have hU : (S.biUnion id).card = ∑ A in S, A.card := by
    simpa using Finset.card_biUnion hpair
  have hsum : (∑ A in S, A.card) ≤ S.card * L := by
    -- each A.card ≤ L
    exact Finset.sum_le_card_nsmul S (fun A => A.card) L (by
      intro A hA
      exact hlen A hA)
  exact le_trans (by simpa [hU]) hsum

end PackingBound
