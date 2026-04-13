# Newstein Simplicial Admissibility Package

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
\text{Fullness}
}
\]

\[
\text{(S0)}\quad
B_R(r)\ \text{is a full simplicial subcomplex of }T.
\]

\[
\boxed{
\text{One-vertex parent replacement}
}
\]

\[
\text{(S1)}\quad
\forall m\ge 0,\ \forall [x_0,\dots,x_m]\in C_m(B_R(r)),\ \forall j\le m,\ 
[x_0,\dots,x_{j-1},p(x_j),x_{j+1},\dots,x_m]\in C_m(B_R(r)).
\]

\[
\boxed{
\text{Full vertexwise parent image}
}
\]

\[
\text{(S2)}\quad
\forall m\ge 0,\ \forall [x_0,\dots,x_m]\in C_m(B_R(r)),\ 
[p(x_0),\dots,p(x_m)]\in C_m(B_R(r)).
\]

\[
\boxed{
\text{Derived prism admissibility}
}
\]

\[
\forall k\ge 0,\ \forall [v_0,\dots,v_k]\in C_k(B_R(r)),\ \forall i\le k,
\]

\[
[v_0,\dots,v_i,p(v_i),p(v_{i+1}),\dots,p(v_k)]\in C_{k+1}(B_R(r)).
\]

\[
\text{Reason: repeated use of (S1) together with fullness (S0).}
\]

\[
\boxed{
\text{Core unconditional package}
}
\]

\[
\text{(S0), (S1), (S2)}.
\]

\[
\boxed{
\text{Weakest compressed form}
}
\]

\[
\text{If fullness is built into the definition of }B_R(r),\text{ then the active admissibility package is exactly (S1) and (S2).}
\]

\[
\text{Status: OPEN.}
\]
