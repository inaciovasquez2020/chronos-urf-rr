# Newstein Direct-Sum Independence Assembly

## Status
OPEN

## Statement
Let the residual quotient after rooted-ball trivialization decompose into fiber-indexed subspaces \(\{Q_i\}\). Suppose each rooted-local fiber contribution has been killed in the quotient and only residual inter-fiber classes remain. If these residual classes are supported on pairwise independent fiber channels, then
\[
\operatorname{rank}\!\left(\sum_i Q_i\right)=\sum_i \operatorname{rank}(Q_i).
\]
Equivalently, the residual quotient is a direct sum of independent fiber components.

## Assembly inputs
1. Fiber quotient-rank assembly.
2. Rank additivity on direct sums.
3. Independence criterion: no nontrivial linear relation mixes distinct surviving fiber channels.

## Proof skeleton
1. By fiber quotient-rank assembly, all rooted-local trivial contributions have been removed, leaving only residual inter-fiber classes.
2. By the independence criterion, any linear relation among surviving classes splits fiberwise.
3. Therefore the intersection of distinct residual fiber components is trivial.
4. Hence the residual quotient decomposes as a direct sum
\[
\bigoplus_i Q_i.
\]
5. By rank additivity on direct sums,
\[
\operatorname{rank}\!\left(\sum_i Q_i\right)=\sum_i \operatorname{rank}(Q_i).
\]

## Dependency edge
\[
\mathrm{DirectSumIndependence}
\Longrightarrow
\mathrm{FiberToGlobalInjection}.
\]
