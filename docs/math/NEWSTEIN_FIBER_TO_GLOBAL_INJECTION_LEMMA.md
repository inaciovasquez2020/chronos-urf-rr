# Newstein Fiber-to-Global Injection Lemma

## Status
Conditional target.

## Lemma
Let \(B_n\) be the torus-of-expanders base. For each torus fiber \(T_v\), let
\[
\iota_v^{\mathrm{triv}}:
Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}
\to
Z_1(G_n)\Big/\Big\langle Z_1(B_r^{G_n}(x)):x\in V(G_n)\Big\rangle
\]
and
\[
\iota_v^{\mathrm{tw}}:
Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}
\to
Z_1(H_n)\Big/\Big\langle Z_1(B_r^{H_n}(x)):x\in V(H_n)\Big\rangle
\]
be induced by inclusion.

Then for every \(v\),
\[
\iota_v^{\mathrm{triv}} \text{ is injective},
\qquad
\iota_v^{\mathrm{tw}} \text{ is injective}.
\]

Moreover, for distinct fibers \(u\neq v\),
\[
\operatorname{im}(\iota_u^{\mathrm{triv}})\cap \operatorname{im}(\iota_v^{\mathrm{triv}})=0,
\qquad
\operatorname{im}(\iota_u^{\mathrm{tw}})\cap \operatorname{im}(\iota_v^{\mathrm{tw}})=0.
\]

Therefore,
\[
\bigoplus_v Z_1(\widetilde T_v^{\mathrm{triv}})/W_v^{\mathrm{triv}}
\hookrightarrow
Z_1(G_n)\Big/\Big\langle Z_1(B_r^{G_n}(x)):x\in V(G_n)\Big\rangle
\]
and
\[
\bigoplus_v Z_1(\widetilde T_v^{\mathrm{tw}})/W_v^{\mathrm{tw}}
\hookrightarrow
Z_1(H_n)\Big/\Big\langle Z_1(B_r^{H_n}(x)):x\in V(H_n)\Big\rangle.
\]

## Consequence
Using the fiber quotient-rank values \(4\) and \(2\), one obtains
\[
\dim Q(G_n)-\dim Q(H_n)\ge 2|V(X_n)|.
\]

## Remaining proof obligations
1. prove no local-ball relation can cancel a nonzero fiber quotient class;
2. prove connector edges do not create cross-fiber identifications modulo local spans;
3. prove direct-sum independence across distinct fibers.

## Overclaim guard
No proof of the lemma is claimed here.
