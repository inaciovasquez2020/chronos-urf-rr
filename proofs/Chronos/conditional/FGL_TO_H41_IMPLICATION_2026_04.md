# FGL to finite-patch H4.1

## Status
Conditional.

For fixed \(k,R,B\), define
\[
U_{k,R,B}:=W_{k,R,B}\oplus \langle 1\rangle.
\]

Assume
\[
\mathrm{FGL}(k,R,B):
\qquad
V_{k,R,B}\cap U_{k,R,B}^{\perp}=\{0\}.
\]

Then
\[
V_{k,R,B}\subseteq U_{k,R,B}=W_{k,R,B}\oplus \langle 1\rangle.
\]

### Proof
Since \(X(\mathcal P_{k,R,B})\) is finite,
\[
\mathbb R^{X(\mathcal P_{k,R,B})}=U_{k,R,B}\oplus U_{k,R,B}^{\perp}.
\]
Hence every \(v\in V_{k,R,B}\) admits a decomposition
\[
v=u+u^{\perp},
\qquad
u\in U_{k,R,B},
\quad
u^{\perp}\in U_{k,R,B}^{\perp}.
\]
Because \(V_{k,R,B}\) is a linear subspace,
\[
u^{\perp}=v-u\in V_{k,R,B}.
\]
Thus
\[
u^{\perp}\in V_{k,R,B}\cap U_{k,R,B}^{\perp}.
\]
By \(\mathrm{FGL}(k,R,B)\),
\[
u^{\perp}=0.
\]
Therefore
\[
v=u\in U_{k,R,B}.
\]
So
\[
V_{k,R,B}\subseteq W_{k,R,B}\oplus \langle 1\rangle.
\]
\(\square\)

## Quotient consequence
If \(h\in V_{k,R,B}\) and
\[
\langle h,1\rangle=0,
\]
then after quotienting out the constant mode,
\[
h\in W_{k,R,B}.
\]

## Finite-patch H4.1
For all \(f,g\in V_{k,R,B}\),
\[
f\neq g,
\qquad
\langle f-g,1\rangle=0
\quad\Longrightarrow\quad
f-g\in W_{k,R,B}.
\]

Hence every nontrivial zero-mean FO\(^k\)-visible local difference induces a bounded-support dual dependency.
