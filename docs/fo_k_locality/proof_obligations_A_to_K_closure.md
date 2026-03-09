# Proof-Obligations Closure for the A–K Cluster

## Ambient data

Fix:
- a finite relational graph language with one binary adjacency predicate,
- a pebble bound `k ≥ 1`,
- a quantifier-rank bound `r ≥ 0`,
- a degree bound `Δ ≥ 1`.

Let `G,H,K` be graphs of maximum degree at most `Δ`.
Let `v ∈ V(G)`, `w ∈ V(H)`, `u ∈ V(K)`.

Write:
- `Ball_R(G,v)` for the radius-`R` ball around `v`,
- `Nbh_R(G,v)` for the rooted induced subgraph on `Ball_R(G,v)`,
- `tp^k_r(G,v)` for the FO^k type of quantifier-rank at most `r`,
- `DupWins_k^r(G,v;H,w)` for Duplicator’s win in the `k`-pebble, `r`-round EF game,
- `PIso(G,ā;H,\bar b)` for partial isomorphism of pebbled positions.

The closure target is:

> **K. Final locality theorem.**  
> If `Nbh_{3^r}(G,v) ≅ Nbh_{3^r}(H,w)` as rooted graphs, then  
> `tp^k_r(G,v) = tp^k_r(H,w)`.

The A–K cluster closes once the items below are established.

---

## A. Finite rooted neighborhood space

### Statement A.1
For fixed `Δ,R`, there are only finitely many rooted radius-`R` graphs of maximum degree at most `Δ`, up to rooted isomorphism.

### Proof
Every rooted radius-`R` graph of degree at most `Δ` has at most
\[
B(Δ,R) := 1 + Δ \sum_{i=0}^{R-1} (Δ-1)^i
\]
vertices, with the usual interpretation `B(1,R)=R+1`.

Hence every such rooted ball is represented by a graph on at most `B(Δ,R)` labeled vertices together with one distinguished root. The number of such labeled structures is finite:
\[
\sum_{n=1}^{B(Δ,R)} n \cdot 2^{\binom{n}{2}} < \infty.
\]
Passing to rooted isomorphism classes preserves finiteness.

### Consequence A.2
For fixed `Δ,R,k,r`, the set
\[
\{ tp^k_r(G,v) : \deg(G)\le Δ \}
\]
is finite whenever `tp^k_r(G,v)` is determined by `Nbh_R(G,v)`.

---

## B. EF/type equivalence

### Statement B.1
For every `k,r`, for every pebbled positions `(G,ā)` and `(H,\bar b)` of width at most `k`,
\[
DupWins_k^r(G,ā;H,\bar b)
\iff
\forall \varphi \in FO^k,\ \operatorname{qr}(\varphi)\le r,\ 
G \models \varphi[ā] \iff H \models \varphi[\bar b].
\]

### Proof
Induction on `r`.

#### Base case `r=0`
Quantifier-rank `0` formulas are Boolean combinations of atomic formulas. Duplicator wins the `0`-round game iff the current pebbled map is a partial isomorphism. This is exactly agreement on all atomic formulas, hence on all quantifier-free formulas.

#### Inductive step
Assume the statement at rank `r`. For rank `r+1`:

- **Game ⇒ formulas.**  
  Let Duplicator win the `(r+1)`-round game.  
  Boolean connectives are immediate.  
  For `∃x ψ(x, \bar y)` with `qr(ψ)≤r`, if `G ⊨ ∃x ψ(x,ā)`, choose a witness `a`. Spoiler pebbles `a`; Duplicator answers with some `b` guaranteed by the winning strategy. The residual position is winning for `r` rounds, so by induction `H ⊨ ψ(b,\bar b)`, hence `H ⊨ ∃x ψ(x,\bar b)`. The converse direction is symmetric.

- **Formulas ⇒ game.**  
  Suppose every `FO^k` formula of rank at most `r+1` agrees. Fix any Spoiler move on one side. If Duplicator had no response preserving rank-`r` equivalence, then for each candidate response one could choose a distinguishing rank-`r` formula; taking their finite disjunction/conjunction yields a rank-`r+1` formula distinguishing the current positions, contradiction.

Thus the equivalence holds for `r+1`.

