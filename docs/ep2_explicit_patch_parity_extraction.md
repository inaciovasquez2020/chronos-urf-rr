# EP2 — Explicit Patch Parity Extraction

## Status
Input artifact / conditional structural lemma.

## Statement
For every \(k,R\), there exists \(C=C(k,R)\) such that for every patch \(S\) with \(|S|\le C\), and all histories \(h_1,h_2\), if \(h_1,h_2\) are \(EF^k_R\)-distinguishable on \(S\), then there exists a cycle \(C_S \in Z_1(S)\) with \(|C_S|\le C\) such that
\[
\sum_{e\in C_S} h_1(e) \ne \sum_{e\in C_S} h_2(e)
\quad\text{in } \mathbb F_2.
\]

## Immediate consequences
1. Define
\[
\Phi(h_1,h_2):=\mathbf 1_{C_S}.
\]

2. Then
\[
w:=\mathbf 1_{C_S}
\]
is a bounded-support witness on \(S\).

3. Support bound:
\[
|\operatorname{supp}(w)| = |C_S| \le C(k,R).
\]

4. Nontrivial separation:
\[
\langle w,h_1\rangle \ne \langle w,h_2\rangle.
\]

5. Cyclone lower bound:
\[
\mathcal C \ge \frac{\delta(k,R)}{C(k,R)} > 0.
\]

## Program role
EP2 closes the bounded-support dual-witness step by turning local \(EF^k_R\)-distinguishability into explicit parity separation on a bounded patch cycle.

## Dependency edge
EP2 implies the bounded-support dual witness lemma and therefore the Cyclone step.

