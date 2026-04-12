# Newstein Rooted-Ball Trivialization Assembly

## Status
OPEN

## Statement
Let \(T\) be a rooted spanning tree of a graph \(G\). Let \(B=B_G(x,r)\) be a rooted ball. If the local coboundary criterion holds on \(B\), then every obstruction class on \(B\) vanishing on the rooted-local fundamental-cycle generators is trivial in the local quotient. Equivalently, the rooted ball trivializes after passage to the local coboundary quotient.

## Assembly inputs
1. Local coboundary criterion assembly.
2. Definition of the local quotient by rooted-local coboundaries.
3. Triviality of a class once all values on a generating family vanish.

## Proof skeleton
1. By local coboundary criterion assembly, the obstruction class on \(B\) is detected by the rooted-local fundamental-cycle generating family.
2. If the class vanishes on that generating family, then it vanishes on the entire generated local cycle space.
3. Passing to the local coboundary quotient kills exactly those classes detected as zero on the generating family.
4. Therefore the obstruction class of \(B\) is trivial in the local quotient.
5. Hence rooted-ball trivialization holds.

## Dependency edge
\[
\mathrm{RootedBallTrivialization}
\Longrightarrow
\mathrm{FiberQuotientRank}.
\]
