# Newstein Tree-Contraction Homotopy Proof Blueprint

Status: OPEN

## Objective
Construct
\[
h : C_k(B_R(r)) \to C_{k+1}(B_R(r))
\]
such that
\[
\operatorname{supp}(h(c)) \subseteq B_R(r),
\qquad
\partial h + h \partial = \mathrm{Id} - \mathrm{Retr}_r.
\]

## Step 1
Define the parent map
\[
\eta(v)=
\begin{cases}
p(v), & v \neq r,\\
r, & v = r.
\end{cases}
\]

## Step 2
Introduce an elementary prism operator \(\phi\) satisfying
\[
\partial \phi + \phi \partial = \mathrm{Id} - \eta_\#.
\]

## Step 3
Define
\[
h = \sum_{j=0}^{R-1} \eta_\#^j \circ \phi.
\]

## Step 4
Prove support locality:
\[
\operatorname{supp}(h(c)) \subseteq B_R(r).
\]

## Step 5
Prove telescoping:
\[
\partial h + h \partial
=
\sum_{j=0}^{R-1}(\eta_\#^j-\eta_\#^{j+1})
=
\mathrm{Id}-\eta_\#^R.
\]

## Step 6
Prove
\[
\eta_\#^R=\mathrm{Retr}_r.
\]

## Output
\[
\partial h + h \partial = \mathrm{Id} - \mathrm{Retr}_r.
\]

## Dependency Chain
TreeContractionHomotopy^thm => RootedBallTrivialization^thm => FiberQuotientRank^thm => DirectSumIndependence^thm => PerStepInformationBound^thm => QuotientGapClosure^unconditional
