# Newstein Geodesic Interpolation Closure Assembly

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(r\). Let \(u\) and \(v\) be vertices in the same one-step parent layer. Then the unique simple geodesic from \(u\) to \(v\) is obtained by concatenating:
1. the ancestor segment from \(u\) to \(\operatorname{LCA}_T(u,v)\), and
2. the ancestor segment from \(\operatorname{LCA}_T(u,v)\) to \(v\).

## Assembly inputs
1. LCA interpolation closure assembly.
2. Uniqueness of simple paths in a tree.
3. Tree geodesics coincide with unique simple paths.

## Proof skeleton
1. By LCA interpolation closure assembly, the synchronized ancestor chains of \(u\) and \(v\) meet at a well-defined lowest common ancestor.
2. The unique simple path from \(u\) to \(\operatorname{LCA}_T(u,v)\) is the reverse of the ancestor chain from \(u\) to the LCA.
3. The unique simple path from \(\operatorname{LCA}_T(u,v)\) to \(v\) is the ancestor chain from the LCA down to \(v\).
4. Concatenating these two simple segments yields a simple path from \(u\) to \(v\).
5. By uniqueness of simple paths in a tree, this concatenation is the unique geodesic from \(u\) to \(v\).

## Dependency edge
\[
\mathrm{GeodesicInterpolationClosure}
\Longrightarrow
\mathrm{TreePathRootedLocality}.
\]
