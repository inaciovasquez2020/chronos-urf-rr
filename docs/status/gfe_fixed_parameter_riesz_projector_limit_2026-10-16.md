# Fixed-parameter GfE Riesz-projector limit

Date: 2026-10-16

## Scope

This note records an exact symbolic certificate at the single parameter point
\[
M=1,\qquad r=3,\qquad \lambda=6,\qquad \omega=i/4,
\]
for the corrected AEH=1/2 guarded Laurent generator in
`artifacts/chronos/gfe_corrected_AEH_half_laurent_generator.json`.

It is a fixed-point result only. It does not assert uniformity in the physical parameters or an invariant projector for all finite \(\beta\).

## Generator and contour

Write \(G(\beta)=N(\beta)/D(\beta)\), using the artifact's reduced numerator and denominator coefficient arrays. At the stated point,
\[
D(\beta)=\frac{\beta(8\beta+135)^2(16\beta-135)}{14348907}.
\]
The determinant numerator is
\[
\det(zD(\beta)I-N(\beta)).
\]
Its exact factorization has a common \(\beta^4\) factor. After cancellation, its limiting \(z\)-dependent factor is proportional to
\[
144z^2-337.
\]
Choose \(\Gamma=\{z:|z|=2\}\). On \(\Gamma\),
\[
|144z^2-337|\ge 144|z|^2-337=239>0.
\]
Therefore the canceled determinant denominator is nonzero on \(\Gamma\) at \(\beta=0\), and by continuity remains nonzero on \(\Gamma\) for all sufficiently small \(|\beta|\).

## Exact resolvent cancellation

The resolvent is
\[
R_\beta(z)=(zI-G(\beta))^{-1}
=\frac{D(\beta)\,\operatorname{adj}(zD(\beta)I-N(\beta))}
{\det(zD(\beta)I-N(\beta))}.
\]
Exact symbolic checks found:
- the determinant has \(\beta\)-valuation exactly 4;
- every one of the 36 entries of the numerator matrix
  \(D(\beta)\operatorname{adj}(zD(\beta)I-N(\beta))\)
  has \(\beta\)-valuation at least 4;
- after cancellation, all 36 resolvent entries have finite limits at \(\beta=0\).

Together with the nonvanishing canceled determinant on the compact contour, the canceled rational expression extends continuously to a neighborhood of \(\{0\}\times\Gamma\). Thus \(R_\beta\to R_0\) uniformly on \(\Gamma\).

## Limiting resolvent and residue certificate

The exact entrywise limit computed symbolically is
\[
R_0(z)=
\begin{pmatrix}
\frac{48(3z+2)}{144z^2-337}&0&0&\frac{364}{3(144z^2-337)}&0&0\\
\frac{96z+337}{144z^2-337}&0&0&\frac{364z}{3(144z^2-337)}&0&0\\
\frac{z(96z+337)}{144z^2-337}&-1&0&\frac{364z^2}{3(144z^2-337)}&0&0\\
\frac{324}{144z^2-337}&0&0&\frac{48(3z-2)}{144z^2-337}&0&0\\
\frac{324z}{144z^2-337}&0&0&-\frac{96z-337}{144z^2-337}&0&0\\
\frac{324z^2}{144z^2-337}&0&-1&-\frac{z(96z-337)}{144z^2-337}&-1&0
\end{pmatrix}.
\]
Its only finite poles are
\[
a_\pm=\pm\frac{\sqrt{337}}{12},
\]
both inside \(\Gamma\). The exact sum of their residues is
\[
P_*=
\begin{pmatrix}
1&0&0&0&0&0\\
\frac23&0&0&\frac{91}{108}&0&0\\
\frac{337}{144}&0&0&0&0&0\\
0&0&0&1&0&0\\
\frac94&0&0&-\frac23&0&0\\
0&0&0&\frac{337}{144}&0&0
\end{pmatrix}.
\]
An exact symbolic matrix comparison returned a zero \(6\times6\) residual for the residue sum minus \(P_*\). Separately, exact checks give \(P_*^2=P_*\), \(\operatorname{tr}P_*=2\), and \(\operatorname{rank}P_*=2\).

## Conclusion

Uniform convergence on \(\Gamma\) permits passage to the contour integral:
\[
P(\beta)=\frac{1}{2\pi i}\oint_\Gamma R_\beta(z)\,dz
\longrightarrow
\frac{1}{2\pi i}\oint_\Gamma R_0(z)\,dz=P_*.
\]
Hence the rank-two Riesz spectral projector associated with the two bounded eigenvalues converges to \(P_*\) as \(\beta\to0^+\), at this one fixed parameter point.

## Explicit non-claims

This certificate does not prove a uniform parameter-neighborhood estimate, an invariant projector for the full finite-\(\beta\) generator, a Fredholm resolution, endpoint admissibility, or horizon/outgoing closure. The calculations above were executed as exact symbolic commands during the derivation; this note records their outputs and argument, but is not itself a standalone automated regression test.
