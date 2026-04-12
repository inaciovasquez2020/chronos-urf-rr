# Newstein Ancestor Descent Closure Assembly

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(r\). Let \(u\) and \(v\) be vertices in the same one-step parent layer. Then along every admissible common parent iteration, the ancestor chains of \(u\) and \(v\) descend through equal rooted depths. Equivalently, for every admissible \(m\),
\[
\operatorname{depth}_T(\operatorname{par}_T^{\,m}(u))
=
\operatorname{depth}_T(\operatorname{par}_T^{\,m}(v)).
\]

## Assembly inputs
1. Parent iteration closure assembly.
2. Definition of ancestor descent as successive parent iteration toward the root.
3. Admissibility condition that both iterates remain defined.

## Proof skeleton
1. Ancestor descent is exactly iteration of the parent map.
2. By parent iteration closure assembly, equal rooted depth is preserved at each admissible common iterate.
3. Therefore the two ancestor chains descend in lockstep through equal rooted depths.
4. This is the required ancestor descent closure.

## Dependency edge
\[
\mathrm{AncestorDescentClosure}
\Longrightarrow
\mathrm{LCAInterpolationClosure}.
\]
