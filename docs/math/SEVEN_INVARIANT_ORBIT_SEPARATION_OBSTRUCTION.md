# Seven-Invariant Orbit-Separation Obstruction

## Status

**Novelty status:** specialized application of classical invariance of
domain; not plausibly new mathematics.

**Boundary:** seven continuous real invariants cannot separate the free
open quotient described below.

**Formalization status:** documentation theorem only. No Lean
formalization is claimed.

## Permitted profile reparameterizations

Let

\[
K_4=(\mathbb C^2)^3
\]

with coordinates

\[
c=((A_2,B_2),(A_3,B_3),(A_4,B_4)).
\]

The permitted group is

\[
T^2=S^1_{\mathrm{frame}}\times S^1_{\mathrm{shift}}.
\]

It acts by

\[
(\alpha,\beta)\cdot A_n
=
e^{i(\alpha+n\beta)}A_n,
\qquad
(\alpha,\beta)\cdot B_n
=
e^{i(\alpha-n\beta)}B_n.
\]

Orientation reversal is excluded. Allowing profile reversal would enlarge
the group to a finite extension \(T^2\rtimes\mathbb Z_2\), but would not
remove the dimension obstruction proved below.

## Nonempty free stratum

Define

\[
U_{\mathrm{free}}
=
\left\{
c\in(\mathbb C^2)^3:
A_2B_2A_3\neq0
\right\}.
\]

This set is open, nonempty, and \(T^2\)-invariant.

If \((\alpha,\beta)\) stabilizes a point of \(U_{\mathrm{free}}\), then

\[
\alpha+2\beta\equiv0,
\qquad
\alpha-2\beta\equiv0,
\qquad
\alpha+3\beta\equiv0
\pmod{2\pi}.
\]

Subtracting the first congruence from the third gives

\[
\beta\equiv0\pmod{2\pi}.
\]

The first congruence then gives

\[
\alpha\equiv0\pmod{2\pi}.
\]

Therefore the action is free on \(U_{\mathrm{free}}\).

## Theorem

Let

\[
U\subset(\mathbb C^2)^3\cong\mathbb R^{12}
\]

be a nonempty \(T^2\)-invariant open set on which the preceding action is
free. Then no continuous \(T^2\)-invariant map

\[
I:U\to\mathbb R^7
\]

separates all \(T^2\)-orbits.

Equivalently,

\[
\forall I:U\to\mathbb R^7
\text{ continuous and \(T^2\)-invariant},
\]

there exist \(c,c'\in U\) such that

\[
I(c)=I(c')
\]

but

\[
T^2\cdot c\neq T^2\cdot c'.
\]

## Proof

Because \(T^2\) is compact, its free action on \(U\) is proper. Therefore

\[
M:=U/T^2
\]

is a smooth manifold of real dimension

\[
\dim_{\mathbb R}M=12-2=10.
\]

Suppose that \(I\) separates all orbits. Since \(I\) is invariant, it
factors through the quotient and induces a continuous injection

\[
\bar I:M\hookrightarrow\mathbb R^7.
\]

Choose a quotient chart \(V\subset M\) homeomorphic to a nonempty open
set

\[
W\subset\mathbb R^{10}.
\]

Restricting \(\bar I\) to this chart gives a continuous injection

\[
f:W\to\mathbb R^7.
\]

Define

\[
g:W\to\mathbb R^{10},
\qquad
g(x)=(f(x),0,0,0).
\]

The map \(g\) is continuous and injective. By invariance of domain,
\(g(W)\) must be open in \(\mathbb R^{10}\). However,

\[
g(W)\subset\mathbb R^7\times\{0\}^3,
\]

and this subspace has empty interior in \(\mathbb R^{10}\). This is a
contradiction.

Therefore no such seven-observable orbit-separating map exists.

## Consequence

Any continuous collection of seven real quotient-invariant spectral
observables fails to classify every orbit on a nonempty free open
stratum.

Orbit separation can only be sought after at least one of the following
changes:

1. use at least ten local real observables;
2. impose at least three independent invariant constraints;
3. restrict to a lower-dimensional non-open stratum.

This obstruction is topological and occurs before any Vandermonde
inversion is relevant.
