# Newstein Parent Depth Decrement Proof Target

## Status
OPEN

## Weakest sufficient missing object
Prove the exact parent-depth decrement statement for the chosen rooted spanning tree \(T\).

## Target statement
Let \(T\) be a rooted tree, let \(r\) be its root, let \(\operatorname{depth}_T(v)\) denote the graph distance from \(r\) to \(v\) inside \(T\), and let \(\operatorname{par}_T(v)\) denote the parent of a non-root vertex \(v\).
Then for every vertex \(v \neq r\),
\[
\operatorname{depth}_T(\operatorname{par}_T(v)) = \operatorname{depth}_T(v) - 1.
\]

## Normalized proof obligations
1. \(v \neq r \Rightarrow \operatorname{par}_T(v)\) is adjacent to \(v\) in \(T\).
2. The unique \(r\)-to-\(v\) path in \(T\) is obtained by appending \(v\) to the unique \(r\)-to-\(\operatorname{par}_T(v)\) path.
3. Therefore path length drops by exactly one under parent application.

## Immediate consequence
This theorem discharges the remaining gap in rooted-distance monotonicity and unlocks the parent-to-geodesic chain.

## Dependency edge
\[
\mathrm{ParentDepthDecrement\ proof}
\Longrightarrow
\mathrm{RootedDistanceMonotonicity}.
\]
