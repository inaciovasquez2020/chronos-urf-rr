# Chronos Borel-2 leading-Laurent analysis

Date: 2026-08-25

Status: formal asymptotic analysis only; no claim of finite-\(\beta\) convergence or Borel summability.

## Setup

For the corrected AEH=1/2 RW-sector formal lift, write

\[
R(\beta)=R_0+\sum_{n\ge2}\beta^n R_n.
\]

The exact reduced equation has principal recurrence

\[
R_n=-a(r)\,\partial_r^2R_{n-1}+\text{lower-radial-jet terms},
\qquad
 a(r)=\frac{5(r-2M)}{6r}.
\]

For the leading Laurent hierarchy at \(r\to0\), use

\[
R_n\sim
\begin{pmatrix}
 a_n r^{-3n} & b_n r^{-3n-3}\\
 c_n r^{-3n+2} & d_n r^{-3n-1}
\end{pmatrix}.
\]

The unique two-derivative term raises the pole order by three per perturbative step and gives the Gevrey-2 scale.

## Zero-mode / R12 channel

For the \(R_{12}\) leading coefficient, if

\[
(R_{n-1})_{12}=b_{n-1}r^{-3n}+\cdots,
\]

then the same-level derivative coefficient is exact. The relevant linearized derivative combination is

\[
X''+2X'R_0+R_0X'-H_2X'.
\]

At \(r\to0\),

\[
(R_0)_{11}\sim 2/r,\qquad
(R_0)_{22}\sim 1/r,\qquad
(H_2)_{11}\sim 3/r.
\]

With \(p=3n\), the coefficient of the same \(R_{12}\) Laurent monomial is

\[
p(p+1)-2p-2p+3p=p^2.
\]

Since

\[
-a(r)\sim \frac{5M}{3r},
\]

the exact same-level transport is

\[
\boxed{b_n=15Mn^2 b_{n-1}+F_n},
\]

where \(F_n\) contains the coupled lower-order forcing and nonlinear convolutions. In particular, there is no \(O(n)b_{n-1}\) correction in this channel.

## Order-2 Borel normalization

Define

\[
\widetilde b_n=\frac{b_n}{(n!)^2},
\qquad
B(\xi)=\sum_{n\ge2}\widetilde b_n\xi^n,
\]

and

\[
\mathcal F(\xi)=\sum_{n\ge3}\frac{F_n}{(n!)^2}\xi^n.
\]

The coefficient recurrence gives the exact formal generating-function identity

\[
\boxed{(1-15M\xi)B(\xi)=\widetilde b_2\xi^2+\mathcal F(\xi)}.
\]

The exact seed is

\[
b_2=\frac{328\,iM^3(\lambda-2)}{9\omega},
\qquad
\widetilde b_2=\frac{82\,iM^3(\lambda-2)}{9\omega}.
\]

Hence at the candidate order-2 Borel barrier

\[
\xi_*=\frac1{15M},
\]

the bare numerator contribution is

\[
\widetilde b_2\xi_*^2
=\frac{82\,iM(\lambda-2)}{2025\,\omega},
\]

which is nonzero for \(\ell\ge2\) and \(\omega\ne0\).

A pole at \(\xi_*\) is therefore removed only if the exact scalar cancellation identity

\[
\boxed{
\mathcal F\!\left(\frac1{15M}\right)
=-\frac{82\,iM(\lambda-2)}{2025\,\omega}
}
\]

holds.

Equivalently, after rescaling \(x=15M\xi\) and factoring the dominant exponential, the renormalized zero-mode amplitude converges to

\[
z_\infty=z_2+\Phi(1).
\]

An actual positive-axis simple pole is certified only if \(z_\infty\ne0\).

## Verified boundary

The currently certified Chronos data do **not** provide a rigorous bound strong enough to prove

\[
|\Phi(1)|<|z_2|,
\]

nor a sign/phase theorem that forbids exact cancellation. The nonlinear coupled forcing preserves the real/imaginary parity of the RW sector but is not sign-definite.

Therefore:

```text
PROVED :=
exact same-level R12 transport b_n = 15 M n^2 b_(n-1) + F_n

PROVED :=
order-2 Borel generating-function denominator 1 - 15 M xi

PROVED :=
bare numerator at xi = 1/(15M) is nonzero for ell >= 2, omega != 0

PROVED :=
pole cancellation is equivalent to one exact scalar identity

NOT_PROVED :=
Phi(1) != -z_2

NOT_PROVED :=
actual positive-axis Borel-2 pole

NOT_PROVED :=
Borel-2 summability or finite-beta invariant RW graph
```

## Next bounded action

Derive an explicit majorant or exact projected forcing representation sufficient to evaluate or bound \(\Phi(1)\). The strongest immediate target is

\[
|\Phi(1)|<|z_2|,
\]

which would certify \(z_\infty\ne0\) and hence the positive-axis pole in the formal order-2 Borel transform.
