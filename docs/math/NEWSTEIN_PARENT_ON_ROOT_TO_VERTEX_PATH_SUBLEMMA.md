# Newstein Parent-on-Root-to-Vertex-Path Sublemma

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(r\). For every non-root vertex \(v\), the parent \(\operatorname{par}_T(v)\) lies on the unique simple path from \(r\) to \(v\).

## Role
This is the Step 1 input for the parent-depth decrement proof blueprint.

## Proof skeleton
1. Since \(v \neq r\), the parent \(\operatorname{par}_T(v)\) is defined.
2. The edge \((\operatorname{par}_T(v),v)\) belongs to \(T\).
3. Removing the final edge of the unique \(r\)-to-\(v\) path leaves a simple \(r\)-to-\(\operatorname{par}_T(v)\) path.
4. Hence \(\operatorname{par}_T(v)\) lies on the unique simple path from \(r\) to \(v\).

## Dependency edge
\[
\mathrm{ParentOnRootToVertexPath}
\Longrightarrow
\mathrm{ParentDepthDecrement\ proof}.
\]
