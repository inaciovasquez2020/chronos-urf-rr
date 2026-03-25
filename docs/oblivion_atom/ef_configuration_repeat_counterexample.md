# EF^k Configuration Repetition Counterexample

## Statement

The following pumping claim is false:

If an infinite Spoiler-winning k-pebble EF strategy revisits the same FO^k configuration type, then there exists a winning strategy supported in a bounded-radius neighborhood depending only on (k,Δ,R).

## Counterexample Family

Let

G_n = C_{2n}
H_n = C_{2n+2}

Both graphs are 2-regular.

Fix k = 2 and R < n.

### Local Structure

For every vertex v:

B_R(v) ⊂ C_{2n} ≅ P_{2R}
B_R(v) ⊂ C_{2n+2} ≅ P_{2R}

Hence all radius-R neighborhoods are isomorphic.

Therefore FO^2 configuration types depend only on pebble distance ≤ R.

All interior placements share the same configuration type.

### Repetition

Spoiler walking a pebble around the cycle revisits the same configuration type Θ(n) times.

Empirical experiments confirm:

distinct_configurations ≈ constant
max_repeat_count grows with n

### Radius Requirement

Any distinguishing strategy must expose the cycle length difference.

Minimum support radius:

ρ*(C_{2n}, C_{2n+2}) = Θ(n)

Thus no radius bound depending only on (k,Δ,R) exists.

## Failure Mechanism

Configuration type records only the G-side structure.

The full EF game state is

(ā, b̄)

Two visits to the same configuration type may correspond to different H-side placements.

Therefore configuration repetition does not imply state repetition.

## Correct Structural Principle

Define

ρ*(G,H,k) = min radius r such that some B_r(v) in G is FO^k-distinguishable from all B_r(w) in H.

Spoiler requires radius ≥ ρ*(G,H,k).

The quantity ρ* has no uniform upper bound as a function of (k,Δ,R).

## Implication for Oblivion Atom

Configuration repetition alone cannot localize EF witnesses.

Additional global structure is required.

The candidate invariant is cycle-overlap rank C_R(G).

Conjectural rigidity principle:

FO^k configuration repetition + bounded cycle-overlap rank ⇒ bounded witness radius.

Cycle families violate this because

C_R(C_{2n}) = Θ(n).

This identifies cycle-overlap rank as the missing structural invariant.
