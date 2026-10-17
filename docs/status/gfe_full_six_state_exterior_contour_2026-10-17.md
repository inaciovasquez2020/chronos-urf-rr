# Full six-state exterior contour exclusion at corrected GQQ rank loss

**Date:** 2026-10-17  
**Scope:** fixed sector \(M=1,\ \beta=5/2,\ \lambda=6,\ \omega=i/4\).

## Exact result

Let
\[
p(x)=x^9+2x^8+4x^7+452x^6-248x^5-112x^4
-5120x^3-1024x^2+22528x-73728,
\]
and let \(x_*\) be its unique real root in \((2571/1000,2572/1000)\), as established by the exterior rank-loss certificate. The corrected \(G_{QQ}\) block has rank one at \(x_*\), while the ordinary-generator guard holds.

Using the authoritative six-state descriptor matrices \(E(x)\) and \(A(x)\), the verifier constructs the exact pencil determinant
\[
Q(z,x)=\operatorname{numerator}\det(zE(x)-A(x)).
\]
It then forms the elimination resultant
\[
R(z)=\operatorname{Res}_x(p(x),Q(z,x)).
\]
The exact computation returns
\[
\deg R=54.
\]
Writing \(R(z)=\sum_{k=0}^{54}a_kz^k\), define the reciprocal-conjugate polynomial
\[
S(z)=\sum_{k=0}^{54}\overline{a_k}\,4^k z^{54-k}.
\]
For every \(z\) with \(|z|=2\), one has \(S(z)=z^{54}\overline{R(z)}\). Therefore any zero of the full pencil determinant on this contour at any root of \(p\) would give a common root of \(R\) and \(S\).

The exact polynomial gcd computation gives
\[
\gcd(R,S)=1.
\]
Hence no full-pencil determinant zero lies on \(|z|=2\) at \(x_*\). In fact, this elimination certificate excludes contour zeros for every complex root of the defining polynomial \(p\), a stronger statement than needed for the isolated real root.

Verifier output:
- **DESCRIPTOR_PENCIL_DETERMINANT_NUMERATOR_SHA256:** 3488398f9687850273972072388dce6e389e6011ca5f66602a098d00f89b1e3b
- **ELIMINATION_RESULTANT_DEGREE:** 54
- **RECIPROCAL_CONJUGATE_GCD_DEGREE:** 0
- **FULL_PENCIL_NONZERO_ON_CONTOUR:** true

The standalone focused GitHub Actions workflow completed successfully on 2026-10-17 (run 39079659353).

## Interpretation and limits

This resolves the specific question left open by the exterior \(G_{QQ}\) rank-loss result: **the full six-state pencil remains nonsingular on the already specified contour \(|z|=2\) at \(x_*\)**. Thus this particular block rank loss does not invalidate that contour's full-pencil resolvent at this point.

It does **not** establish global parameter uniformity, a global uniform resolvent bound, a Fredholm resolution, endpoint admissibility, horizon/outgoing closure, or all-orders invariant-graph closure. It also does not turn the \(G_{QQ}\) block into an invertible block at \(x_*\); its rank loss remains exact.
