# Chronos: first-choice collision inequality and a two-scale counterexample

Date: 2026-11-15. Status: PROVED conditional on the published Fishburn correlation theorem; finite exact checks COMPUTATION_PASS. No Lean verification. No Git mutation. Minkowski sampling limit OPEN.

## Definitions

For a finite N-element poset P, let e(P) be its number of linear extensions, and for each minimal x define q_x=e(P\setminus{x})/e(P) (the first-choice probability). Let c(P)=sum_{x minimal}q_x^2, the probability that two independent uniform extensions choose the same first vertex. Let p(P,2) be the probability the first two elements in one uniformly chosen extension are comparable.

## Theorem A (sharper first-choice collision inequality)

For N>2,

    0 <= p(P,2) <= [N*c(P)-1]/(N-1) <= c(P) <= max_x q_x.

The middle inequality follows from c(P)<=1. The first nontrivial inequality follows from the published Fishburn correlation inequality for distinct minimal x,y:

    e(P)*e(P\{x,y})/[e(P\{x})e(P\{y})] >= N/(N-1).

Condition on the first vertex x. Every second vertex incomparable with x must be a distinct minimal vertex y of P. Thus

    Pr(second incomparable | first=x)
      = sum_{y minimal, y!=x} e(P\{x,y})/e(P\{x})
      >= N/(N-1) sum_{y!=x}q_y
      = N/(N-1)(1-q_x).

Multiply by q_x, sum, and subtract from 1. The upper bound is sharp: for m disjoint chains of common length L, N=mL and q_x=1/m, and p(P,2)=(L-1)/(mL-1)=[N/m-1]/(N-1).

The all-four-element-poset exact regression checked 219 labeled partial orders, with 137 equalities and 82 strict cases; 290 disjoint equal-chain parameter checks also passed. A finite check is not the proof of the external Fishburn theorem.

**Sufficient condition for Minkowski first-two decay:** if, for P_N sampled by Minkowski sprinkling, max_x q_x ->0 in probability, then p(P_N,2)->0 in probability and E[p(P_N,2)]->0 by bounded convergence. The required geometric delocalization of q_x is OPEN. This conditional implication is not an estimate of q_x.

## Theorem B (first-two behavior does NOT determine the iterated double limit)

Fix an integer m>=2 and L>=1. Put Q_{m,L} equal to the disjoint union of m chains, each length L. Let H_0 be a two-element antichain, H_1 a two-element chain, and form P_{m,L,a}=H_a \oplus Q_{m,L} for a in {0,1}; N=mL+2.

The first two positions are necessarily the two H_a vertices. The remainder is a uniform multiset shuffle of the chain labels, and every pair of positions in that shuffle has probability (L-1)/(mL-1) to share a chain. Therefore, for 2<=n<=N,

    p(P_{m,L,a},n)
       = [a + binom(n-2,2) * (L-1)/(mL-1)] / binom(n,2).

Here p(P,n) is the expected proportion of comparable unordered pairs among the first n elements of a uniformly random linear extension.

For each fixed n and L->infinity,

    f_{m,a}(n) = [a + binom(n-2,2)/m]/binom(n,2).

Taking n->infinity gives 1/m for either a. However, the first-two limit is a (0 or 1), not 1/m. The global comparable-pair density is

    [a+2mL+m binom(L,2)]/binom(mL+2,2) -> 1/m.

Choosing m=10 yields two sequences with *both* global density and iterated prefix limit equal 1/10, but with first-two limits 0 and 1. This is a deterministic counterexample to the assertion that establishing the two-element-prefix benchmark 1/10 is necessary for the double limit to equal 1/10. It is NOT a Minkowski counterexample.

The exact finite formulas were independently tested by enumeration of all multiset shuffles for 12 small cases.

## Actual Minkowski-specific obstruction

The infinite-growth sampling problem concerns lim_{n->infinity} lim_{N->infinity} p_{N,n}; showing p_{N,2}->0 would not settle the outer limit. A credible proof needs controls that are uniform as n grows after N->infinity, or a limit law describing the complete prefix process. An extension-weight ratio for two-element ideals is a necessary ingredient for p_{N,2} alone, NOT sufficient to determine the full double limit. The weaker counts H_{N,j} and global comparable density cannot substitute for these extension weights, by prior explicit counterexamples.

## Validation

`chronos_first_choice_fishburn_sharp_audit_20261115.py`: exact 219 labeled four-poset check, 137 equality/82 strict; disjoint equal chains parameter checks PASS.

`chronos_double_limit_vs_two_prefix_certificate_20261115.py`: 12 exhaustive small multiset-word checks, exact rational formula PASS.

Lean NOT_RUN; new Git commit/push/merge NOT_PERFORMED.

Reference for external inequality: I. Pak and collaborators' *Linear Extensions of Finite Posets* survey, Section 7.1, theorem 7.1, cites [CP24b], especially its lower bound. See https://www.math.ucla.edu/~pak/papers/LEsurvey11.pdf . Its theorem is not new here.
