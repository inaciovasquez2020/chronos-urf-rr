# Newstein Parent Iteration Closure Assembly

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(r\). Let \(u\) and \(v\) be vertices in the same one-step parent layer. Then for every admissible iteration count \(m\) for which both iterates are defined,
\[
\operatorname{depth}_T(\operatorname{par}_T^{\,m}(u))
=
\operatorname{depth}_T(\operatorname{par}_T^{\,m}(v)).
\]

## Assembly inputs
1. One-step parent stability assembly.
2. Parent-depth decrement assembly.
3. Inductive iteration of the parent map on non-root vertices.

## Proof skeleton
1. Base case \(m=0\): equality holds from one-step parent stability assembly.
2. Inductive step: assume
\[
\operatorname{depth}_T(\operatorname{par}_T^{\,m}(u))
=
\operatorname{depth}_T(\operatorname{par}_T^{\,m}(v)).
\]
3. Apply parent-depth decrement assembly to both non-root iterates to obtain
\[
\operatorname{depth}_T(\operatorname{par}_T^{\,m+1}(u))
=
\operatorname{depth}_T(\operatorname{par}_T^{\,m}(u))-1
\]
and
\[
\operatorname{depth}_T(\operatorname{par}_T^{\,m+1}(v))
=
\operatorname{depth}_T(\operatorname{par}_T^{\,m}(v))-1.
\]
4. Substitute the inductive hypothesis.
5. Conclude
\[
\operatorname{depth}_T(\operatorname{par}_T^{\,m+1}(u))
=
\operatorname{depth}_T(\operatorname{par}_T^{\,m+1}(v)).
\]

## Dependency edge
\[
\mathrm{ParentIterationClosure}
\Longrightarrow
\mathrm{AncestorDescentClosure}.
\]
