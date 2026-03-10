# Short-Cycle Symmetric-Difference Gap

## Status

This is the single remaining unproved lemma required for full Cyclone closure.

---

## Lemma

Let \(G\) be a bounded-degree graph with maximum degree \(\Delta\).  
Let \(C_1,C_2\) be simple cycles with identical local signatures under
\(\mathrm{FO}^k\) radius-\(R\) neighborhood types.

Define the symmetric difference

\[
D = C_1 \oplus C_2 .
\]

Prove that every connected component of \(D\) is a simple cycle of length
bounded by a constant \(L=L(k,\Delta,R)\).

---

## Required Consequences

If proved, this yields:

1. bounded symmetric-difference components,
2. short-cycle decomposition,
3. basis-signature injectivity,
4. bounded cycle-overlap rank,
5. full Cyclone closure.

---

## Exact Remaining Task

Show that local edge agreement on all \(k\)-vertex windows forces any
disagreement component of \(C_1 \oplus C_2\) to remain inside a bounded-radius
tube and therefore have uniformly bounded length.

