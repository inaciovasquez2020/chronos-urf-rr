# Newstein One-Step Parent-Depth Decrement Proof

Status: OPEN

## Assumptions
Assume:
\[
(\eta(w),w)\in E,
\qquad
\eta(w)\ \text{lies on a shortest path from } w \text{ to } r,
\qquad
w\neq r.
\]

## Upper bound
Because \((\eta(w),w)\in E\), the triangle inequality gives
\[
d(w,r)\le d(\eta(w),r)+1.
\]
Hence
\[
d(\eta(w),r)\ge d(w,r)-1.
\]

## Lower bound
Because \(\eta(w)\) lies on a shortest path from \(w\) to \(r\),
\[
d(w,r)=1+d(\eta(w),r).
\]
Hence
\[
d(\eta(w),r)\le d(w,r)-1.
\]

## Equality
Therefore
\[
d(\eta(w),r)=d(w,r)-1.
\]

## Output
OneStepParentDepthDecrement is reduced to parent-edge admissibility plus the geodesic-parent law.
