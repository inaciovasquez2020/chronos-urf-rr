# Random-linear-extension order-ideal sampling audit (2026-11-12)

**Status:** exact finite combinatorics PROVED; scripts COMPUTATION_PASS in an isolated Python 3 environment; original Minkowski-sprinkling double limit OPEN; Lean NOT_RUN; independent review PENDING. This is not a physical spacetime emergence claim.

## Weighted-ideal identity

For a finite poset \(P\) and an order ideal \(I\) of size \(n\), a uniformly random linear extension \(L\) satisfies

\[
\Pr(\{L_1,\ldots,L_n\}=I)
=\frac{e(I)e(P\setminus I)}{e(P)}.
\]

Indeed, each extension having prefix set \(I\) consists of one extension of the induced order on \(I\), then one on its complement. The factorization requires the ideal condition.

For a random finite causal order \(P_N\), put \(c_2(I)=\#\{\text{comparable unordered pairs in }I\}/\binom n2\). The induced two-element prefix-sample distribution has total-variation distance to the four-dimensional Minkowski diamond two-point target equal to

\[
\left|\mathbb E\left[\sum_{I\lhd P_N,\ |I|=n}
\frac{e(I)e(P_N\setminus I)}{e(P_N)}c_2(I)\right]-\frac1{10}\right|.
\]

This is a scalar reduction because there are exactly two unlabeled two-element orders.

## Counterexample: finite full-sample statistics do not imply prefix stability

Let \(P_N=A_N\oplus B_N\) be the ordinal sum of two antichains with
\(a_N=|A_N|=\lfloor\alpha N\rfloor\),
\(\alpha=(1-\sqrt{4/5})/2\), and \(|B_N|=N-a_N\).
Then

\[
\Pr(\text{uniform full-sample pair comparable})
=\frac{a_N(N-a_N)}{\binom N2}\longrightarrow\frac1{10}.
\]

Every linear extension lists all \(A_N\) before any \(B_N\). For each fixed \(n\ge2\), all first \(n\) elements eventually belong to the antichain \(A_N\), so prefix-pair comparability is zero. Therefore

\[
\lim_{n\to\infty}\limsup_{N\to\infty}
d_{\mathrm{TV}}(R_{N,n,2},Q_2^{(4)})=\frac1{10}.
\]

**Scope:** This refutes unrestricted inference from matching full-sample pair statistics, **not** the limit for actual randomly sprinkled four-dimensional Minkowski diamonds.

## Isolated reproducible checks

- `tools/verifier/chronos_order_ideal_counterexample_20261112.py`: 15 exact formula checks against independently enumerated linear extensions (PASS); block example sizes 40, 100, 1000, 10000 (PASS).
- `tools/verifier/chronos_sprinkled_prefix_exact_20261112.py`: four-dimensional Minkowski diamond sprinklings with seed 20261112; exact integer linear-extension counts per realized poset. Finite averages:

| N | Trials | Full-pair comparability | First-two prefix comparability |
|---:|---:|---:|---:|
| 6 | 500 | 0.098800 | 0.080642 |
| 8 | 400 | 0.107054 | 0.078128 |
| 10 | 250 | 0.105333 | 0.073438 |
| 12 | 150 | 0.091919 | 0.061570 |
| 14 | 100 | 0.097692 | 0.059719 |

These finite averages do not prove an asymptotic trend, concentration theorem, or physical growth law. The floating-point sprinkling generator is not a certified exact sampler; exactness refers to finite poset extension counting once the relations are constructed.

## Open obligations

1. Prove or refute the actual random-linear-extension ideal sampling limit for the four-dimensional Minkowski sprinkling ensemble, beginning with k=2.
2. Formalize the infinite exchangeability + past-finiteness antichain lemma with precise probability hypotheses.
3. Formalize the Minkowski-height Poisson prefix-coupling bound under precise Poisson and dilation hypotheses.
4. Only after intrinsic covariant sampling stability: address emergent Lorentzian metric and curvature dynamics.

**Research gate:** no Lean verification, independent proof review, physical fifth-dimension inference, spacetime emergence, or gravitational field equation derivation claimed.
