# Newstein Parent Iteration Depth Formula Reduction

Status: OPEN

## Reduction statement
Assume the one-step decrement law:
\[
\forall w \in B_R(r),\quad w \neq r \Longrightarrow d(\eta(w),r)=d(w,r)-1.
\]

Then for every \(v \in B_R(r)\) and every integer \(n\) with \(0 \le n \le d(v,r)\),
\[
d\!\left(\eta^{\,n}(v),r\right)=d(v,r)-n.
\]

## Proof skeleton
The proof is by induction on \(n\).

### Base case
At \(n=0\),
\[
d\!\left(\eta^{\,0}(v),r\right)=d(v,r).
\]

### Inductive step
Assume
\[
d\!\left(\eta^{\,n}(v),r\right)=d(v,r)-n
\]
for some \(n<d(v,r)\). Then \(\eta^{\,n}(v)\neq r\), so the one-step decrement law applies to \(w=\eta^{\,n}(v)\), giving
\[
d\!\left(\eta^{\,n+1}(v),r\right)
=
d\!\left(\eta(\eta^{\,n}(v)),r\right)
=
d\!\left(\eta^{\,n}(v),r\right)-1
=
d(v,r)-(n+1).
\]

## Output
ParentIterationDepthFormula is reduced to induction plus the one-step decrement law.
