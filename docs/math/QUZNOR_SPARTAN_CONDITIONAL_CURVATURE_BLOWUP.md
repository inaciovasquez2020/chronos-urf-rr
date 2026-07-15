# Spartan Theorem: Conditional Fixed-Fiber Curvature Blowup

## Status

**Conditional.**

This note packages an exact conditional implication. It does not prove
the profile-scale convergence, the endpoint-ratio limits, the
six-dimensional curvature identity, or control of higher-derivative
corrections.

The algebraic profile construction, fixed-charge identities, fixed
\(H_5\) multipoles, regularity threshold, and embeddedness estimate are
explicit.

## 1. Fixed parameters

Fix

\[
Q_5>0,
\qquad
L>0,
\qquad
M>0,
\qquad
M<E<2M.
\]

Define

\[
q=\frac{2\pi}{L}
\]

and

\[
Q_1=Q_5q^2E.
\]

Set

\[
N_{\mathrm{reg}}
=
\max
\left\{
2,
\left\lfloor
\sqrt{\frac{E}{2M-E}}
\right\rfloor+1
\right\}.
\]

For every integer \(N\ge N_{\mathrm{reg}}\), define

\[
x_N
=
\frac{N^2M-E}{N^2-1},
\qquad
y_N
=
\frac{E-M}{N^2-1},
\]

and

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

## 2. Exact fixed-fiber identities

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

Hence the trace-free second moment is

\[
Q(F_N)
=
\frac M4
\operatorname{diag}(1,1,-1,-1).
\]

Therefore the \(H_5\) multipoles through order \(r^{-4}\) are fixed:

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

The profile-speed energy is also fixed:

\[
\left\langle
|(F_N)_\theta|^2
\right\rangle
=
x_N+N^2y_N
=
E.
\]

Thus

\[
\boxed{
Q_1(F_N)
=
Q_5q^2E
=
Q_1
}
\]

for every \(N\).

## 3. Regularity and embeddedness

Write

\[
z_N(\theta)
=
\sqrt{x_N}e^{i\theta}
+
\sqrt{y_N}e^{iN\theta}.
\]

The threshold inequality

\[
N^2>\frac{E}{2M-E}
\]

is equivalent to

\[
x_N>N^2y_N.
\]

Indeed,

\[
x_N-N^2y_N
=
\frac{(2M-E)N^2-E}{N^2-1}.
\]

Therefore

\[
\sqrt{x_N}>N\sqrt{y_N}.
\]

The reverse triangle inequality gives

\[
|z_N'(\theta)|
\ge
\sqrt{x_N}-N\sqrt{y_N}
>0.
\]

For any \(\theta,\varphi\),

\[
|e^{iN\theta}-e^{iN\varphi}|
\le
N|e^{i\theta}-e^{i\varphi}|.
\]

Consequently,

\[
|z_N(\theta)-z_N(\varphi)|
\ge
\left(
\sqrt{x_N}-N\sqrt{y_N}
\right)
|e^{i\theta}-e^{i\varphi}|.
\]

If \(\theta\neq\varphi\) as points of \(S^1\), the right side is
strictly positive. Thus \(F_N\) is a smooth regular embedding for every

\[
N\ge N_{\mathrm{reg}}.
\]

## 4. Standard Lunin–Mathur fields

Assume the circle quantization

\[
R_y=\frac{2\pi Q_5}{L}.
\]

The associated two-charge fields are

\[
Z_{2,N}(x)
=
1+Q_5
\left\langle
\frac1{|x-F_N(\theta)|^2}
\right\rangle
\]

and

\[
Z_{1,N}(x)
=
1+Q_5q^2
\left\langle
\frac{|F_{N,\theta}(\theta)|^2}
{|x-F_N(\theta)|^2}
\right\rangle.
\]

The six-dimensional metric and scalar are written as

\[
ds_{6,N}^2
=
-\frac{2}{\sqrt{Z_{1,N}Z_{2,N}}}
(dv+\beta_N)(du+\omega_N)
+
\sqrt{Z_{1,N}Z_{2,N}}\,
dx\cdot dx
\]

and

\[
e^{2\sqrt2X_N}
=
\frac{Z_{1,N}}{Z_{2,N}}.
\]

The standard local Lunin–Mathur regularity argument is invoked only
under the already proved profile regularity, injectivity, and unit
KK-monopole quantization above.

## 5. Blow-up profile

Let

\[
p_N=F_N(0),
\qquad
\alpha=\sqrt M,
\qquad
b=\sqrt{E-M}.
\]

Define

\[
\Gamma(u)
=
i\alpha u+b(e^{iu}-1).
\]

For

\[
X\in\mathbb R^4\setminus\Gamma(\mathbb R),
\]

define

\[
h_5(X)
=
\frac{Q_5}{2\pi}
\int_{\mathbb R}
\frac{du}{|X-\Gamma(u)|^2}
\]

and

