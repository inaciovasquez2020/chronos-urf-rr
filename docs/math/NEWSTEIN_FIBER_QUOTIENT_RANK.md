# Newstein Fiber Quotient Rank

## Status
OPEN

## Dependency
- `NEWSTEIN_ROOTED_BALL_TRIVIALIZATION.md`

## Minimal sufficient assumption
Assume `RootedBallTrivialization`:
\[
\forall k \ge 1,\qquad Z_k(B_R(r)) = B_k(B_R(r)).
\]

## Target statement
Let \(W(B_R(r))\) denote the local witness space and let
\[
Q(B_R(r)) := Z_1(B_R(r)) / B_1(B_R(r)).
\]
Then
\[
\operatorname{rank} Q(B_R(r)) = 0.
\]

## Derivation
By `RootedBallTrivialization` with \(k=1\),
\[
Z_1(B_R(r)) = B_1(B_R(r)).
\]
Therefore
\[
Q(B_R(r)) = Z_1(B_R(r))/B_1(B_R(r)) = 0,
\]
hence
\[
\operatorname{rank} Q(B_R(r)) = 0.
\]

## Closure criterion
This file may be flipped from `OPEN` to `PROVED` exactly when `RootedBallTrivialization` is flipped from conditional to proved.

## Forward chain
\[
\mathrm{FiberQuotientRank}
\Longrightarrow
\mathrm{DirectSumIndependence}
\Longrightarrow
\mathrm{PerStepInformationBound}
\Longrightarrow
\mathrm{QuotientGapClosure}.
\]

