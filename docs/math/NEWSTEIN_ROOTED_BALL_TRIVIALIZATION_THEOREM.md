# Newstein Rooted-Ball Trivialization Theorem

\[
\boxed{
\text{Assumptions}
}
\]

Assume (A1)--(A4) and the simplicial admissibility package (S0)--(S2).

\[
\boxed{
\text{Prism operators}
}
\]

For every oriented simplex
\[
\sigma=[v_0,\dots,v_k],
\]
define
\[
\Delta_i(\sigma):=[v_0,\dots,v_i,p(v_i),p(v_{i+1}),\dots,p(v_k)],
\qquad 0\le i\le k,
\]
and
\[
K_k(\sigma):=\sum_{i=0}^{k}(-1)^i\Delta_i(\sigma).
\]

\[
\boxed{
\text{Chain-homotopy identity}
}
\]

\[
\partial K_k+K_{k-1}\partial=\operatorname{id}-p_{\#}
\qquad\text{on }C_k(B_R(r)),
\]

where
\[
p_{\#}([v_0,\dots,v_k]):=[p(v_0),\dots,p(v_k)].
\]

\[
\boxed{
\text{Telescoping operator}
}
\]

\[
L_k^{(R)}:=\sum_{t=0}^{R-1}p_{\#}^{\,t}K_k.
\]

Then
\[
\partial L_k^{(R)}+L_{k-1}^{(R)}\partial
=
\operatorname{id}-p_{\#}^{\,R}.
\]

\[
\boxed{
\text{Collapse to the root}
}
\]

Let
\[
\rho(v):=r.
\]

By (A4),
\[
p_{\#}^{\,R}=\rho_{\#}.
\]

In normalized chains,
\[
\rho_{\#}=0
\qquad\text{on }C_k(B_R(r)),\quad k\ge 1.
\]

\[
\boxed{
\text{Theorem}
}
\]

\[
\forall c\in Z_k(B_R(r)),\ k\ge 1,\ \exists b=L_k^{(R)}(c)\in C_{k+1}(B_R(r))
\text{ such that }\partial b=c.
\]

\[
\boxed{
\text{Proof}
}
\]

For
\[
c\in Z_k(B_R(r)),\qquad k\ge 1,
\]
set
\[
b:=L_k^{(R)}(c).
\]
Then
\[
\partial b
=
(\partial L_k^{(R)}+L_{k-1}^{(R)}\partial)(c)
=
(\operatorname{id}-p_{\#}^{\,R})(c)
=
(\operatorname{id}-\rho_{\#})(c)
=
c.
\]

\[
\boxed{
\text{Terminal frontier}
}
\]

\[
\text{The sole active obstruction is unconditional discharge of the simplicial admissibility package (S0)--(S2).}
\]

\[
\text{Status: CONDITIONAL on (S0)--(S2).}
\]
