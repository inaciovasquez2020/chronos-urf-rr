# Chronos: exact mixed-past/future dipole operator matrix

Date: 2026-11-15. **Classification:** PROVED exact \(\ell=1\) angular action by polynomial causal-cap integration; COMPUTATION_PASS exact rational degree-one/two matrices and strict probability enclosure; **CONDITIONAL** on previously archived 4-point identity, \(A_0\), mode masses \(b_1,\ldots,b_5\), and angular trace decomposition. Full \(p_{4,2}\) and infinite-growth stability remain **OPEN**. Lean NOT_RUN. No Git writes.

## Exact operator integral

Use the four-dimensional unit Alexandrov interval, null coordinates \(0<a<b<1\) with normalized radial density \(12(b-a)^2\,da\,db\), spatial radius \(r=(b-a)/2\), and normalized past/future volumes

\[
U(a,b)=(ab)^2,\qquad V(a,b)=((1-a)(1-b))^2.
\]

Let \(K_1\) denote the radial dipole component of the causal integral operator acting on \(F_{ij}(a,b)=rU^iV^j\). For a target at null coordinates \((c,d)\), \(0<c<d<1\), only the partially overlapping null-interval region \(0<a<c<b<d\) contributes: the angular \(\ell=1\) eigenvalue vanishes in the full-angle region. On the partial region,

\[
f=\frac{(c-a)(d-b)}{(b-a)(d-c)},\qquad
1-f=\frac{(b-c)(d-a)}{(b-a)(d-c)},\qquad
\lambda_1=\tfrac12\int_{1-2f}^{1}z\,dz=f(1-f).
\]

The \((b-a)^2\) radial density cancels the angular denominator. Therefore the dipole operator action has the exact **polynomial** representation

\[
\boxed{K_1 F_{ij}(c,d)=\frac{6}{(d-c)^2}
\int_0^c\!\int_c^d
(c-a)(d-b)(b-c)(d-a)(b-a)
(ab)^{2i}[(1-a)(1-b)]^{2j}\,db\,da.}
\]

For \(a=cu\), \(b=c+(d-c)v\), the integral is over \([0,1]^2\), with prefactor \(6c^2(d-c)\) and a polynomial integrand. Thus **every mixed \(U^iV^j\) dipole action and every Gram/energy entry is rational, for all nonnegative integers \(i,j\)**.

Direct sample formulas are

\[
K_1(r)=\tfrac12 rU,
\]

and

\[
K_1(rV)(c,d)=\frac{c^2d^2(d-c)}{60}
\big(c^2d^2-4c^2d+6c^2-4cd^2+16cd-18c+6d^2-18d+15\big).
\]

Setting \(j=0\) reproduces the independently derived one-variable Lorentz-covariant action \(K_1(rU^i)=\kappa_{1,i}\,rU^{i+1}\) for \(i=0,1,2\) (exact symbolic identity checks).

## Mixed Gram and energy matrices

For monomials \(\mathcal B_2=(1,U,V,U^2,UV,V^2)\), define

\[
G_{\alpha\beta}=\int_{0<c<d<1} 12(d-c)^2 F_\alpha(c,d)F_\beta(c,d)\,dc\,dd,
\]

\[
B_{\alpha\beta}=\int_{0<c<d<1}12(d-c)^2
(K_1F_\alpha)(c,d)(K_1F_\beta)(c,d)\,dc\,dd.
\]

All 21 independent entries of each symmetric 6×6 matrix were evaluated exactly as rational numbers. The standalone certificate prints both matrices in full, as well as the exact invariants

\[
\boxed{t_1=\operatorname{tr}(G^{-1}B)=\frac{1400200756617059}{506108512802256000}}
\]

and

\[
\boxed{s_1=\operatorname{tr}[(G^{-1}B)^2]=\frac{443742069139529854836879193872803}{92980935103320811138262404301568000000}.}
\]

The exact three-function (degree-one) invariants were independently computed as

\[
t_1^{[1]}=\frac{8995603}{4069665600},\quad
s_1^{[1]}=\frac{572268224972761}{149059602862410240000}.
\]

## Conditional updated probability interval

Using the previously archived exact zero-mode trace \(A_0=513/875875\), five angular Hilbert–Schmidt masses \(b_1,\ldots,b_5\), higher-mode (\(\ell=2,\ldots,5\)) eight-function \(U\)-only trace compressions, and angular tail \(R_5^2/13\), replace **only** the \(\ell=1\) compression by the new dense bivariate polynomial compression. The positive-operator enclosure is

\[
s_1\le\operatorname{tr}[(K_1^*K_1)^2]\le s_1+b_1^2-t_1^2.
\]

The standalone bound certificate checks the strict endpoints *with exact rational arithmetic* using the published rational \(\pi\) intervals:

\[
\boxed{0.0854106288<p_{4,2}<0.0854289315.}
\]

The previous conditional enclosure was \(0.085396726<p_{4,2}<0.085438735\). This shrinks interval width from approximately \(4.20\times10^{-5}\) to \(1.83\times10^{-5}\), without any quadrature, approximate matrix entry, Monte Carlo estimate, or unverified high-mode claim.

## Exact validation receipt / scope

- SymPy exact polynomial integration, exact rational Gram/energy matrix construction, invertibility, positive traces: **COMPUTATION_PASS** for bivariate total degrees 1 and 2.
- Dipole causal-cap identity and rationality for arbitrary polynomial indices: **PROVED** by algebraic change of variables.
- Previous one-variable dipole action for \(j=0\): **PASS** for \(i=0,1,2\).
- Independent archival eight-function higher-mode trace bounds: **previously replayed**, not re-proved in this audit.
- Exact \(p_{4,2}\), exact entire common-future second moment: **OPEN**.
- Lean compiler/axiom audit, independent external review: **NOT_RUN**.
- GitHub commit, push, merge: **NOT_PERFORMED**.

### Reproduction

Run `python chronos_mixed_uv_dipole_exact_20261115.py` to compute the exact matrices. Run `python chronos_mixed_uv_dipole_bounds_20261115.py` with the archived `chronos_two_sided_harmonic_trace_certificate_20261115.py` in the same directory to verify the strict global bounds. Requires Python 3 with SymPy for the mixed polynomial integrations. The second file also imports the new first file. All calculations are bounded at total degree 2.