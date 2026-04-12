# Newstein Rooted-Distance Monotonicity Assembly

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(r\). Let \(u\) and \(v\) be non-root vertices with
\[
\operatorname{par}_T(u)=\operatorname{par}_T(v).
\]
Then
\[
\operatorname{depth}_T(u)=\operatorname{depth}_T(v).
\]

## Assembly inputs
1. Parent-depth decrement assembly.
2. Definition
\[
\operatorname{depth}_T(x)=d_T(r,x).
\]
3. Equality substitution under equal parents.

## Proof skeleton
1. By parent-depth decrement assembly,
\[
\operatorname{depth}_T(\operatorname{par}_T(u))=\operatorname{depth}_T(u)-1.
\]
2. By parent-depth decrement assembly,
\[
\operatorname{depth}_T(\operatorname{par}_T(v))=\operatorname{depth}_T(v)-1.
\]
3. Using
\[
\operatorname{par}_T(u)=\operatorname{par}_T(v),
\]
substitute to obtain
\[
\operatorname{depth}_T(u)-1=\operatorname{depth}_T(v)-1.
\]
4. Hence
\[
\operatorname{depth}_T(u)=\operatorname{depth}_T(v).
\]

## Dependency edge
\[
\mathrm{RootedDistanceMonotonicity}
\Longrightarrow
\mathrm{OneStepParentStability}.
\]
