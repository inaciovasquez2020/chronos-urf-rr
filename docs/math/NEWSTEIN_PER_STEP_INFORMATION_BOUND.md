# Newstein Per-Step Information Bound

Status: OPEN

## Status
OPEN

## Target statement

In the intended admissible refinement model, prove
\[
\Delta I_t \le C.
\]

Equivalently,
\[
I(X;Y_t \mid \mathcal H_{t-1}) \le C.
\]

## Inputs

1. Explicit admissible refinement model.
2. Definition of one-step transcript/information increment.
3. Uniform constant-capacity bound per admissible step.
4. Independence of the bound from \(n\).
5. Compatibility with the quotient-gap assembly.

## Consequence

Combined with the quotient-gap theorem,
\[
T_n \ge \frac{2|V(X_n)|}{C}.
\]

If \(|V(X_n)|=\Theta(n)\), then
\[
T_n=\Omega(n).
\]

## Finish condition

Replace this file by a proof sufficient to close the complexity/lower-bound branch.
