# Newstein Parent Iteration To Root Reduction

Status: OPEN

## Reduction statement
Assume ParentIterationDepthFormula:
\[
\forall v \in B_R(r),\ \forall n \le d(v,r),\qquad
d\!\left(\eta^{\,n}(v),r\right)=d(v,r)-n.
\]

Then for every \(v \in B_R(r)\),
\[
\eta^{\,d(v,r)}(v)=r.
\]

## Proof
Set \(n=d(v,r)\). Then
\[
d\!\left(\eta^{\,d(v,r)}(v),r\right)=d(v,r)-d(v,r)=0.
\]
A vertex has distance \(0\) from \(r\) if and only if it is \(r\). Therefore
\[
\eta^{\,d(v,r)}(v)=r.
\]

## Output
ParentIterationToRoot is reduced to ParentIterationDepthFormula plus the identity-of-indiscernibles for graph distance.
