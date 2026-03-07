# Cycle–Overlap Visibility Lemma (Proof Outline)

## Goal

Show that for bounded-degree graphs there exists T such that

COR_R(G) ≥ T  ⇒  ∃ u,v : tp_3(u) ≠ tp_3(v)

Equivalently

COR_R(G) ≥ T  ⇒  WL² distinguishes vertices.

## Structure

1. Local Cycle Generators

Let

L_R(G) = {cycles contained in B_R(v)}

Define

COR_R(G) = dim_F2 span(L_R(G))

2. Overlap Graph

Define H with

V(H) = L_R(G)

(σ,τ) ∈ E(H) ⇔ σ ∩ τ ≠ ∅

3. Component Rank Decomposition

Empirically observed

COR_R(G) = Σ rank(C_i)

for overlap components C_i.

4. Cycle Visibility

For sufficiently large component rank,

cycle overlap patterns create distinguishable
pair-neighborhood structures.

These structures are visible to WL².

5. WL² ⇒ FO³

Using

WL^k ≡ FO^{k+1}

we obtain

WL² separation ⇒ FO³ type diversity.

## Status

Empirically validated on rr_n12000_d4_seed9.

Formal proof remains open.

