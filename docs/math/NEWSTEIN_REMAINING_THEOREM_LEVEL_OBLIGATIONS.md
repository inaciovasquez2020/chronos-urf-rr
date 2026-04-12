# Remaining theorem-level obligations in the Newstein chain

## I. Rooted-ball branch

### I.1 Local triangle-generation theorem

Prove, for every \(x \in V(B_n)\),
\[
Z_1\!\bigl(B_r^{B_n}(x)\bigr)
=
\left\langle \partial\tau : \tau \subseteq B_r^{B_n}(x)\ \text{a triangle}\right\rangle_{\mathbb F_2}.
\]

This requires:

\[
\text{(a) }L>2r+1 \Longrightarrow \text{ no radius-}r\text{ ball wraps around a torus fiber;}
\]

\[
\text{(b) }\operatorname{girth}(X_n)>2r+1 \Longrightarrow \text{ no radius-}r\text{ ball contains a backbone cycle;}
\]

\[
\text{(c) }\text{the local }2\text{-complex is simply connected;}
\]

\[
\text{(d) }\text{every local } \mathbb F_2\text{-cycle is a sum of triangle boundaries.}
\]

### I.2 Triangle-vanishing theorem

Prove, for every local triangle \(\tau\),
\[
\phi_H(\partial\tau)=0.
\]

This requires:

\[
\text{(a) explicit cocycle definition on every edge class;}
\]

\[
\text{(b) direct parity check on each triangle type;}
\]

\[
\text{(c) additivity of }\phi_H\text{ on }\mathbb F_2\text{-boundary sums.}
\]

### I.3 Local cycle-vanishing theorem

Deduce, from I.1 and I.2, that for every local cycle \(C\subseteq B_r^{B_n}(x)\),
\[
\phi_H(C)=0.
\]

### I.4 Local coboundary theorem

Prove: if \(U\) is connected and \(\phi(C)=0\) for every cycle \(C\subseteq U\), then there exists
\[
f:V(U)\to\mathbb F_2
\quad\text{with}\quad
\phi=\delta f.
\]

This requires:

\[
\text{(a) path-difference gives an }\mathbb F_2\text{-cycle;}
\]

\[
\text{(b) path integral is path-independent;}
\]

\[
\text{(c) edgewise verification } \phi(uv)=f(u)+f(v).
\]

### I.5 Rooted-ball trivialization theorem

Combine I.3 and I.4 to prove, for every \(x\),
\[
\widetilde B_r^{,\mathrm{tw}}(x)\cong \widetilde B_r^{,\mathrm{triv}}(x),
\]
hence
\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n).
\]

## II. Fiber quotient-rank branch

### II.1 Quotient-homology identification

Prove, for each lifted torus fiber \(\widetilde T\),
\[
Z_1(\widetilde T)/W \cong H_1(\widetilde T;\mathbb F_2),
\]
where \(W\) is the span of lifted triangle boundaries.

### II.2 Trivial fiber rank computation

Prove, for the trivial double cover,
\[
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T^{\mathrm{triv}})/W^{\mathrm{triv}}\bigr)=4.
\]

This requires showing \(\widetilde T^{\mathrm{triv}}\) is a disjoint union of two tori.

### II.3 Twisted fiber rank computation

Prove, for the twisted double cover,
\[
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T^{\mathrm{tw}})/W^{\mathrm{tw}}\bigr)=2.
\]

This requires:

\[
\text{(a) the chosen monodromy is odd on exactly one primitive torus direction;}
\]

\[
\text{(b) the cover is connected;}
\]

\[
\text{(c) the lifted fiber is a single torus, not two disjoint tori.}
\]

### II.4 Fiber rank gap theorem

Conclude, for each fiber \(v\),
\[
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}\bigr)
-
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}\bigr)
=2.
\]

## III. Fiber-to-global branch

### III.1 Injectivity for one fiber

For each fiber \(v\), prove the inclusion-induced map
\[
\iota_v^{\mathrm{triv}}:
Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}
\to
Q(G_n)
\]
is injective, and likewise
\[
\iota_v^{\mathrm{tw}}:
Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}
\to
Q(H_n)
\]
is injective, where
\[
Q(G):=
Z_1(G)\Big/\Big\langle Z_1(B_r^G(x)):x\in V(G)\Big\rangle.
\]

This requires proving that no local-ball relation kills a nonzero fiber quotient class.

### III.2 Cross-fiber independence

For distinct fibers \(u\neq v\), prove
\[
\operatorname{im}(\iota_u)\cap \operatorname{im}(\iota_v)=0.
\]

This requires proving connector edges do not create quotient identifications between different fibers.

### III.3 Direct-sum embedding

Deduce
\[
\bigoplus_v Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}
\hookrightarrow Q(G_n),
\qquad
\bigoplus_v Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}
\hookrightarrow Q(H_n).
\]

## IV. Global assembly branch

### IV.1 Quotient-gap theorem

Combine I.5, II.4, and III.3 to prove
\[
\dim_{\mathbb F_2}Q(G_n)-\dim_{\mathbb F_2}Q(H_n)\ge 2|V(X_n)|.
\]

Hence
\[
\dim_{\mathbb F_2}Q(G_n)-\dim_{\mathbb F_2}Q(H_n)=\Omega(n).
\]

### IV.2 Non-factorization consequence

From
\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n)
\quad\text{and}\quad
Q(G_n)\neq Q(H_n),
\]
deduce \(Q\) does not factor through rooted radius-\(r\) type or \(FO^k_r\)-type.

## V. Complexity/lower-bound branch

### V.1 Per-step information bound

Prove, in the intended refinement model,
\[
\Delta I_t \le C
\quad\text{for every admissible step }t.
\]

### V.2 Transcript lower bound

Combine IV.1 and V.1 to obtain
\[
T_n \ge \frac{2|V(X_n)|}{C}.
\]

If \(|V(X_n)|=\Theta(n)\), then
\[
T_n=\Omega(n).
\]

## Minimal closure set

The irreducible unresolved items are:

1. Local triangle-generation theorem.
2. Triangle-vanishing theorem.
3. Fiber quotient-rank computation \(4\) vs. \(2\).
4. Fiber-to-global injectivity/direct-sum independence.
5. Per-step information bound.

## Repository status

`chronos-urf-rr`: reduction-complete, theorem-incomplete.

## Next executable structural actions

1. Prove the local triangle-generation theorem for radius-\(r\) balls.
2. Fix an explicit twisted cocycle and verify triangle-vanishing by case split on triangle types.
3. Prove \(Z_1(\widetilde T)/W \cong H_1(\widetilde T;\mathbb F_2)\) fiberwise.
4. Prove fiber inclusion injects modulo local-ball spans.
5. State the admissible refinement model and prove \(\Delta I_t\le C\).
