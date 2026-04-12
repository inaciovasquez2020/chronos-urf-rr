# Newstein Tree-Path Rooted Locality Assembly

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(r\). Let \(u\) and \(v\) be vertices in the same one-step parent layer. Then the unique geodesic from \(u\) to \(v\) is completely determined by rooted ancestor data: it is the union of the two rooted ancestor segments from \(u\) and \(v\) to \(\operatorname{LCA}_T(u,v)\). In particular, the \(u\)-to-\(v\) tree path is rooted-local.

## Assembly inputs
1. Geodesic interpolation closure assembly.
2. Lowest common ancestor uniqueness in rooted trees.
3. Rooted ancestor segments determine the path to the LCA.

## Proof skeleton
1. By geodesic interpolation closure assembly, the unique geodesic from \(u\) to \(v\) is obtained by concatenating the ancestor segment from \(u\) to \(\operatorname{LCA}_T(u,v)\) with the ancestor segment from \(\operatorname{LCA}_T(u,v)\) to \(v\).
2. Each segment is determined entirely by repeated parent iteration in the rooted tree.
3. Therefore the full \(u\)-to-\(v\) tree path is determined by rooted ancestor data alone.
4. Hence the path is rooted-local.

## Dependency edge
\[
\mathrm{TreePathRootedLocality}
\Longrightarrow
\mathrm{FundamentalCycleGeneration}.
\]
