# Unbounded Mu2 on a Fixed Charge-and-H5-Multipole Fiber

## Status

**Selected field:** \(H_5=Z_2\).

**Theorem:** the second-derivative Fourier energy \(\mu_2\) is unbounded
above on one fixed fiber of

\[
(\mathsf S_2,\mathsf S_3,\mathsf S_4,Q_1,Q_5).
\]

This strengthens the finite two-profile collision recorded in

`docs/math/QUZNOR_H5_MULTIPOLE_FIBER_COLLISION.md`.

**Novelty status:** explicit regular embedded D1–D5 profile realization
of the classical failure of \(H^1\) data to control \(H^2\) energy. The
core mechanism is classical Fourier and Sobolev non-control.

**Boundary:** this is not a new general mathematical principle. No full
supergravity smoothness or orbifold-free microstate theorem is claimed.

## 1. D1–D5 profile fields

For a closed two-charge Lunin–Mathur profile

\[
F:[0,L]\to\mathbb R^4,
\]

the positional harmonic field is

\[
H_5(x)
=
1+\frac{Q_5}{L}
\int_0^L
\frac{dv}{|x-F(v)|^2}.
\]

Set

\[
\theta=\frac{2\pi v}{L},
\qquad
\langle h\rangle
=
\frac1{2\pi}\int_0^{2\pi}h(\theta)\,d\theta.
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

In the normalization used here, the D1 charge is

\[
Q_1
=
Q_5\left(\frac{2\pi}{L}\right)^2
\left\langle|F_\theta|^2\right\rangle.
\]

## 2. Fixed parameters

Fix

\[
Q_5>0,
\qquad
L>0,
\]

and real numbers

\[
M>0,
\qquad
M<E<2M.
\]

For every integer \(N\ge2\), define

\[
y_N
=
\frac{E-M}{N^2-1},
\qquad
x_N
=
\frac{N^2M-E}{N^2-1}.
\]

Because \(M<E\) and \(N^2M>E\), both coefficients are positive.

Define

\[
F_N(\theta)
=
\begin{pmatrix}
\sqrt{x_N}\cos\theta+\sqrt{y_N}\cos N\theta\\
\sqrt{x_N}\sin\theta+\sqrt{y_N}\sin N\theta\\
0\\
0
\end{pmatrix}.
\]

Equivalently, in complex notation,

\[
z_N(\theta)
=
\sqrt{x_N}e^{i\theta}
+
\sqrt{y_N}e^{iN\theta}.
\]

## 3. Fixed positional moments

Direct algebra gives

\[
x_N+y_N=M
\]

and

\[
x_N+N^2y_N=E.
\]

Every profile is centered:

\[
\langle F_N\rangle=0.
\]

Fourier orthogonality gives

\[
\left\langle
(F_N)_i(F_N)_j
\right\rangle
=
\operatorname{diag}
\left(
\frac M2,\frac M2,0,0
\right)_{ij}.
\]

Thus the second-moment tensor is independent of \(N\).

Let

\[
C_{ij}(F)
=
\langle F_iF_j\rangle
\]

and

\[
Q_{ij}(F)
=
C_{ij}(F)
-\frac14\delta_{ij}\operatorname{tr}C(F).
\]

For every \(N\),

\[
Q(F_N)
=
\frac M4
\operatorname{diag}(1,1,-1,-1).
\]

Consequently, the \(H_5\) multipole data through order \(r^{-4}\) are
independent of \(N\):

\[
\boxed{\mathsf S_2(F_N)=Q_5},
\]

\[
\boxed{\mathsf S_3(F_N)=0},
\]

and

\[
\boxed{
\mathsf S_4(F_N)
=
Q_5M\,
\operatorname{diag}(1,1,-1,-1)
}.
\]

## 4. Fixed D1 charge

Differentiating the profile and using Fourier orthogonality gives

\[
\left\langle
|(F_N)_\theta|^2
\right\rangle
=
x_N+N^2y_N
=
E.
\]

Therefore all profiles have the same D1 charge:

\[
\boxed{
Q_1
=
Q_5
\left(\frac{2\pi}{L}\right)^2E
}.
\]

Hence the complete data

\[
(\mathsf S_2,\mathsf S_3,\mathsf S_4,Q_1,Q_5)
\]

are fixed throughout the family.

## 5. Exact growth of the second-derivative energy

Define

\[
\mu_2(F)
=
\left\langle
|F_{\theta\theta}|^2
\right\rangle.
\]

For \(F_N\),

\[
\mu_2(F_N)
=
x_N+N^4y_N.
\]

Substituting the definitions of \(x_N\) and \(y_N\) gives

\[
\begin{aligned}
\mu_2(F_N)
&=
\frac{N^2M-E+N^4(E-M)}{N^2-1}\\
&=
E+(E-M)N^2.
\end{aligned}
\]

Therefore

\[
\boxed{
\mu_2(F_N)
=
E+(E-M)N^2
}.
\]

Since \(E-M>0\),

\[
\boxed{
\mu_2(F_N)\longrightarrow+\infty
\qquad
(N\to\infty)
}.
\]

## 6. Explicit regularity threshold

The derivative satisfies

\[
z_N'(\theta)
=
i\sqrt{x_N}e^{i\theta}
+
iN\sqrt{y_N}e^{iN\theta}.
\]

The reverse triangle inequality gives

\[
|z_N'(\theta)|
\ge
\sqrt{x_N}-N\sqrt{y_N}.
\]

The strict inequality

\[
\sqrt{x_N}>N\sqrt{y_N}
\]

is equivalent to

\[
x_N>N^2y_N.
\]

Exact substitution gives

\[
x_N-N^2y_N
=
\frac{(2M-E)N^2-E}{N^2-1}.
\]

Thus regularity holds whenever

\[
(2M-E)N^2>E,
\]

or equivalently,

\[
N^2>\frac{E}{2M-E}.
\]

Since \(E<2M\), all sufficiently large \(N\) satisfy this condition.

One explicit threshold is

\[
N_0
=
\max
\left\{
2,
\left\lfloor
\sqrt{\frac{E}{2M-E}}
\right\rfloor+1
\right\}.
\]

For every \(N\ge N_0\),

\[
|z_N'(\theta)|>0
\]

for every \(\theta\).

## 7. Embeddedness

For \(\theta,\varphi\in S^1\),

\[
z_N(\theta)-z_N(\varphi)
=
\sqrt{x_N}
\left(e^{i\theta}-e^{i\varphi}\right)
+
\sqrt{y_N}
\left(e^{iN\theta}-e^{iN\varphi}\right).
\]

Using

\[
u^N-v^N
=
(u-v)
\sum_{k=0}^{N-1}u^{N-1-k}v^k
\]

with \(|u|=|v|=1\), one obtains

\[
|e^{iN\theta}-e^{iN\varphi}|
\le
N|e^{i\theta}-e^{i\varphi}|.
\]

Therefore

\[
\begin{aligned}
|z_N(\theta)-z_N(\varphi)|
&\ge
\sqrt{x_N}
|e^{i\theta}-e^{i\varphi}|\\
&\quad-
\sqrt{y_N}
|e^{iN\theta}-e^{iN\varphi}|\\
&\ge
\left(
\sqrt{x_N}-N\sqrt{y_N}
\right)
|e^{i\theta}-e^{i\varphi}|.
\end{aligned}
\]

For \(N\ge N_0\), the first factor is strictly positive. If
\(\theta\neq\varphi\) as points of \(S^1\), then

\[
|e^{i\theta}-e^{i\varphi}|>0.
\]

Hence

\[
|z_N(\theta)-z_N(\varphi)|>0.
\]

Thus every \(F_N\) with \(N\ge N_0\) is a smooth regular embedded
profile.

## 8. Sharp obstruction theorem

For every \(N\ge N_0\), the profile \(F_N\) is smooth, regular, and
embedded, and all profiles lie in the same fixed fiber of

\[
(\mathsf S_2,\mathsf S_3,\mathsf S_4,Q_1,Q_5).
\]

Nevertheless,

\[
\mu_2(F_N)
=
E+(E-M)N^2
\longrightarrow+\infty.
\]

Therefore:

\[
\boxed{
\mu_2
\text{ is unbounded above on one fixed charge-and-}
H_5
\text{-multipole fiber}
}.
\]

In particular, there is no recovery function

\[
\Psi
\]

such that

\[
\mu_2(F)
=
\Psi(
\mathsf S_2(F),
\mathsf S_3(F),
\mathsf S_4(F),
Q_1(F),
Q_5(F)
)
\]

on any profile class containing this family.

More strongly, there is no finite-valued upper-bound function

\[
B(
\mathsf S_2,
\mathsf S_3,
\mathsf S_4,
Q_1,
Q_5
)
\]

satisfying

\[
\mu_2(F)
\le
B(
\mathsf S_2(F),
\mathsf S_3(F),
\mathsf S_4(F),
Q_1(F),
Q_5(F)
)
\]

on such a class.

## Boundary and stopping rule

\[
\texttt{NOVELTY\_STATUS}
:=
\text{explicit embedded profile realization of classical }
H^1\not\Rightarrow H^2
\text{ control}.
\]

\[
\texttt{BOUNDARY}
:=
\neg\,
\text{new general mathematical principle}.
\]

\[
\texttt{BOUNDARY}
:=
\neg\,
\text{globally smooth, orbifold-free supergravity geometry proved}.
\]

\[
\texttt{STOP\_BRANCH}
:=
\texttt{true}.
\]

No further finite-mode collision should be added on this branch.
