# Quznor Three-Mode Row Equilibration and Conditioning

## Status

This note analyzes the coordinate-dependent numerical conditioning of
the exact three-mode coefficient reconstruction recorded in

`lean/Chronos/Frontier/QuznorD1D5ThreeModeVandermondeInversion.lean`.

The calculations use exact rational arithmetic.

**Novelty status:** ordinary finite-dimensional matrix conditioning; not
plausibly new mathematics.

**Boundary:** no empirical D1–D5 observables, experimental error model,
or noise distribution has been supplied. No claim of globally optimal
two-sided diagonal scaling is made.

## 1. Row-equilibration strategy

The unscaled reconstruction matrix is

\[
M=
\begin{pmatrix}
1&1&1\\
4&9&16\\
16&81&256
\end{pmatrix}.
\]

Normalize the largest absolute entry in every row to \(1\) by defining

\[
D=
\begin{pmatrix}
1&0&0\\
0&\frac1{16}&0\\
0&0&\frac1{256}
\end{pmatrix}.
\]

For

\[
A=MS,
\]

define

\[
\widetilde A:=DA.
\]

Then

\[
\widetilde A=M_{\mathrm{eq}}S,
\qquad
M_{\mathrm{eq}}:=DM.
\]

Because \(D\) is invertible, this does not change the exact coefficient
vector \(S\). It changes the coordinates in which observable
perturbations are measured.

## 2. Equilibrated system

\[
M_{\mathrm{eq}}
=
\begin{pmatrix}
1&1&1\\[1mm]
\frac14&\frac9{16}&1\\[1mm]
\frac1{16}&\frac{81}{256}&1
\end{pmatrix}.
\]

Since

\[
M_{\mathrm{eq}}=DM,
\]

\[
M_{\mathrm{eq}}^{-1}=M^{-1}D^{-1},
\qquad
D^{-1}=\operatorname{diag}(1,16,256).
\]

Exact multiplication gives

\[
M_{\mathrm{eq}}^{-1}
=
\begin{pmatrix}
\frac{12}{5}&-\frac{20}{3}&\frac{64}{15}\\[2mm]
-\frac{64}{35}&\frac{64}{7}&-\frac{256}{35}\\[2mm]
\frac37&-\frac{52}{21}&\frac{64}{21}
\end{pmatrix}.
\]

## 3. Exact infinity-norm condition number

For \(X=(x_{ij})\), use

\[
\|X\|_\infty=\max_i\sum_j|x_{ij}|.
\]

The absolute row sums of \(M_{\mathrm{eq}}\) are

\[
3,\qquad \frac{29}{16},\qquad \frac{353}{256}.
\]

Therefore

\[
\boxed{\|M_{\mathrm{eq}}\|_\infty=3}.
\]

The absolute row sums of its inverse are

\[
\frac{40}{3},\qquad
\frac{128}{7},\qquad
\frac{125}{21}.
\]

Thus

\[
\boxed{\|M_{\mathrm{eq}}^{-1}\|_\infty=\frac{128}{7}}
\]

and

\[
\boxed{
\kappa_\infty(M_{\mathrm{eq}})
=
\frac{384}{7}
\approx54.8571
}.
\]

For the unscaled matrix,

\[
\|M\|_\infty=353,
\qquad
\|M^{-1}\|_\infty=\frac{17}{6},
\]

so

\[
\kappa_\infty(M)=\frac{6001}{6}\approx1000.1667.
\]

The relative reduction is

\[
1-\frac{\frac{384}{7}}{\frac{6001}{6}}
=
\frac{39703}{42007}
\approx0.945152.
\]

This is an approximately \(94.515\%\) reduction in the selected
coordinate-dependent condition number. It is not a claim that the same
percentage of physical or statistical instability was illusory.

## 4. Row equilibration is not globally optimal

Every row and column of \(M_{\mathrm{eq}}\) has maximum absolute entry
\(1\). This does not prove optimality under further diagonal coordinate
changes.

Let

\[
R=
\operatorname{diag}
\left(
\frac{56}{25},
\frac{384}{125},
1
\right).
\]

Then

\[
M_{\mathrm{eq}}R
=
\begin{pmatrix}
\frac{56}{25}&\frac{384}{125}&1\\[2mm]
\frac{14}{25}&\frac{216}{125}&1\\[2mm]
\frac7{50}&\frac{243}{250}&1
\end{pmatrix}.
\]

Direct exact calculation gives

\[
\|M_{\mathrm{eq}}R\|_\infty=\frac{789}{125}
\]

and

\[
\|(M_{\mathrm{eq}}R)^{-1}\|_\infty=\frac{125}{21}.
\]

Consequently,

\[
\boxed{
\kappa_\infty(M_{\mathrm{eq}}R)
=
\frac{263}{7}
\approx37.5714
}.
\]

Thus right diagonal scaling can improve the condition number further.

If

\[
S=RY,
\]

then

\[
\widetilde A=M_{\mathrm{eq}}RY.
\]

This changes the coefficient coordinates and their relative-error
metric, not the underlying exact inverse problem. The displayed \(R\)
is only an explicit improvement; no global optimality is claimed.

## 5. Error-amplification interpretation

For

\[
\widetilde A+\Delta\widetilde A
=
M_{\mathrm{eq}}(S+\Delta S),
\]

with nonzero \(S\) and \(\widetilde A\),

\[
\boxed{
\frac{\|\Delta S\|_\infty}{\|S\|_\infty}
\le
\frac{384}{7}
\frac{\|\Delta\widetilde A\|_\infty}
     {\|\widetilde A\|_\infty}
}.
\]

The factor \(384/7\) is a worst-case normwise upper bound. It does not
mean that every perturbation is amplified by approximately \(55\).

The decimal-digit estimate is

\[
\log_{10}\left(\frac{384}{7}\right)\approx1.739.
\]

An adversarially aligned perturbation may therefore be bounded as losing
approximately \(1.74\) decimal digits in these coordinates. This is not
a guaranteed or universal loss.

## 6. Numerical and physical implications

The scaling shows that much of the large raw infinity-norm condition
number comes from different numerical scales among the three Euler
observables.

It does not establish that:

- reconstruction is sufficiently stable for a particular experiment;
- physical errors follow the infinity norm;
- errors have equal scale or are uncorrelated;
- calibration and model uncertainty are negligible;
- regularization is unnecessary;
- the observables are physically realized D1–D5 measurements.

Those conclusions require a model specifying absolute and relative
errors, covariance or correlation information, calibration uncertainty,
and expected observable magnitudes.

For exact symbolic observables, reconstruction remains exact. For noisy
empirical data, scaling must be selected together with the noise model.
The need for regularization cannot be inferred from the condition number
alone.

## Boundary and stopping rule

\[
\texttt{BOUNDARY}
:=
\neg\,
\text{empirical D1–D5 observables or their noise distribution supplied}.
\]

\[
\texttt{BOUNDARY}
:=
\neg\,
\text{global optimality of the displayed two-sided scaling proved}.
\]

Further optimization stops unless a fixed empirical error metric is
supplied.
