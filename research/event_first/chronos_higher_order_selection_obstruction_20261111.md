# Chronos–URF–RR: exact four-event successor-correlation obstruction

Date: 2026-11-11. STATUS: finite-poset statement **PROVED**; exact bounded test **COMPUTATION_PASS**; 4D geometric realizability **PROVED**; uniform-tail Minkowski limit **OPEN**. Lean verification NOT_RUN. Independent mathematical review OPEN.

## Target

The exact N=3 first-birth density has a correction involving a three-event causal-cone overlap. Determine whether this level of causal-overlap data can also determine the first-birth probability of a distinguished event for N=4.

## Theorem — irreducible additional order information at N=4

There exist two four-event causal posets P,Q and a distinguished minimal event x such that they agree on:

1. The number of strict predecessors, strict successors, and events incomparable with x: respectively (0,2,1).
2. The number of ordered overlap witnesses (z,y) with z incomparable to x, x<y, z<y: exactly 1.

Nevertheless, under a uniformly random linear extension,

- Pr_P(x is first) = 3/5;
- Pr_Q(x is first) = 2/3.

The gap is **1/15**. Hence those first-order and three-event overlap counts do **not** determine the N=4 first-birth law on each realized causal set.

## Explicit witnesses

Label vertices (x,z,a,b)=(0,1,2,3).

- P has the order relations x<a, x<b, z<a, and no others.
- Q has x<a, x<b, z<a, b<a, and their transitive consequences; z and b remain incomparable.

For P, the valid natural extensions are (x,z,a,b), (x,z,b,a), (x,b,z,a), (z,x,a,b), and (z,x,b,a), giving 3/5 first-x probability.

For Q, they are (x,z,b,a), (x,b,z,a), and (z,x,b,a), giving 2/3.

The overlap witness in both is (z,a); adding b<a changes the first-birth probability despite not creating a new overlap witness involving an event incomparable to x.

## Minkowski realizability

These are not merely abstract forbidden order types. They are both strictly realizable in 1+1-dimensional Minkowski spacetime, hence also in 3+1 dimensions by setting the other spatial coordinates to zero.

Use the common Alexandrov interval with tips p=(-10,0), q=(15,0), and coordinates (t,r):

- x=(0,0), z=(0,2), a=(5,1) for both.
- In P choose b=(4,-3).
- In Q choose b=(2,-1).

All relations and incomparabilities are strict; consequently open neighborhoods of the four coordinates retain the same induced poset. Each witness has **positive probability** in an iid volume-uniform four-event sprinkling of a sufficiently large 4D diamond.

Important limitation: this does not establish whether the *integrated spatial first-birth density* h_4(x) can be reduced to a specially chosen collection of lower-dimensional geometric integrals. It proves only that the realized-poset first-birth probability cannot be reconstructed from the listed local counts.

## Independent finite verification

Standalone `chronos_higher_order_selection_obstruction_20261111.py` checks the two examples with independent full-permutation linear-extension enumeration; verifies the integer Minkowski inequalities; exhaustively iterates 284 distinguished forward-edge DAG configurations for N=2,3,4 and their transitive closures. This is a bounded, dependency-free standard-library computation; it does not test an N->infinity theorem.

## Consequence / next use

Attempting to extend the N=3 overlap correction to general N solely by reusing the scalar pair-cone statistic is **insufficient at the realized-poset level**. One must retain successor-order relationships, e.g. the earliest-successor-rank distribution (or a higher-order conditional geometry functional).

The sharp open goal remains a uniform-N bound on the expected first-successor insertion rank for geometrically conditioned minimal points. Neither this N=4 result nor any finite enumeration establishes Minkowski uniform-tail sampling stability or gravitational dynamics.

Source background: Brightwell & Łuczak (2012), *Order-Invariant Measures on Fixed Causal Sets*, DOI 10.1017/S0963548311000721; De Loof, De Meyer & De Baets (2006), *Exploiting the Lattice of Ideals Representation of a Poset*, DOI 10.3233/FUN-2006-712-309.