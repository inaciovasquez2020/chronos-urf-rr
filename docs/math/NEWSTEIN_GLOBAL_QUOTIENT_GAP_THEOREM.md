# Newstein Global Quotient-Gap Theorem

## Target statement

\[
\dim_{\mathbb F_2}Q(G_n)-\dim_{\mathbb F_2}Q(H_n)\ge 2|V(X_n)|.
\]

Hence
\[
\dim_{\mathbb F_2}Q(G_n)-\dim_{\mathbb F_2}Q(H_n)=\Omega(n).
\]

## Inputs

### 1. Rooted-ball trivialization

Assume
\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n).
\]

### 2. Fiber rank-gap theorem

For each fiber \(v\),
\[
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}\bigr)
-
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}\bigr)
=2.
\]

### 3. Direct-sum embedding

Assume
\[
\bigoplus_v Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}
\hookrightarrow Q(G_n),
\qquad
\bigoplus_v Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}
\hookrightarrow Q(H_n).
\]

## Required subclaims

### 1. Trivial global lower bound

Prove
\[
\dim_{\mathbb F_2}Q(G_n)\ge
\sum_v \dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}\bigr).
\]

### 2. Twisted global lower bound

Prove
\[
\dim_{\mathbb F_2}Q(H_n)\ge
\sum_v \dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}\bigr).
\]

### 3. Fiberwise accumulation

Use the per-fiber gap to obtain
\[
\sum_v
\left(
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}\bigr)
-
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}\bigr)
\right)
=
2|V(X_n)|.
\]

### 4. Global gap transfer

Transfer the fiberwise accumulated gap into the global quotient gap.

## Deduction

By direct-sum embedding and the fiber rank-gap theorem,
\[
\sum_v
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}\bigr)
-
\sum_v
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}\bigr)
=
2|V(X_n)|.
\]

Thus the global quotients differ by at least the accumulated embedded fiber gap:
\[
\dim_{\mathbb F_2}Q(G_n)-\dim_{\mathbb F_2}Q(H_n)\ge 2|V(X_n)|.
\]

If \(|V(X_n)|=\Theta(n)\), then
\[
\dim_{\mathbb F_2}Q(G_n)-\dim_{\mathbb F_2}Q(H_n)=\Omega(n).
\]

## Assembly theorem

The local equality branch and the fiber/global rank branch combine to yield linear global quotient separation.

## Status

This is the first global assembly target in the Newstein chain.

## Dependencies discharged by this theorem

1. Input to non-factorization.
2. Input to transcript lower bounds.
3. Global linear-growth obstruction in the Newstein chain.
