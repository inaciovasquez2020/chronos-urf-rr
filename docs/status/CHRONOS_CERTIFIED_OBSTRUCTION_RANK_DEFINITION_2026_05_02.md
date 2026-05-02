# Chronos Certified Obstruction Rank Definition — 2026-05-02

Status: DEFINITION LOCK / THEOREM FRONTIER INPUT

## Ambient Object

Let \(G=(V,E)\) be a finite undirected graph.

All chain groups are over \(\mathbb F_2\).

\[
C_1(G)=\mathbb F_2^E,\qquad C_0(G)=\mathbb F_2^V.
\]

Let

\[
\partial:C_1(G)\to C_0(G)
\]

be the incidence boundary map.

## Cycle Space

\[
Z_1(G)=\ker(\partial).
\]

## Radius-\(R\) Local Cycle Subspace

For \(v\in V\), let \(B_R(v)\) be the radius-\(R\) graph ball.

Define

\[
L_R(G)
=
\operatorname{span}_{\mathbb F_2}
\{z\in Z_1(G): \operatorname{supp}(z)\subseteq E(B_R(v))\text{ for some }v\in V\}.
\]

## Certified Obstruction Rank

\[
\operatorname{COR}_R(G)
=
\dim_{\mathbb F_2}\bigl(Z_1(G)/L_R(G)\bigr).
\]

Equivalently,

\[
\operatorname{COR}_R(G)
=
\dim_{\mathbb F_2}Z_1(G)
-
\dim_{\mathbb F_2}L_R(G).
\]

## Family-Level Growth Input

A graph family \((G_n)\) has linear certified obstruction rank growth at radius \(R\) if there exists \(\alpha>0\) and \(n_0\) such that

\[
\operatorname{COR}_R(G_n)\ge \alpha |V(G_n)|
\]

for every \(n\ge n_0\).

## Theorem-Level Role

This is the exact obstruction-rank input intended for the Chronos theorem path:

\[
\text{bounded local transcript capacity}
+
\operatorname{COR}_R(G_n)\ge \alpha |V(G_n)|
\Longrightarrow
\operatorname{EntropyDepth}(G_n)=\Omega(|V(G_n)|).
\]

## Boundary

This document fixes a definition only.

It does not prove the Chronos theorem-level closure.

It does not prove the finite-to-general lift.

It does not prove the locality-to-depth bridge.

It does not assert that every existing certificate already computes \(\operatorname{COR}_R\).

## Weakest Missing Lemma

The remaining theorem-level bridge is:

\[
\operatorname{COR}_R(G_n)\ge \alpha |V(G_n)|
\Longrightarrow
\text{every Chronos-admissible refinement has EntropyDepth }\Omega(|V(G_n)|).
\]

