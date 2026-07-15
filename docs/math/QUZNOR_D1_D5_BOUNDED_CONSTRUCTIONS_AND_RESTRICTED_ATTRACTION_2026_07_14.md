RESULT := four bounded constructions are proved. One requested identification is only partial: the seven spectral invariants are functions of asymptotic multipole data, but they are not individually equal to seven low-order asymptotic coefficients.

## ASYMPTOTIC_SPECTRAL_RELATION :=

Write

[
z(\theta)=F_3(\theta)+iF_4(\theta)
=\sum_{n=2}^{4}\left(A_ne^{in\theta}+B_ne^{-in\theta}\right),
]

and set

[
S_n=|A_n|^2+|B_n|^2,\qquad
C_n=A_nB_n,
]

[
P_n=|C_n|^2,\qquad
C_{23}^{\mathrm{inv}}=\operatorname{Re}(C_2\overline{C_3}).
]

For (r>|F|), the four-dimensional Green kernel has the convergent expansion

[
\frac1{|x-F|^2}
===============

\frac1{r^2}
\sum_{\ell=0}^{\infty}
\frac{|F|^\ell}{r^\ell}
C_\ell^{1}!\left(\widehat x\cdot\widehat F\right).
]

Hence

[
H_{5,c}(r,\widehat x)
=====================

1+
\frac{Q_5}{r^2}
\sum_{\ell=0}^{\infty}
\frac{\mathcal H_{\ell,c}(\widehat x)}{r^\ell},
]

where

[
\mathcal H_{\ell,c}(\widehat x)
===============================

\frac1{2\pi}
\int_0^{2\pi}
|F_c(\theta)|^\ell
C_\ell^1!\left(\widehat x\cdot\widehat F_c(\theta)\right)d\theta .
]

The D1–D5 fields are determined by the profile integrals (H_1,H_5,A), and their leading large-distance corrections are profile moments such as (\langle\dot F_iF_j\rangle). 

For the quadrupole,

[
\mathcal H_{2,c}(\widehat x)
============================

4\widehat x_i\widehat x_j
\left\langle F_iF_j\right\rangle
--------------------------------

\left\langle|F|^2\right\rangle.
]

The exact transverse second-moment identities are

[
\left\langle |z|^2\right\rangle
===============================

S_2+S_3+S_4,
]

[
\left\langle z^2\right\rangle
=============================

2(C_2+C_3+C_4),
]

and

[
\left\langle|z'|^2\right\rangle
===============================

4S_2+9S_3+16S_4.
]

Thus the (H_5) quadrupole contains the combinations

[
\mu_0:=S_2+S_3+S_4
]

and

[
C_2+C_3+C_4,
]

rather than the six quantities (S_n,P_n) separately.

The squared transverse quadrupole contains

[
\frac14\left|\left\langle z^2\right\rangle\right|^2
===================================================

|C_2+C_3+C_4|^2
]

# [

P_2+P_3+P_4
+
2\operatorname{Re}
\left(
C_2\overline{C_3}
+C_2\overline{C_4}
+C_3\overline{C_4}
\right).
]

Therefore (C_{23}^{\mathrm{inv}}) occurs in the asymptotic quadrupole norm, but it is mixed with two other cross terms.

The leading asymptotic one-form coefficient is

[
A_i(x)
======

-2Q_5\widehat f_{ij}\frac{x_j}{r^4}
+O(r^{-4}),
\qquad
\widehat f_{ij}
===============

\frac1L\int_0^L\dot F_iF_j,dv.
]

In the transverse plane,

[
\widehat f_{34}
===============

-\frac{\omega}{2}
\sum_{n=2}^{4}
n\left(|A_n|^2-|B_n|^2\right).
]

This is an additional weighted spectral combination visible at leading current-multipole order. The same profile-moment structure appears explicitly in the known D1–D5 asymptotic expansion. 

If the three weighted moments

[
\mu_k=\sum_{n=2}^{4}n^{2k}S_n,
\qquad k=0,1,2,
]

are known, then the individual (S_n) are recovered by the Vandermonde inversion

[
S_2
===

\frac{12}{5}\mu_0
-\frac5{12}\mu_1
+\frac1{60}\mu_2,
]

[
S_3
===

-\frac{64}{35}\mu_0
+\frac47\mu_1
-\frac1{35}\mu_2,
]

[
S_4
===

\frac37\mu_0
-\frac{13}{84}\mu_1
+\frac1{84}\mu_2.
]

However,

[
\mu_2=\left\langle|z''|^2\right\rangle
]

has not been identified with a single standard low-order coefficient of (H_1,H_5,A,B).

