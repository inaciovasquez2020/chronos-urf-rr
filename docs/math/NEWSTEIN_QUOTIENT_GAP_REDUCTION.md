# Newstein Quotient-Gap Reduction

## Status
Conditional reduction only.

## Corrected target
Let \(B_n\) be a bounded-degree torus-of-expanders base, with trivial \(2\)-lift \(G_n\) and twisted \(2\)-lift \(H_n\). Fix \(k,r\).

Target conclusions:

1. \(\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n)\).
2. The quotient-cycle gap
   \[
   \dim_{\mathbb F_2}\!\left(
   Z_1(G_n)\Big/\Big\langle Z_1(B_r^{G_n}(x)):x\in V(G_n)\Big\rangle
   \right)
   -
   \dim_{\mathbb F_2}\!\left(
   Z_1(H_n)\Big/\Big\langle Z_1(B_r^{H_n}(x)):x\in V(H_n)\Big\rangle
   \right)
   = \Omega(n).
   \]

## Weakest sufficient missing lemma
### Fiber Quotient-Rank Lemma
For each torus gadget \(T_v\subset B_n\), let \(W_v^{\mathrm{triv}}\) and \(W_v^{\mathrm{tw}}\) denote the \(\mathbb F_2\)-spans of lifted triangle boundaries in the trivial and twisted \(2\)-lifts of \(T_v\). Then:

\[
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}\bigr)=4,
\qquad
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}\bigr)=2.
\]

Moreover, these fiber quotient classes inject into the global quotients
\[
Z_1(G_n)\Big/\Big\langle Z_1(B_r^{G_n}(x)):x\in V(G_n)\Big\rangle,
\qquad
Z_1(H_n)\Big/\Big\langle Z_1(B_r^{H_n}(x)):x\in V(H_n)\Big\rangle,
\]
and remain independent across distinct fibers \(v\).

## Consequence
If the rooted-ball trivialization lemma holds at radius \(r\), then
\[
\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n)
\]
and the global quotient-cycle gap is at least \(2|V(X_n)|\), hence \(\Omega(n)\).

## Remaining proof obligations
1. Rooted-ball trivialization for the twisted cocycle on every radius-\(r\) ball.
2. Fiber quotient-rank computation \(4\) vs \(2\).
3. Direct-sum injection of fiber classes into the global quotient.
4. Independence across fibers.
5. Final transfer to the URF non-factorization statement.

## Overclaim guard
No full proof of the \(\Omega(n)\) quotient-gap theorem is claimed here.
Only the reduction to the Fiber Quotient-Rank Lemma is claimed.
