# Independent CSG four-to-five box obstruction (2026-11-16)

**Status:** `COMPUTATION_PASS` for the finite rational coupling box; `CONDITIONAL` for the unrestricted four-event nonextension claim. **Lean:** `NOT_RUN`. **Global four-event uniqueness replay:** `INCOMPLETE_LOCAL_SOURCE`. **Novelty and independent mathematical review:** `OPEN`.

## Model and claim

Classical sequential growth (CSG) with `t₀ = 1` and nonnegative couplings. Write `x=t₁, y=t₂, z=t₃, w=t₄`. Let `P_k^(n)` be the expected density of induced total chains of size k among uniformly selected unordered k-subsets of the first n births, **not** the probability that the first k births form a chain.

Define the exact rational box

```
center = (684064/100000000, 222049/10000000, 17390282/100000000)
radius = 1/100000
B = [center₁±radius] × [center₂±radius] × [center₃±radius]
```

**Finite-box theorem:** For every `(x,y,z)∈B` and every `w≥0`:

- `P₂^(5) > 19/100 > 1/10`
- `P₃^(5) > 1/50 > 1/350`
- `P₄^(5) > 7/10000 > 1/29400`

The **pair-only** first inequality already contradicts retention of the four-event target pair statistic. This implication is **conditional** on the separate four-event global uniqueness proof establishing that every nonnegative triple matching `(1/10, 1/350, 1/29400)` belongs to `B`.

## Proof-certificate mechanism

Enumerate all 40 naturally labeled four-event posets and their 357 five-event successors, using nonnegative polynomial transition weights over `Q[x,y,z]`. The verifier constructs the exact numerator and denominator coefficient polynomials for

`P_k^(5)(x,y,z,w) = (N_{k,0}(x,y,z) + w N_{k,1}(x,y,z)) / (D₀(x,y,z) + w D₁(x,y,z))`.

It explicitly checks that every coefficient of all eight polynomial expressions is nonnegative; therefore lower/upper corner evaluations bound the expressions throughout the positive rational box. For thresholds `q=(19/100,1/50,7/10000)`, both `N_{k,j}(lower) - q_k D_j(upper)` are positive for `j=0,1`. Since `w≥0` and the denominator is positive, all three inequalities follow uniformly, with no upper bound on w.

## Exact numerical receipts — independent Python run

```text
CHAIN_2_CONSTANT_GAP := 1013063961174957153651626472909/78125000000000000000000000000000
CHAIN_2_T4_GAP := 554712718765127690458397/1562500000000000000000000
CHAIN_3_CONSTANT_GAP := 12079508639858923162655957049/9765625000000000000000000000000
CHAIN_3_T4_GAP := 84509112617067970841451/1562500000000000000000000
CHAIN_4_CONSTANT_GAP := 94323101994244517511163018059/976562500000000000000000000000000
CHAIN_4_T4_GAP := 20424394584429517986891/9765625000000000000000000
N4_STATES := 40
N5_STATES := 357
SYMBOLIC_ALL_COEFFICIENTS_NONNEGATIVE := PASS
UNIFORM_FIVE_EVENT_BOX_NONEXTENSION := COMPUTATION_PASS
GLOBAL_FOUR_EVENT_UNIQUENESS := NOT_REPLAYED
LEAN_VERIFIED := NO
NOVELTY := OPEN
```

Source for integration: [`rr_csg_independent_box_nonextension_20261116.py`](csg_certificates/rr_csg_independent_box_nonextension_20261116.py). A substantively equivalent standalone verifier passed in the research environment on November 16, 2026. **The newly committed GitHub source has not yet been rerun at its exact commit HEAD**, so the receipt is not presented as an exact-HEAD CI result.

## Four-event global nonnegative uniqueness — independent replay

An independent SymPy 1.14 exact-arithmetic calculation on 2026-11-16 reconstructed the 40 naturally labeled four-birth growth states, verified the three symbolic chain-moment numerators, computed a degree-16 lexicographic elimination polynomial, isolated all **10** real roots using exact Sturm/rational methods, and certified that **exactly one** reconstructed (t₁,t₂,t₃) triple is componentwise nonnegative. The unique triple is enclosed by the same rational box used above.

[Independent source verifier](csg_certificates/rr_csg_independent_global_uniqueness_20261116.py). This result is **COMPUTATION_PASS** for the independently executed algebraic algorithm. The newly committed GitHub source itself still requires exact-HEAD CI replay; no Lean proof or independent scholarly review is claimed. The original upstream archival scripts were not rerun on the user's Mac in this session.

Combining the independent four-event global uniqueness and the separately checked five-event box certificate gives a **computationally certified finite-stage CSG nonextension statement** for the specified moment target and all nonnegative couplings. This is not a continuum limit theorem, a gravity result, or a verified originality claim.

## Upstream dependency and non-claims

The prior four-event existence, elimination-ideal, and Sturm verification sources are in `research/event_first/csg_certificates/`: `rr_csg_common_four_exact_existence_py39.py`, `rr_csg_elimination_ideal_audit_py39.py`, and `rr_csg_global_uniqueness.py`. They were inspected at revision `166ec0e2749edb766f562fa6389c86b18cd6a8b7` but their full chain was **not replayed on the Mac during this integration**: the pinned revision and exact local scripts were unavailable. Existing archived receipts are not replaced.

No conclusion is drawn about continuum limits, spacetime emergence, gravity, arbitrary growth processes, or novelty relative to prior literature. No Lean proof or independent review is claimed. The research branch does not change the original CSG certificates.
