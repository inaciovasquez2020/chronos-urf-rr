# Newstein Quotient-Gap Assembly Theorem

## Status
Conditional target.

## Theorem
Let
\[
Q(G):=
Z_1(G)\Big/\Big\langle Z_1(B_r^{G}(x)):x\in V(G)\Big\rangle.
\]

Assume:

1. \(\operatorname{Type}_{k,r}(G_n)=\operatorname{Type}_{k,r}(H_n)\);
2. for every torus fiber \(v\),
   \[
   \dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}\bigr)=4;
   \]
3. for every torus fiber \(v\),
   \[
   \dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}\bigr)=2;
   \]
4. the direct sum of trivial-lift fiber quotients injects into \(Q(G_n)\);
5. the direct sum of twisted-lift fiber quotients injects into \(Q(H_n)\).

Then
\[
\dim_{\mathbb F_2} Q(G_n)-\dim_{\mathbb F_2} Q(H_n)\ge 2|V(X_n)|.
\]

In particular,
\[
\dim_{\mathbb F_2} Q(G_n)-\dim_{\mathbb F_2} Q(H_n)=\Omega(n).
\]

If, moreover, each admissible local refinement step reveals at most \(C\) bits of information, then any such process distinguishing \(G_n\) from \(H_n\) satisfies
\[
T_n \ge \frac{2|V(X_n)|}{C}.
\]

## Interpretation
The rooted-ball trivialization lemma, the fiber quotient-rank lemma, and the fiber-to-global injection lemma assemble into a linear quotient-gap theorem and hence a linear lower bound on local transcript length.

## Remaining proof obligations
1. discharge rooted-ball trivialization;
2. discharge fiber quotient-rank computation;
3. discharge fiber-to-global injection;
4. verify the per-step information bound in the target refinement model.

## Overclaim guard
No proof of the theorem is claimed here.
