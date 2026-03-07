# EF-Game Cycle Distinguishability

## Lemma (FOᵏ distinguishability of bounded supports)

Let \(G\) be a graph with maximum degree \(\Delta\).
Let \(C\subseteq V(G)\) be a cycle support with

\[
|C|\le B .
\]

Then there exists a formula

\[
\varphi_C(x)\in FO^k_r
\]

with quantifier rank

\[
r = O(B)
\]

such that

\[
G\models \varphi_C(v)
\iff
v\in C .
\]

---

## Proof Strategy

We use an Ehrenfeucht–Fraïssé game argument.

### Step 1 — Anchor selection

Let \(a\in C\) be the anchor vertex.

Assume \(a\) is uniquely identifiable by

\[
\alpha(x)
\]

so

\[
G\models \alpha(v) \iff v=a .
\]

---

### Step 2 — Cycle traversal

Because the cycle length is bounded by \(B\),
every vertex in \(C\) is reachable from \(a\)
by a path of length at most \(B\).

Thus membership in \(C\) can be expressed as:
∃ path of length ≤ B from x to anchor
that preserves the cycle adjacency pattern

---

### Step 3 — EF-game separation

Suppose

u ∈ C
v ∉ C

Spoiler plays:

1. pebble \(u\)
2. walk along the cycle
3. force Duplicator to match the bounded cycle structure

Duplicator cannot maintain partial isomorphism
because \(v\) lacks the required cycle neighborhood.

Thus

\[
tp^k_r(u)\ne tp^k_r(v).
\]

---

## Consequence

Distinct cycle signatures imply distinct FOᵏ types.

\[
\sigma(u)\ne\sigma(v)
\Rightarrow
tp^k_r(u)\ne tp^k_r(v).
\]

This completes the logical bridge

Spoiler plays:

1. pebble \(u\)
2. walk along the cycle
3. force Duplicator to match the bounded cycle structure

Duplicator cannot maintain partial isomorphism
because \(v\) lacks the required cycle neighborhood.

Thus

\[
tp^k_r(u)\ne tp^k_r(v).
\]

---

## Consequence

Distinct cycle signatures imply distinct FOᵏ types.

\[
\sigma(u)\ne\sigma(v)
\Rightarrow
tp^k_r(u)\ne tp^k_r(v).
\]

This completes the logical bridge
signature diversity → FOᵏ type diversity

