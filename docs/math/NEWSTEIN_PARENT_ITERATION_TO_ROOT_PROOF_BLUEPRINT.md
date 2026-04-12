# Newstein Parent-Iteration-to-Root Proof Blueprint

Status: OPEN

## Objective
Prove, for every vertex \(v \in B_R(r)\),
\[
\eta^R(v)=r,
\]
and hence on chains
\[
\eta_\#^R=\mathrm{Retr}_r.
\]

## Inputs
- `TreeDepthMetricIdentity^thm`
- `MetricDepthCoincidence^thm`
- `ParentDepthDecrement^thm`

## Step 1
Let
\[
d(v):=\operatorname{dist}(r,v).
\]
For \(v \in B_R(r)\),
\[
d(v)\le R.
\]

## Step 2
For every non-root vertex \(v\neq r\),
\[
d(\eta(v))=d(v)-1.
\]

## Step 3
By induction on \(j\),
\[
d(\eta^j(v))=\max(d(v)-j,0).
\]

## Step 4
Since \(d(v)\le R\),
\[
d(\eta^R(v))=0.
\]

## Step 5
Distance \(0\) from the root implies
\[
\eta^R(v)=r.
\]

## Step 6
Extend vertexwise equality to chains:
\[
\eta_\#^R=\mathrm{Retr}_r.
\]

## Role in chain
\[
\mathrm{ParentIterationToRoot}^\mathrm{thm}
\Longrightarrow
\mathrm{TreeContractionHomotopy}^\mathrm{thm}
\Longrightarrow
\mathrm{RootedBallTrivialization}^\mathrm{thm}.
\]
