# Newstein Non-Factorization Consequence

## Target statement

If
\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n)
\]
but
\[
Q(G_n)\neq Q(H_n),
\]
then the quotient invariant \(Q\) does not factor through rooted radius-\(r\) type or \(FO^k_r\)-type.

## Inputs

### 1. Rooted-ball trivialization

Assume
\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n).
\]

### 2. Global quotient-gap theorem

Assume
\[
\dim_{\mathbb F_2}Q(G_n)-\dim_{\mathbb F_2}Q(H_n)\ge 2|V(X_n)|.
\]

In particular,
\[
Q(G_n)\neq Q(H_n).
\]

## Required subclaims

### 1. Factorization implication

If \(Q\) factors through rooted radius-\(r\) type, then equal rooted type implies equal \(Q\)-value.

### 2. \(FO^k_r\)-type implication

If \(Q\) factors through \(FO^k_r\)-type, then equal \(FO^k_r\)-type implies equal \(Q\)-value.

### 3. Contradiction step

Equal local type together with unequal \(Q\)-value contradicts either factorization hypothesis.

## Deduction

Assume \(Q\) factors through rooted radius-\(r\) type or \(FO^k_r\)-type.

By rooted-ball trivialization,
\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n).
\]

Hence the factorization hypothesis forces
\[
Q(G_n)=Q(H_n).
\]

But by the global quotient-gap theorem,
\[
Q(G_n)\neq Q(H_n).
\]

Contradiction.

Therefore \(Q\) does not factor through rooted radius-\(r\) type or \(FO^k_r\)-type.

## Assembly theorem

Local indistinguishability together with global quotient separation yields non-factorization.

## Status

This closes the non-factorization branch of the Newstein chain at the theorem-ledger level.

## Dependencies discharged by this theorem

1. Final structural obstruction statement for the Newstein quotient invariant.
2. Input to the complexity/lower-bound branch.
3. Local-versus-global separation certificate in the Newstein chain.
