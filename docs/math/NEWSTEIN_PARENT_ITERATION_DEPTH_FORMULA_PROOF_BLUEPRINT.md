# Newstein Parent Iteration Depth Formula Proof Blueprint

Status: OPEN

## Target
Prove
\[
\forall v \in B_R(r),\ \forall n \le d(v,r),\qquad
d\!\left(\eta^{\,n}(v), r\right)=d(v,r)-n.
\]

## Base case
For \(n=0\),
\[
d\!\left(\eta^{\,0}(v), r\right)=d(v,r).
\]

## Step input
Assume
\[
d\!\left(\eta^{\,n}(v), r\right)=d(v,r)-n.
\]

## Step promotion
If \(n+1 \le d(v,r)\), then
\[
d\!\left(\eta(\eta^{\,n}(v)), r\right)=d\!\left(\eta^{\,n}(v), r\right)-1.
\]

## Inductive conclusion
Therefore
\[
d\!\left(\eta^{\,n+1}(v), r\right)=d(v,r)-(n+1).
\]

## Dependency
The only nontrivial input is the one-step decrement law
\[
d(\eta(w),r)=d(w,r)-1
\]
for non-root vertices \(w\).

## Output
This reduces ParentIterationDepthFormula to induction plus the one-step parent-depth decrement law.
