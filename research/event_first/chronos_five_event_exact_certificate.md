# Five-event naturally labeled causal growth: exact finite certificate

Status (2026-11-12): **FINITE EXACT COMPUTATION_PASS** in isolated Python runtime and independently reproduced as an abbreviated Mac certificate; **LEAN_VERIFIED: NOT_RUN**; **INDEPENDENT MATHEMATICAL REVIEW: SKIPPED AT REQUEST**. Source is a reconstructed certificate, not the missing original `chronos_finite_covariant_growth_audit.py`.

## Scope and distribution

Naturally labeled finite posets are represented by predecessor bitmasks `p[j]`, which include transitive closure. There are 357 distinct natural-label presentations on five births, partitioned into 63 unlabeled classes. Choose a terminal law supported on four unlabeled isomorphism classes:

| Five-event class | Class mass | Naturally labeled representatives |
|---|---:|---:|
| Antichain | 11/70 | 1 |
| One comparable pair plus three isolates | 5/7 | 10 |
| Three-element chain plus two isolates | 1/35 | 10 |
| Two disjoint two-element chains plus one isolate | 1/10 | 15 |

All other classes have zero mass. Each natural-label representation of a class receives equal mass (class mass divided by representation count). Exactly 36 terminal presentations have positive mass. Every supported prefix has mass equal to the sum of its terminal extensions.

Define `M_n(p)` to be its prefix mass and `w_n(p,a) = M_(n+1)(p+(a,))/M_n(p)` on positive-mass parents. Normalization follows from the prefix-mass sum and is checked exactly using `fractions.Fraction`.

The terminal **expected induced-subset densities**, not laws of fixed birth-prefixes, are:

- Comparable pair: `1/10`.
- Three-element chain: `1/350`.
- Induced four-element `2+2`: `1/50`.

The first two quantities are matched by *choice of the terminal distribution*, not predicted from dynamics. No asymptotic Minkowski limit or all-`N` consistent extension follows.

## Adjacent-birth covariance-square census

A directed square is represented by a naturally labeled `n`-parent and two downsets `a,b` such that both distinct birth orders `p+(a,b)` and `p+(b,a)` are valid natural-label histories. Equality of their terminal-prefix masses is checked exactly, including zero-mass histories. On positive-mass squares, the two products of conditional transition probabilities also agree.

| Parent size | All directed squares | Positive-mass directed squares | Positive-mass squares modulo swapping `a,b` |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 |
| 1 | 4 | 3 | 2 |
| 2 | 25 | 10 | 6 |
| 3 | 238 | 29 | 17 |
| **Total** | **268** | **43** | **26** |

The older staging report states **218** reachable covariance squares, but its original companion script is absent at the inspected staging HEAD. **218 is not independently reproduced** and may use an unidentified enumeration convention. Do not replace the count silently or claim that these two conventions coincide.

## Non-Bell-causal witness

For the antichain of size two, transition weights to an empty precursor and to precursor `{0}` are `247/315` and `34/315`. Removing its spectator to obtain a one-element parent yields weights `9/10` and `1/10`. Their cross-product difference is exactly `-59/3150`, so this finite law violates that spectator-independence test. This is not a theorem about all causal-set growth processes.

## Reproduction and limitations

Run `python3 -B research/event_first/chronos_five_event_exact_certificate.py` with Python 3.9+ (stdlib only). The certificate constructs 357 posets and all 63 unlabeled classes; computes the terminal mass, all three moments and all 268 square equalities with exact arithmetic; and prints `CERTIFICATE := COMPUTATION_PASS; FINITE_N_ONLY; LEAN_NOT_RUN` plus a detailed census. The `assert` statements must remain enabled (do not run with `python -O`).

This five-event construction is finite-horizon and relies on a deliberately chosen law. Infinite consistent extension, intrinsic order-invariant Minkowski sampling, spacetime emergence, gravity and novelty all remain **OPEN / NOT ESTABLISHED**. Independent review was skipped at the researcher's request; this certificate is **not** a global theorem-completion claim.
