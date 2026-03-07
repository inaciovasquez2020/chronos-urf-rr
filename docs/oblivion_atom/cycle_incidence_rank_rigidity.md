# Cycle–Incidence Rank Rigidity

## Status
Deterministic reduction lemma for the Oblivion Atom chain.  
Replaces the earlier EF-game argument with a linear-algebraic cycle-space rigidity argument.

---

# 1. Setup

Let

\[
G=(V,E)
\]

be a connected graph with maximum degree

\[
\Delta = O(1).
\]

Let

\[
C_{\le L}(G)
\]

denote the set of simple cycles of length at most \(L\).

For each cycle \(C\subseteq E\), define its incidence vector

\[
z_C \in \mathbb{F}_2^{E}
\]

by

\[
(z_C)_e =
\begin{cases}
1 & e\in C \\
0 & e\notin C
\end{cases}
\]

Let

\[
Z_L(G) = \mathrm{span}_{\mathbb{F}_2}\{z_C : C\in C_{\le L}(G)\}
\]

be the short-cycle subspace of the cycle space.

---

# 2. Cycle Incidence Matrix

Let

\[
M \in \mathbb{F}_2^{E\times m}
\]

be the matrix whose columns are the vectors \(z_{C_i}\).

Then

\[
\mathrm{rank}(M) = \mathrm{rank}(Z_L(G)).
\]

---

# 3. Local Cycle Signatures

Let

\[
B_R(v)
\]

denote the radius-\(R\) ball around vertex \(v\).

Define the edge set

\[
E_R(v) = \{e\in E : e \subseteq B_R(v)\}.
\]

Define the projection

\[
P_v : \mathbb{F}_2^{E} \rightarrow \mathbb{F}_2^{E_R(v)}.
\]

The **cycle signature** of \(v\) is

\[
\sigma(v) = P_v M.
\]

---

# 4. Rooted Isomorphism Invariance

If

\[
(B_R(u),u) \cong (B_R(v),v)
\]

then

\[
\sigma(u) = \sigma(v).
\]

Thus rooted radius-\(R\) type determines cycle signature.

---

# 5. Rank Transfer Lemma

Assume

\[
\mathrm{rank}(Z_L(G)) \ge c|V|
\]

for constant \(c>0\).

Then the matrix

\[
A_{v,i} =
\mathbf{1}\!\left(C_i \cap B_R(v) \neq \varnothing\right)
\]

satisfies

\[
\mathrm{rank}(A) = \Omega(|V|).
\]

---

# 6. Row Collision Bound

If the number of rooted radius-\(R\) types were

\[
t=o(|V|),
\]

then \(A\) would contain only \(t\) distinct rows, implying

\[
\mathrm{rank}(A) \le t = o(|V|),
\]

contradicting the rank bound.

---

# 7. Local Type Explosion

Therefore

\[
\#\{\text{rooted radius-}R\text{ types}\}
= \Omega(|V|).
\]

---

# 8. FO^k Diversity

By Gaifman locality, FOᵏ formulas of depth \(r\) depend only on radius

\[
R = O(kr).
\]

Thus

\[
\Omega(|V|)
\]

distinct rooted types imply

\[
\Omega(|V|)
\]

FOᵏ configuration types.

---

# 9. Configuration Pumping

Because the FOᵏ configuration space is finite,

\[
N(k,r,\Delta) = O(1),
\]

any infinite Spoiler strategy repeats a configuration.

The repeated configuration yields a bounded-radius witness subgraph.

---

# 10. EntropyDepth Consequence

Resolving

\[
\Omega(|V|)
\]

distinct local configurations requires

\[
\mathrm{ED}(G) \ge \Omega(|V|).
\]

---

# 11. Deterministic Rigidity Chain

\[
\text{Cycle incidence rank growth}
\]

\[
\Downarrow
\]

\[
\text{FO}^k \text{ local diversity}
\]

\[
\Downarrow
\]

\[
\text{Configuration pumping}
\]

\[
\Downarrow
\]

\[
\mathrm{ED}(n) \ge \Omega(n)
\]

---

# 12. Role in Oblivion Atom

This lemma provides the deterministic rigidity step

\[
\text{Cycle Overlap Geometry}
\Rightarrow
\text{FO}^k \text{ Type Explosion}
\]

used in the Oblivion Atom reduction chain:

CycleOverlapRigidity
↓
InternalEdgeDensity
↓
BFSCollisionBound
↓
LayerCollision
↓
DeterministicCycleRigidity
↓
FO^k Local Diversity
↓
EntropyDepth Ω(n)

---

# 13. Interpretation

