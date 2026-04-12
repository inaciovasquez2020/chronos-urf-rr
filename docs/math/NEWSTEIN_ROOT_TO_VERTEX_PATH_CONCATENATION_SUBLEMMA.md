# Newstein Root-to-Vertex Path Concatenation Sublemma

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(r\). For every non-root vertex \(v\), the unique simple path from \(r\) to \(v\) is the concatenation of:
1. the unique simple path from \(r\) to \(\operatorname{par}_T(v)\), and
2. the edge \((\operatorname{par}_T(v),v)\).

## Role
This is the Step 2 input for the parent-depth decrement proof blueprint.

## Proof skeleton
1. By the parent-on-root-to-vertex-path sublemma, \(\operatorname{par}_T(v)\) lies on the unique simple path from \(r\) to \(v\).
2. The vertices before \(v\) on that path form a simple path from \(r\) to \(\operatorname{par}_T(v)\).
3. By uniqueness of simple paths in a tree, that initial segment is the unique simple path from \(r\) to \(\operatorname{par}_T(v)\).
4. Appending the final edge \((\operatorname{par}_T(v),v)\) reconstructs the unique simple path from \(r\) to \(v\).

## Dependency edge
\[
\mathrm{RootToVertexPathConcatenation}
\Longrightarrow
\mathrm{ParentDepthDecrement\ proof}.
\]
