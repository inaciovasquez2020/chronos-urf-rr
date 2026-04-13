# Newstein Simplicial Multi-Parent Replacement Lemma

\[
\boxed{
\text{Ambient data}
}
\]

\[
T\ \text{a simplicial complex},\qquad r\in T^{(0)},\qquad B_R(r)\subseteq T\ \text{the rooted-ball subcomplex}.
\]

\[
p:T^{(0)}\to T^{(0)}.
\]

\[
\text{(A1)}\ p(r)=r,\qquad
\text{(A2)}\ x\in B_R(r)^{(0)}\Rightarrow p(x)\in B_R(r)^{(0)},
\]

\[
\text{(A3)}\ p(v)\neq v\Rightarrow d(p(v),r)=d(v,r)-1,\qquad
\text{(A4)}\ \forall v\in B_R(r)^{(0)}\ \exists m\le R:\ p^m(v)=r.
\]

\[
\boxed{
\text{Lemma}
}
\]

\[
\forall m\ge 0,\ \forall [x_0,\dots,x_m]\in C_m(B_R(r)),\ \forall I\subseteq\{0,\dots,m\},
\quad
[y_0,\dots,y_m]\in C_m(B_R(r)),
\]
where
\[
y_t=
\begin{cases}
p(x_t), & t\in I,\\
x_t, & t\notin I.
\end{cases}
\]

\[
\boxed{
\text{Specializations}
}
\]

\[
I=\{j\}
\Longrightarrow
[x_0,\dots,x_{j-1},p(x_j),x_{j+1},\dots,x_m]\in C_m(B_R(r)).
\]

\[
I=\{0,\dots,m\}
\Longrightarrow
[p(x_0),\dots,p(x_m)]\in C_m(B_R(r)).
\]

\[
\boxed{
\text{Frontier status}
}
\]

\[
\text{OPEN}.
\]

\[
\boxed{
\text{Terminal frontier}
}
\]

\[
\text{Unconditional proof of the multi-parent replacement lemma.}
\]