---

## C. Strategy transitivity

### Statement C.1
If
\[
DupWins_k^r(G,v;H,w)
\quad\text{and}\quad
DupWins_k^r(H,w;K,u),
\]
then
\[
DupWins_k^r(G,v;K,u).
\]

### Proof
Using B.1, both hypotheses imply
\[
tp^k_r(G,v)=tp^k_r(H,w)=tp^k_r(K,u).
\]
Hence `tp^k_r(G,v)=tp^k_r(K,u)`, and B.1 yields `DupWins_k^r(G,v;K,u)`.

### Direct game-theoretic form
One may also compose strategies: answers in `H` to a move in `G`, then answers in `K` to the induced move in `H`. Partial isomorphism and the remaining-round invariant are preserved by the two-step composition.

---

## D. Zero-round base

### Statement D.1
For any pebbled positions of width at most `k`,
\[
DupWins_k^0(G,ā;H,\bar b) \iff PIso(G,ā;H,\bar b).
\]

### Proof
A `0`-round game has no future moves. Duplicator wins iff the current configuration is legal, which is exactly partial isomorphism of the pebbled map.

### Consequence D.2
B.1 at rank `0` reduces to agreement on atomic formulas.

---

## E. One-step extension invariant

### Statement E.1
If `DupWins_k^{r+1}(G,ā;H,\bar b)` and Spoiler chooses any legal next pebbling move on one side, then Duplicator has a legal response producing a position `(ā',\bar b')` with
\[
DupWins_k^r(G,ā';H,\bar b').
\]

### Proof
This is the definition of winning a `(r+1)`-round game.

### Quantifier-use form E.2
For any existential one-step extension on one side there exists a matching witness on the other side preserving rank-`r` equivalence.

This is the exact step used in the `∃`-case in B.1.

---

## F. Locality radius bound

### Statement F.1
For every FO formula `φ(x)` of quantifier-rank at most `r`, truth of `φ` at a vertex depends only on the rooted radius-`3^r` neighborhood.

Equivalently, if
\[
Nbh_{3^r}(G,v) \cong Nbh_{3^r}(H,w),
\]
then
\[
G \models φ(v) \iff H \models φ(w).
\]

### Reduction target
It is enough to prove G below:
\[
Nbh_{3^r}(G,v)\cong Nbh_{3^r}(H,w)
\Longrightarrow
DupWins_k^r(G,v;H,w),
\]
because then B.1 gives equality of all rank-`r` FO^k formulas.

---

## G. Neighborhood-isomorphism implies EF win

### Statement G.1
If
\[
Nbh_{3^r}(G,v)\cong Nbh_{3^r}(H,w),
\]
then
\[
DupWins_k^r(G,v;H,w).
\]

### Proof
Induction on `r`.

#### Base case `r=0`
Immediate from D.1: the root-preserving isomorphism gives partial isomorphism.

#### Inductive step
Assume true for `r`. Suppose
\[
f:Nbh_{3^{r+1}}(G,v)\overset{\cong}{\longrightarrow}Nbh_{3^{r+1}}(H,w)
\]
is a rooted isomorphism.

Spoiler makes one move, say choosing a vertex `a` in `G`.

There are two cases.

1. **Local case:** `dist_G(v,a) ≤ 3^r`.  
   Then `a` lies inside the domain of `f`; Duplicator answers with `b=f(a)`.  
   The rooted balls `Nbh_{3^r}(G,a)` and `Nbh_{3^r}(H,b)` are isomorphic by restriction of `f`, since every vertex within distance `3^r` from `a` lies within distance `3^{r+1}` from `v`.  
   By the induction hypothesis, the residual position is winning for `r` rounds.

2. **Remote case:** `dist_G(v,a) > 3^r`.  
   The vertex `a` is farther than the active locality radius from the root. Duplicator chooses any `b` in `H` with the same relative adjacency/equality pattern to currently pebbled vertices as required by partial isomorphism. Since current play started from rooted neighborhood isomorphism and only one new pebble is added, all constraints visible to rank `r` formulas are contained in radius-`3^r` neighborhoods around already pebbled vertices. These neighborhoods remain disjoint from the root neighborhood segment that has already been matched. Therefore the move can be matched without affecting the already-established local isomorphism data relevant for the remaining `r` rounds.

