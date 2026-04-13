# Newstein Next-Step Registry

## Solved
- `TreeDepthMetricIdentity`
- `MetricDepthCoincidence`
- `ParentDepthDecrement`

## Locked frontier
- `TreeContractionHomotopy`

## Conditional consequences already locked
- `RootedBallTrivialization`
- `FiberQuotientRank`

## Weakest sufficient missing object
A repo-native local contraction homotopy
\[
h:C_k(B_R(r))\to C_{k+1}(B_R(r))
\]
such that
\[
\operatorname{supp}(h(c))\subseteq B_R(r)
\quad\wedge\quad
\partial h+h\partial=\mathrm{Id}-\mathrm{Retr}_r.
\]

## Remaining theorem chain
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


## Theorem-level frontier
Weakest missing theorem-level object: ParentIterationDepthFormula^thm

## Loop stop
Do not add further theorem-target locks or proof blueprints for the Newstein chain until one placeholder theorem is replaced by a nontrivial Lean proof.

## Next proof-replacement order
1. ParentIterationDepthFormula^thm
2. ParentIterationToRoot^thm
3. TreeContractionHomotopy^thm
4. RootedBallTrivialization^thm

## Current stop condition
Reduction-complete. Do not add new reduction locks.

## Single remaining frontier
OneStepParentDepthDecrement:
\[
\forall w \in B_R(r),\qquad
w \neq r \Longrightarrow d(\eta(w),r)=d(w,r)-1.
\]

## Required action
Replace the remaining frontier by a proof, not by another reduction note.

