# Quznor H5 Multipole Fiber Collision

## Status

**Selected field:** \(H_5=Z_2\).

**Result:** the second-derivative Fourier energy \(\mu_2\) is not
constant on the fibers of the charge-preserving \(H_5\) multipole map
through order \(r^{-4}\).

**Novelty status:** explicit Fourier collision derived from the
classical D1–D5 harmonic-profile formula. The proof reduces to finite
moment algebra and is not plausibly new mathematics.

**Boundary:** regularity of the profiles is proved, but embeddedness and
the existence of globally smooth, orbifold-free microstate geometries
are not proved.

## 1. Selected D1–D5 field

For a closed profile

\[
F:[0,L]\to\mathbb R^4,
\]

the two-charge harmonic field is

\[
H_5(x)
=
1+\frac{Q_5}{L}
\int_0^L
\frac{dv}{|x-F(v)|^2}.
\]

The companion field \(Z_1\) contains the weight \(|F'(v)|^2\). Thus
\(H_5\) is the cleaner field for isolating positional moments of the
profile.

Set

\[
\theta=\frac{2\pi v}{L},
\qquad
\langle h\rangle
=
\frac1{2\pi}
\int_0^{2\pi}h(\theta)\,d\theta.
\]

Then

\[
H_5(x)
=
1+Q_5
\left\langle
\frac1{|x-F(\theta)|^2}
\right\rangle.
\]

## 2. Charge-preserving regular profile stratum

Fix

\[
L>0,\qquad Q_1>0,\qquad Q_5>0,\qquad \rho>0.
\]

Define

\[
\mathcal A(Q_1,Q_5,\rho)
=
\left\{
F\in C^2_{\mathrm{per}}(S^1,\mathbb R^4):
\begin{array}{l}
\langle F\rangle=0,\\
F_\theta(\theta)\neq0\text{ for every }\theta,\\
\|F\|_\infty\le\rho,\\
Q_5\left(\frac{2\pi}{L}\right)^2
\langle|F_\theta|^2\rangle=Q_1
\end{array}
\right\}.
\]

The last condition fixes the leading \(r^{-2}\) coefficient of \(Z_1\),
and hence fixes the D1 charge while \(Q_5\) is held fixed.

## 3. Exact multipole data

Define the first and second moments

\[
M_i(F)=\langle F_i\rangle,
\qquad
C_{ij}(F)=\langle F_iF_j\rangle.
\]

Define the trace-free second moment

\[
Q_{ij}(F)
=
C_{ij}(F)
-\frac14\delta_{ij}\operatorname{tr}C(F).
\]

The radial expansion identifies

\[
\boxed{\mathsf S_2(F)=Q_5},
\]

\[
\boxed{\mathsf S_{3,i}(F)=2Q_5M_i(F)},
\]

and

\[
\boxed{\mathsf S_{4,ij}(F)=4Q_5Q_{ij}(F)}.
\]

On the centered stratum,

\[
\mathsf S_3(F)=0.
\]

The first profile-dependent coefficient is therefore the trace-free
quadrupolar \(r^{-4}\) coefficient.

## 4. Far-field expansion and controlled remainder

Let

\[
x=rn,\qquad |n|=1,
\]

and set

\[
a(\theta)=n\cdot F(\theta),
\qquad
b(\theta)=|F(\theta)|^2.
\]

Then

\[
|rn-F|^2
=
r^2-2ra+b
=
r^2(1-q),
\]

where

\[
q=\frac{2a}{r}-\frac{b}{r^2}.
\]

Using

\[
\frac1{1-q}
=
1+q+q^2+\frac{q^3}{1-q},
\]

one obtains

\[
\frac1{|rn-F|^2}
=
\frac1{r^2}
+\frac{2a}{r^3}
+\frac{4a^2-b}{r^4}
+R(\theta,r),
\]

with the exact remainder representation

\[
R(\theta,r)
=
-\frac{4ab}{r^5}
+\frac{b^2}{r^6}
+\frac{q^3}{r^2(1-q)}.
\]

Assume

\[
r\ge4\rho.
\]

Since

\[
|a|\le\rho,
\qquad
0\le b\le\rho^2,
\]

we have

\[
|q|
\le
2\frac{\rho}{r}
+\frac{\rho^2}{r^2}
\le
\frac9{16}.
\]

Also,

\[
|q|
\le
\frac94\frac{\rho}{r}.
\]

Therefore

\[
\left|
-\frac{4ab}{r^5}
\right|
\le
4\frac{\rho^3}{r^5},
\]

\[
\frac{b^2}{r^6}
\le
\frac14\frac{\rho^3}{r^5},
\]

and

\[
\left|
\frac{q^3}{r^2(1-q)}
\right|
\le
\frac{729}{28}
\frac{\rho^3}{r^5}.
\]

Adding the three bounds gives

\[
4+\frac14+\frac{729}{28}
=
\frac{212}{7}.
\]

Hence

\[
\boxed{
|R(\theta,r)|
\le
\frac{212}{7}
\frac{\rho^3}{r^5}
}.
\]

After averaging,

\[
\boxed{
H_5(rn)
=
1
+\frac{\mathsf S_2}{r^2}
+\frac{n^i\mathsf S_{3,i}}{r^3}
+\frac{n^in^j\mathsf S_{4,ij}}{r^4}
+\mathcal R_5(r,n)
}
\]

with

\[
\boxed{
|\mathcal R_5(r,n)|
\le
\frac{212}{7}
\frac{Q_5\rho^3}{r^5}
}.
\]

On the centered stratum, the \(r^{-4}\) angular coefficient is

\[
\boxed{
a_4(n;F)
=
n^in^j\mathsf S_{4,ij}(F)
=
Q_5
\left\langle
4(n\cdot F)^2-|F|^2
\right\rangle
}.
\]

## 5. Explicit charge-preserving fiber collision

Set

\[
a
=
\frac{L}{2\pi}
\sqrt{\frac{Q_1}{108Q_5}}.
\]

Assume

\[
\rho
\ge
a(\sqrt7+\sqrt5).
\]

Define

\[
F(\theta)
=
a
\begin{pmatrix}
\sqrt7\cos2\theta+\sqrt5\cos4\theta\\
\sqrt7\sin2\theta+\sqrt5\sin4\theta\\
0\\
0
\end{pmatrix}
\]

and

\[
G(\theta)
=
a
\begin{pmatrix}
\sqrt{12}\cos3\theta\\
\sqrt{12}\sin3\theta\\
0\\
0
\end{pmatrix}.
\]

Both profiles are centered.

For \(F\), the reverse triangle inequality gives

\[
|F_\theta|
\ge
a(4\sqrt5-2\sqrt7)>0.
\]

For \(G\),

\[
|G_\theta|
=
3\sqrt{12}\,a>0.
\]

Thus both profiles are regular.

Their sup norms satisfy

\[
\|F\|_\infty
\le
a(\sqrt7+\sqrt5)
\le\rho
\]

and

\[
\|G\|_\infty
=
a\sqrt{12}
<
a(\sqrt7+\sqrt5)
\le\rho.
\]

Therefore the radius constraint is satisfied.

## 6. Equal moments and equal charges

Fourier orthogonality gives

\[
C(F)=C(G)
=
\operatorname{diag}(6a^2,6a^2,0,0).
\]

Consequently,

\[
\mathsf S_2(F)=\mathsf S_2(G)=Q_5,
\]

\[
\mathsf S_3(F)=\mathsf S_3(G)=0,
\]

and

\[
\boxed{\mathsf S_4(F)=\mathsf S_4(G)}.
\]

The first-derivative energies are

\[
\langle|F_\theta|^2\rangle
=
7\cdot2^2a^2+5\cdot4^2a^2
=
108a^2
\]

and

\[
\langle|G_\theta|^2\rangle
=
12\cdot3^2a^2
=
108a^2.
\]

By the definition of \(a\),

\[
Q_5
\left(\frac{2\pi}{L}\right)^2
108a^2
=
Q_1.
\]

Thus

\[
F,G\in\mathcal A(Q_1,Q_5,\rho)
\]

and they lie in the same fixed-\((Q_1,Q_5)\) charge fiber.

## 7. Unequal second-derivative Fourier energy

Define

\[
\boxed{
\mu_2(F)
=
\left\langle
|F_{\theta\theta}|^2
\right\rangle
}.
\]

For the first profile,

\[
\mu_2(F)
=
7\cdot2^4a^2+5\cdot4^4a^2
=
1392a^2.
\]

For the second profile,

\[
\mu_2(G)
=
12\cdot3^4a^2
=
972a^2.
\]

Therefore

\[
\boxed{
\mu_2(F)-\mu_2(G)
=
420a^2
\neq0
}.
\]

## 8. Fiber non-recovery theorem

The two regular profiles satisfy

\[
\boxed{
(\mathsf S_2,\mathsf S_3,\mathsf S_4)(F)
=
(\mathsf S_2,\mathsf S_3,\mathsf S_4)(G)
}
\]

and

\[
\boxed{
Q_1(F)=Q_1(G),
\qquad
Q_5(F)=Q_5(G)
}
\]

but

\[
\boxed{\mu_2(F)\neq\mu_2(G)}.
\]

Hence \(\mu_2\) is not constant on the fibers of the charge-preserving
\(H_5\) multipole map.

In particular, no function

\[
\Psi
\]

can satisfy

\[
\mu_2
=
\Psi(\mathsf S_2,\mathsf S_3,\mathsf S_4,Q_1,Q_5)
\]

on any profile class containing both \(F\) and \(G\).

## Boundary and stopping rule

\[
\texttt{BOUNDARY}
:=
\neg\,
\text{embeddedness of the two profiles proved}.
\]

\[
\texttt{BOUNDARY}
:=
\neg\,
\text{globally smooth, orbifold-free microstate geometries proved}.
\]

\[
\texttt{STOP\_BRANCH}
:=
\texttt{true}.
\]

The collision is fully explained by finite Fourier moment algebra, so no
further mathematical expansion is warranted on this branch.
