# Cycle–Overlap Visibility Lemma — Proof Tasks

Goal:

COR_R(G) ≥ T  ⇒  ∃ u,v : tp_3(u) ≠ tp_3(v)

Equivalently

COR_R(G) ≥ T  ⇒  WL² separates vertices.

---

## Remaining mathematical steps

### 1. Local overlap signature

Define

S_R(v) = multiset of cycles in B_R(v)

Prove:

large COR_R(G) ⇒ variation in S_R(v)

---

### 2. Pair-neighborhood lifting

Show that two vertices with different cycle-overlap
signatures induce different WL² pair colors.

---

### 3. WL² witness construction

Construct vertices u,v with

χ_WL²(u) ≠ χ_WL²(v)

using cycle overlap chains.

---

### 4. FO³ extraction

Apply

WL² ≡ FO³

to obtain

tp₃(u) ≠ tp₃(v).

---

## Current status

Empirical validation:
rr_n12000_d4_seed9

COR_R(G) = 649

WL² separation observed.

Formal proof: open.
