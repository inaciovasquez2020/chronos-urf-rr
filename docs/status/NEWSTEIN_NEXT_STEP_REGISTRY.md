# Newstein Next-Step Registry

## Current proved layer
- `TreeDepthMetricIdentity`
- `MetricDepthCoincidence`
- `ParentDepthDecrement`

## Current frontier
- `TreeContractionHomotopy`

## Weakest sufficient missing object
Local contraction homotopy on \(B_R(r)\):
\[
h:C_k(B_R(r))\to C_{k+1}(B_R(r)),
\qquad
\operatorname{supp}(h(c))\subseteq B_R(r),
\qquad
\partial h+h\partial=\mathrm{Id}-\mathrm{Retr}_r.
\]

## Immediate theorem chain
\[
\mathrm{TreeContractionHomotopy}
\Longrightarrow
\mathrm{RootedBallTrivialization}
\Longrightarrow
\mathrm{FiberQuotientRank}
\Longrightarrow
\mathrm{DirectSumIndependence}
\Longrightarrow
\mathrm{PerStepInformationBound}
\Longrightarrow
\mathrm{QuotientGapClosure}.
\]

## Truth condition
Proof closure is not 100% until `TreeContractionHomotopy` is formalized or explicitly assumed.

