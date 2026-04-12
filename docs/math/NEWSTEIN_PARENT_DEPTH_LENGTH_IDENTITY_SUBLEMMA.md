# Newstein Parent-Depth Length Identity Sublemma

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(r\). For every non-root vertex \(v\),
\[
d_T(r,v)=d_T(r,\operatorname{par}_T(v))+1.
\]

## Role
This is the Step 3 input for the parent-depth decrement proof blueprint.

## Proof skeleton
1. By the root-to-vertex path concatenation sublemma, the unique simple path from \(r\) to \(v\) is the concatenation of the unique simple path from \(r\) to \(\operatorname{par}_T(v)\) with the edge \((\operatorname{par}_T(v),v)\).
2. Path length is additive under concatenation.
3. The appended terminal segment has length \(1\).
4. Therefore
\[
d_T(r,v)=d_T(r,\operatorname{par}_T(v))+1.
\]

## Dependency edge
\[
\mathrm{ParentDepthLengthIdentity}
\Longrightarrow
\mathrm{ParentDepthDecrement\ proof}.
\]
