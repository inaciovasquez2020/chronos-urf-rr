# Strict Minkowski bounds for the four-event prefix probability

**Result:** ANALYTIC_PROOF_WITH_EXACT_RATIONAL_CERTIFICATE.  
**Exact p_(4,2): OPEN.** **Lean:** NOT_RUN. **Novelty:** NOT_AUDITED.

## Theorem

Let four points be sampled independently and uniformly from the unit
four-dimensional Minkowski causal diamond. Given their induced causal
poset, choose uniformly among its linear extensions. Let p_(4,2) be
the probability that the first two events in that extension are
causally related. Then

```text
157/2100 < p_(4,2) < 2603/29400.
```

This improves the non-strict endpoint inequalities in the existing
four-event rational-moment certificate. It does **not** evaluate p_(4,2).

## Proof via a realized motif

The 219 labeled four-element posets reduce to 16 isomorphism classes.
Use the deterministic ordering in
`tools/verifier/chronos_sampling_20261114/primary/chronos_four_point_chain_bounds_certificate.py`.
Write q_i for the Minkowski probability of class i.

The lower rational dual certificate has class-7 slack 1/30; the upper
rational dual certificate has class-7 slack 2/15. All remaining slacks
are nonnegative. The same 14 known moment/symmetry constraints therefore imply

```text
p_(4,2) >= 157/2100 + q_7/30
p_(4,2) <= 2603/29400 - 2*q_7/15.
```

Thus we need only prove q_7>0 **for actual Minkowski sampling**.
The following are exact rational coordinates (t,x,y,z), each listed integer
divided by 10000:

```text
P0 = (2032,   378,  1284,   24)
P1 = (6773,  2448, -1465,  797)
P2 = (9101,   443,  -319,  120)
P3 = (3821, -1888, -2040, -154)
```

For each i, 0<t_i<1 and
`||spatial_i||² < min(t_i²,(1-t_i)²)`, so each event lies
strictly inside the Minkowski diamond. An exact integer/rational
check of `(t_j-t_i)² - ||spatial_j-spatial_i||²` and time orientations
gives precisely the three strict relations

```text
P0 < P1, P0 < P2, P3 < P2
```

with every other pair spacelike. This strict poset is isomorphic to
class 7. All six pairs have nonzero time differences and nonzero
Minkowski-square gaps.

Moreover a coordinatewise rational cube of radius
`epsilon = 1/10000000` about each of the four points preserves the
diamond membership, time-order directions, and all causal/spacelike
comparisons. Indeed, the exact witness satisfies every diamond-square
margin >9 epsilon, every |time difference|>2 epsilon, and every
absolute pairwise Minkowski-square margin >17 epsilon. The conservative
perturbation bounds for the corresponding quadratic expressions are
<9 epsilon and <17 epsilon, respectively.

The sixteen-dimensional product of four such open cubes has positive
Lebesgue measure, hence positive probability under four independent
uniform diamond samples. Therefore q_7>0 and **both stated bounds
are strict**.

## Verification scope and open frontier

A separate stdlib-only local Python certificate verifies the finite
dual inequalities for all 16 classes, all 219 labeled posets, the
canonical class-7 witness, all exact rational geometric margins, and
the stated bound-slack values. Its run reported PASS; the full
standalone source is retained separately and is not committed in this
documentation-only addition.

The actual geometric value of q_7 (and the other residual motif
probabilities), exact p_(4,2), Lean verification, and independent
scholarly review remain OPEN. This is not a result about emergence
of spacetime or an observational prediction.
