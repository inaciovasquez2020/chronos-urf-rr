# Oblivion Atom — Proof Dependency Graph

This document records the dependency structure of the Cycle–Overlap Rank Rigidity proof.

---

## Main Theorem

Cycle–Overlap Rank Rigidity

FO^k_R-homogeneous(G)
⇒ rank_F2(M_R(G)) ≤ T

---

## Dependency Graph

Cycle Coding Lemma
        ↓
Finite Local Type Bound
        ↓
Cycle Signature Boundedness
        ↓
Row Normalization Lemma
        ↓
Cycle–Overlap Rank Rigidity
        ↓
FO^k Local Rigidity
        ↓
EntropyDepth Lower Bound
        ↓
Chronos Framework

---

## Logical Structure

1. Cycles are encoded by bounded tuples.
2. Bounded neighborhoods yield finitely many FO^k types.
3. Homogeneity collapses local types.
4. Therefore only finitely many cycle signatures exist.
5. Cycle signatures determine compressed matrix rows.
6. Thus cycle-incidence rank is bounded.

---

## Contrapositive

Large cycle-overlap rank
⇒ FO^k local type diversification.

---

## Program Context

This theorem provides the structural core of the Oblivion Atom program,
which feeds into the Chronos / EntropyDepth complexity lower bound framework.
