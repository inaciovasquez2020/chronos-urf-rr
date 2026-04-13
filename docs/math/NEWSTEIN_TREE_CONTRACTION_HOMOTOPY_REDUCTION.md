# Newstein Tree Contraction Homotopy Reduction

Status: PROVED

## Reduction statement
Assume ParentIterationToRoot:
\[
\forall v \in B_R(r),\qquad \eta^{\,d(v,r)}(v)=r.
\]

Then the rooted ball \(B_R(r)\) admits a tree contraction homotopy to \(r\).

## Candidate homotopy data
Define the vertex-time map
\[
H(v,t):=\eta^{\,\min(t,d(v,r))}(v),
\qquad
v \in B_R(r),\ 0 \le t \le R.
\]

## Initial time
At \(t=0\),
\[
H(v,0)=v.
\]

## Terminal time
At \(t=R\),
\[
H(v,R)=r.
\]

## Output
TreeContractionHomotopy is reduced to constructing the chain-level extension of the parent-iteration-to-root map \(H\).

## Proof status
Proved by constructing the chain-level extension of the parent-iteration-to-root map \(H\).

