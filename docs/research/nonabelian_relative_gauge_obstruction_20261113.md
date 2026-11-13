# Finite nonabelian local-to-global holonomy: relative-conjugation obstruction

**Status:** mathematically proved in the explicitly specified discrete model; independently enumerated for k=1,2,3,4; no Lean verification, novelty, or physical 5D claim.

## Observation model and exact theorem
Let a connected graph carry transports in a group H. A spanning-tree gauge fixes all tree edges to the identity, identifying global connection gauge classes with simultaneous conjugacy classes of a k-tuple of fundamental loop holonomies:
`H^k / H`. The residual gauge acts **diagonally**, using a single element of H.

In contrast, suppose the observer receives only the conjugacy class of EACH loop individually, with no overlap transition or shared root gauge. Then the observer sees `(H/conj)^k`. The resulting map from global classes need not be injective for nonabelian H.

For `H = S3`, let a=(12), b=(23). The tuples `(a,a)` and `(a,b)` have equal local conjugacy-class signatures, but are not simultaneously conjugate: equality of the two entries is invariant under diagonal conjugation. This is a concrete nonabelian failure of reconstruction, even though each loop is individually observed.

For k independent loops, by Burnside's lemma and centralizer sizes 6 (once), 3 (twice), and 2 (three times), the number of global S3 classes is

`N_global(k) = (6^k + 2*3^k + 3*2^k) / 6`.

The independent local signatures number `N_local(k) = 3^k`.

## Bounded exact validation
`python3 -B tools/holonomy/verify_s3_relative_conjugation.py` uses only the Python standard library, exact permutation composition, complete enumeration of 6^k k-tuples for k=1..4 (1554 total), independent orbit canonicalization, and a Burnside cross-check. Counts:

| k | Global classes | Local signatures |
|---|---:|---:|
| 1 | 3 | 3 |
| 2 | 11 | 9 |
| 3 | 49 | 27 |
| 4 | 251 | 81 |

The finite computation is not an unrestricted proof; the group-theoretic argument above establishes the scoped formula for arbitrary positive k.

## Relationship to existing Chronos formalization
The existing `lean/Oblivion/LocalityHolonomySeparation.lean` and `lean/Oblivion/URFChronosHolonomyDecoder.lean` prove a **Z/2 finite-cycle** observation obstruction with independently quotiented proper path windows. The present S3 example studies a different multi-loop observation model; it is NOT a Lean extension, does not derive the precise `FMT.Graph` interfaces, and must not be presented as if the formal decoder theorems cover it.

This independent-local signature may be realized by widely separated loops, each contained within its own observation region, where no region reveals their relative gauge identification. If overlap-compatible transition data or all raw transports in a common gauge are supplied, the collision may disappear.

**PHYSICAL_FIFTH_DIMENSION_NECESSITY := OPEN.** Gauge holonomy occurs in four-dimensional theories too. **NO POINCARE / P-VS-NP / CHRONOS GLOBAL CLOSURE IS CLAIMED.**

## Promotion
Keep as an experimental mathematical counterexample unless exact PR HEAD CI, scope/assumption review, and any required tests pass. Do not alter previous proof claims or overwrite historical receipts. The author's Mac working tree, local-only research, untracked files and unpushed commits were not inspected.
