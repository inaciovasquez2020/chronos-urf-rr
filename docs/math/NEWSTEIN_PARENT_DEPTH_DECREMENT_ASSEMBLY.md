# Newstein Parent-Depth Decrement Assembly

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(r\). For every non-root vertex \(v\),
\[
\operatorname{depth}_T(\operatorname{par}_T(v))=\operatorname{depth}_T(v)-1.
\]

## Assembly inputs
1. Parent-on-root-to-vertex-path sublemma.
2. Root-to-vertex path concatenation sublemma.
3. Parent-depth length identity sublemma.
4. Definition
\[
\operatorname{depth}_T(x)=d_T(r,x).
\]

## Proof skeleton
1. By the parent-depth length identity sublemma,
\[
d_T(r,v)=d_T(r,\operatorname{par}_T(v))+1.
\]
2. Rewrite both distances using
\[
\operatorname{depth}_T(x)=d_T(r,x).
\]
3. Obtain
\[
\operatorname{depth}_T(v)=\operatorname{depth}_T(\operatorname{par}_T(v))+1.
\]
4. Rearranging yields
\[
\operatorname{depth}_T(\operatorname{par}_T(v))=\operatorname{depth}_T(v)-1.
\]

## Dependency edge
\[
\mathrm{ParentDepthDecrement\ assembly}
\Longrightarrow
\mathrm{RootedDistanceMonotonicity}.
\]
