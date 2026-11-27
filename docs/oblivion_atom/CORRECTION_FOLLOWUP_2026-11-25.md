# Mathematical erratum — 2026-11-25

Base: `32e6697f7f31fe21352d36687389197a77141940`.

## [chronos/Logic/PSH_k_Delta.tex](../../chronos/Logic/PSH_k_Delta.tex)

The uniform bound on sizes of pebble-equivalence classes is false. For every $n\ge3$, $C_n$ has degree two and is vertex-transitive, so all $n$ vertices have the same pointed type even at unrestricted quantifier rank. Finiteness of the number of types never implies bounded sizes of their classes.

## [docs/oblivion_atom/cycle_local_rigidity.tex](../../docs/oblivion_atom/cycle_local_rigidity.tex)

The constant global span bound and cycle-rank-to-type-divergence theorem are false. The connected vertex-transitive graph $C_m\square C_m$ for even $m\ge6$ has degree four, one rooted type, and at least $m^2/4$ independent unit-square boundaries supported in radius-two balls.

## [docs/oblivion_atom/theory/fo_k_cycle_invariance.tex](../../docs/oblivion_atom/theory/fo_k_cycle_invariance.tex)

The lemma is false for unrestricted $k$. For $k=1$, rooted radius-one balls in $K_3$ and $P_3$ (root at the middle vertex) have the same one-variable graph type but cycle ranks one and zero. Even with a named root constant, one variable cannot detect adjacency between distinct nonroot vertices. Take the disjoint union to realize both roots in one degree-two graph. Rooted graph isomorphism is a sufficient replacement hypothesis.

## [docs/oblivion_atom/theory/fo_k_cycle_invariance_strong.tex](../../docs/oblivion_atom/theory/fo_k_cycle_invariance_strong.tex)

The implication from finite-variable equivalence to rooted graph isomorphism is false. For $k=1$, take the roots of a triangle and the middle of a three-vertex path in their disjoint union, with $R=1$, $r=2$. Both balls have three vertices, with two nonroot neighbors of the root. One-variable formulas (even with a named root constant) cannot compare the two distinct nonroot vertices. Their radius-one balls have different cycle ranks. Rooted isomorphism suffices instead; an adequate variable budget must be proved separately.

## [manuscripts/scoped_universality/Scoped_Universality_and_Cycle_Rigidity.tex](../../manuscripts/scoped_universality/Scoped_Universality_and_Cycle_Rigidity.tex)

The unrestricted graph cycle-rigidity lemma is false: $C_m$ is vertex-transitive, and its cycle rank is one, while the intended overlap rank grows linearly on the vertex-transitive degree-four toroidal grids $C_m\square C_m$ (even $m\ge6$), because the definition permits self-intersections $C\cap C=C$ and hence contains the entire cycle space. This refutes the graph-level implication, not by itself a typed CNF-specific variant. The claimed depth equivalence is not established: a per-step split bound and progress condition require separate hypotheses, and sublinear rank need not mean bounded rank. Fixed-variable logic does not supply a fixed Gaifman radius independent of quantifier rank. No universal SAT depth bound is certified.

Historical statements are preserved. These are paper counterexamples and proof-gap notices, not new Lean certificates. No unrelated theorem or PDF is reclassified.
