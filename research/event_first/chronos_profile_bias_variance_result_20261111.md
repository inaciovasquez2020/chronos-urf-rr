# Event-first spacetime — exact causal-profile variance decomposition

**Status:** PROVED (elementary finite probability identity); COMPUTATION_PASS (standalone exact-rational test); four-dimensional emergent dynamics OPEN. 2026-11-11.

**Repository staging:** `inaciovasquez2020/chronos-urf-rr`, isolated branch `research/event-first-audit-staging-20261111`. No Lean build or independent review claimed.

## Distinguish three probabilistic convergence claims

For a finite causal set `P` of size `N`, choose a uniformly random linear extension and retain its first `n` events as an order ideal `I`. Fix `k<=n`. Let `F_H(I)` be the fraction of `k`-element subsets of `I` that induce unlabeled order type `H`. Let `F(I)` be the finite vector of those frequencies, and let `Q` denote the analogous vector for a four-dimensional Minkowski causal diamond. Let `P` itself be random (for example from a Minkowski sprinkling).

**Annealed sampling convergence** means `E F(I) -> Q`; it is equivalent to convergence of the law of one uniformly sampled `k`-subset to `Q`. No concentration is required.

**Quenched sampling convergence** in probability means `F(I) -> Q` in probability, a stronger requirement. Because all profile coordinates lie in `[0,1]`, this is equivalent to `E ||F(I)-Q||_2^2 -> 0`.

Define conditional mean `m(P)=E[F(I)|P]` and unconditional mean `\bar m=E m(P)`. Independent prefix replicas `I,J` are sampled from independent uniform linear extensions conditional on the **same** `P`; independent environment replicas `P,P'` are sampled independently from the poset law.

Then the exact finite identity is

```
 E ||F(I)-Q||_2^2
   = (1/2) E ||F(I)-F(J)||_2^2
   + (1/2) E ||m(P)-m(P')||_2^2
   + ||\bar m-Q||_2^2.
```

This follows from two applications of the variance decomposition and the identity `E||Z-Z'||^2=2(E||Z||^2-||EZ||^2)` for iid finite-dimensional vectors.

Hence the stronger **quenched** target holds if and only if **each of the three nonnegative terms tends to zero**. For the original **annealed** target only the last term is necessary and sufficient.

## Rigorous failure of necessity of set-level replica overlap

For an `N`-element antichain, the first `n` elements of a uniformly random linear extension are a uniform `n`-subset. For two independent prefixes,

```
 E|I △ J|/n = 2(1-n/N).
```

For `n/N -> alpha < 1` this converges to `2(1-alpha)>0`. Nevertheless, *all* induced-order profiles `F_H(I)` are deterministic for every `k`: the antichain type has probability 1 and all other types probability 0. Hence the order-profile replica variance is exactly zero. Therefore set-level replica concentration is sufficient but not necessary for order-profile stability.

## Exact validation

Standalone source `chronos_profile_bias_variance_audit_20261111.py`:
- All forward-edge configurations with transitive closure through `N=5` (some posets repeated) and all relevant `2<=k<=min(n,3)` gave 7,514 exact-rational decomposition checks.
- Canonical unlabeled order signatures encode *both* edge directions under relabeling; an initial incomplete encoding was corrected before the successful run.
- The maximum observed conditional profile variance (Euclidean squared norm convention) was `384/625`; thus the test did not trivially pass with zero variance.
- A two-environment fixture (equiprobable four-element chain and antichain) has zero conditional replica variance, between-environment variance `1/2`, and zero annealed bias when the target is the equally weighted mixture.
- Antichain `N=20,n=10`: normalized set-level replica disagreement exactly `1`, while profile replica variance is zero.

These are finite results, not a new continuum theorem. No mathematical novelty claim or Lean verification is made.

## Decisive next use

Measure the **three terms separately** in a bounded Minkowski sprinkling experiment. A direct quantitative asymptotic theorem for the annealed sampling law requires control of `||E F(I)-Q||`, not of set-level replica disagreement. Proving it is still OPEN. A metric-free selecting dynamics and gravitational equations remain OPEN.