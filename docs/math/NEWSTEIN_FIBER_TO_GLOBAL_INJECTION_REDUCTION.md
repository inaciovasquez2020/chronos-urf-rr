# Newstein Fiber-to-Global Injection Reduction

Status: OPEN

## Reduction statement
Assume the local coboundary criterion on every rooted ball \(B_R(r)\):
\[
\forall z \in Z_1(B_R(r);\mathbf F_2),\qquad
\exists c \in C_2(B_R(r);\mathbf F_2)\ \text{such that}\ \partial c = z.
\]

Let \([\gamma]\) be a nonzero class in a fiber quotient. If its image in the global quotient were zero, then \(\gamma\) would be a global boundary:
\[
\gamma = \partial C
\]
for some global \(2\)-chain \(C\).

Restricting \(C\) to the supporting rooted ball gives a local \(2\)-chain \(c\) with
\[
\partial c = \gamma.
\]
By the local coboundary criterion, this makes \([\gamma]\) zero already in the fiber quotient, a contradiction.

## Output
FiberToGlobalInjection is reduced to the local coboundary criterion plus restriction of global boundaries to the supporting rooted ball.
