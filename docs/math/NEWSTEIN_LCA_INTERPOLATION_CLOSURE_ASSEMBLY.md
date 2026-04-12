# Newstein LCA Interpolation Closure Assembly

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(r\). Let \(u\) and \(v\) be vertices in the same one-step parent layer. Then the synchronized ancestor descent chains of \(u\) and \(v\) admit a well-defined lowest common ancestor interpolation stage. Equivalently, there exists an admissible iterate \(m_\ast\) such that
\[
\operatorname{par}_T^{\,m_\ast}(u)=\operatorname{par}_T^{\,m_\ast}(v),
\]
and for every \(0 \le m < m_\ast\),
\[
\operatorname{depth}_T(\operatorname{par}_T^{\,m}(u))
=
\operatorname{depth}_T(\operatorname{par}_T^{\,m}(v)).
\]

## Assembly inputs
1. Ancestor descent closure assembly.
2. Finiteness of rooted depth in a finite tree.
3. Existence and uniqueness of lowest common ancestors in rooted trees.

## Proof skeleton
1. By ancestor descent closure assembly, the two ancestor chains descend in lockstep through equal rooted depths.
2. Since rooted depth is finite and decreases under admissible parent iteration, both chains reach a common ancestor.
3. Let \(m_\ast\) be the first admissible iterate at which the two ancestor chains coincide.
4. By minimality of \(m_\ast\), this coincidence point is the lowest common ancestor interpolation stage.
5. Therefore the LCA interpolation closure holds.

## Dependency edge
\[
\mathrm{LCAInterpolationClosure}
\Longrightarrow
\mathrm{GeodesicInterpolationClosure}.
\]
