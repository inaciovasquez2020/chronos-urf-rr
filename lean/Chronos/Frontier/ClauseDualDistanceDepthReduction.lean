import Mathlib.Data.Fintype.Card

namespace Chronos
namespace Frontier
namespace ClauseDualDistanceDepthReduction

/--
Abstract data for a clause-local transcript at a candidate successful depth.
`dualDistance` is the clause-dual support wall, `perStepSupport` is the maximum
number of fresh clause coordinates exposed per step, and `depth` is zero-based.
-/
structure ClauseLocalDepthInput where
  dualDistance : Nat
  perStepSupport : Nat
  depth : Nat

/-- Maximum cumulative clause support after steps `0, ..., depth`. -/
def cumulativeClauseSupport (X : ClauseLocalDepthInput) : Nat :=
  (X.depth + 1) * X.perStepSupport

/--
A semantic locality wall: below the clause-dual distance, the target success
predicate cannot hold.  This is the object that must be proved from the actual
transcript semantics and the clause-parity indistinguishability argument.
-/
def ClauseDualSupportWall
    (Success : ClauseLocalDepthInput → Prop) : Prop :=
  ∀ X : ClauseLocalDepthInput,
    cumulativeClauseSupport X < X.dualDistance →
    ¬ Success X

/--
Correct depth reduction: once the locality wall is available, success at depth
`t` forces the cumulative exposed support `(t+1)q` to reach the clause-dual
distance.  No claim is made that `q < d` blocks success for all time.
-/
theorem success_forces_cumulative_support_reaches_dual_distance
    {Success : ClauseLocalDepthInput → Prop}
    (hwall : ClauseDualSupportWall Success)
    {X : ClauseLocalDepthInput}
    (hsuccess : Success X) :
    X.dualDistance ≤ cumulativeClauseSupport X := by
  cases Nat.lt_or_ge (cumulativeClauseSupport X) X.dualDistance with
  | inl hlt =>
      exact (hwall X hlt hsuccess).elim
  | inr hge =>
      exact hge

/--
Equivalent fail-closed form used before the threshold is reached.
-/
theorem no_success_below_dual_distance
    {Success : ClauseLocalDepthInput → Prop}
    (hwall : ClauseDualSupportWall Success)
    (X : ClauseLocalDepthInput)
    (hbelow : cumulativeClauseSupport X < X.dualDistance) :
    ¬ Success X :=
  hwall X hbelow

/-- A `d`-coordinate parity support embedded in an `m`-coordinate instance. -/
structure IndexedClauseParitySupport (m d : Nat) where
  coord : Fin d → Fin m
  coord_injective : Function.Injective coord

/--
If every parity-support coordinate occurs among `t` queried coordinates, then
there must be at least `d` query slots.  Repeated queries do not help.
-/
theorem support_card_le_query_card_of_cover
    {m d t : Nat}
    (S : IndexedClauseParitySupport m d)
    (queries : Fin t → Fin m)
    (hcover : ∀ i : Fin d, ∃ j : Fin t, S.coord i = queries j) :
    d ≤ t := by
  let slot : Fin d → Fin t := fun i => Classical.choose (hcover i)
  have hslot : ∀ i : Fin d, S.coord i = queries (slot i) := by
    intro i
    exact Classical.choose_spec (hcover i)
  have hslot_injective : Function.Injective slot := by
    intro a b hab
    apply S.coord_injective
    calc
      S.coord a = queries (slot a) := hslot a
      _ = queries (slot b) := by rw [hab]
      _ = S.coord b := (hslot b).symm
  have hcard := Fintype.card_le_of_injective slot hslot_injective
  simpa using hcard

/--
If fewer than `d` query slots are available, some coordinate of a `d`-element
parity support is absent from the query list.
-/
theorem exists_unqueried_support_coordinate
    {m d t : Nat}
    (S : IndexedClauseParitySupport m d)
    (queries : Fin t → Fin m)
    (hlt : t < d) :
    ∃ i : Fin d, ∀ j : Fin t, S.coord i ≠ queries j := by
  apply Classical.byContradiction
  intro hnone
  have hcover : ∀ i : Fin d, ∃ j : Fin t, S.coord i = queries j := by
    intro i
    apply Classical.byContradiction
    intro hi
    apply hnone
    refine ⟨i, ?_⟩
    intro j hij
    exact hi ⟨j, hij⟩
  have hle : d ≤ t := support_card_le_query_card_of_cover S queries hcover
  exact (Nat.not_le_of_gt hlt) hle

def FrontierStatus : String :=
  "CONDITIONAL_CLAUSE_DUAL_DEPTH_REDUCTION"

def Boundary : String :=
  "The arithmetic depth reduction and parity-support query pigeonhole are proved. The semantic implication from actual adaptive transcript success to covering the parity support is not proved here; no unconditional EntropyDepth, Oblivion, P vs NP, or Clay-problem closure is claimed."

def NextMissingLemma : String :=
  "Prove that an exact adaptive clause-query decision tree which determines a supported parity must query every support coordinate along each successful leaf; then combine with exists_unqueried_support_coordinate."

end ClauseDualDistanceDepthReduction
end Frontier
end Chronos