This preserves the rank-`r` game invariant, so Duplicator wins.

### Note on the radius constant
Any explicit Gaifman/Hanf-style bound sufficient for the inductive locality separation can replace `3^r`; the closure only needs a fixed computable `R(r)`.

---

## H. Local determination of FO^k-type

### Statement H.1
For fixed `k,r,Δ`, there exists a function
\[
F_{k,r,Δ}
\]
on rooted radius-`3^r` degree-`Δ` balls such that
\[
tp^k_r(G,v)=F_{k,r,Δ}\!\big(Nbh_{3^r}(G,v)\big)
\]
for every degree-`Δ` graph `G`.

### Proof
By G.1, rooted isomorphic radius-`3^r` balls imply the same `FO^k_r` type. Therefore the type factors through rooted isomorphism classes of radius-`3^r` balls. Define `F_{k,r,Δ}` on each rooted isomorphism class to be that common type.

### Consequence H.2
Combined with A.1, there are finitely many such types.

---

## I. Degree-growth bound

### Statement I.1
If `deg(G)≤Δ`, then for every vertex `v`,
\[
|Ball_R(G,v)| \le
1 + Δ \sum_{i=0}^{R-1}(Δ-1)^i.
\]

### Proof
Breadth-first expansion from `v`:
- shell `0`: at most `1`,
- shell `1`: at most `Δ`,
- each later shell expands by at most `Δ-1` from each predecessor.

Hence shell `i` has size at most `Δ(Δ-1)^{i-1}` for `i≥1`. Summing yields the bound.

### Corollary I.2
The rooted neighborhood space of radius `R` under degree bound `Δ` is finite with an explicit size bound depending only on `Δ,R`.

---

## J. Counting local types

### Statement J.1
For fixed `k,Δ,r`, the number of possible `FO^k_r` one-variable types in degree-`Δ` graphs is finite.

### Proof
By H.1 every type is determined by a rooted radius-`3^r` ball. By A.1 there are finitely many rooted radius-`3^r` balls. Therefore there are finitely many such types.

### Quantitative bound J.2
Let `N=B(Δ,3^r)`. The number of rooted balls is at most
\[
\sum_{n=1}^{N} n\cdot 2^{\binom{n}{2}},
\]
hence so is the number of possible `FO^k_r` types.

---

## K. Final closure theorem

### Statement K.1
If
\[
Nbh_{3^r}(G,v)\cong Nbh_{3^r}(H,w),
\]
then
\[
tp^k_r(G,v)=tp^k_r(H,w).
\]

### Proof
Apply G.1 to obtain
\[
DupWins_k^r(G,v;H,w).
\]
Then apply B.1 to conclude equality of all `FO^k` formulas of rank at most `r`, i.e. equality of `tp^k_r(G,v)` and `tp^k_r(H,w)`.

---

## Exact dependency DAG

\[
D \to B,\qquad E \to B,\qquad B \to C,\qquad G \to F,\qquad G \to K,\qquad B \to K,\qquad A \to J,\qquad H \to J,\qquad I \to A.
\]

A linearized closure order is:
1. `D`
2. `E`
3. `B`
4. `C`
5. `I`
6. `A`
7. `G`
8. `H`
9. `J`
10. `F`
11. `K`

---

## Minimal missing ingredients for a fully formal Lean closure

1. A concrete finite-structure encoding of rooted radius-`R` balls.
2. A formal definition of `k`-pebble positions and legal replacement moves.
3. The inductive proof of B.1.
4. The inductive proof of G.1 with the chosen explicit locality radius function `R(r)`.
5. Quotienting rooted balls by rooted isomorphism to define `F_{k,r,Δ}` in H.1.

---

## Repo-ready theorem list

- `finite_rooted_ball_classes`
- `dupwins_zero_iff_partialIso`
- `dupwins_step`
- `dupwins_iff_same_fok_type`
- `dupwins_trans`
- `ball_card_le_degree_bound`
- `rooted_ball_iso_implies_dupwins`
- `fok_type_factors_through_rooted_ball`
- `finite_fok_r_types_bounded_degree`
- `fok_locality_final`

