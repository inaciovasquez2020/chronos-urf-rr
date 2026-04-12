# Newstein Parent-Iteration Depth Formula Theorem

Status: OPEN

## Statement
For every vertex \(v \in B_R(r)\) and every \(j \in \mathbb{N}\),
\[
d(\eta^j(v))=\max(d(v)-j,0).
\]

## Inputs
- `MetricDepthCoincidence^thm`
- `ParentDepthDecrement^thm`

## Role
This is the minimal induction lemma needed to derive
\[
\eta^R(v)=r
\]
and hence
\[
\eta_\#^R=\mathrm{Retr}_r.
\]

## Dependency Chain
ParentIterationDepthFormula^thm => ParentIterationToRoot^thm => TreeContractionHomotopy^thm => RootedBallTrivialization^thm
