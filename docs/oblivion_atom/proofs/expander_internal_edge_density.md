# Expander Internal Edge Density

## 1. Setup

Let (G=(V,E)) be a finite (d)-regular graph.

Assume (G) is an (\varepsilon)-edge-expander:

[
\forall S\subseteq V,\quad |S|\le |V|/2
\Rightarrow
|\partial S|\ge \varepsilon |S|.
]

Let (v\in V) be a root vertex.

Define BFS layers

[
L_r(v)={u\in V:\mathrm{dist}(v,u)=r}.
]

Define the radius-(R) ball

[
B_R(v)=\bigcup_{r=0}^R L_r(v).
]

---

# 2. Tree Benchmark

A tree with (|B_R|) vertices has exactly

[
|B_R|-1
]

edges.

Any additional edge creates a cycle.

Define

[
E_{\text{int}}(R,v)=|E(B_R(v))|.
]

Define excess edges

[
E_{\text{ex}}(R,v)=E_{\text{int}}(R,v)-( |B_R(v)|-1 ).
]

Then

[
E_{\text{ex}}(R,v)=\beta_1(B_R(v)).
]

---

# 3. Expansion Constraint

Let

[
S=B_R(v).
]

Edge expansion implies

[
|\partial S|\ge \varepsilon |S|.
]

Total degree inside (S):

[
d|S|=2E_{\text{int}}(R,v)+|\partial S|.
]

Therefore

[
E_{\text{int}}(R,v)=\frac{d|S|-|\partial S|}{2}.
]

Substitute the expansion bound:

[
E_{\text{int}}(R,v)\le\frac{d-\varepsilon}{2}|S|.
]

---

# 4. Internal Edge Density (Target)

For expanders, BFS layers eventually intersect.

These intersections create internal edges among vertices of similar distance.

The goal is to prove existence of constants

[
\alpha>0,\quad R_0>0
]

such that

[
E_{\text{int}}(R,v)\ge (1+\alpha)|B_R(v)|.
]

---

# 5. Expander Internal Edge Density Lemma (Target)

Fix (d\ge3) and (\varepsilon>0).

There exist constants

[
\alpha>0,\quad R_0>0
]

such that for every finite (d)-regular (\varepsilon)-expander (G), every vertex (v), and every radius

[
1\le R\le R_0\log_{d-1}|V|,
]

[
|E(B_R(v))|\ge (1+\alpha)|B_R(v)|.
]

---

# 6. Consequence

Using

[
\beta_1(B_R(v))=|E(B_R(v))|-|B_R(v)|+1,
]

the lemma implies

[
\beta_1(B_R(v))\ge \alpha(d-1)^R.
]

---

# 7. Role in Oblivion Chain

[
\text{Expansion}
\Rightarrow
\text{Internal Edge Density}
\Rightarrow
\beta_1(B_R)
\Rightarrow
CORR_R(G)
\Rightarrow
FO^k\text{ type diversity}.
]

---

# 8. Status

| Component                    | Status    |
| ---------------------------- | --------- |
| expansion inequality         | proven    |
| edge accounting              | classical |
| empirical collision evidence | verified  |
| deterministic density bound  | open      |

The lemma represents the final deterministic combinatorial ingredient required to close the expander rigidity chain.

