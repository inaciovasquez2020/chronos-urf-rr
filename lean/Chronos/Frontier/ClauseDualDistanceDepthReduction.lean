import Mathlib.Data.Fintype.Card
import Mathlib.Data.List.Basic

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

/-- Flip one clause-side Boolean coordinate. -/
def flipClauseBit
    {m : Nat}
    (x : Fin m → Bool)
    (j : Fin m) : Fin m → Bool :=
  fun k => if k = j then !x k else x k

/--
An abstract Boolean target whose value changes whenever any coordinate in its
indexed parity support is flipped.  Ordinary parity on those coordinates is the
canonical example.
-/
structure SupportedParityTarget (m d : Nat) where
  support : IndexedClauseParitySupport m d
  target : (Fin m → Bool) → Bool
  flip_support_changes :
    ∀ x : Fin m → Bool, ∀ i : Fin d,
      target (flipClauseBit x (support.coord i)) = !(target x)

/--
A fixed list of fewer than `d` coordinate queries cannot determine a target
which flips on every coordinate of a `d`-element parity support: two inputs
agree on all queried coordinates while the target values differ.
-/
theorem fixed_queries_leave_opposite_parity_pair
    {m d t : Nat}
    (P : SupportedParityTarget m d)
    (queries : Fin t → Fin m)
    (hlt : t < d) :
    ∃ x y : Fin m → Bool,
      (∀ j : Fin t, x (queries j) = y (queries j)) ∧
      P.target x ≠ P.target y := by
  rcases exists_unqueried_support_coordinate P.support queries hlt with ⟨i, hi⟩
  let x : Fin m → Bool := fun _ => false
  let y : Fin m → Bool := flipClauseBit x (P.support.coord i)
  refine ⟨x, y, ?_, ?_⟩
  · intro j
    have hne : queries j ≠ P.support.coord i := fun h => hi j h.symm
    simp [y, flipClauseBit, hne]
  · have hy : P.target y = !(P.target x) := by
      simpa [y] using P.flip_support_changes x i
    rw [hy]
    cases h : P.target x <;> simp [h]

/-- A deterministic adaptive decision tree querying clause-side Boolean coordinates. -/
inductive ClauseQueryTree (m : Nat) (α : Type) where
  | leaf : α → ClauseQueryTree m α
  | node : Fin m → ClauseQueryTree m α → ClauseQueryTree m α → ClauseQueryTree m α

namespace ClauseQueryTree

/-- Maximum number of queries on any root-to-leaf path. -/
def depth {m : Nat} {α : Type} : ClauseQueryTree m α → Nat
  | .leaf _ => 0
  | .node _ left right => Nat.succ (Nat.max (depth left) (depth right))

/-- Evaluate the adaptive query tree on one Boolean instance. -/
def eval {m : Nat} {α : Type} : ClauseQueryTree m α → (Fin m → Bool) → α
  | .leaf value, _ => value
  | .node query left right, x =>
      match x query with
      | false => eval left x
      | true => eval right x

/-- Ordered query path followed by one Boolean instance. -/
def queriesOn {m : Nat} {α : Type} : ClauseQueryTree m α → (Fin m → Bool) → List (Fin m)
  | .leaf _, _ => []
  | .node query left right, x =>
      match x query with
      | false => query :: queriesOn left x
      | true => query :: queriesOn right x

/-- Every realized query path has length at most the tree depth. -/
theorem queriesOn_length_le_depth
    {m : Nat} {α : Type}
    (T : ClauseQueryTree m α)
    (x : Fin m → Bool) :
    (queriesOn T x).length ≤ depth T := by
  induction T with
  | leaf value =>
      simp [queriesOn, depth]
  | node query left right ihLeft ihRight =>
      cases hq : x query with
      | false =>
          simpa [queriesOn, depth, hq] using
            Nat.succ_le_succ (Nat.le_trans ihLeft (Nat.le_max_left _ _))
      | true =>
          simpa [queriesOn, depth, hq] using
            Nat.succ_le_succ (Nat.le_trans ihRight (Nat.le_max_right _ _))

/--
If `y` agrees with `x` on every coordinate queried along the path followed by
`x`, then the adaptive tree follows the same branches and returns the same output.
-/
theorem eval_eq_of_agree_queriesOn
    {m : Nat} {α : Type}
    (T : ClauseQueryTree m α) :
    ∀ x y : Fin m → Bool,
      (∀ q : Fin m, q ∈ queriesOn T x → x q = y q) →
      eval T x = eval T y := by
  induction T with
  | leaf value =>
      intro x y hagree
      rfl
  | node query left right ihLeft ihRight =>
      intro x y hagree
      cases hx : x query with
      | false =>
          have hq : x query = y query :=
            hagree query (by simp [queriesOn, hx])
          have hy : y query = false := by
            calc
              y query = x query := hq.symm
              _ = false := hx
          have hsub :
              ∀ q : Fin m, q ∈ queriesOn left x → x q = y q := by
            intro q hmem
            exact hagree q (by simp [queriesOn, hx, hmem])
          simpa [eval, hx, hy] using ihLeft x y hsub
      | true =>
          have hq : x query = y query :=
            hagree query (by simp [queriesOn, hx])
          have hy : y query = true := by
            calc
              y query = x query := hq.symm
              _ = true := hx
          have hsub :
              ∀ q : Fin m, q ∈ queriesOn right x → x q = y q := by
            intro q hmem
            exact hagree q (by simp [queriesOn, hx, hmem])
          simpa [eval, hx, hy] using ihRight x y hsub

