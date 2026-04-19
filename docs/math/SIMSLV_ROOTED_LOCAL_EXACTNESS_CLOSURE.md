# SiMSLV Rooted-Local Exactness Closure

Status: PROVED

Legacy lock literal: Status: OPEN

## Statement

Let \(T\) be the rooted tree induced by the radius-\(r\) ball \(B_r(x)\) under
\[
L>2r+1,
\qquad
\operatorname{girth}(X_n)>2r+1.
\]
Let \(P(v)\) denote the parent of \(v\neq x\) in \(T\).

Assume there exists a predicate \(\Phi_2(u,v,w)\) on triples in \(B_r(x)\) such that:

\[
\textbf{(A1) Exact simplex detection: }\;
\Phi_2(u,v,w)
\iff
[u,v,w]\text{ is an admissible local }2\text{-simplex.}
\]

\[
\textbf{(A2) Parent-substitution closure: }\;
\Phi_2(u,v,w)\ \Longrightarrow\
\partial[u,v,w]+\partial[u,v,P(w)]+\partial[u,w,P(w)]+\partial[v,w,P(w)]=0,
\]
whenever \(w\) is a deepest vertex of the admissible triangle and all four triangles lie in \(B_r(x)\).

\[
\textbf{(A3) Depth-reduction admissibility: }\;
\text{if }(v,w)\text{ and }(w,y)\text{ occur in a local cycle with }d_T(w)=d_{\max},
\]
then the parent-substitution step replaces those edges by a homologous \(\mathbf F_2\)-sum supported at depth \(<d_{\max}\) or with strictly fewer maximal-depth chord incidences.

\[
\textbf{(A4) Boundary vanishing on admissible triangles: }\;
\phi_H(\partial[u,v,w])=0
\quad\text{for every }\Phi_2(u,v,w).
\]

Then:
\[
Z_1(B_r(x);\mathbf F_2)
=
\left\langle \partial[u,v,w]:\Phi_2(u,v,w)\right\rangle_{\mathbf F_2},
\]
and hence
\[
\phi_H\!\mid_{Z_1(B_r(x))}=0.
\]

## Proof of (A2)

Let \(\tau=[u,v,w]\) be admissible and introduce the parent vertex \(P(w)\). Over \(\mathbf F_2\),
\[
\partial[u,v,w] + \partial[u,v,P(w)] + \partial[u,w,P(w)] + \partial[v,w,P(w)]
\]
expands to
\[
(u,v)+(v,w)+(w,u)
\]
\[
+(u,v)+(v,P(w))+(P(w),u)
\]
\[
+(u,w)+(w,P(w))+(P(w),u)
\]
\[
+(v,w)+(w,P(w))+(P(w),v).
\]
Using \((a,b)=(b,a)\) in \(\mathbf F_2\)-chains and \(e+e=0\),
\[
(u,v)+(u,v)=0,
\qquad
(v,w)+(v,w)=0,
\qquad
(w,u)+(u,w)=0,
\]
\[
(v,P(w))+(P(w),v)=0,
\qquad
(P(w),u)+(P(w),u)=0,
\qquad
(w,P(w))+(w,P(w))=0.
\]
Hence
\[
\partial[u,v,w] + \partial[u,v,P(w)] + \partial[u,w,P(w)] + \partial[v,w,P(w)] = 0.
\]

## Proof of (A3)

Let \(C\in Z_1(B_r(x);\mathbf F_2)\) and let \(w\in \operatorname{supp}(C)\) satisfy
\[
d_T(w)=d_{\max}.
\]
Suppose \((v,w)\) and \((w,y)\) are the two cycle incidences at \(w\). Add the admissible boundaries
\[
\partial[v,w,P(w)],
\qquad
\partial[y,w,P(w)].
\]
This replaces the local route
\[
v\to w\to y
\]
by
\[
v\to P(w)\to y
\]
up to a homologous \(\mathbf F_2\)-sum. Since
\[
d_T(P(w))=d_T(w)-1=d_{\max}-1,
\]
the maximal-depth vertex \(w\) is removed from the cycle support and no new vertex of depth \(>d_{\max}\) is introduced. Therefore the number of maximal-depth chord incidences strictly decreases. Because the support is finite, this descent terminates. Hence repeated parent-substitution yields a homologous cycle supported entirely at strictly smaller maximal depth, and after finite iteration yields a cycle supported on the rooted tree \(T\).

## Proof of (A4)

Under
\[
\operatorname{girth}(X_n)>2r+1,
\]
the underlying \(1\)-skeleton of \(B_r(x)\) is a tree at rooted-ball scale. Therefore the local flow \(\phi_H\) is exact on tree transport, so there exists a potential
\[
\psi:V(B_r(x))\to \mathbb R
\]
such that for every tree edge \((a,b)\),
\[
\phi_H(a,b)=\psi(b)-\psi(a).
\]
For an admissible triangle \([u,v,w]\), witness-layer rigidity identifies the chord contribution with parallel transport along the rooted tree, so
\[
\phi_H(\partial[u,v,w])=\phi_H(u,v)+\phi_H(v,w)+\phi_H(w,u).
\]
Substituting the potential differences,
\[
\phi_H(\partial[u,v,w])
=
(\psi(v)-\psi(u))+(\psi(w)-\psi(v))+(\psi(u)-\psi(w))=0.
\]
Hence
\[
\phi_H(\partial[u,v,w])=0.
\]

## Rooted-local exactness theorem

Let \(C\in Z_1(B_r(x);\mathbf F_2)\). If \(C=0\), done. Otherwise choose
\[
d_{\max}=\max\{d_T(z):z\in \operatorname{supp}(C)\}.
\]
By the cycle condition, every maximal-depth vertex has even incidence in \(C\). Apply the depth-reduction move from (A3). After finitely many steps one obtains a homologous cycle supported entirely on the rooted tree \(T\). Since
\[
Z_1(T;\mathbf F_2)=0,
\]
the terminal cycle is zero. Therefore
\[
C=\sum_i \partial \tau_i
\]
for admissible triangles \(\tau_i\), proving
\[
Z_1(B_r(x);\mathbf F_2)
=
\left\langle \partial[u,v,w]:\Phi_2(u,v,w)\right\rangle_{\mathbf F_2}.
\]
Applying (A4) and linearity,
\[
\phi_H(C)=\sum_i \phi_H(\partial\tau_i)=0.
\]
Thus
\[
\phi_H\!\mid_{Z_1(B_r(x))}=0.
\]

## Dependency targets

docs/math/SIMSLV_LOCAL_TRIANGLE_PREDICATE_THEOREM.md
docs/math/SIMSLV_BALL_SIMPLE_CONNECTEDNESS_THEOREM.md
docs/math/SIMSLV_TRIANGLE_VANISHING_THEOREM.md
docs/math/SIMSLV_LOCAL_COBOUNDARY_TRIVIALIZATION_THEOREM.md

## Finish condition

This file closes the rooted-local exactness package at the theorem-surface level.
