# Newstein Tree-Contraction Homotopy Theorem

Status: OPEN

## Statement
Let \(r\) be a root and \(B_R(r)\) the rooted ball of radius \(R\). Then there exists a chain homotopy
\[
h : C_k(B_R(r)) \to C_{k+1}(B_R(r))
\]
such that:
\[
\operatorname{supp}(h(c)) \subseteq B_R(r),
\qquad
\partial h + h \partial = \mathrm{Id} - \mathrm{Retr}_r.
\]

## Inputs
- `TreeDepthMetricIdentity^thm`
- `MetricDepthCoincidence^thm`
- `ParentDepthDecrement^thm`

## Construction target
Define the parent map \(\eta\) and prism operator \(\phi\), then set
\[
h = \sum_{j=0}^{R-1} \eta_\#^j \circ \phi.
\]

## Proof obligations
1. `tree_homotopy` is well-defined on chains in `B_R(r)`.
2. `supp (tree_homotopy c) ⊆ B_R(r)`.
3. `∂ h + h ∂ = Id - Retr_r`.

## Dependency Chain
TreeContractionHomotopy^thm => RootedBallTrivialization^thm => FiberQuotientRank^thm => DirectSumIndependence^thm => PerStepInformationBound^thm => QuotientGapClosure^unconditional
