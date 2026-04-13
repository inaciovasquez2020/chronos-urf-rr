# Newstein Local Coboundary Criterion Reduction

Status: PROVED

## Reduction statement
Assume RootedBallTrivialization:
\[
\forall z \in Z_1(B_R(r);\mathbf F_2),\qquad
\exists c \in C_2(B_R(r);\mathbf F_2)\ \text{such that}\ \partial c = z.
\]

Then the local coboundary criterion holds on \(B_R(r)\).

## Proof
Let \(z \in Z_1(B_R(r);\mathbf F_2)\) be any \(1\)-cycle.
By RootedBallTrivialization, there exists \(c \in C_2(B_R(r);\mathbf F_2)\) such that
\[
\partial c = z.
\]
Therefore every local \(1\)-cycle is a local boundary.

## Output
LocalCoboundaryCriterion is reduced to RootedBallTrivialization.

## Proof status
Proved from RootedBallTrivialization.

