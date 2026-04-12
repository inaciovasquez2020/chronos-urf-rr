# Newstein Parent-Iteration-to-Root Theorem

Status: OPEN

## Statement
Let \(B_R(r)\) be a rooted ball with parent map \(\eta\). Then for every vertex \(v \in B_R(r)\),
\[
\eta^R(v)=r.
\]
Equivalently, on chains,
\[
\eta_\#^R=\mathrm{Retr}_r.
\]

## Inputs
- `TreeDepthMetricIdentity^thm`
- `MetricDepthCoincidence^thm`
- `ParentDepthDecrement^thm`

## Proof idea
By `ParentDepthDecrement^thm`, each application of \(\eta\) lowers rooted depth by one until the root is reached.
By `MetricDepthCoincidence^thm`, rooted depth agrees with metric depth on \(B_R(r)\).
Hence every \(v \in B_R(r)\) reaches \(r\) in at most \(R\) parent steps.

## Role in chain
This is the telescoping terminal identity needed for `TreeContractionHomotopy^thm`.

## Dependency Chain
ParentIterationToRoot^thm => TreeContractionHomotopy^thm => RootedBallTrivialization^thm => FiberQuotientRank^thm => DirectSumIndependence^thm => PerStepInformationBound^thm => QuotientGapClosure^unconditional
