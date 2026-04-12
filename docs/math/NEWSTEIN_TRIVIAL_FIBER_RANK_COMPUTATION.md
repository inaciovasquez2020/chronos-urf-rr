# Newstein Trivial Fiber Rank Computation

## Target statement

For the trivial double cover,
\[
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T^{\mathrm{triv}})/W^{\mathrm{triv}}\bigr)=4.
\]

## Inputs

### 1. Quotient-homology identification

Assume
\[
Z_1(\widetilde T^{\mathrm{triv}})/W^{\mathrm{triv}}
\cong
H_1(\widetilde T^{\mathrm{triv}};\mathbb F_2).
\]

### 2. Trivial-cover decomposition

Prove
\[
\widetilde T^{\mathrm{triv}} \cong T \sqcup T.
\]

## Required subclaims

### 1. Homology of one torus

For a single torus \(T\),
\[
\dim_{\mathbb F_2} H_1(T;\mathbb F_2)=2.
\]

### 2. Homology of a disjoint union

For disjoint components,
\[
H_1(T \sqcup T;\mathbb F_2)\cong H_1(T;\mathbb F_2)\oplus H_1(T;\mathbb F_2).
\]

### 3. Dimension count

Therefore
\[
\dim_{\mathbb F_2} H_1(\widetilde T^{\mathrm{triv}};\mathbb F_2)=2+2=4.
\]

## Deduction

By quotient-homology identification,
\[
Z_1(\widetilde T^{\mathrm{triv}})/W^{\mathrm{triv}}
\cong
H_1(\widetilde T^{\mathrm{triv}};\mathbb F_2).
\]

By trivial-cover decomposition and the direct-sum homology computation,
\[
\dim_{\mathbb F_2} H_1(\widetilde T^{\mathrm{triv}};\mathbb F_2)=4.
\]

Hence
\[
\dim_{\mathbb F_2}\!\bigl(Z_1(\widetilde T^{\mathrm{triv}})/W^{\mathrm{triv}}\bigr)=4.
\]

## Status

This is the first numerical rank computation in the Newstein fiber branch.

## Dependencies discharged by this theorem

1. One half of the \(4\) versus \(2\) fiber-rank gap.
2. Input to the fiber rank-gap theorem.
3. Input to the global quotient-gap assembly.
