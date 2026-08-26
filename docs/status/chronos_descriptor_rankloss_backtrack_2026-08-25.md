# Chronos finite-beta descriptor rank-loss backtrack

Date: 2026-08-25

Status: exact local principal-symbol certificate. No claim that the horizon-selected physical ingoing branch necessarily fails the crossing condition.

## Exact principal determinant

For the corrected AEH=1/2 hash-locked Fourier-radial odd Euler system, the stored exact principal determinant factors as

\[
\boxed{
\det P_{\rm princ}
=
\frac{\beta^2\lambda^2(\lambda-2)(r-2M)^3
(-16M\beta+5r^3)(8M\beta+5r^3)}{36r^{11}}
}.
\]

For \(\beta>0\), \(\ell\ge2\), and \(r>2M\), the positive exterior finite-radius rank-loss surface is

\[
\boxed{-16M\beta+5r^3=0},
\qquad
r_c=\left(\frac{16M\beta}{5}\right)^{1/3}.
\]

This zero is already present in the principal matrix of the exact Euler equations; it is not created only after solving the six-state descriptor system.

## Exact null direction

At

\[
\beta_c(r)=\frac{5r^3}{16M},
\]

the principal matrix reduces to

\[
P_c=A_c
\begin{pmatrix}
1&i\omega\\
i\omega&-\omega^2
\end{pmatrix},
\qquad
A_c=-\frac{25\lambda r^2(r-2M)}{64M}.
\]

Under the ordinary exterior guards, \(A_c\ne0\), so \(P_c\) has rank exactly one. Exact right and left null vectors may both be chosen as

\[
\boxed{v_c=(-i\omega,1)^T},
\qquad
\boxed{w_c^T=(-i\omega,1)}.
\]

Thus for the two full Euler equations \(\mathfrak E_0=0\), \(\mathfrak E_1=0\), the lost-principal-direction projection is

\[
\boxed{-i\omega\,\mathfrak E_0+\mathfrak E_1=0}
\]

at \(r=r_c\). Its highest-derivative term vanishes there, leaving a lower-order compatibility condition.

## Backtrack decision

The exact finite-beta generator previously certified from the same Euler system has an uncancelled rank-one pole on the same surface; in particular the radial residue in the singular fast direction is nonzero. Therefore the projected lower-order condition is not an identity on the full state space. Generic state data fail it.

This selects alternative **(b)** locally:

```text
DECISION := (b)

PROVED :=
principal rank drops by exactly one at r_c

PROVED :=
left/right null direction is (-i omega, 1)

PROVED :=
the lost highest-derivative equation becomes a genuine nontrivial compatibility condition, not an automatic identity

PROVED :=
generic state data are obstructed at the crossing

NOT_PROVED :=
the horizon-selected physical ingoing branch violates the compatibility condition

NOT_PROVED :=
all physical axial solutions are singular at r_c
```

## Curvature-state interpretation

Using the GR/Ricci residuals

\[
\mathcal E_0,
\qquad
\mathcal E_1,
\]

the regular six-state change of variables may be organized as

\[
(h_0,h_1,\mathcal E_0,\mathcal E_1,\mathcal E_0',\mathcal E_1').
\]

For \(r_c>2M\) and \(\omega\ne0\), this change of variables is invertible, so the nontrivial compatibility condition remains nontrivial in curvature coordinates. An exact reduction to a condition involving only the four curvature coordinates has not yet been certified.

## Good stopping boundary

The local algebraic question is closed. The remaining physical question is global:

\[
\mathcal C_{\rm phys}(\beta,\omega,\ell)
=
w_c^T F\bigl(X_{\rm ingoing}(r_c^-)\bigr).
\]

The missing object is the finite-\(\beta\) horizon-to-\(r_c\) connection map for the exact hash-locked Chronos system.

```text
NEXT_ACTION :=
construct a horizon-regular Frobenius/shooting certificate for the exact finite-beta odd system and evaluate the projected compatibility functional at r_c

STOP_REASON :=
no local identity can determine that value; further progress requires the global radial connection problem
```

This is the intended stopping point: the generic rank-loss obstruction is certified, while the physical-branch obstruction remains explicitly open.