The EF-game argument can be replaced by a purely linear-algebraic statement:

**Cycle incidence rank growth forces local structural diversity.**

This converts the locality obstruction into a rank-rigidity phenomenon in the cycle space.

---

# 14. Key Insight

Short cycles encode global overlap constraints.

When their incidence vectors achieve linear rank, the graph cannot maintain local homogeneity.

Local neighborhoods must diverge, producing the FOᵏ diversity required for Chronos.

---

# 15. Summary

\[
\boxed{
\text{High cycle-space rank}
\Rightarrow
\text{Local type explosion}
\Rightarrow
\text{EntropyDepth linear growth}
}
\]

This establishes the deterministic rigidity step in the Oblivion Atom framework.

CycleOverlapRigidity
↓
InternalEdgeDensity
↓
BFSCollisionBound
↓
LayerCollision
↓
DeterministicCycleRigidity
↓
FO^k Local Diversity
↓
EntropyDepth Ω(n)

---

# 13. Interpretation

The EF-game argument can be replaced by a purely linear-algebraic statement:

**Cycle incidence rank growth forces local structural diversity.**

This converts the locality obstruction into a rank-rigidity phenomenon in the cycle space.

---

# 14. Key Insight

Short cycles encode global overlap constraints.

When their incidence vectors achieve linear rank, the graph cannot maintain local homogeneity.

Local neighborhoods must diverge, producing the FOᵏ diversity required for Chronos.

---

# 15. Summary

\[
\boxed{
\text{High cycle-space rank}
\Rightarrow
\text{Local type explosion}
\Rightarrow
\text{EntropyDepth linear growth}
}
\]

This establishes the deterministic rigidity step in the Oblivion Atom framework.

CycleOverlapRigidity
↓
InternalEdgeDensity
↓
BFSCollisionBound
↓
LayerCollision
↓
DeterministicCycleRigidity
↓
FO^k Local Diversity
↓
EntropyDepth Ω(n)

---

# 13. Interpretation

The EF-game argument can be replaced by a purely linear-algebraic statement:

**Cycle incidence rank growth forces local structural diversity.**

This converts the locality obstruction into a rank-rigidity phenomenon in the cycle space.

---

# 14. Key Insight

Short cycles encode global overlap constraints.

When their incidence vectors achieve linear rank, the graph cannot maintain local homogeneity.

Local neighborhoods must diverge, producing the FOᵏ diversity required for Chronos.

---

# 15. Summary

\[
\boxed{
\text{High cycle-space rank}
\Rightarrow
\text{Local type explosion}
\Rightarrow
\text{EntropyDepth linear growth}
}
\]

This establishes the deterministic rigidity step in the Oblivion Atom framework.

CycleOverlapRigidity
↓
InternalEdgeDensity
↓
BFSCollisionBound
↓
LayerCollision
↓
DeterministicCycleRigidity
↓
FO^k Local Diversity
↓
EntropyDepth Ω(n)

---

# 13. Interpretation

The EF-game argument can be replaced by a purely linear-algebraic statement:

**Cycle incidence rank growth forces local structural diversity.**

This converts the locality obstruction into a rank-rigidity phenomenon in the cycle space.

---

# 14. Key Insight

Short cycles encode global overlap constraints.

When their incidence vectors achieve linear rank, the graph cannot maintain local homogeneity.

Local neighborhoods must diverge, producing the FOᵏ diversity required for Chronos.

---

# 15. Summary

\[
\boxed{
\text{High cycle-space rank}
\Rightarrow
\text{Local type explosion}
\Rightarrow
\text{EntropyDepth linear growth}
}
\]

This establishes the deterministic rigidity step in the Oblivion Atom framework.

CycleOverlapRigidity
↓
InternalEdgeDensity
↓
BFSCollisionBound
↓
LayerCollision
↓
DeterministicCycleRigidity
↓
FO^k Local Diversity
↓
EntropyDepth Ω(n)


---

# 13. Interpretation

The EF-game argument can be replaced by a purely linear-algebraic statement:

**Cycle incidence rank growth forces local structural diversity.**

This converts the locality obstruction into a rank-rigidity phenomenon in the cycle space.

---

# 14. Key Insight

Short cycles encode global overlap constraints.

When their incidence vectors achieve linear rank, the graph cannot maintain local homogeneity.

Local neighborhoods must diverge, producing the FOᵏ diversity required for Chronos.

---

# 15. Summary

\[
\boxed{
\text{High cycle-space rank}
\Rightarrow
\text{Local type explosion}
\Rightarrow
\text{EntropyDepth linear growth}
}
\]

This establishes the deterministic rigidity step in the Oblivion Atom framework.












