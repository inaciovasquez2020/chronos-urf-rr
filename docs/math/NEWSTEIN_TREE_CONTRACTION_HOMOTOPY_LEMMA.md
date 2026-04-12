# Newstein Tree-Contraction Homotopy Lemma

## Status
OPEN

## Weakest sufficient missing object
A local contraction homotopy
\[
h:C_k(B_R(r))\to C_{k+1}(B_R(r))
\]
such that
\[
\operatorname{supp}(h(c))\subseteq B_R(r)
\quad\text{and}\quad
\partial h+h\partial=\mathrm{Id}-\mathrm{Retr}_r.
\]

## Inputs already proved
- `TreeDepthMetricIdentity`
- `MetricDepthCoincidence`
- `ParentDepthDecrement`

## Target statement
For every rooted ball \(B_R(r)\) in the Newstein witness complex, there exists a linear operator
\[
h:C_k(B_R(r))\to C_{k+1}(B_R(r))
\]
with:

1. **Support locality**
   \[
   \forall c,\quad \operatorname{supp}(h(c))\subseteq B_R(r).
   \]

2. **Prism identity**
   \[
   \partial h+h\partial=\mathrm{Id}-\mathrm{Retr}_r.
   \]

## Construction blueprint
Let \(\eta\) be the parent map:
\[
\eta(v)=
\begin{cases}
p(v), & v\neq r,\\
r, & v=r.
\end{cases}
\]
Assume the elementary prism operator \(\phi\) satisfies
\[
\partial\phi+\phi\partial=\mathrm{Id}-\eta_\#.
\]
Define
\[
h=\sum_{j=0}^{R-1}\eta_\#^j\circ\phi.
\]
Then
\[
\partial h+h\partial
=
\sum_{j=0}^{R-1}(\eta_\#^j-\eta_\#^{j+1})
=
\mathrm{Id}-\eta_\#^R
=
\mathrm{Id}-\mathrm{Retr}_r.
\]

## Remaining obligations
1. Define `tree_homotopy`.
2. Prove `supp (h c) ⊆ B_R(r)`.
3. Prove `∂ h + h ∂ = Id - Retr_r`.
4. Deduce `RootedBallTrivialization`.
5. Propagate to `FiberQuotientRank`.

## Theorem chain
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

## Closure criterion
This file may be flipped from `OPEN` to `PROVED` exactly when a repo-native formalization establishes the two defining identities:
- support locality in \(B_R(r)\),
- prism identity \(\partial h+h\partial=\mathrm{Id}-\mathrm{Retr}_r\).

