# Chronos COR Finite Family Registry — 2026-05-02

Status: FINITE FAMILY REGISTRY / THEOREM ASSUMPTION SURFACE

## Object

This registry verifies a finite list of COR incidence-basis certificates under one shared radius \(R\) and one shared rational lower-bound constant \(\alpha\).

For every listed finite certificate, the registry checks:

\[
\operatorname{COR}_R(G_i)\ge \alpha |V(G_i)|.
\]

## Checked Inputs

The registry verifies:

- each listed certificate exists,
- each certificate passes the incidence-basis verifier,
- each certificate uses field \(\mathbb F_2\),
- each certificate has the registry's shared radius \(R\),
- each certificate satisfies the shared finite inequality
  \[
  \operatorname{COR}_R(G_i)\ge \alpha |V(G_i)|.
  \]

## Boundary

This registry verifies a finite family of incidence-basis certificates only.

It does not prove an infinite graph-family theorem.

It does not prove the finite-to-general lift.

It does not prove the locality-to-depth bridge.

It does not prove theorem-level Chronos closure.

## Weakest Next Lemma

The next theorem-level bridge is the finite-to-general lift:

\[
\forall i\in I_{\mathrm{finite}},\ 
\operatorname{COR}_R(G_i)\ge \alpha |V(G_i)|
\quad\Longrightarrow\quad
\forall n\ge n_0,\ 
\operatorname{COR}_R(G_n)\ge \alpha' |V(G_n)|.
\]

