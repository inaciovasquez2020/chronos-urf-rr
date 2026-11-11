# CSG no-go and finite projectivity audit (2026-11-11)

Status: PROVED — positive Minkowski 2+2 probability, exact N=3 uniform-extension prefix discrepancy. COMPUTATION_PASS — exact rational enumeration and strictly separated Minkowski boxes. Large-N uniform-extension profile OPEN. Lean NOT_RUN. Independent novelty NOT_ESTABLISHED.

## Primary no-go theorem and crucial scope

Nicholas Georgiou and Graham Brightwell, "Continuum limits for classical sequential growth models", Random Structures & Algorithms 36 (2010), 218–250, DOI 10.1002/rsa.20278, https://nicholasgeorgiou.webspace.durham.ac.uk/wp-content/uploads/sites/199/2021/04/contlim.pdf .

Theorem 1.6: if a sequence of classical sequential growth models has an induced-sampling continuum limit, it is an almost-semiorder. Theorem 1.5 implies asymptotic exclusion of the induced 2+2 and 3+1 patterns (Figure 1).

Four-dimensional Minkowski sprinklings have strictly positive induced 2+2 probability: in the normalized unit-duration diamond, use spacetime cube centers (t,x,y,z)
a=(2/5,-1/5,0,0), b=(11/20,-1/5,0,0),
c=(2/5,1/5,0,0), d=(11/20,1/5,0,0).
Give each cube coordinate half-width eta=1/100. Within pairs a<b,c<d, time gap >=0.13 whereas 3D displacement <=0.02sqrt(3); cross-pairs are spacelike because x-separation >=0.38 while time difference <=0.17. All cubes are inside the unit causal diamond, whose 4-volume equals pi/24. Since each cube has probability p=24/(50^4*pi), the induced four-event Minkowski order has

Q4(2+2) >= 24*p^4 > 5.35e-23 >0.

Therefore full 4D Minkowski induced sampling cannot be a continuum limit of **classical sequential growth**.

IMPORTANT: A uniform natural extension of a finite, externally pre-sprinkled causal set has not been shown to satisfy CSG axioms. This existing no-go theorem does NOT refute the proposed uniform-extension construction or other non-CSG covariant growth.

## Exact fresh-sprinkling versus prefix mismatch

For a 4D unit Minkowski diamond, exact moments E[S]=1/20, E[S^2]=1/105, E[SF]=1/2100 give the unlabeled three-point order-type probabilities:

antichain 53/70; single comparable pair 33/175; fork 9/350; merge 9/350; full chain 1/350.

Independent exhaustive enumeration of linear extensions gives the conditional probability that the first two births are comparable: antichain 0; single edge 1/3; fork 0; merge 1; chain 1. Thus the uniform-extension first-two law for N=3 has

P(first two comparable) = 16/175,

whereas a fresh N=2 sprinkling gives 1/10. Their difference is exactly 3/350.

Therefore the finite N-indexed family obtained by taking the first two births of a uniform natural extension does not equal the fresh two-point Minkowski sampling law at N=3. This DOES NOT disprove an N->infinity subsequential projective limit or the later n->infinity Minkowski induced-profile limit.

## Reproduction and remaining obligation

The Python certificate chronos_csg_no_go_compact_20261111.py (stdlib only) checks the exact rational order-type probabilities, independently enumerates valid linear extensions, and tests the Minkowski 2+2 box margins and positive lower bound. An extended independent local certificate was also executed.

Decisive remaining goal: establish the model class and the actual limiting order-ideal sampling law, rather than assume that the finite uniform-extension prefix is a classical sequential-growth law or a fresh smaller sprinkling.

CSG MINKOWSKI LIMIT := EXCLUDED_BY_EXISTING_THEOREM.
UNIFORM_EXTENSION MINKOWSKI LIMIT := OPEN.
LEAN VERIFIED := NOT_RUN.
No production merge; only isolated staging research.
