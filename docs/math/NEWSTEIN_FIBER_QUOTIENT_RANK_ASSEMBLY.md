# Newstein Fiber Quotient-Rank Assembly

## Status
OPEN

## Statement
Let \(G\) be decomposed into rooted local fibers \(\{B_i\}\). Suppose each rooted ball \(B_i\) trivializes in the local coboundary quotient. Then the global quotient rank is determined entirely by the surviving inter-fiber classes. Equivalently, the contribution of each trivialized rooted fiber to the quotient rank is zero, so the quotient rank is the rank of the residual fiber-to-fiber interaction space.

## Assembly inputs
1. Rooted-ball trivialization assembly.
2. Additivity of rank under quotient decomposition into trivial and surviving parts.
3. Definition of fiber quotient rank as the rank of the residual quotient after killing rooted-local trivial classes.

## Proof skeleton
1. By rooted-ball trivialization assembly, each rooted fiber \(B_i\) contributes only trivial classes in the local quotient.
2. Trivial classes contribute zero to quotient rank.
3. Therefore all rank contribution from rooted-local fibers vanishes.
4. The only remaining quotient-rank contribution comes from residual inter-fiber classes.
5. Hence the fiber quotient rank equals the rank of the residual fiber interaction quotient.

## Dependency edge
\[
\mathrm{FiberQuotientRank}
\Longrightarrow
\mathrm{DirectSumIndependence}.
\]
