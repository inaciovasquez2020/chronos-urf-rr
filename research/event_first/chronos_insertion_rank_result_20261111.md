# Chronos–URF–RR: exact insertion-window rank marginals

**Date:** 2026-11-11. **Scope:** finite-poset combinatorics. **Proof:** elementary and unrestricted. **Lean:** NOT_RUN. **Four-dimensional Minkowski prefix limit:** OPEN.

## Theorem 1 — exact rank-inclusion via deletion and insertion

Let `P` be a finite poset of `N` elements, `x ∈ P`, and `LE(P\{x})` the set of linear extensions of the deleted poset. For each extension `τ`, number its elements `1,...,N−1` and define

- `A_x(τ) = max_{y<x} rank_τ(y)`, with maximum of an empty set `0`;
- `B_x(τ) = min_{x<y} rank_τ(y)`, with minimum of an empty set `N`;
- `r_x(τ)=B_x(τ)−A_x(τ)`.

Every predecessor of `x` precedes every successor of `x` in the deleted poset. The insertion positions of `x` that produce linear extensions of `P` are precisely the integers `A_x(τ)+1,...,B_x(τ)`.

Consequently,

`e(P) = Σ_{τ∈LE(P\{x})} (B_x(τ)−A_x(τ))`.

Under a uniform random linear extension of `P`, the probability `q_n(x)` that `x` belongs to the first `n` positions is

`q_n(x) = [Σ_τ max(0, min(n,B_x(τ))−A_x(τ))] / [Σ_τ (B_x(τ)−A_x(τ))]`.

This holds for **every** `1≤n≤N`, including nonminimal elements. The numerator and denominator are counts of distinct valid linear extensions; thus the identity is exact.

For a minimal event, `A_x≡0`, so with `R_x(τ)=B_x(τ)`:

`q_n(x)= E_{τ uniform LE(P\{x})}[min(n,R_x)] / E_{τ uniform LE(P\{x})}[R_x]`, and

`Pr(x is first)=1/E[R_x]`.

Here `R_x` is the position of the earliest strict successor of `x` in `τ`, or `N` if `x` has no successors.

## Theorem 2 — first-birth bound from successor count

For minimal `x`, let `U(x)={y:x<y}`. Since all elements before the first successor lie outside `U(x)`, `1≤R_x(τ)≤N−|U(x)|`. Hence

`1/(N−|U(x)|) ≤ Pr(x is first) ≤ 1`.

This bound is tight for isolated elements and elements below every other element. It does not establish nontrivial large-N selection asymptotics for typical 4D sprinklings; in particular, it can be only `~1/N` for an event near a null boundary with few strict successors.

## Theorem 3 — successor-set dominance among minima

Let `x,y` be distinct minimal elements and assume `U(y)⊆U(x)`. Then for every `1≤n≤N`,

`q_n(x)≥q_n(y)`.

Proof by injection: given a linear extension with `y` in the first `n` positions and `x` outside, swap the positions of `x` and `y`. All successors of `y` must originally occur after `x` because `U(y)⊆U(x)`. The swap preserves all precedence constraints and places `x` within the first `n` positions while moving `y` outside. This injects the event `{y in prefix, x not}` into `{x in prefix, y not}`, proving the inequality. The same swap proves that `x` is at least as likely as `y` to be first.

**Limitation:** Minkowski spacelike-separated sprinkled minima generally have nonnested strict-future sets, so this is a partial ordering criterion, not a general comparison of all minimal-event weights.

## Exact independent regression

Source: `chronos_insertion_rank_certificate_20261111.py`.

- Exhaustive forward-edge configurations for `N=2,3,4,5`: **1,098** cases. Every forward-edge configuration is transitively closed before evaluation.
- Exact marginal comparisons between insertion-window formula and independent full linear-extension enumeration: **16,054**.
- Additional per-event bound and successor-dominance assertions: **PASS**.
- Python standard-library `Fraction`; no randomized input, network access, repository mutation, or dependencies.
- An initial implementation error erroneously assigned a positive first-birth probability to nonminimal elements. The implementation was repaired, and the entire test rerun **PASS**. The final script uses `numerator[1]/total`, not `len(LE(P\{x}))/total`, for general `x`.

## Mathematical boundary

The formula isolates the unresolved **earliest-successor-rank distribution** in random 4D Minkowski posets after deleting a candidate minimal event. Controlling this rank distribution *under the geometry and size-biased extension law* would control first-birth weights and could support a later prefix-statistic limit theorem. A universal finite-poset bound alone cannot prove the iterated Minkowski uniform-subset limit.

**Novelty:** NOT_ESTABLISHED. Linear-extension ideal-lattice and rank methods are known; see De Loof, De Meyer, De Baets, *Exploiting the Lattice of Ideals Representation of a Poset* (2006), DOI 10.3233/FUN-2006-712-309, and Brightwell and Łuczak, *Order-Invariant Measures on Fixed Causal Sets* (2012), DOI 10.1017/S0963548311000721. This report claims only the derivation and verification within the present investigation, not priority.

**Research status:** FINITE THEOREMS PROVED; COMPUTATION_PASS; ASYMPTOTICS OPEN; LEAN NOT_RUN; INDEPENDENT REVIEW OPEN; GRAVITY OPEN.