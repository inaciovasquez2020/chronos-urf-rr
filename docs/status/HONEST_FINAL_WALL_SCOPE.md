# Honest Final-Wall Scope and Corrected Status

## Fixed definitions required before any unconditional Lean claim

Let
\[
I_R(G) := \operatorname{rank}_{\mathbf F_2}\!\Big(Z_1(G)\Big/\big\langle Z_1(B_R(v)) : v\in V(G)\big\rangle\Big).
\]

Only after fixing \(I_R(G)\) in this form do Statements (1)–(3) become mathematically definite.

---

## Unconditional graph-side target

Construct a zero-new-axiom Lean development proving:

\[
\forall k,\Delta,R\,\forall C\,\exists G\;
\big(\mathrm{FO}^k\text{-homogeneous}_R(G)\wedge I_R(G)>C\big),
\]

\[
\exists (G^+,G^-)\;
\big(\mathrm{EF}^{R}_{k}(G^+,G^-)\wedge I_R(G^+)\neq I_R(G^-)\big),
\]

\[
\neg\exists f\in \mathrm{FO}^k_R\text{-Def}\;
\forall G\;\big(I_R(G)=f(\operatorname{tp}^k_R(G))\big).
\]

### Honest status
These are the graph-side unconditional targets.

They require:
1. formal definition of \(I_R(G)\),
2. constructive regular-cover growth theorem,
3. constructive \(W(5)\) rank-separation witness,
4. formal transfer from EF/local-type agreement to non-definability.

---

## Conditional complexity-side target

Conditional on precise definitions of \(ED(P_n)\), normalization, and universality class:

\[
\mathrm{ED}(P_n)\ge \Omega(n\log n),
\]

\[
\forall A\in \mathrm{P}_{\det}\;\exists R_A\;\forall n\;
T_A(n)\ge \mathrm{ED}(P_n)/\operatorname{polylog}(n).
\]

### Honest status
Open unless and until:
1. \(ED(P_n)\) is fixed as a formal invariant,
2. the normalization theorem is stated and proved,
3. the universality embedding is stated and proved.

Without these definitions, no unconditional Lean theorem is presently well-typed.

---

## Corrected zero-axiom requirement

Interpret “zero axiom” as:

- no new user-declared `axiom`,
- no `sorry`,
- no `admit`,

in critical project modules.

This does not mean “axiom-free foundation,” since Lean/Mathlib already uses foundational principles.

---

## Corrected Final-Wall claim

“Finite combinatorial closure of the Final Wall” is not yet a theorem statement.

It must first be replaced by a precise finite theorem, e.g. a constructive bounded witness theorem or a finite obstruction-completeness theorem.

Until then:

\[
\textbf{Status: Open problem.}
\]

---

## Corrected irreducibility claim

The mathematically meaningful form is:

No proof of non-factorization may pass only through WL-equivalence or purely spectral coincidence; the separating invariant must survive explicit comparison with those methods and exceed their expressive power on the certified witness family.

### Status
Open unless formal comparison lemmas are supplied.

---

## Corrected external-verification claim

“Independent external verification with forced citation dependency” is not a theorem.
It is a publication/dependency objective.

### Status
Organizational objective, not Lean content.

---

## Current honest program

### Unconditional
1. Define \(I_R(G)\) formally.
2. Prove constructive unboundedness.
3. Prove explicit \(W(5)\) separation.
4. Derive FO\(^k_R\)-non-definability.

### Conditional / Open
1. EntropyDepth lower bound.
2. Universality / normalization embedding.
3. Final-Wall finite closure theorem.
4. Beyond-WL / beyond-spectral irreducibility theorem.
5. External forced-dependency outcome.

---

## Immediate Lean-critical obligations

1. `localTwoComplexH1Rank_growth`
2. `W5_rank_separation`
3. elimination of remaining critical `axiom` / `sorry` / `admit`
4. formal non-factorization over all FO\(^k_R\)-definable maps
5. formal \(ED\) lower bound and universality embedding after definitions are fixed
