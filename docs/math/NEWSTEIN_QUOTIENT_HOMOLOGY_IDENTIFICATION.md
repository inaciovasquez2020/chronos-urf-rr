# Newstein Quotient-Homology Identification

## Target statement

For each lifted torus fiber \(\widetilde T\),
\[
Z_1(\widetilde T)/W \cong H_1(\widetilde T;\mathbb F_2),
\]
where \(W\) is the \(\mathbb F_2\)-span of lifted triangle boundaries in \(\widetilde T\).

## Definitions

### 1. Cycle space
\[
Z_1(\widetilde T):=\ker(\partial_1:C_1(\widetilde T;\mathbb F_2)\to C_0(\widetilde T;\mathbb F_2)).
\]

### 2. Triangle-boundary span
\[
W:=\left\langle \partial \tau : \tau \subseteq \widetilde T\ \text{a lifted triangle}\right\rangle_{\mathbb F_2}.
\]

### 3. First homology
\[
H_1(\widetilde T;\mathbb F_2):=Z_1(\widetilde T)/B_1(\widetilde T),
\]
where
\[
B_1(\widetilde T):=\operatorname{im}(\partial_2:C_2(\widetilde T;\mathbb F_2)\to C_1(\widetilde T;\mathbb F_2)).
\]

## Required subclaims

### 1. Boundary inclusion
Prove
\[
W \subseteq B_1(\widetilde T).
\]

### 2. Reverse inclusion
Prove every \(2\)-boundary in the lifted torus fiber is an \(\mathbb F_2\)-sum of lifted triangle boundaries, hence
\[
B_1(\widetilde T)\subseteq W.
\]

### 3. Equality of boundary spaces
Conclude
\[
W=B_1(\widetilde T).
\]

## Deduction

By the definition of homology,
\[
H_1(\widetilde T;\mathbb F_2)=Z_1(\widetilde T)/B_1(\widetilde T).
\]

By boundary-space equality,
\[
B_1(\widetilde T)=W.
\]

Hence
\[
Z_1(\widetilde T)/W \cong H_1(\widetilde T;\mathbb F_2).
\]

## Status

This is the first theorem-level target in the fiber quotient-rank branch.

## Dependencies discharged by this theorem

1. Input to the trivial fiber rank computation.
2. Input to the twisted fiber rank computation.
3. Entry point for the \(4\) versus \(2\) fiber-rank gap.
