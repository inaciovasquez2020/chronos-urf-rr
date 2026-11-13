# Finite-stage CSG four-to-five chain-moment obstruction (2026-11-12)

**Status:** exact finite computational certificate, independently run on macOS; **Lean: NOT_RUN**; **independent human review: OPEN**. This is a finite-stage statement, **not** a continuum no-go theorem or a derivation of gravity.

## Precisely scoped claim

Use standard Rideout–Sorkin classical sequential growth (CSG) with nonnegative couplings \(t_0=1, t_i\ge0\). Let \(P_k^{(n)}\) be the expected density of induced \(k\)-element *total chains* among uniformly chosen \(k\)-subsets of the first \(n\) births, **not** the probability that the first \(k\) births form a chain. Set the *numerical target vector*

\[
q=(1/10,\;1/350,\;1/29400).
\]

The following claims are supported by the four exact certificates named below.

1. There is exactly one nonnegative triple \((t_1,t_2,t_3)\) satisfying \((P_2^{(4)},P_3^{(4)},P_4^{(4)})=q\). Existence and local uniqueness use a rational interval-Newton contraction check. Global uniqueness uses exact polynomial ideal equivalence and Sturm root/sign isolation.
2. For the unique triple, and **every** \(t_4\ge0\), the five-birth common-sample chain statistics satisfy
   \[
   P_2^{(5)}>19/100,\qquad P_3^{(5)}>1/50,\qquad P_4^{(5)}>7/10000.
   \]
   Each strictly exceeds its corresponding target.

Thus **the same fixed nonnegative CSG couplings cannot match these three common-sample targets at both \(n=4\) and \(n=5\)**. This does **not** exclude CSG continuum scaling, different sampling prescriptions, or non-CSG growth.

## Verification chain and provenance

Four standalone Python 3.9-compatible standard-library programs were run with Python assertions enabled on the user's Mac (terminal outputs supplied 2026-11-12). The analysis environment also reran the exact four programs on 2026-11-12. Record these source identities to prevent confusing certificates across revisions:

| Certificate filename | SHA-256 of tested source | Mac observed output |
|---|---|---|
| `rr_csg_common_four_exact_existence_py39.py` | `90e98f44fe874258c6089fbcf0054676a844b7e056c354a50f76dafb1d952319` | `INDEPENDENT_40_STATE_ENUMERATION := PASS`, `EXACT_INTERVAL_NEWTON := PASS` |
| `rr_csg_five_event_nonextension.py` | `4a897d7171220caee4f6fed0b2267d2c10d15ec6b914c1f93f9563c981e66ca3` | `N5_NATURALLY_LABELED_STATES := 357`, `T4_FREE_NONNEGATIVE := ALL_THREE_TARGETS_IMPOSSIBLE` |
| `rr_csg_global_uniqueness.py` | `179ee9e148bf0ea4c68a30709d1b6a7445966e73ea49d24bb15c1a07306eab03` | `GLOBAL_REAL_ROOT_COUNT := 10`, `NONNEGATIVE_COUPLING_CANDIDATES := 1` |
| `rr_csg_elimination_ideal_audit_py39.py` | `a995f13622a7ebee61dfb9a931c201c026d66aa4caf8456a0f46690ee13942e0` | `GROEBNER_IDEAL_EQUIVALENCE := PASS`, 26-element Buchberger basis, 325 pairs |

**Source availability:** All four exact certificate scripts are now included under `research/event_first/csg_certificates/`. The first is the Python 3.9-compatible replacement of the original generated script. Verify hashes and execute the entire suite at the PR HEAD; CI green alone does not replace independent mathematical review.

## Exact mathematical workflow

- Four-birth distribution: enumerate the 40 naturally labeled posets and compute CSG transition weights for admissible downsets using
  \[
  \lambda(\varpi,m)=\sum_{k=m}^{\varpi}\binom{\varpi-m}{k-m}t_k,\qquad \Pr(\text{new precursor})=\lambda(\varpi,m)/\lambda(n,0).
  \]
- The rational interval-Newton audit isolates the positive solution in a narrow box around \((0.00684064,0.02220106,0.17391102)\), with Jacobian contraction row bounds below \(1/50\).
- Global algebraic audit verifies that the original cleared numerator ideal equals the triangular ideal \(\langle P(x),y-Y(x),z-Z(x)\rangle\), with \(\deg P=16\). Rational Sturm isolation finds 10 real candidates, exactly one with nonnegative couplings. Denominator positivity is checked for the nonnegative domain.
- Five-birth audit enumerates 357 naturally labeled posets and writes each chain density for variable \(w=t_4\ge0\) as \((A_k+B_k w)/(C+D w)\). Exact box bounds show positive numerator coefficient gaps against each claimed strict lower bound for both constant and \(w\) coefficients.

## Non-claims and promotion gates

- **Finite mathematical result:** conditional on integrity of the independent exact arithmetic implementations and input conventions; computationally checked, not Lean-verified.
- **Physics:** 4D continuum emergence, persistent Minkowski sampling statistics at large \(N\), observational interpretation of chain targets, and gravitation are **OPEN**.
- **Nov-elty:** NOT ESTABLISHED. Independent mathematical review: OPEN.
- **Promotion requires:** verify the four SHA-256 source hashes, rerun at exact PR HEAD with assertions enabled, inspect dependencies and the complete diff, confirm required CI, and obtain independent mathematical scrutiny. A successful suite is computational verification, not a Lean proof.

## Prior-art comparison (2026-11-12)

**Directly relevant existing theorem:** N. Georgiou and G. Brightwell, *Continuum Limits for Classical Sequential Growth Models*, *Random Structures & Algorithms*, DOI [10.1002/rsa.20278](https://doi.org/10.1002/rsa.20278) (2010). [Author manuscript](https://nicholasgeorgiou.webspace.durham.ac.uk/wp-content/uploads/sites/199/2021/04/contlim.pdf), especially Definitions 1.2–1.3 and Theorems 1.5–1.6.

- Their finite-poset sampling definition uses uniformly chosen distinct induced subsets; this is materially the same uniform sampling convention used here.
- Theorem 1.5 states that for sufficiently large n every CSG distribution is close in expected pair-disagreement to a semiorder, uniformly in its coupling sequence. Theorem 1.6 gives the almost-semiorder constraint on continuum limits. Their paper concludes that Minkowski regions of dimension >= 2 do not arise as these continuum limits.
- **ALREADY ESTABLISHED (not novel here):** the general no-Minkowski-continuum conclusion for classical sequential growth under that notion of continuum convergence. The specific finite 4-to-5 chain-moment exact nonextension certificate is a different, much narrower claim; its *novelty is unestablished* pending a dedicated theorem-level prior-art review.
- Rideout and Sorkin, *Classical sequential growth dynamics for causal sets*, *Phys. Rev. D* 61, 024002 (1999/2000), DOI [10.1103/PhysRevD.61.024002](https://doi.org/10.1103/PhysRevD.61.024002), provide the underlying nonnegative CSG transition framework.

**Literature-screening limitation:** These references establish the core overlapping continuum claim but do not constitute an exhaustive search for the exact finite numerical certificate. A green program run or this preliminary screening is not independent mathematical review.
