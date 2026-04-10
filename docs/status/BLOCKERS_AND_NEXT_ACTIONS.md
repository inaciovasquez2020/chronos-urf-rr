# Blockers and Next Actions

## Active blockers (unconditional graph-side closure)

The following two items are the only remaining constructive bottlenecks:

1. `localTwoComplexH1Rank_growth`
2. `W5_rank_separation`

All higher-level theorems reduce to these engines.

## Precise blocking statements

### Growth engine (required)
Constructively prove:
\[
\forall R\,\forall C\,\exists G\;(I_R(G)>C)
\]
with radius-\(R\) local uniformity sufficient for FO\(^k_R\)-homogeneity.

### Separation engine (required)
Constructively prove:
\[
\exists (G^+,G^-)\;
\big(
tp_k_R(G^+) = tp_k_R(G^-)
\wedge
I_R(G^+) \neq I_R(G^-)
\big).
\]

## Non-blocking layers (already reducible)

- Nonfactorization theorem
- Reduction schemas
- Specification completeness
- Dependency structure

These require no new mathematics beyond the two engines.

## Immediate executable actions

### Action 1 — Growth construction
Implement explicit regular-cover family:
- base graph with girth \(>2R\),
- \(r\)-sheeted cover,
- prove \(I_R(G_r)\to\infty\).

### Action 2 — Local tree lemma
Prove:
\[
\text{girth}(G) > 2R \;\Rightarrow\; B_R(v)\ \text{is a tree}.
\]

### Action 3 — Quotient-rank computation
Prove:
\[
I_R(G_r) = \beta_1(G_r)
\]
under local-tree condition.

### Action 4 — W5 construction
Encode explicit witness pair:
- construct \(G^+\), \(G^-\),
- prove local-type equality.

### Action 5 — Rank separation
Compute:
\[
I_R(G^+) \neq I_R(G^-).
\]

## Closure condition

Unconditional graph-side package is complete iff:

- both engines are constructive,
- zero `axiom` / `sorry` / `admit` in critical modules,
- Theorem A/B/C are packaged.

