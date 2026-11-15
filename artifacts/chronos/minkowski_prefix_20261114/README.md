# Minkowski two-point prefix / first-position collision certificates

Status: **FINITE COMPUTATION_PASS; ASYMPTOTIC OPEN; LEAN NOT_RUN**.

Repository: `inaciovasquez2020/chronos-urf-rr`
Base remote `main` commit at branch creation: `2ad482cfc2ae7ee633f6baf3aa530d3fbdd7eed7`.
Data provenance: generated research certificates and accompanying recorded outputs from November 14, 2026. Their historical receipts are not Lean proof certificates or independent mathematical review.

## Model and observables

A uniform permutation `p` of `0,...,n-1` encodes the two-dimensional order `i <_P j` iff `i<j` and `p[i]<p[j]`. Its linear extensions are counted by exact integer dynamic programming.

For any nonempty finite poset P with linear-extension count e(P), let
- `p_a = e(P-a)/e(P)` for minimal a.
- `C(P) = sum_a p_a^2`, the first-element collision probability of two conditionally independent uniform linear extensions.
- `A(P) = Pr(L_1 <_P L_2 | P)`, the two-prefix comparability probability.

The finite-poset reduction (using the published Fishburn/Chan–Pak minimal-element correlation inequality, with its hypotheses) is
`A(P) <= (n*C(P)-1)/(n-1) <= C(P)`, for n>=2.
These scripts test the integer-cleared inequality; **the scripts do not formalize or prove the published inequality**.

## Contents and verification

- `chronos_collision_exact_audit.py` and `chronos_collision_exact_results.txt`: enumeration n=2..8, output averages are rounded floating-point.
- `chronos_collision_n9_certificate.py` and `chronos_collision_n9_receipt.txt`: exact-integer extension counts and inequality check across all 9! = 362880 permutation orders; finite expectation accumulation uses floating-point.
- `chronos_2d_minima_counterexample.py` and receipt: chain plus isolated elements; exact Fraction checks for n=6,8,10,12.
- `chronos_balanced_shape_counterexample.py` and receipt: explicit permutation family with logarithmically many minima and Theta(sqrt(n)) height and width; checks finite instances. The asymptotic general-family claim is a mathematical argument, NOT kernel verified.
- `chronos_extreme_shape_tail_certificate.py` and receipt: exact rational combinatorial bounds `Pr(LIS>=k or LDS>=k) <= 2*binom(n,k)/k!`, alongside log10 floating-point approximations.

Run using Python 3.9+ with standard library only:
```sh
python3 -B chronos_collision_exact_audit.py
python3 -B chronos_collision_n9_certificate.py 9
python3 -B chronos_2d_minima_counterexample.py
python3 -B chronos_balanced_shape_counterexample.py
python3 -B chronos_extreme_shape_tail_certificate.py
```

## Validation boundary

The five scripts were rerun in an isolated environment here; n=9 output:
```
COUNT := 362880
FINITE_PREFIX_MEAN := 0.346922472444
COLLISION_MEAN := 0.502242804919
MAX_FIRST_PROB_MEAN := 0.588518009309
INVARIANTS := extension normalization and integer Fishburn bound PASS for every permutation
ASYMPTOTIC_CONCLUSION := OPEN
```

The two explicit counterexample families demonstrate that controlling only minimal-element count, or that count together with height and width of their natural orders of magnitude, does not imply deterministic collision decay. They do **not** refute decay under a uniform random permutation law.

**OPEN:** Prove or refute `E_{P_n}[C(P_n)] -> 0` for uniform random 2D permutation orders (and independently `E_{P_n}[A(P_n)] -> 0`). No 4D extension, Lean compilation, CI result or unrestricted spacetime sampling-stability theorem is asserted.

Publication: isolated research branch only; no merge to main. Mac authoritative working-tree status and repository-wide tests have NOT been inspected in this environment.
