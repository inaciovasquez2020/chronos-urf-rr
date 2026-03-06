# Cycle–Overlap Rigidity Theorem (Complete Statement)

## 1. Setting

Let (G = (V,E)) be a finite graph with maximum degree

[
\maxdeg(G) \le \Delta .
]

Fix integers

[
k \ge 2, \qquad \Delta \ge 2 .
]

Define the radius

[
R(k,\Delta) = \lfloor \log_{\Delta} k \rfloor - 1 .
]

Define the rigidity threshold

[
T(k,\Delta) = k^2 + 1 .
]

---

# 2. Rooted Balls

For a vertex (v \in V(G)), define the closed radius-(R) ball

[
B_R(v) = {u \in V(G) : d_G(u,v) \le R }.
]

Let

[
B_R(v)^{\text{ind}}
]

denote the induced subgraph on this vertex set.

---

# 3. Cycle Rank

For a finite graph (H), define

[
\beta_1(H)
==========

\dim_{\mathbb{F}_2} Z(H)
]

where (Z(H)) is the cycle space of (H).

Basic bound:

[
\beta_1(H) \le |E(H)|.
]

---

# 4. Quotient Cycle–Overlap Correlation Rank

Define the set of rooted ball isomorphism classes

[
I_R(G) =
{ [B_R(v)]_{\cong} : v \in V(G) }.
]

Define

[
CORR_R(G)
=========

\sum_{\tau \in I_R(G)}
\beta_1(\tau)^2 .
]

This definition collapses all vertex-translated copies of identical local
structures into a single contribution.

---

# 5. Ball Size Bounds

For graphs with degree at most (\Delta):

[
|V(B_R(v))| \le
\sum_{t=0}^{R} \Delta^t
\le 2 \Delta^R .
]

[
|E(B_R(v))|
\le
\Delta^{R+1}.
]

Hence

[
\beta_1(B_R(v)) \le \Delta^{R+1}.
]

---

# 6. Scott Sentence Completeness

**Theorem (Scott 1965).**

For every finite structure (A) of size (n) there exists a first-order
sentence (\varphi_A) using at most (n) variables such that

[
B \models \varphi_A
\iff
B \cong A .
]

Therefore if

[
k \ge |B_R(v)|
]

and two rooted structures share the same (FO^k) theory, they are
isomorphic.

---

# 7. Self-Consistency of (R(k,\Delta))

By construction

[
\Delta^{R(k,\Delta)+1} \le k .
]

Thus

[
|B_R(v)| \le k
]

for every vertex.

Therefore the Scott sentence theorem applies.

---

# 8. Cycle–Overlap Rigidity Theorem

**Theorem.**

Let (k,\Delta \ge 2).

Let

[
R = R(k,\Delta)
]

and

[
T = T(k,\Delta).
]

For every finite graph (G) with (\maxdeg(G)\le\Delta),

[
CORR_R(G) \ge T
\quad\Rightarrow\quad
G \text{ is not } FO^k_R\text{-homogeneous}.
]

---

# 9. Proof

Assume (G) is (FO^k_R)-homogeneous:

[
\tau_{k,R}(u) = \tau_{k,R}(v)
\quad
\forall u,v \in V(G).
]

### Step 1 — Isomorphism of balls

Since

[
k \ge |B_R(v)|
]

the Scott sentence theorem implies

[
B_R(u) \cong B_R(v)
\quad
\forall u,v .
]

Thus every vertex has the same local structure (B^*).

---

### Step 2 — Only one ball type

[
I_R(G) = { [B^*] }.
]

---

### Step 3 — CORR collapses

[
CORR_R(G) = \beta_1(B^*)^2 .
]

---

### Step 4 — Cycle rank bound

[
\beta_1(B^*) \le |E(B^*)|
\le \Delta^{R+1}
\le k .
]

---

### Step 5 — CORR bound

[
CORR_R(G)
\le k^2
< k^2 + 1
= T .
]

This contradicts the assumption

[
CORR_R(G) \ge T .
]

---

### Step 6 — Conclusion

Therefore

[
CORR_R(G) \ge T
\Rightarrow
G \text{ is not } FO^k_R\text{-homogeneous}.
]

∎

---

# 10. Corollary (FOᵏ Type Diversity)

[
CORR_R(G) \ge T
\Rightarrow
\exists u,v \in V(G)
\quad
tp_k(u) \ne tp_k(v).
]

Thus sufficiently large cycle-overlap rigidity forces **first-order type
diversity**.

---

# 11. Interpretation

The theorem establishes a structural principle:

```
cycle complexity of local neighborhoods
           ↓
increase of CORR invariant
           ↓
forced FOᵏ type diversity
```

This provides the logical bridge between:

* graph cycle structure
* finite model theory
* refinement complexity
* EntropyDepth rigidity mechanisms.

