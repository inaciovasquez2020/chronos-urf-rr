# Newstein Local Cycle-Vanishing Theorem

## Target statement

For every \(x \in V(B_n)\) and every local cycle \(C \subseteq B_r^{B_n}(x)\),
\[
\phi_H(C)=0.
\]

## Inputs

### 1. Local triangle-generation theorem

Assume
\[
Z_1\!\bigl(B_r^{B_n}(x)\bigr)
=
\left\langle \partial\tau : \tau \subseteq B_r^{B_n}(x)\ \text{a triangle}\right\rangle_{\mathbb F_2}.
\]

### 2. Triangle-vanishing theorem

Assume
\[
\phi_H(\partial\tau)=0
\quad
\text{for every local triangle } \tau.
\]

## Deduction

Let \(C \subseteq B_r^{B_n}(x)\) be a local \(\mathbb F_2\)-cycle.

By local triangle-generation,
\[
C=\sum_i \partial\tau_i
\]
for local triangles \(\tau_i \subseteq B_r^{B_n}(x)\).

By additivity of \(\phi_H\),
\[
\phi_H(C)=\sum_i \phi_H(\partial\tau_i).
\]

By triangle-vanishing,
\[
\phi_H(\partial\tau_i)=0
\quad
\text{for all } i.
\]

Hence
\[
\phi_H(C)=0.
\]

## Assembly theorem

Combining the two rooted-ball inputs yields
\[
\phi_H(C)=0
\quad
\text{for every local cycle } C \subseteq B_r^{B_n}(x).
\]

## Status

This is the derived closure step between triangle-vanishing and local coboundary.

## Dependencies discharged by this theorem

1. Input to the local coboundary theorem.
2. Input to rooted-ball trivialization.
3. Input to local-type equality in the Newstein chain.
