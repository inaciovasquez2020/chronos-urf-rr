# Deterministic Cycle–Expander Rigidity

## Target Statement

Fix \(d \ge 3\) and \(\varepsilon > 0\).

There exist constants \(c>0\) and \(R_0 \in \mathbb{N}\) such that for every finite
\(d\)-regular \(\varepsilon\)-edge-expander \(G\), every vertex \(v\), and every radius
\(1 \le R \le R_0 \log_{d-1}|V(G)|\),

\[
\beta_1(B_R(v)) \ge c (d-1)^R .
\]

## Reduction Skeleton

To prove the target statement it is sufficient to establish the following lemma.

### Layer-Collision Lemma
There exist constants \(\alpha>0\) and \(R_0\) such that for every finite
\(d\)-regular \(\varepsilon\)-edge-expander \(G\), every vertex \(v\), and every
\(1 \le R \le R_0 \log_{d-1}|V(G)|\), the induced ball \(B_R(v)\) contains at least

\[
\alpha (d-1)^R
\]

non-tree edges.

## Deduction from Layer-Collision Lemma

If \(B_R(v)\) is connected, then

\[
\beta_1(B_R(v)) = |E(B_R(v))| - |V(B_R(v))| + 1.
\]

Writing \(T_R(v)\) for a spanning tree of \(B_R(v)\), every non-tree edge increases
\(\beta_1\) by at least \(1\). Hence

\[
\#\{\text{non-tree edges in } B_R(v)\} \le \beta_1(B_R(v)).
\]

Therefore the Layer-Collision Lemma implies

\[
\beta_1(B_R(v)) \ge \alpha (d-1)^R.
\]

Thus the deterministic rigidity theorem reduces to proving uniform lower bounds on
layer collisions inside expander balls.

## Missing Lemma

A deterministic collision bound converting edge expansion of \(G\) into a lower bound
on internal excess edges of every radius-\(R\) ball.

Status: open.
