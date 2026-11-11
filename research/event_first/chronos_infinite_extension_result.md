# Chronos causal-growth: exact infinite projective extension of the five-event survivor

Status: PROVED mathematical construction, COMPUTATION_PASS for independent finite checks; Lean NOT_RUN. Repository unchanged.

Checkpoint: `inaciovasquez2020/chronos-urf-rr` PR #1347, `abef2b3e61dcb24a3ebb65ad0df7a76f63d4869f`.

## Definition and theorem

Let μ₅ be the *naturally labeled* five-event law from `chronos_finite_covariant_growth_audit.py`: unlabeled class masses 11/70 for the antichain, 5/7 for a single two-chain plus three isolated elements, 1/35 for a single three-chain plus two isolated elements, and 1/10 for two disjoint two-chains plus an isolated element. In each isomorphism class, assign equal probability to every natural labeling. Let μₙ (n≤5) be the prefix restriction of μ₅.

For n≥5 extend a causet deterministically by adjoining an event whose past is the entire current causet. Write `Cone(C)` for this one-point future extension. Let μₙ be the push-forward of μ₅ under `Cone^(n−5)` for n>5.

**Theorem.** (i) Every μₙ is a normalized finite measure on naturally labeled causal orders. (ii) Prefix deletion of birth n+1 recovers μₙ for all n, so these laws are infinitely projectively consistent. (iii) All natural labelings of a fixed unlabeled terminal causet have equal probability, so the construction is discrete generally covariant. (iv) The pair and triple-chain densities tend to 1, while induced 2+2 density tends to 0.

**Proof.** (i) and (ii) follow from the ordinary push-forward of μ₅ through the deterministic successor and from μ₅'s finite prefix marginals. For (iii), the first five-event histories were already covariant. For n≥6, the last event is a unique global maximum, so it must be last in every natural labeling. Removing it recursively reduces equality of histories to equality at n=5. The same argument proves all covariance-square identities, including those with zero transition mass. For (iv), write m=n−5. The five-event core has expected pair count 1, expected three-chain count 1/35, and expected induced 2+2 count 1/10, as checked by exact five-event enumeration. Every new event is comparable to all prior elements and every two added events are comparable. Consequently the expected numbers of these features in the full n-event causet are:

- Comparable pairs: `binom(n,2) − 9`.
- Three-chains: `binom(m,3) + 5 binom(m,2) + m + 1/35`.
- Induced 2+2 configurations: `1/10`.

Dividing by `binom(n,2)`, `binom(n,3)`, `binom(n,4)` gives the normalized expectations and the asserted limits. QED.

## Exact receipts

n | expected pair fraction | expected three-chain fraction | induced 2+2 fraction
---|---|---|---
5 | 1/10 | 1/350 | 1/50
6 | 2/5 | 9/175 | 1/150
10 | 4/5 | 569/1050 | 1/2100
20 | 181/190 | 17413/19950 | 1/48450
100 | 549/550 | 2814613/2829750 | 1/39212250

Independent script: `chronos_infinite_extension_audit.py`, Python standard library only, exact fractions, 43 adjacent-swap cases checked through n=10, and moment identities checked by direct enumeration at n=5..10.

## Interpretation and boundaries

The earlier description 'infinite projective consistency OPEN' for this specific five-event law is now superseded: an infinite extension exists. However, matching the desired 4D pair/triple/fork statistics at n=5, being infinitely consistent, and passing general covariance do **not** imply an acceptable continuum limit. The extension passes the consistency gates but fails the geometry gate decisively.

This does not prove that no other infinite extension of μ₅ can approach four-dimensional causal geometry. It provides an explicit counterexample to any claim that finite matching + infinite projectivity + discrete general covariance suffice.

No source files were modified and no Mac or Lean verification was run.