[
\mathrm{BOUNDARY}
:=
\neg,
\text{the seven spectral invariants are seven independently isolated finite-order asymptotic coefficients}.
]

They are rigorously encoded in the complete asymptotic moment sequence; finite low-order inversion remains unproved.

---

## FULL_FIXED_GAUGE_WAVE_OPERATOR :=

For profiles without internal (T^4) excitations, set

[
W_c=\sqrt{H_{1,c}H_{5,c}}.
]

The six-dimensional metric is

[
g_c
===

W_c^{-1}
\left[-(dt-A_c)^2+(dy+B_c)^2\right]
+
W_c,dx_i,dx_i,
]

with

[
dB_c=-*_4dA_c.
]

This is the standard Lunin–Mathur metric form. 

Fix the gauge

[
\delta_{\mathbb R^4}B_c=0,
\qquad
B_c\longrightarrow0
\quad\text{as }r\to\infty.
]

On an exterior annulus

[
\Omega_R={R_0<|x|<R_1},
\qquad
R_0>\sup_{c,\theta}|F_c(\theta)|,
]

all profile kernels and their spatial and parameter derivatives are uniformly bounded. The fixed-gauge Hodge equation then gives uniform bounds for (B_c) on every slightly smaller exterior annulus.

Using the coframe

[
dt-A_c,\qquad dy+B_c,\qquad dx^i,
]

one obtains

[
\sqrt{|\det g_c|}=W_c.
]

The densitized inverse coefficients

[
G_c^{\mu\nu}
============

\sqrt{|\det g_c|},g_c^{\mu\nu}
]

are

[
G^{tt}= -W_c^2+|A_c|^2,
]

[
G^{ty}=-A_c\cdot B_c,
\qquad
G^{ti}=A_{c,i},
]

[
G^{yy}=W_c^2+|B_c|^2,
\qquad
G^{yi}=-B_{c,i},
]

[
G^{ij}=\delta^{ij}.
]

Let

[
\Sigma=S_y^1\times\Omega_R,
\qquad
V=H_0^1(\Sigma),
\qquad
H=L^2(\Sigma),
\qquad
V^*=H^{-1}(\Sigma).
]

Define

[
m_c=W_c^2-|A_c|^2,
]

[
b_c=
\left(-A_c\cdot B_c,\ A_c\right),
]

and the spatial matrix

[
C_c=
\begin{pmatrix}
W_c^2+|B_c|^2 & -B_c^{\mathsf T}\
-B_c & I_4
\end{pmatrix}.
]

For a spatial covector ((\eta,\xi)),

[
C_c[(\eta,\xi),(\eta,\xi)]
==========================

W_c^2\eta^2+|\xi-\eta B_c|^2.
]

If

[
M_B=\sup_{c,x}|B_c(x)|,
]

then

[
C_c[\zeta,\zeta]
\ge
\lambda_C|\zeta|^2,
\qquad
\lambda_C
=========

\frac1{3+2M_B^2}.
]

Choose (R_0) sufficiently large that

[
\sup_{c,x}|A_c(x)|\le\frac12.
]

Since (W_c\ge1),

[
m_c\ge\frac34.
]

The weak operators are

[
\langle\mathcal A_cu,v\rangle
=============================

\int_\Sigma
C_c^{\alpha\beta}
\partial_\beta u,\partial_\alpha v,
]

and

[
\langle\mathcal B_cv,w\rangle
=============================

\int_\Sigma
b_c^\alpha
\left(
v\partial_\alpha w-w\partial_\alpha v
\right).
]

Therefore

[
\mathcal A_c\in\mathcal L(H_0^1,H^{-1}),
\qquad
\mathcal B_c\in\mathcal L(H_0^1,H^{-1}),
]

with

[
\langle\mathcal A_cu,u\rangle
\ge
\lambda_C|u|_{H_0^1}^2,
]

[
|\mathcal B_cv|*{H^{-1}}
\le
2|b_c|*\infty|v|_{H_0^1}.
]

The full fixed-gauge scalar equation is

[
\boxed{
m_c\ddot u_c
+
\mathcal B_c\dot u_c
+
\mathcal A_cu_c
===============

f_c
\quad\text{in }H^{-1}.
}
]

Uniform differentiation of the exterior coefficients gives

[
c\longmapsto
(m_c,\mathcal B_c,\mathcal A_c)
]

as a (C^1) map into

[
\mathcal L(L^2,L^2)
\times
\mathcal L(H_0^1,H^{-1})
\times
\mathcal L(H_0^1,H^{-1}).
]

In particular,

