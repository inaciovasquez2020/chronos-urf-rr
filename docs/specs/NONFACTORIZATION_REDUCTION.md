# Nonfactorization Reduction

## Fixed objects

Let `IR R G` denote the quotient cycle-rank invariant at radius `R`.

Let `tp_k_R(G)` denote the common FO\(^k_R\)-local type datum assigned to `G`.

Let `FOkRDefinable` denote the class of graph invariants factoring through `tp_k_R`.

## Reduction theorem schema

To prove
\[
\neg \exists f \in \mathrm{FO}^k_R\text{-Def}\;\forall G\;(IR(R,G)=f(tp_k_R(G))),
\]
it suffices to prove the following two items.

### Item 1: indistinguishable witness pair
\[
\exists (G^+,G^-)\;
\big(
tp_k_R(G^+) = tp_k_R(G^-)
\big).
\]

### Item 2: separated invariant
\[
IR(R,G^+) \neq IR(R,G^-).
\]

## Formal contradiction pattern

Assume
\[
\exists f\;\forall G\;(IR(R,G)=f(tp_k_R(G))).
\]

Choose \(G^+,G^-\) from Item 1 and Item 2.

Then
\[
tp_k_R(G^+) = tp_k_R(G^-)
\implies
f(tp_k_R(G^+)) = f(tp_k_R(G^-)).
\]

Hence
\[
IR(R,G^+) = IR(R,G^-),
\]
contradicting Item 2.

Therefore no such \(f\) exists.

## Lean-facing closure dependency

A complete Lean proof of nonfactorization requires only:

1. a type of local data `LocalType k R`,
2. a map `tp : Graph → LocalType k R`,
3. a witness theorem `tp Gplus = tp Gminus`,
4. a witness theorem `IR R Gplus ≠ IR R Gminus`.

Everything else is propositional reduction.

## Immediate packaging target

Package the graph-side nonfactorization theorem as:

`theorem IR_not_FOkR_definable`

depending only on:
- `W5_rank_separation`,
- local-type equality for the witness pair.
