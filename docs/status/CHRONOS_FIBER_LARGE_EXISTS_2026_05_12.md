# Chronos Fiber Large Exists Lemma — 2026-05-12

Status: PROVED_COMBINATORIAL_LEMMA

Lean module:

- Chronos.Frontier.FiberLargeExists

Theorem:

- Chronos.Frontier.fiber_large_exists

Statement:

For finite types X and nonempty Y, if a map f : X -> Y satisfies

Fintype.card X >= Fintype.card Y * q ^ g

then there exists y : Y such that

Fintype.card {x : X // f x = y} >= q ^ g

Proof surface:

- handles q ^ g = 0 separately;
- constructs the explicit sigma-fiber equivalence;
- combines Fintype.card_sigma with Fintype.card_congr;
- bounds the finite sum of fibers;
- closes by contradiction using Nat.pred_lt.

Boundary:

This is a theorem-level combinatorial pigeonhole lemma only.

It does not prove RankRateGap.

It does not prove SemanticRankRateToFiberEntropySoundness.

It does not prove CountingFiberSeparation.

It does not prove FiberMassBalance.

It does not prove UniversalFiberEntropyGap.

It does not prove Chronos-RR.

It does not prove H4.1/FGL.

It does not prove P vs NP or any Clay-problem closure.