\[
h_1(X)
=
\frac{Q_5q^2}{2\pi}
\int_{\mathbb R}
\frac{|\Gamma'(u)|^2}
{|X-\Gamma(u)|^2}\,du.
\]

For

\[
X_R=(0,0,R,0),
\qquad
R>0,
\]

define

\[
I_0(R)
=
\int_{\mathbb R}
\frac{du}{|X_R-\Gamma(u)|^2}
\]

and

\[
I_1(R)
=
\int_{\mathbb R}
\frac{|\Gamma'(u)|^2}
{|X_R-\Gamma(u)|^2}\,du.
\]

Then

\[
\frac{h_1(X_R)}{h_5(X_R)}
=
q^2\frac{I_1(R)}{I_0(R)}.
\]

## 6. Analytic hypotheses

Assume the profile-scale convergence

\[
\frac{
Z_{i,N}(p_N+X/N)
}{N}
\longrightarrow
h_i(X)
\]

in \(C^1_{\mathrm{loc}}\) away from
\(\Gamma(\mathbb R)\), for \(i=1,2\).

Assume also the endpoint-ratio limits

\[
\lim_{R\downarrow0}
\frac{I_1(R)}{I_0(R)}
=
(\alpha+b)^2
\]

and

\[
\lim_{R\to\infty}
\frac{I_1(R)}{I_0(R)}
=
\alpha^2+b^2.
\]

Since

\[
(\alpha+b)^2-(\alpha^2+b^2)
=
2\alpha b
>0,
\]

the ratio \(I_1/I_0\) is not constant. Under its \(C^1\) regularity,
there exists \(R_0>0\) such that

\[
\nabla_X
\log\frac{h_1}{h_5}(X_{R_0})
\neq0.
\]

## 7. Curvature hypothesis

Assume the six-dimensional Einstein equation has the stated
one-tensor-multiplet normalization and that its three-form contribution
is trace-free, so that

\[
\operatorname{Scal}(g_N)
=
2|dX_N|_{g_N}^2
\]

and therefore

\[
\operatorname{Scal}(g_N)
=
\frac1{4\sqrt{Z_{1,N}Z_{2,N}}}
\left|
\nabla_{\mathbb R^4}
\log\frac{Z_{1,N}}{Z_{2,N}}
\right|^2.
\]

This identity is an explicit hypothesis of the theorem package; it is
not derived in this repository note.

## 8. Conditional curvature blowup

The \(C^1\) convergence implies

\[
\frac1N
\operatorname{Scal}(g_N)
\left(
p_N+\frac{X_{R_0}}N
\right)
\longrightarrow
c_0,
\]

where

\[
c_0
=
\frac1{4\sqrt{h_1(X_{R_0})h_5(X_{R_0})}}
\left|
\nabla_X
\log\frac{h_1}{h_5}(X_{R_0})
\right|^2.
\]

By construction,

\[
c_0>0.
\]

It follows that

\[
\operatorname{Scal}(g_N)
\left(
p_N+\frac{X_{R_0}}N
\right)
\longrightarrow+\infty.
\]

Since the supremum dominates this sample value,

\[
\boxed{
\sup_x
\operatorname{Scal}(g_N)(x)
\longrightarrow+\infty
}.
\]

At the same time,

\[
\boxed{
(\mathsf S_2,\mathsf S_3,\mathsf S_4,Q_1,Q_5)
}
\]

is independent of \(N\).

## 9. Spartan Theorem

**Conditional.** Under the profile-scale convergence, endpoint-ratio,
Einstein-equation normalization, and scalar-curvature identity stated
above, there exists a sequence of smooth regular embedded once-wound
Lunin–Mathur profiles with fixed

\[
(\mathsf S_2,\mathsf S_3,\mathsf S_4,Q_1,Q_5)
\]

whose associated six-dimensional scalar-curvature suprema diverge:

\[
\boxed{
\sup_x
\operatorname{Scal}(g_N)(x)
\to+\infty
}.
\]

## Source boundary

The standard profile harmonic functions, charge formula, local
regularity mechanism, unit quantization condition, and
non-self-intersection condition are described in:

O. Lunin, J. Maldacena, and L. Maoz,
“Gravity solutions for the D1-D5 system with angular momentum,”
arXiv:hep-th/0212210.

This repository note does not claim that the cited paper proves the
new profile-scale convergence or endpoint-ratio assumptions used here.

## Boundary and stopping rule

\[
\texttt{BOUNDARY}
:=
\neg\,
\text{profile-scale convergence proved}.
\]

\[
\texttt{BOUNDARY}
:=
\neg\,
\text{endpoint-ratio limits independently audited}.
\]

\[
\texttt{BOUNDARY}
:=
\neg\,
\text{curvature normalization independently formalized}.
\]

\[
\texttt{BOUNDARY}
:=
\neg\,
\text{string-scale or higher-derivative corrections controlled}.
\]

\[
\texttt{BOUNDARY}
:=
\neg\,
\text{unconditional curvature-blowup theorem}.
\]

\[
\texttt{STOP\_BRANCH}
:=
\texttt{true}.
\]
