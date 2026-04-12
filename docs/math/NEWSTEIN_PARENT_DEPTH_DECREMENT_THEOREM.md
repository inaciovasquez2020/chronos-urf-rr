# NEWSTEIN PARENT-DEPTH DECREMENT THEOREM

Status: PROVED

## Statement
For a rooted shortest-path tree \(G\) on \(B_R(r)\), assume:
1. \(x \neq r\).
2. \(p(x)\) is the parent of \(x\) in \(G\).
3. \(\forall u \in B_R(r),\ \operatorname{depth}_G(u)=d_T(r,u)\).
4. \(\forall u \neq r,\ u \in B_R(r)\Rightarrow d_T(r,p(u))=d_T(r,u)-1\).
5. \(\forall u \in B_R(r),\ p(u)\in B_R(r)\).

Then
\[
\forall x \in B_R(r),\ x \neq r \Rightarrow \operatorname{depth}_G(p(x))=\operatorname{depth}_G(x)-1.
\]

## Discharge
Rewrite both depth terms using `MetricDepthCoincidence`, apply `parent_dist_step`, and use `parent_in_ball` for the parent vertex.

## Dependency Chain
ParentDepthDecrement^proved => RootedBallTrivialization^conditional => FiberQuotientRank^conditional => DirectSumIndependence^conditional => PerStepInformationBound^conditional => QuotientGapClosure^conditional
