# Cycle–Overlap ⇒ FOᵏ Local-Type Diversity ⇒ EntropyDepth

## Status

Proposed structural bridge in the Oblivion / Chronos framework.

Goal: connect the **cycle-overlap rank invariant** of bounded-degree graphs to **FOᵏ local-type diversity**, which then feeds directly into the **EntropyDepth lower bound** used in Chronos.

This document records the precise definitions, statements, and logical chain.

---

# 1. Local Cycle Visibility

Let \(G = (V,E)\) be a finite graph with maximum degree \(\Delta\).

For \(v \in V\), denote the radius-\(R\) ball

\[
B_R(v) = \{u \in V : \mathrm{dist}(u,v) \le R\}.
\]

Let

\[
Z_1(H)
\]

denote the cycle space of a graph \(H\) over \(\mathbb{F}_2\).

Each ball contributes local cycles

\[
Z_1(B_R(v)).
\]

These embed into the global cycle space of \(G\).

---

# 2. Cycle–Overlap Rank

Define the inclusion map

\[
\Phi_R :
\bigoplus_{v\in V} Z_1(B_R(v))
\longrightarrow
Z_1(G)
\]

sending a local cycle to its embedding in \(G\).

---

## Definition (Cycle–Overlap Rank)

\[
\mathrm{COR}_R(G)
=
\dim_{\mathbb{F}_2}
\operatorname{Im}(\Phi_R)
\]

This measures how many **independent global cycles are locally visible** inside radius-\(R\) balls.

Interpretation:

* Small COR ⇒ cycles globally structured
* Large COR ⇒ many independent local cycle witnesses

---

# 3. FOᵏ Local Types

Let \(FO^k_R\) denote first-order logic with

* \(k\) variables
* formulas restricted to radius \(R\)

Two vertices have the same **FOᵏ local type** if

\[
(G,v) \equiv_{FO^k_R} (G,u)
\]

i.e. no \(k\)-variable formula of radius \(R\) distinguishes them.

---

## FOᵏ Homogeneity

A graph is **FOᵏ\(_R\)-homogeneous** if

\[
(G,v) \equiv_{FO^k_R} (G,u)
\quad \forall u,v.
\]

All radius-\(R\) neighborhoods look identical to \(k\)-variable logic.

---

# 4. Cycle–Overlap Rigidity Principle

The central conjectural rigidity statement:

---

## Conjecture (Cycle–Overlap ⇒ FOᵏ Diversity)

For every \(k,\Delta\) there exist constants

\[
R = R(k,\Delta), \quad T = T(k,\Delta)
\]

such that for any graph \(G\) with maximum degree \(\le \Delta\),

\[
\mathrm{COR}_R(G) \ge T
\]

implies

\[
G \text{ is not } FO^k_R\text{-homogeneous}.
\]

Equivalently,

\[
|\mathrm{Types}_{k,R}(G)| \ge 2.
\]

---

# 5. Intuition

FOᵏ logic can only observe bounded neighborhoods.

If every neighborhood has the same FOᵏ type, then:

* the possible local cycle structures are finite
* all global cycles must be combinations of finitely many templates

Thus

\[
\mathrm{COR}_R(G)
\le
C(k,\Delta,R).
\]

Large cycle-overlap rank therefore forces a breakdown of FOᵏ homogeneity.

---

# 6. Configuration Pumping Interpretation

In the Ehrenfeucht–Fraïssé \(k\)-pebble game:

FOᵏ homogeneity means Duplicator wins when comparing vertices.

Cycle-overlap diversity produces vertices

\[
u,v
\]

with

\[
(G,u) \not\equiv_{FO^k_R} (G,v).
\]

Spoiler wins using only local witnesses.

This gives the **Configuration Pumping Principle** used in the Oblivion framework.

---

# 7. From FOᵏ Diversity to Information Gain

Consider a SAT refinement algorithm operating on instance state \(X\).

Assume the algorithm is **FOᵏ-admissible**:

each refinement step depends only on bounded-radius structure.

Let

\[
T_v
\]

be the FOᵏ type of vertex \(v\).

Because the number of FOᵏ types is finite,

\[
|\mathrm{Types}_{k,R}| \le N(k,\Delta,R).
\]

Thus one refinement step can reveal at most

\[
\log N(k,\Delta,R)
\]

bits of information.

---

# 8. EntropyDepth Lower Bound

Let the instance entropy be

\[
H(X) = \Theta(n).
\]

Each FOᵏ refinement step reduces entropy by at most

\[
O(1).
\]

Therefore any algorithm must perform at least

\[
\mathrm{ED}(F)
\ge
\frac{H(X)}{O(1)}.
\]

Hence

\[
\boxed{
\mathrm{ED}(F) \ge \Omega(n)
}
\]

---

# 9. Patch-Rank Amplification

In affine XOR patch constructions used in Chronos:

* each patch contributes logarithmic entropy
* patches are weakly dependent

This yields the stronger bound

\[
\boxed{
\mathrm{ED}(F) \ge \Omega(n \log n)
}
\]

under Patch-Rank Rigidity.

---

# 10. Chronos Logical Chain

The structural pipeline is

Cycle overlap growth
↓
FOᵏ local-type diversity
↓
Configuration pumping
↓
Bounded information per refinement
↓
EntropyDepth lower bound


Result:

\[
\boxed{
\mathrm{ED}(F) \ge \Omega(n)
}
\]

and in patch constructions

\[
\boxed{
\mathrm{ED}(F) \ge \Omega(n\log n)
}
\]

---

# 11. Role in the Oblivion Framework

This statement forms the bridge

Oblivion Atom
↓
Cycle-overlap rigidity
↓
FOᵏ configuration pumping
↓
Chronos entropy accounting


Completing this bridge closes the structural path from **graph rigidity** to **algorithmic entropy barriers**.

---

# 12. Open Technical Tasks

Remaining proof obligations:

1. Bound COR under FOᵏ homogeneity

\[
FO^k_R\text{-homogeneous} \Rightarrow \mathrm{COR}_R(G) \le C(k,\Delta,R)
\]

2. Show expander / lift families achieve

\[
\mathrm{COR}_R(G) = \Omega(n)
\]

3. Connect FOᵏ diversity to bounded transcript information.

---

# 13. Relation to Existing Components

This lemma links:

| Component | Role |
|-----------|------|
| Oblivion Atom | cycle-overlap rigidity |
| Configuration Pumping | EF-game compression |
| FOᵏ locality | algorithmic restriction |
| EntropyDepth | computational lower bound |

Together they form the **Chronos barrier mechanism**.

---

# 14. Summary

The proposed rigidity principle is:

\[
\mathrm{COR}_R(G) \text{ large }
\Rightarrow
FO^k \text{ local diversity}
\Rightarrow
\text{bounded information per step}
\Rightarrow
\mathrm{ED}(F) \ge \Omega(n)
\]

which is the core obstruction used in the Chronos program.

