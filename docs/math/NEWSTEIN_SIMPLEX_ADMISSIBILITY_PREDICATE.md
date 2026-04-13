# Newstein Simplex Admissibility Predicate

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
\boxed{
\text{Exact predicate}
}
\]

\[
\mathrm{Simp}_m(x_0,\dots,x_m)
\iff
[x_0,\dots,x_m]\in C_m(B_R(r)).
\]

\[
\boxed{
\text{Explicit closure target}
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
\text{Exact preservation form}
}
\]

\[
\forall m\ge 0,\ \forall x_0,\dots,x_m,\quad
\mathrm{Simp}_m(x_0,\dots,x_m)\Longrightarrow \mathrm{Simp}_m(y_0,\dots,y_m).
\]

\[
\boxed{
\text{Status}
}
\]

\[
\text{OPEN}.
\]

\[
\boxed{
\text{Truth condition}
}
\]

\[
\text{No unconditional defining formula for }\mathrm{Simp}_m\text{ is yet fixed in the repository.}
\]
