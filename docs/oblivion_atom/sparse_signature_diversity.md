# Sparse Incidence → Signature Diversity

## Lemma

Let

\[
M \in \mathbb F_2^{V \times m}
\]

be the incidence matrix of normalized supports.

Assume:

1. Column sparsity

\[
|supp(C_j)| \le B
\]

2. Row sparsity

\[
|\{j : v \in supp(C_j)\}| \le B
\]

3. Column independence

\[
rank(M) = m
\]

Then the number of distinct rows satisfies

\[
|\{\sigma(v)\}| \ge \beta m
\]

for constant

\[
\beta = \frac{1}{B^2}.
\]

---

## Proof Sketch

Each column introduces at most \(B\) nonzero rows.

Because rows also contain at most \(B\) ones, each row can support
only \(B\) columns.

Thus a column must introduce at least \(1/B\) new rows before
linear dependence becomes possible.

Counting argument:

\[
|rows| \ge \frac{m}{B^2}.
\]

Thus

\[
|\sigma(V)| \ge \beta m.
\]

