# Exact exterior rank-loss obstruction for corrected GfE GQQ (2026-10-17)

## Result

The corrected finite-\(\beta\) block \(G_{QQ}\) loses rank at a real point strictly outside the horizon in the physical accumulation sector
\[
M=1,\qquad \beta=\frac52,\qquad \lambda=6,\qquad \omega=\frac{i}{4}.
\]
This is an exact obstruction to a global inverse or a uniform inverse bound for \(G_{QQ}\) over the full exterior. It is **not** a proof that the full resolvent or Riesz projector fails to exist.

## Exact factorization

Let \(x=r/M\), \(b=\beta/M^2\), and \(w=M\omega\). In the sector above, the determinant numerator \(\Delta\) from the authoritative corrected P/Q/GQQ artifact specializes to
\[
\Delta(x)=-\frac{25}{16}(x-2)p(x),
\]
where
\[
\begin{aligned}
p(x)={}&x^9+2x^8+4x^7+452x^6-248x^5-112x^4\\
&-5120x^3-1024x^2+22528x-73728.
\end{aligned}
\]
The exact rational endpoint evaluations satisfy
\[
p\!\left(\frac{257}{100}\right)<0,
\qquad
p\!\left(\frac{129}{50}\right)>0.
\]
Continuity therefore gives at least one \(x_*\in(2.57,2.58)\) with \(p(x_*)=0\). In particular, \(x_*>2\), so this is an exterior rank-loss point, not the horizon factor \(x=2\).

## Guard audit at the bracket

The determinant denominator is
\[
r^2(r-2)^2(-40+5r^3)(20+5r^3).
\]
It is strictly positive for every \(r\in(2.57,2.58)\): each factor is positive there, and \(-40+5r^3=5(r^3-8)>0\) for all \(r>2\). The existing exact exterior-continuation verifier certifies the source descriptor \(E\) is invertible and all descriptor coefficients are regular for every real \(r>2\) in this same fixed sector. Thus the zero occurs within the ordinary-generator guard, where the corrected artifact's exact rank classification applies: rank two if \(\Delta\ne0\), rank one if \(\Delta=0\).

## Consequences and limits

- **Proved by exact algebra plus the intermediate value theorem:** a real exterior point exists where \(G_{QQ}\) has rank one.
- **Ruled out on the full exterior:** an everywhere-defined inverse \(G_{QQ}^{-1}\), and hence any uniform bound for that inverse across the full exterior.
- **Not proved:** failure of the full six-state resolvent, failure of a Riesz projector, failure of local-uniform Riesz convergence near \(M=1\), or failure of every restricted-domain estimate.
- **Still possible:** estimates on guarded subdomains that stay a positive distance from \(\Delta=0\), with constants allowed to depend on that separation.
- **Not claimed:** a Fredholm resolution, endpoint admissibility, or horizon/outgoing closure.

## Reproduction

Run the command: python3 tools/gfe/verify_gfe_corrected_gqq_exterior_rankloss_obstruction.py

The verifier reads artifacts/chronos/gfe_corrected_AEH_half_pq_gqq.json, checks the exact factorization and rational endpoint signs, and checks positivity of the GQQ determinant denominator at both bracket endpoints. The companion exterior-continuation gate establishes the ordinary-generator guard on the whole open exterior in this sector.