[
|D\mathcal A_c[h]|*{H_0^1\to H^{-1}}
+
|D\mathcal B_c[h]|*{H_0^1\to H^{-1}}
+
|Dm_c[h]|_{L^2\to L^2}
\le C_R|h|.
]

This extends the previous reduced operator estimate to the complete six-dimensional scalar (\Box_{g_c}) on the selected fixed-gauge exterior region.

[
\mathrm{BOUNDARY}
:=
\neg,
\text{uniform estimates through an ergoregion or across the profile cap}.
]

---

## HAAR_AVERAGED_OPERATIONAL_SHADOW :=

Let

[
H=T^2
]

act freely on (U_{\mathrm{free}}\subset K_4), and let (\mu_H) be normalized Haar measure.

Assume the raw time delays

[
\tau_j(c),\qquad j=1,2,
]

and complex finite-window response

[
\mathcal R(c)
]

are defined and (C^1) for every point of each (H)-orbit.

Define

[
\overline{\tau}_j([c])
======================

\int_H\tau_j(h\cdot c),d\mu_H(h),
]

[
V_{\tau_j}([c])
===============

\int_H
\left|
\tau_j(h\cdot c)-\overline{\tau}_j([c])
\right|^2d\mu_H(h),
]

[
\overline{\mathcal R}([c])
==========================

\int_H\mathcal R(h\cdot c),d\mu_H(h),
]

and

[
P_{\mathcal R}([c])
===================

\int_H|\mathcal R(h\cdot c)|^2d\mu_H(h).
]

The seven-coordinate operational shadow is

[
\boxed{
\Psi_H([c])
===========

\left(
\overline{\tau}*1,
\overline{\tau}*2,
V*{\tau_1},
V*{\tau_2},
\operatorname{Re}\overline{\mathcal R},
\operatorname{Im}\overline{\mathcal R},
P_{\mathcal R}
\right).
}
]

For (g\in H),

[
\overline{\tau}_j([g\cdot c])
=============================

# \int_H\tau_j(hg\cdot c),d\mu_H(h)

\overline{\tau}_j([c]),
]

by Haar invariance. The same proof applies to every component of (\Psi_H).

Thus

[
\boxed{
\Psi_H:U_{\mathrm{free}}/T^2\to\mathbb R^7
}
]

is well-defined. If the raw maps have uniformly bounded first derivatives, differentiation under the compact Haar integral proves that (\Psi_H) is (C^1).

---

## INVARIANT_MULTIPOLE_DISTANCE_BOUND :=

For the attraction theorem, replace the singular point-source reference by the same-charge circular Lunin–Mathur geometry

[
F_\circ(\theta)
===============

\left(
\sqrt\kappa\cos\theta,,
\sqrt\kappa\sin\theta,,
0,,
0
\right).
]

This is a stationary same-charge profile geometry; the circular profile and its exact fields are standard explicit members of the D1–D5 family. 

Define the trace-free second moment

[
Q_{ij}(c)
=========

## \left\langle F_iF_j\right\rangle

\frac14\delta_{ij}
\left\langle|F|^2\right\rangle,
]

and

[
\Delta Q(c)=Q(c)-Q(\circ).
]

Let

[
D=\operatorname{diag}(1,1,-1,-1).
]

Since (\operatorname{tr}D=0),

[
D:\Delta Q
==========

\left\langle
F_1^2+F_2^2-F_3^2-F_4^2
\right\rangle_c
-\kappa.
]

Using

[
a(c)^2=\kappa-\mu_1,
\qquad
\mu_0=S_2+S_3+S_4,
\qquad
\mu_1=4S_2+9S_3+16S_4,
]

gives

[
D:\Delta Q
==========

-(\mu_0+\mu_1).
]

Because (|D|_{\mathrm F}=2),

[
\boxed{
|\Delta Q(c)|_{\mathrm F}
\ge
\frac{\mu_0+\mu_1}{2}.
}
]

The leading difference in (H_5) is

[
H_{5,c}-H_{5,\circ}
===================

\frac{4Q_5}{r^4}
\widehat x_i\widehat x_j
\Delta Q_{ij}
+
O(r^{-5}).
]

Let the field distance include the scalar component

[
d_R(\mathfrak B_c,\mathfrak B_\circ)
\ge
\sup_{|x|\ge R}
|H_{5,c}(x)-H_{5,\circ}(x)|.
]

For (R) sufficiently large that the convergent multipole tail is at most half the quadrupole term,

[
d_R(\mathfrak B_c,\mathfrak B_\circ)
\ge
\frac{Q_5}{R^4}
|\Delta Q(c)|_{\mathrm F}.
]

Therefore

