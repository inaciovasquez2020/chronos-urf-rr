# Exact four-event linear-extension prefix probability in a 4D Minkowski diamond

**Status:** `CONDITIONAL_ON_UPSTREAM_GEOMETRIC_REDUCTION` pending independent end-to-end review; final rational kernel has two independent exact-arithmetic evaluations and numerical quadrature; `LEAN := NOT_RUN`. **Novelty relative to published literature:** `NOT_ESTABLISHED`. **Repository:** draft research PR #1375; not merged.

## Theorem and conventions

Let `D=J⁺((0,0)) ∩ J⁻((1,0))` in four-dimensional Minkowski space (signature `+---`), with four i.i.d. points sampled uniformly with respect to 4-volume. Let `P` be their induced strict causal order. Given `P`, choose one of its linear extensions uniformly, and let `p_(4,2)` be the probability that the first two elements of that extension are causally related. Then

\[
\boxed{p_{4,2}=\frac{1344000\pi^2-13239637}{294000}}
\quad\approx 0.08541263627244212147467994501206505395.
\]

This is a probability for the **specified** 4D Minkowski model; it is not a spacetime-emergence theorem or evidence of physical fifth dimensions.

## Dependency A — the finite positive-DAG identity

The separate exact 219-labeled-poset / 16-isomorphism-class certificate and an independent ordered-simplex integral establish

\[
p_{4,2}=\frac{24919}{294000}+\frac65 J,
\]

where

\[
J=\mathbb E\big[\mathbf1_{\{X\parallel Y\}} W^+(X,Y)^2\big],
\qquad W^+(X,Y)=\frac{\operatorname{Vol}(J^+(X)\cap J^+(Y)\cap D)}{\operatorname{Vol}(D)}.
\]

The exact N-shaped positive DAG term used in this reduction is `A=953/705600` (two independent rational ordered-simplex integrations). The timelike contribution to the inclusive 2+2 DAG term is `1/17640`. Audit these dependencies separately before promoting this theorem.

## Dependency B — general conditional common-future volume

Let `R=(1,0)` and let `a=√((R−X)²)`, `c=√((R−Y)²)`, `b=((R−X)·(R−Y))/a`, and `d=√(b²−c²)`. For spacelike `X,Y`, `d>|a−b|`. The previously audited null-rectangle calculation gives the normalized common-future fraction

\[
W^+=24f,\qquad
f=\frac{a(b-d)^2\big(-a^2+2ab+ad-b^2+d^2\big)}{24d}.
\]

This formula was independently tested against an exact polygon-volume evaluator for 251 rational configurations and was derived from a symbolic null-rectangle partition. We use it here as a cited mathematical dependency, not as an independent reconstruction from scratch.

## Reduction of J by null coordinates and scale symmetry

For each event let `U=1−t−r`, `V=1−t+r` (so `0<U<V<1`). For the second event use `P=1−s−w`, `Q=1−s+w` (so `0<P<Q<1`). Their normalized radial-time densities are `12(V−U)² dU dV` and `12(Q−P)² dP dQ`; their relative-angle cosine is uniform on `[−1,1]`.

Let `a=√(UV)`, `c=√(PQ)` and `b=((U+V)(P+Q)−(V−U)(Q−P) μ)/(4a)`. At `μ=1` and `μ=−1`, respectively,

\[
b_- = \frac{UQ+VP}{2a},\qquad
b_+ = \frac{UP+VQ}{2a}.
\]

Converting `dμ` to `db` produces an exact four-variable representation

\[
J=288\int_{0<U<V<1 \atop 0<P<Q<1}
 a(V-U)(Q-P)\int_{b_-}^{b_+}\mathbf1_{\rm spacelike}(24f)^2\,db\,dU\,dV\,dP\,dQ.
\]

(The display uses an inner angular integral and an outer four-variable integral.)

The integrand including `db` is homogeneous under common positive scaling of `U,V,P,Q` of degree 12. Split the domain into `V≥Q` and `Q≥V`; by exchange symmetry they contribute equally. For the first part write

\[
V=\lambda,\quad U=\lambda u,\quad Q=\lambda q,\quad P=\lambda qv,
\qquad 0<u,v,q,\lambda<1.
\]

