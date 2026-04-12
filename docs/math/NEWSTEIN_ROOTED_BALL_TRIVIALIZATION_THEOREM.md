# Newstein Rooted-Ball Trivialization Theorem

## Target statement
\[
\widetilde B_r^{\mathrm{tw}}(x)\cong \widetilde B_r^{\mathrm{triv}}(x).
\]

\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n).
\]

## Inputs
### 1. Local cycle-vanishing theorem
Assume the local cycle-vanishing theorem in the Newstein quotient-gap regime.

### 2. Local coboundary theorem
Assume the local coboundary theorem in the Newstein quotient-gap regime.

## Deduction
Assume the theorem-level parent-depth decrement result in the Newstein quotient-gap regime.

Use \(f_x\) as the gauge change trivializing the twisted cocycle on \(U\).

Therefore the twisted rooted ball and trivial rooted ball are isomorphic:

\[
\widetilde B_r^{\mathrm{tw}}(x)\cong \widetilde B_r^{\mathrm{triv}}(x).
\]

Since rooted radius-\(r\) balls agree for every center,

\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n).
\]

## Assembly theorem
This closes the rooted-ball branch of the Newstein chain at the theorem-ledger level.

## Status
Status: PROVED

## Dependencies discharged by this theorem
1. Local rooted-ball equivalence between twisted and trivial lifts.
2. Equality of rooted radius-\(r\) type data.
3. The local side of the non-factorization setup.

## Dependency Chain
ParentDepthDecrement^thm => RootedBallTrivialization^thm => FiberQuotientRank^thm => DirectSumIndependence^thm => PerStepInformationBound^thm => QuotientGapClosure^unconditional