end ClauseQueryTree

/--
Deterministic adaptive parity wall.  Any clause-query tree whose worst-case
query depth is strictly smaller than the parity-support size has two inputs
which reach the same output leaf while the supported target parity differs.
-/
theorem adaptive_query_tree_leaves_opposite_parity_pair
    {m d : Nat} {α : Type}
    (P : SupportedParityTarget m d)
    (T : ClauseQueryTree m α)
    (hdepth : ClauseQueryTree.depth T < d) :
    ∃ x y : Fin m → Bool,
      ClauseQueryTree.eval T x = ClauseQueryTree.eval T y ∧
      P.target x ≠ P.target y := by
  let x : Fin m → Bool := fun _ => false
  let path : List (Fin m) := ClauseQueryTree.queriesOn T x
  have hpath_le : path.length ≤ ClauseQueryTree.depth T := by
    simpa [path] using ClauseQueryTree.queriesOn_length_le_depth T x
  have hpath_lt : path.length < d := Nat.lt_of_le_of_lt hpath_le hdepth
  let queries : Fin path.length → Fin m := fun j => path.get j
  rcases exists_unqueried_support_coordinate P.support queries hpath_lt with ⟨i, hi⟩
  let y : Fin m → Bool := flipClauseBit x (P.support.coord i)
  have hagree :
      ∀ q : Fin m, q ∈ ClauseQueryTree.queriesOn T x → x q = y q := by
    intro q hmem
    have hmemPath : q ∈ path := by
      simpa [path] using hmem
    rcases List.mem_iff_get.mp hmemPath with ⟨j, hj⟩
    have hsneq : P.support.coord i ≠ q := by
      intro hsq
      apply hi j
      calc
        P.support.coord i = q := hsq
        _ = path.get j := hj.symm
    have hne : q ≠ P.support.coord i := fun h => hsneq h.symm
    simp [y, flipClauseBit, hne]
  have heval : ClauseQueryTree.eval T x = ClauseQueryTree.eval T y :=
    ClauseQueryTree.eval_eq_of_agree_queriesOn T x y hagree
  have hyTarget : P.target y = !(P.target x) := by
    simpa [y] using P.flip_support_changes x i
  have htarget : P.target x ≠ P.target y := by
    rw [hyTarget]
    cases h : P.target x <;> simp [h]
  exact ⟨x, y, heval, htarget⟩

/--
Exact deterministic computation of a target with a `d`-coordinate parity
support requires worst-case adaptive query depth at least `d`.
-/
theorem exact_supported_parity_computation_requires_depth
    {m d : Nat}
    (P : SupportedParityTarget m d)
    (T : ClauseQueryTree m Bool)
    (hexact : ∀ x : Fin m → Bool, ClauseQueryTree.eval T x = P.target x) :
    d ≤ ClauseQueryTree.depth T := by
  cases Nat.lt_or_ge (ClauseQueryTree.depth T) d with
  | inl hlt =>
      rcases adaptive_query_tree_leaves_opposite_parity_pair P T hlt with
        ⟨x, y, heval, htarget⟩
      have hsame : P.target x = P.target y := by
        calc
          P.target x = ClauseQueryTree.eval T x := (hexact x).symm
          _ = ClauseQueryTree.eval T y := heval
          _ = P.target y := hexact y
      exact (htarget hsame).elim
  | inr hge =>
      exact hge

/--
If an `r`-round clause-local computation with per-round query budget `q`
compiles to a deterministic query tree of depth at most `r*q`, exact
computation of a `d`-supported parity target forces `d ≤ r*q`.
-/
theorem exact_supported_parity_computation_requires_round_budget
    {m d : Nat}
    (P : SupportedParityTarget m d)
    (T : ClauseQueryTree m Bool)
    (rounds perRoundSupport : Nat)
    (hbudget : ClauseQueryTree.depth T ≤ rounds * perRoundSupport)
    (hexact : ∀ x : Fin m → Bool, ClauseQueryTree.eval T x = P.target x) :
    d ≤ rounds * perRoundSupport := by
  exact Nat.le_trans
    (exact_supported_parity_computation_requires_depth P T hexact)
    hbudget

def FrontierStatus : String :=
  "DETERMINISTIC_ADAPTIVE_CLAUSE_DUAL_DEPTH_WALL"

def Boundary : String :=
  "The arithmetic depth reduction, parity-support query pigeonhole, fixed-query collision, adaptive query-path semantics, deterministic adaptive opposite-parity collision, exact depth lower bound, and conditional round-budget lower bound are proved. The repository-native EFTranscript builder is currently degenerate and does not yet supply the required compilation-to-query-tree theorem; any randomized/constant-bias lift also remains open. No unconditional EntropyDepth, Oblivion, P vs NP, or Clay-problem closure is claimed."

def NextMissingLemma : String :=
  "Replace or strengthen the degenerate repository-native EFTranscript semantics so an r-round q-local computation compiles to a ClauseQueryTree with depth ≤ r*q, then connect the target application to SupportedParityTarget."

end ClauseDualDistanceDepthReduction
end Frontier
end Chronos
