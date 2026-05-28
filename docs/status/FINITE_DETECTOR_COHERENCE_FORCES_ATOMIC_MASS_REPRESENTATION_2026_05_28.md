# Finite Detector Coherence Forces Atomic Mass Representation

**Status:** `FINITE_COHERENCE_THEOREM_SOLVED`

## Theorem

Let `Detector` be a type with decidable equality.  A finite detector extraction consists of

\[
m : Detector \to \mathbb{N},
\qquad
E : \operatorname{Finset}(Detector) \to \mathbb{N}.
\]

Assume:

1. `E ∅ = 0`.
2. If `A` and `B` are disjoint finite detector families, then
   \[
   E(A \cup B) = E(A) + E(B).
   \]
3. For every detector atom `d`,
   \[
   E(\{d\}) = m(d).
   \]

Then for every finite detector family `A`,

\[
E(A) = \sum_{d \in A} m(d).
\]

Consequently, two coherent finite detector extractions with the same atomic mass assignment are identical on every finite detector family.

## Proof

The proof is by finite-set induction on `A`.

For `A = ∅`, the claim is exactly empty-zero, together with the empty finite-sum identity.

For the induction step, write `insert a A` with `a ∉ A`.  The singleton `{a}` is disjoint from `A`, hence by disjoint additivity,

\[
E(\{a\} \cup A) = E(\{a\}) + E(A).
\]

Since `{a} ∪ A = insert a A`, singleton calibration gives

\[
E(insert\ a\ A) = m(a) + E(A).
\]

By the induction hypothesis,

\[
E(A) = \sum_{d \in A} m(d).
\]

Therefore

\[
E(insert\ a\ A)
=
m(a) + \sum_{d \in A} m(d)
=
\sum_{d \in insert\ a\ A} m(d).
\]

This proves atomic mass representation.

The uniqueness theorem follows immediately: if two coherent extractions have the same atomic mass assignment, both equal the same finite atomic sum.

## Comparison to Existing Formalization

Mathlib already supplies finite-set and finite-sum infrastructure.  This theorem is not a replacement for that infrastructure.  It is a domain-specific rigidity statement over a detector interface: the extraction operation is arbitrary at the outset and is forced into the atomic finite-sum form by coherence axioms.

This is weaker than full measure-theoretic uniqueness theorems such as Haar-measure uniqueness, because it is finite and natural-valued.  It is stronger than a local interface lemma, because it proves that no alternative coherent extraction can depend on ordering, regrouping, or finite blocking.

## Research Novelty

The novelty is the detector-interface rigidity formulation:

> local atom calibration plus finite disjoint additivity uniquely determines global extraction.

The result converts detector extraction from a chosen implementation into a forced invariant.  This matters because downstream gravity or mass-accounting bridges can use the extraction value without depending on the arbitrary presentation of active detectors.

## Harder Obstruction Removed

The removed obstruction is finite regrouping dependence.

Before this theorem, an extraction interface could appear to be locally calibrated while still leaving open whether different finite presentations of the same detector family produced different total extracted mass.  The theorem removes that possibility under explicit coherence axioms.

## Boundary

This artifact proves only a finite detector-coherence theorem.

It does not prove:

- physical detector-field extraction map;
- Einstein-matter PDE well-posedness;
- trapped-surface formation theorem;
- black-hole formation theorem;
- cosmic censorship proof;
- hoop conjecture proof;
- unrestricted `QL_CollapseGate`;
- unrestricted `UniversalBoundaryCompactness`;
- unrestricted `Chronos-RR`;
- unrestricted `H4.1/FGL`;
- `P vs NP`;
- any Clay problem.
