# Chronos–URF–RR: exact geometric envelopes for the first-born location

**Date:** 2026-11-11. **Status:** PROVED (finite-poset and probabilistic arguments); COMPUTATION_PASS (bounded rational checks); LEAN NOT_RUN; Minkowski uniform-tail sampling OPEN. No independent priority or novelty claim. No repository state changes performed by the certificate.

## 1. Assumptions

Let \(D\) be a finite-volume, non-atomic causally ordered spacetime domain, with normalized volume measure \(\mu\). Draw \(N\ge2\) iid uniform events and choose a uniformly random linear extension of their induced causal order. Condition on a distinguished event at \(z\), where

\[
S=S(z)=\mu(J^-(z)\cap D), \qquad F=F(z)=\mu(J^+(z)\cap D), \qquad 0\le S+F\le1.
\]

Let \(h_N(z)\) be the density of the position of the **first** event under the joint sprinkling/linear-extension law with respect to \(\mu\). By exchangeability, \(h_N(z)=N\Pr(z\text{ is first}\mid\text{one event fixed at }z)\).

## 2. Two-sided geometric envelope

Define \(p=F/(1-S)\) for \(S<1\). Then

\[
\boxed{
(1-S)^{N-1}\sum_{j=0}^{N-1}p^j
\;\le\; h_N(z)\;\le\;
(1-S)^{N-1}\bigl(1+(N-1)p\bigr).
}
\]

The expressions are continuous at \(p=1\) by defining the sum in the obvious way. The lower and upper bounds are exact at \(N=2\):

\[
\boxed{h_2(z)=1-S(z)+F(z).}
\]

For \(N=3\), the difference of the geometric upper and lower envelopes equals

\[
U_3(z)-L_3(z)= F(z)\,[1-S(z)-F(z)].
\]

### Proof

For a realized poset containing a distinguished event \(x\), the event can appear first only if it is minimal. Write \(f\) for its number of strict successors. The finite-poset insertion-window and upper-set shuffle bounds give

\[
\frac{1}{N-f}\le\Pr(x\text{ first}\mid P)\le\frac{1+f}{N}
\]

whenever \(x\) is minimal, and zero otherwise.

Conditional on the geometric position \(z\), the other \(N-1\) iid points lie independently in the past (probability \(S\)), future (probability \(F\)), or spacelike/incomparable part (probability \(1-S-F\)). Conditional on no past point, \(f\sim\mathrm{Bin}(N-1,p)\), and that conditioning occurs with probability \((1-S)^{N-1}\).

The upper bound follows from \(\mathbb E[1+f\mid\text{minimal}]=1+(N-1)p\).

For the lower bound, use

\[
\mathbb E\!\left[\frac{N}{N-f}\right]
=\sum_{j=0}^{N-1}p^j,
\]

where the identity follows from \(1/(N-f)=\int_0^1 t^{N-f-1}\,dt\) and the binomial theorem. Multiply by the minimal-event probability. QED.

**Limits:** The upper-set shuffle bound follows by conditioning on extensions internal to the strict-future upper set and its complementary lower ideal. Valid interleavings form an increasing event in the distributive lattice of binary shuffles; the earliest future-element position is increasing. Uniform shuffles are positively associated (Harris/FKG). Consequently the expected first future position in a uniform extension of \(P\setminus\{x\}\) is at least that in a random shuffle, \(N/(f+1)\). The insertion formula then yields the stated upper bound. This proof does not assume that the geometry-conditioned linear-extension law is uniform in the candidate set.

## 3. Four-dimensional Minkowski specialization

Normalize the Alexandrov interval between \(p=(0,\mathbf0)\) and \(q=(1,\mathbf0)\). Null radial coordinates \(u=t+r, w=t-r\) satisfy \(0<w<u<1\). Normalized volume density is

\[
12(u-w)^2\,du\,dw,\quad S=(uw)^2,\quad F=[(1-u)(1-w)]^2.
\]

The upper envelope gives a rigorous spatial bound for every measurable region \(A\):

\[
\Pr(X_1\in A)\le \int_A \bigl[(1-S)^{N-1}+(N-1)F(1-S)^{N-2}\bigr]d\mu.
\]

For the future-null coordinate strip \(1-\varepsilon\le u\le 1\), \(0<\varepsilon\le1/2\), \(N\ge3\), use \(F\le(1-u)^2\), \((u-w)^2\le u^2\) and the Gaussian integral to obtain

\[
\boxed{\Pr(U(X_1)\ge1-\varepsilon)\le
\frac{6\sqrt\pi}{\sqrt{N-2}}\left[\varepsilon+\frac{(N-1)\varepsilon^3}{3}\right].}
\]

For any \(\varepsilon_N=o(N^{-1/6})\), this probability tends to zero. This is **a thin-strip exclusion theorem**, not a limit law for \(U(X_1)\), and it is **not** a proof of causal-profile sampling stability. For finite \(N\), the displayed upper bound can exceed one and should then be truncated to one.

## 4. Reproducibility

Source `chronos_first_birth_geometric_envelope_20261111.py`:

- Exactly enumerates all \(3^{N-1}\) past/future/incomparable assignments for six rational parameter pairs, for \(N=2,\ldots,6\); verifies the explicit lower and upper expressions with `fractions.Fraction`. **30/30 PASS**.
- Verifies exact collapse of bounds to \(h_2=1-S+F\).
- Evaluates integrated envelopes over the 4D null-coordinate triangle by deterministic midpoint quadrature as a separate numerical sanity check, not a rigorous integral certificate.
- Evaluates future-null-strip probability upper bounds, including regimes where they are weak or trivial.

Observed global 4D envelope integrals (150-grid midpoint quadrature):

| N | Lower | Upper |
|---:|---:|---:|
| 2 | 0.99997069 | 0.99997069 |
| 3 | 0.96854467 | 1.00854381 |
| 4 | 0.93711784 | 1.02279620 |
| 8 | 0.84015854 | 1.11054396 |
| 16 | 0.72508844 | 1.34116030 |

This widening demonstrates that the current envelopes do **not** prove normalization-level concentration or a spatial first-birth limit. The analytical two-sided inequalities are nevertheless valid.

## 5. Exact open boundary

The ratios of linear-extension counts depend on relations *among* future and incomparable candidates, not merely on the past/future volume fractions. The geometric envelope is therefore insufficient for an asymptotic first-birth density. In particular, even knowing the first-birth density would not settle the iterated large-prefix Minkowski order-profile limit.

**NEXT:** Condition on the full geometry of the successor cone and prove a sharpened rank inequality with an asymptotically nontrivial normalized spatial envelope; otherwise seek a direct profile-drift bound. No Lean verification, Git merge or independent mathematical review has been performed.