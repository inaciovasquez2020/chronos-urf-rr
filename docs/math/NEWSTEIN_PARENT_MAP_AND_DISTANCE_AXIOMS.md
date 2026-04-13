# Newstein Parent Map and Distance Axioms

Status: OPEN

## Parent map domain
There is a rooted ball \(B_R(r)\) with distinguished root \(r\) and parent map
\[
\eta : B_R(r) \to B_R(r).
\]

## Root fixed point
\[
\eta(r)=r.
\]

## Parent-edge admissibility
For every \(w \in B_R(r)\) with \(w \neq r\),
\[
(\eta(w),w)\in E.
\]

## Graph distance
The graph distance to the root is the integer-valued function
\[
d(\,\cdot\,,r): B_R(r)\to \mathbf N.
\]

## Distance normalization
\[
d(r,r)=0.
\]

## Geodesic-parent law
For every \(w \in B_R(r)\) with \(w \neq r\), the vertex \(\eta(w)\) lies on a shortest path from \(w\) to \(r\).

## Triangle inequality specialization
For every edge \((u,v)\in E\),
\[
d(u,r)\le d(v,r)+1
\qquad\text{and}\qquad
d(v,r)\le d(u,r)+1.
\]

## Frontier target
The unique remaining frontier is
\[
\forall w \in B_R(r),\qquad
w \neq r \Longrightarrow d(\eta(w),r)=d(w,r)-1.
\]
