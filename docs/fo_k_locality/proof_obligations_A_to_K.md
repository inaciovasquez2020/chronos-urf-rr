# FO^k Locality / EF-Game Program  
## Proof Obligations Cluster (A–K)

This document enumerates the complete proof-obligation set required for the FO^k locality formalization used across the Chronos / EntropyDepth / Oblivion program. Each item corresponds to a concrete lemma or structural invariant required to close the EF-game → locality → rigidity pipeline.

All obligations are written so they can be directly mirrored into Lean declarations.

---

# A. Finite Neighborhood Type Enumeration

**Statement**

Let Δ,k,r ∈ ℕ be fixed.

For every graph G with maximum degree ≤ Δ and every vertex v ∈ V(G), the r-neighborhood:

\[
B_r(G,v)
\]

admits only finitely many FO^k types.

**Formal Form**

\[
|\text{FO}^k\text{-Type}_r(Δ)| < ∞
\]

**Lean Obligation**
lemma finite_fok_types
(k r Δ : ℕ) :
Fintype (FOType k r Δ)

---

# B. EF-Game Type Equivalence

**Statement**

Duplicator winning the k-pebble r-round EF game is equivalent to equality of FO^k formulas of quantifier rank ≤ r.

\[
G,v \equiv^{k,r} H,w
\]

iff

\[
\text{EF}_{k,r}(G,v,H,w)
\]

**Lean Obligation**

theorem ef_game_equiv_fok
(k r : ℕ)
(G H : Graph)
(v : G.V)
(w : H.V) :
DupWins k r G H v w ↔ FOTypeEq k r G H v w

---

# C. EF Strategy Transitivity

**Statement**

Duplicator strategies compose.

If

\[
G ≡^{k,r} H
\]

and

\[
H ≡^{k,r} K
\]

then

\[
G ≡^{k,r} K
\]

**Lean Obligation**

lemma dupwins_trans
(k r : ℕ)
(G H K : Graph)
(v : G.V)
(w : H.V)
(u : K.V) :
DupWins k r G H v w →
DupWins k r H K w u →
DupWins k r G K v u

---

# D. Partial Isomorphism Base Case

**Statement**

At r = 0 EF equivalence reduces to partial isomorphism.

\[
EF_{k,0}(G,H)
\]

iff

atomic formulas agree.

**Lean Obligation**

lemma ef_zero_round
(k : ℕ)
(G H : Graph)
(v : G.V)
(w : H.V) :
DupWins k 0 G H v w ↔ PartialIso G H v w

---

# E. Quantifier Extension Property

**Statement**

If Duplicator wins r rounds then for any Spoiler move there exists a response maintaining the invariant.

**Lean Obligation**

lemma dupwins_extend
(k r : ℕ)
(G H : Graph)
(v : G.V)
(w : H.V) :
DupWins k (r+1) G H v w →
∀ u ∈ G.V,
∃ t ∈ H.V,
DupWins k r G H u t

---

# F. Gaifman Locality

**Statement**

Every FO formula of rank r depends only on neighborhoods of radius

\[
R = 3^r
\]

**Lean Obligation**

theorem gaifman_locality
(φ : FOFormula)
(r : ℕ)
(G H : Graph)
(v : G.V)
(w : H.V) :
NeighborhoodIso (3^r) G H v w →
Eval φ G v = Eval φ H w

---

# G. Radius Reduction

**Statement**

Neighborhood isomorphism implies EF-equivalence.

\[
B_R(G,v) ≅ B_R(H,w)
\]

⇒

\[
G,v ≡^{k,r} H,w
\]

**Lean Obligation**

lemma neighborhood_iso_implies_ef
(k r : ℕ)
(G H : Graph)
(v : G.V)
(w : H.V) :
NeighborhoodIso (3^r) G H v w →
DupWins k r G H v w

---

# H. Local Type Stability

**Statement**

FO^k type is determined entirely by the local neighborhood type.

\[
Type_{FO^k}(v) = f(B_R(v))
\]

**Lean Obligation**

lemma fok_type_local
(k r : ℕ)
(G : Graph)
(v : G.V) :
∃ f,
FOType k r G v = f (Neighborhood r G v)

---

# I. Bounded Degree Growth Bound

**Statement**

In Δ-bounded graphs,

\[
|B_r(v)| ≤ 1 + Δ + Δ^2 + … + Δ^r
\]

**Lean Obligation**

lemma bounded_degree_ball
(Δ r : ℕ)
(G : Graph)
(v : G.V)
(hΔ : maxDegree G ≤ Δ) :
|Ball r G v| ≤ geomSeries Δ r

---

# J. Type Count Bound

**Statement**

Number of FO^k types grows at most exponentially in radius.

\[
T(r) ≤ C^{Δ^r}
\]

for constant C(k).

**Lean Obligation**

lemma fok_type_count_bound
(k Δ r : ℕ) :
∃ C,
typeCount k Δ r ≤ C^(Δ^r)

---

# K. Locality Theorem (Final Closure)

**Statement**

Every FO^k formula is determined by bounded neighborhoods.

\[
φ(G,v) = φ(H,w)
\]

whenever

\[
B_R(G,v) ≅ B_R(H,w)
\]

for

\[
R = 3^r
\]

**Lean Obligation**

theorem fok_locality
(k r : ℕ)
(φ : FOFormula)
(G H : Graph)
(v : G.V)
(w : H.V) :
NeighborhoodIso (3^r) G H v w →
Eval φ G v = Eval φ H w

---

# Dependency Structure

A → J
B → C
D → B
E → B
F → K
G → B
H → K
I → J
J → K

---

# Status

| Obligation | Status |
|------------|--------|
A | required |
B | required |
C | required |
D | required |
E | required |
F | required |
G | required |
H | required |
I | required |
J | required |
K | final theorem |

