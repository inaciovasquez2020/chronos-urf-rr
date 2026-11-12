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
| `rr_csg_common_four_exact_existence_py39.py` | `3935698e95936cade78d5a1e024ce21bca0e6b95fc961da2a26bf799f557b3bc` | `INDEPENDENT_40_STATE_ENUMERATION := PASS`, `EXACT_INTERVAL_NEWTON := PASS` |
| `rr_csg_five_event_nonextension.py` | `4a897d7171220caee4f6fed0b2267d2c10d15ec6b914c1f93f9563c981e66ca3` | `N5_NATURALLY_LABELED_STATES := 357`, `T4_FREE_NONNEGATIVE := ALL_THREE_TARGETS_IMPOSSIBLE` |
| `rr_csg_global_uniqueness.py` | `179ee9e148bf0ea4c68a30709d1b6a7445966e73ea49d24bb15c1a07306eab03` | `GLOBAL_REAL_ROOT_COUNT := 10`, `NONNEGATIVE_COUPLING_CANDIDATES := 1` |
| `rr_csg_elimination_ideal_audit_py39.py` | `a995f13622a7ebee61dfb9a931c201c026d66aa4caf8456a0f46690ee13942e0` | `GROEBNER_IDEAL_EQUIVALENCE := PASS`, 26-element Buchberger basis, 325 pairs |

**Important:** These four certificates are separately retained local research files and are **not included in this documentation-only change**; the SHA-256 fingerprints are not substitutes for shipping the underlying scripts. No new exact-head CI can validate the full theorem without their source. The repository snapshot and PR must be treated as *research documentation only* until the scripts and their tests are added.

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
- **Promotion requires:** include or independently reproduce all four certificate sources; verify their SHA-256 hashes, rerun at exact PR HEAD with assertions enabled, inspect dependency and provenance, review the resulting diff, and obtain independent mathematical scrutiny. Do not treat a green documentation CI run as full proof validation.
