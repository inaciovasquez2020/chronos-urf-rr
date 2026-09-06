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

def FrontierStatus : String :=
  "CONDITIONAL_CLAUSE_DUAL_DEPTH_REDUCTION"

def Boundary : String :=
  "The arithmetic depth reduction is proved. The semantic ClauseDualSupportWall for the actual transcript process is not proved here; no unconditional EntropyDepth, Oblivion, P vs NP, or Clay-problem closure is claimed."

def NextMissingLemma : String :=
  "Prove ClauseDualSupportWall from the actual q-clause-local transcript semantics and clause-parity indistinguishability, tracking cumulative queried support across time."

end ClauseDualDistanceDepthReduction
end Frontier
end Chronos
