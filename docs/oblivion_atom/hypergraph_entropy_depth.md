# Hypergraph FOᵏ Diversity → EntropyDepth

## Lemma

Let \(H=(V,\mathcal E)\) be a bounded-overlap gadget hypergraph
embedded in a bounded-degree graph \(G\).

If the system produces

\[
T_k(G)=\Omega(n)
\]

distinct FOᵏ local types, then any FOᵏ-admissible refinement process \(P\)
satisfies

\[
ED(P)=\Omega(n).
\]

---

## Argument

Local refinement rules only inspect bounded-radius neighborhoods.

Thus each refinement step can distinguish only \(O(1)\) FOᵏ types.

If

\[
T_k(G)=\Omega(n),
\]

then resolving all types requires

\[
\Omega(n)
\]

refinement steps.

Therefore

\[
ED(P)=\Omega(n).
\]

---

## Hypergraph Rigidity Chain

\[
\text{HyperedgeOverlap}
\Rightarrow
\text{RankGrowth}
\Rightarrow
\text{FO}^k\text{ Diversity}
\Rightarrow
\text{EntropyDepth}.
\]

---

## Unified Oblivion Atom

Combining both regimes:

Cycle regime:

\[
\text{CycleOverlap}
\Rightarrow
\text{EntropyDepth}.
\]

Hypergraph regime:

\[
\text{HyperedgeOverlap}
\Rightarrow
\text{EntropyDepth}.
\]

This yields the structural core of the **Oblivion Atom** principle.

