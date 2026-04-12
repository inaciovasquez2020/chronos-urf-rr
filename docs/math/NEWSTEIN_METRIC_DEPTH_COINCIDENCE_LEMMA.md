# NEWSTEIN METRIC-DEPTH COINCIDENCE LEMMA

Status: PROVED

## Statement
Let \(T\) be the ambient local graph, let \(G\) be a rooted shortest-path tree on \(B_R(r)\), and let \(x \in B_R(r)\). Assume:
1. \(G \subseteq T\).
2. \(G\) is a BFS/shortest-path tree rooted at \(r\).
3. \(\forall x,\ \operatorname{depth}_G(x)=d_G(r,x)\).
4. \(\forall x \in B_R(r),\ d_G(r,x)=d_T(r,x)\).

Then
\[
\forall x \in B_R(r),\ \operatorname{depth}_G(x)=d_T(r,x).
\]

## Discharge
Use `TreeDepthMetricIdentity` to rewrite \(\operatorname{depth}_G(x)\) as \(d_G(r,x)\), then use `bfs_dist_eq_graph_dist` to rewrite \(d_G(r,x)\) as \(d_T(r,x)\).

## Dependency Chain
MetricDepthCoincidence^proved => ParentDepthDecrement^conditional => RootedBallTrivialization^conditional => FiberQuotientRank^conditional => DirectSumIndependence^conditional => PerStepInformationBound^conditional => QuotientGapClosure^conditional