The scale integral is `∫₀¹ λ¹⁵ dλ=1/16` and the exchange factor is 2. Introduce `β=b/q`, `δ=√(β²−v)`, `ζ=β−δ`, and `h=ζ/√u`. For the spacelike portion the integration bounds become

\[
v\le h\le\min(1,v/u),\qquad uh/v\le q\le1.
\]

The spacelike common-future fraction is

\[
24f=\frac{2\sqrt u\,q\,\zeta^3}{v-\zeta^2}
\left(-u+\frac{\sqrt u\,q(3v+\zeta^2)}{2\zeta}-vq^2\right).
\]

The changes of variables yield the **exact** three-variable rational integral

\[
J=72\int_0^1du\int_0^1dv\int_v^{\min(1,v/u)}dh\,
\frac{u^4(1-u)(1-v)h^4}{v-uh^2}
\int_{uh/v}^{1} q^5
\left(-u+\frac{q(3v+uh^2)}{2h}-vq^2\right)^2dq.
\]

Next set `v=hk` and `u=kr`. The domain becomes the simple product `0<r<1`, `0<h<1`, `0<k<1`, and the inner `q` runs from `r` to 1. The factor containing `k` is

\[
k^6(1-kr)(1-kh).
\]

Since

\[
\int_0^1k^6(1-kr)(1-kh)\,dk
=\frac17-\frac{r+h}{8}+\frac{rh}{9},
\]

we obtain the exact *two-variable rational kernel*

\[
\boxed{
J=72\int_0^1\!\int_0^1
\frac{r^4 h^4}{1-rh}
\left(\frac17-\frac{r+h}{8}+\frac{rh}{9}\right)
\left[\int_r^1q^5\left(-r+\frac{q(3+rh)}2-hq^2\right)^2dq\right]
\,dh\,dr.}
\]

The bracket is a finite **polynomial** in `r,h`, obtained by exact integration in `q`; it introduces no unevaluated geometric integral.

## Exact evaluation by harmonic sums

Write the polynomial numerator of the final rational integrand as `Σ C_(m,n) r^m h^n`, with 26 nonzero rational coefficients. The two-dimensional integral of a monomial is

\[
\int_0^1\!\int_0^1\frac{r^m h^n}{1-rh}\,dh\,dr
=\sum_{j\ge0}\frac1{(m+j+1)(n+j+1)}
=\begin{cases}
\dfrac{H_n-H_m}{n-m},&m\ne n,\\[6pt]
\zeta(2)-H_m^{(2)},&m=n.
\end{cases}
\]

Expanding `1/(1-rh)` is justified by monotone convergence for each nonnegative monomial; the final signed sum has finitely many monomials, so linearity applies. Exact rational arithmetic gives

\[
\boxed{J=-\frac{3316139}{88200}+\frac{160}{7}\zeta(2)
=\frac{336000\pi^2-3316139}{88200}}.
\]

Finally, substitute into `p_(4,2)=24919/294000+(6/5)J` to obtain the theorem.

## Validation and limits

* `chronos_p42_exact_global_candidate.py`: SymPy exact polynomial/harmonic sum evaluation plus independent numerical 3D Gauss-Legendre cubature (`n=18,36,72`).
* `chronos_p42_exact_stdlib_certificate.py`: **independent** exact coefficient generation and harmonic sums using only stdlib `fractions`, without SymPy.
* `chronos_p42_two_dimensional_J_kernel.py`: exact rational `q` integration, algebraic antiderivative recurrence, 16 independent high-precision quadrature comparisons.
* `chronos_p42_null_coordinate_kernel_audit.py`: null-coordinate endpoint identities, exact normalization and 1997 rational branch checks.
* Existing dependency receipts: `chronos_p42_positive_dag_reduction.py`, `chronos_p42_N_DAG_exact.py`, and `chronos_p42_four_dimensional_angular_kernel_audit.py` have been replayed.

**PASS** here means exact symbolic/algebraic checks and reproducible computational cross-checks. **NOT_RUN:** Lean axiom audit. **NOT_ESTABLISHED:** originality relative to the complete literature; external peer review. **REPOSITORY:** research checkpoint committed to draft PR #1375; no merge or main-branch changes. Run `python3 research/event_first/p42_exact_20261121/run_p42_chain.py` on the exact PR revision for repository-native replay.

