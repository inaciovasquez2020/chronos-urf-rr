# Newstein One-Step Parent Stability Assembly

## Status
OPEN

## Statement
Let \(T\) be a rooted tree with root \(r\). Let \(u\) and \(v\) be non-root vertices with
\[
\operatorname{par}_T(u)=\operatorname{par}_T(v).
\]
Then \(u\) and \(v\) lie at the same rooted depth and therefore belong to the same one-step parent layer.

## Assembly inputs
1. Rooted-distance monotonicity assembly.
2. Definition of one-step parent layer as the set of vertices with common parent depth increment.

## Proof skeleton
1. By rooted-distance monotonicity assembly,
\[
\operatorname{depth}_T(u)=\operatorname{depth}_T(v).
\]
2. Vertices with the same parent and the same rooted depth occupy the same one-step parent layer.
3. Therefore \(u\) and \(v\) satisfy one-step parent stability.

## Dependency edge
\[
\mathrm{OneStepParentStability}
\Longrightarrow
\mathrm{ParentIterationClosure}.
\]
