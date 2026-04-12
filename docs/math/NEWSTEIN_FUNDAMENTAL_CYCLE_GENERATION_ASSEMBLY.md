# Newstein Fundamental Cycle Generation Assembly

## Status
OPEN

## Statement
Let \(T\) be a rooted spanning tree of a graph \(G\). Let \(e=\{u,v\}\) be a non-tree edge. Then the unique simple \(u\)-to-\(v\) path in \(T\), together with \(e\), generates a unique fundamental cycle
\[
C_T(e)=P_T(u,v)\cup\{e\}.
\]

## Assembly inputs
1. Tree-path rooted locality assembly.
2. Uniqueness of simple paths in a tree.
3. Definition of a fundamental cycle with respect to a spanning tree.

## Proof skeleton
1. By tree-path rooted locality assembly, the tree path \(P_T(u,v)\) is uniquely determined by rooted ancestor data.
2. Since \(e=\{u,v\}\) is not an edge of \(T\), adjoining \(e\) to \(P_T(u,v)\) closes the path into a cycle.
3. The path \(P_T(u,v)\) is simple, so the resulting cycle is simple.
4. Uniqueness of \(P_T(u,v)\) implies uniqueness of the cycle \(C_T(e)\).
5. Therefore each non-tree edge generates a unique fundamental cycle.

## Dependency edge
\[
\mathrm{FundamentalCycleGeneration}
\Longrightarrow
\mathrm{LocalCoboundaryCriterion}.
\]
