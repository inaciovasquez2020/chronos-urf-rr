# Cycle–Local Rigidity (CLR) Dependency Map

Main theorem:

Cycle–Local Rigidity (CLR)

For fixed parameters

k, Δ, R

there exists

C(k,Δ,R)

such that any bounded-degree graph with identical FO^k
radius-R neighborhood types satisfies

COR(G) ≤ C(k,Δ,R)

---

# Dependency DAG

CLR
│
├─ Rank Bound
│
├─ Cycle Signature Bound
│   ├─ Vertex Signature Bound
│   │   └─ FO^k Type Finiteness
│   └─ Cycle Pumping Lemma
│
└─ Symmetric Difference Decomposition
    ├─ Edge Agreement Lemma
    │   └─ Local EF Extension Lemma
    │       └─ Gaifman Locality
    └─ Short Cycle Decomposition

---

# Purpose

This document records the logical structure of the CLR proof
for reviewers and Lean formalization.
