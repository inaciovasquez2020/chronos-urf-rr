# Final Wall — Audited Consequences

Status date: 2026-09-06

## 1. Raw Oblivion / Colap route

The original implication from fixed-radius FO-local homogeneity to bounded global cycle/overlap rank is not retained. The repository now contains a verifier-backed negative closure of the current unconstrained Colap rank surface, and the torus family gives the mathematical counterexample to the raw local-type-diversity principle.

## 2. Certified deterministic replacement

The surviving Lean-certified statement is a parity/query-depth lower bound. For a parity target supported on `d` independent clause coordinates, any deterministic adaptive query tree computing the target exactly must have depth at least `d`.

Under an additional compilation hypothesis that `rounds` rounds with per-round support budget `perRoundSupport` produce a query tree of depth at most their product, exact computation therefore forces

```text
d <= rounds * perRoundSupport.
```

The legacy repository `buildTranscript` is also certified to be input-independent, so it cannot supply the missing transcript/refinement compilation theorem.

## 3. Proof-complexity endpoint

For bounded-degree expander Tseitin contradictions, the audited unconditional proof-complexity endpoint is

```text
W(F_n) = Omega(n)
=>
Size_Res(F_n) = 2^{Omega(n)},
```

using the standard expansion width lower bound together with the Ben-Sasson--Wigderson size--width tradeoff.

## 4. Retired promotions

The following are **not** certified consequences and must not be quoted as established results:

- `ED(F_n) >= Omega(n)` from FO-locality or resolution width alone;
- a theorem that every locality-bounded refinement algorithm is blocked by incidence-cycle dependency extraction;
- unlifted `IC_mu(Search_Tseitin) = Omega(n)`;
- `IC_mu(Search_F) <= O(log L(F))` for arbitrary DAG-like resolution;
- unrestricted algorithmic-time, P versus NP, or Clay-problem closure.

## 5. Current boundary

A future EntropyDepth lower bound requires an explicit formal refinement class, a proved simulation from successful refinements into a proof-complexity object, and a quantitative inequality connecting the refinement cost to that object's lower bound. Until that bridge exists, EntropyDepth remains a boundary rather than a theorem.

Repository status:

- raw Oblivion route: refuted / negatively closed;
- deterministic parity-depth replacement: Lean-verified;
- communication/information route: audited and scope-corrected;
- expander-Tseitin resolution width/size lower bound: retained as the unconditional proof-complexity endpoint;
- EntropyDepth transfer: unproved.
