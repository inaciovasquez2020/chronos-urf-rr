# NEWSTEIN TREE-DEPTH METRIC IDENTITY

Status: PROVED

## Statement
Assume a rooted shortest-path tree structure with:
1. \(\operatorname{depth}_G(r)=0\).
2. \(d_G(r,r)=0\).
3. \(\forall x \neq r,\ \operatorname{depth}_G(x)=\operatorname{depth}_G(p(x))+1\).
4. \(\forall x \neq r,\ d_G(r,x)=d_G(r,p(x))+1\).
5. \(\forall x,\ \exists n,\ p^{[n]}(x)=r\).

Then
\[
\forall x,\ \operatorname{depth}_G(x)=d_G(r,x).
\]

## Dependency
TreeDepthMetricIdentity^proved => MetricDepthCoincidence^conditional => ParentDepthDecrement^conditional => RootedBallTrivialization^conditional => FiberQuotientRank^conditional => DirectSumIndependence^conditional => PerStepInformationBound^conditional => QuotientGapClosure^conditional
