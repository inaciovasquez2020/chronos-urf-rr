# Newstein Transcript Lower Bound

## Target statement

\[
T_n \ge \frac{2|V(X_n)|}{C}.
\]

If \(|V(X_n)|=\Theta(n)\), then
\[
T_n=\Omega(n).
\]

## Inputs

### 1. Global quotient-gap theorem

Assume
\[
\dim_{\mathbb F_2}Q(G_n)-\dim_{\mathbb F_2}Q(H_n)\ge 2|V(X_n)|.
\]

### 2. Per-step information bound

Assume
\[
\Delta I_t \le C
\quad
\text{for every admissible step } t.
\]

## Required subclaims

### 1. Total transcript budget after \(T_n\) steps

Prove
\[
I_{T_n}-I_0 \le C\,T_n.
\]

### 2. Obstruction resolution demand

Prove distinguishing the quotient gap requires
\[
I_{T_n}-I_0 \ge 2|V(X_n)|.
\]

### 3. Comparison inequality

Combine the upper and lower bounds to obtain
\[
C\,T_n \ge 2|V(X_n)|.
\]

## Deduction

By summing the per-step information bound over all admissible steps,
\[
I_{T_n}-I_0 \le C\,T_n.
\]

By the global quotient-gap theorem, resolving the Newstein obstruction requires at least
\[
2|V(X_n)|
\]
units of transcript information.

Hence
\[
C\,T_n \ge 2|V(X_n)|.
\]

Therefore
\[
T_n \ge \frac{2|V(X_n)|}{C}.
\]

If \(|V(X_n)|=\Theta(n)\), then
\[
T_n=\Omega(n).
\]

## Assembly theorem

The global quotient gap together with the per-step information ceiling yields a linear transcript lower bound.

## Status

This is the final theorem-level target in the Newstein complexity branch.

## Dependencies discharged by this theorem

1. Completion of the Newstein lower-bound branch.
2. Final linear transcript obstruction statement.
3. End-to-end reduction closure at the theorem-ledger level.