[
\boxed{
d_R(\mathfrak B_c,\mathfrak B_\circ)
\ge
\frac{Q_5}{2R^4}
\left(
5S_2+10S_3+17S_4
\right).
}
]

Thus every nonzero higher Fourier mode has a positive invariant exterior-distance obstruction from the circular reference.

---

## DISSIPATIVE_RESTRICTED_EVOLUTION :=

Choose damping rates

[
\gamma_2,\gamma_3,\gamma_4>0,
\qquad
\gamma_*=\min_n\gamma_n.
]

Define

[
A_n(t)=e^{-\gamma_nt}A_n(0),
\qquad
B_n(t)=e^{-\gamma_nt}B_n(0),
]

and enforce the fixed-charge condition by

[
a(t)^2
======

\kappa-
\sum_{n=2}^{4}
n^2
\left(
|A_n(t)|^2+|B_n(t)|^2
\right).
]

Since the spectral energy decreases,

[
a(t)^2\ge a(0)^2\ge a_*^2.
]

Therefore the flow exists globally and preserves (K_4).

It commutes with the (T^2)-action because each complete mode pair is multiplied by a real scalar depending only on (n). Hence it descends to (K_4/T^2).

The seven spectral invariants evolve exactly as

[
S_n(t)=e^{-2\gamma_nt}S_n(0),
]

[
P_n(t)=e^{-4\gamma_nt}P_n(0),
]

[
C_{23}^{\mathrm{inv}}(t)
========================

e^{-2(\gamma_2+\gamma_3)t}
C_{23}^{\mathrm{inv}}(0).
]

Thus all seven converge to zero.

Moreover,

[
|F_{c(t)}-F_\circ|*{C^k}
\le
C_k e^{-\gamma**t},
]

because the transverse modes decay at rate (e^{-\gamma_*t}), while

[
0\le\sqrt\kappa-a(t)
====================

\frac{\kappa-a(t)^2}{\sqrt\kappa+a(t)}
\le
C e^{-2\gamma_*t}.
]

Uniform exterior smoothness of the profile-to-field map gives

[
d_R(\mathfrak B_{c(t)},\mathfrak B_\circ)
\le
C_R e^{-\gamma_*t}.
]

If (\Psi_H) is (C^1) on a compact invariant set, it is Lipschitz there, so

[
|\Psi_H([c(t)])-\Psi_H([\circ])|
\le
C_\Psi e^{-\gamma_*t}.
]

For an initial compact ensemble (E_0\subset K_4), let

[
E(t)=\mathcal D_t(E_0).
]

Its shadow diameter satisfies

[
D_R(t)
======

\sup_{c,c'\in E(t)}
|\Psi_H([c])-\Psi_H([c'])|
\le
2C_\Psi e^{-\gamma_*t}.
]

Hence, for

[
t_Q(\varepsilon)
================

\frac1{\gamma_*}
\log
\frac{\max(C_R,2C_\Psi)}{\varepsilon},
]

one has

[
d_R(\mathfrak B_{c(t)},\mathfrak B_\circ)
\le\varepsilon,
\qquad
D_R(t)\le\varepsilon
]

for every (t\ge t_Q(\varepsilon)).

A perturbation (\delta c) applied at (t_Q) obeys

[
|\delta c(t)|
\le
C_{a_*}e^{-\gamma_*(t-t_Q)}
|\delta c(t_Q)|.
]

Therefore the terminal-stability modulus can be chosen as

[
\eta(s)=e^{-\gamma_*s}.
]

[
\boxed{
\text{The circular D1–D5 orbit is a terminally stable Quznor attractor for this restricted dissipative flow.}
}
]

Uniformly damped abstract wave systems can exhibit exponential energy decay under positivity and compatibility assumptions, but the coefficient flow above is proved directly and does not require identifying it with such a physical damping mechanism. 

[
\mathrm{BOUNDARY}
:=
\neg,
\text{the dissipative coefficient flow solves the undamped D1–D5 supergravity evolution equations}.
]

[
\mathrm{BOUNDARY}
:=
\neg,
\text{physical black-hole evolution converges to the circular Quznor reference}.
]

NEXT_ACTIONS :=

1. Isolate (\mu_2) from a specific higher asymptotic field coefficient or prove that no such single coefficient suffices.
2. Prove the fixed-gauge Hodge estimate for (B_c) with explicit annular constants.
3. Verify uniform geodesic branches and wave well-posedness over every (T^2)-orbit used in (\Psi_H).
4. Compute the exact quadrupole-tail radius needed for the distance lower bound.
5. Derive the dissipative mode equations from a specified effective action or retain them explicitly as phenomenological dynamics.
