# Chronos-RR: four-event series and Lean-import audit (2026-11-23)

**Scope:** Independently verified rational-series algebra and read-only GitHub source audit. This document is **not** a full `ChronosUrf` build receipt, a verification of the continuum Minkowski integral, or an audit of the Mac-only Codex Lean certificate.

## Repository identity and isolation

- Repository: `inaciovasquez2020/chronos-urf-rr`.
- GitHub inspection branch: `proof/gfe-corrected-generator-projector-20260814-070005` at `51997341796e6dd8f22a4e6dc2b70149f24ac812` (GitHub inspection, 2026-11-23).
- Subsequent Mac preflight verified local HEAD `605aca6330c7b834c09eae77275763b8a374f864` on the named branch. The live GitHub branch and local tracking ref were both `51997341796e6dd8f22a4e6dc2b70149f24ac812`; locally, the branch was 0 behind and 1 ahead. The local commit has not been published by this checkpoint.
- GitHub `main` baseline at inspection: `12c8854c398b96831eff05db3ffec6a35ba8d5f3`.
- `lean-toolchain`: `leanprover/lean4:v4.29.0`.
- `lakefile.lean`: `lean_lib Chronos` has root `Chronos`; `lean_lib ChronosUrf` has roots `Chronos.XorReduce`, `Chronos.EP2Bundle`, `Oblivion`, with `srcDir := "lean"`.
- Subsequent Mac preflight identified 13 intended tracked maintenance edits, two untracked four-event files, and 90 unrelated tracked `.venv` modifications, with zero files in the real Git index. The proposed 15-file diff was assembled using a temporary Git index; the `.venv` changes remain excluded and preserved.

## Independent exact series result

Let

\[
 t_n = \frac{18(2n^3+59n^2+583n+1933)}{7(n+5)^2(n+6)^2(n+7)^2(n+8)^2},\qquad n\ge0.
\]

**PROVED (ordinary mathematics; not Lean-verified):** The following partial-fraction identity holds as an identity in \(\mathbb Q(n)\):

\[
\begin{aligned}
 t_n={}&-\frac{374}{7(n+5)}+\frac{243}{14(n+5)^2}
 -\frac{162}{7(n+6)}+\frac{1143}{14(n+6)^2}\\
 &+\frac{486}{7(n+7)}+\frac{513}{14(n+7)^2}
 +\frac{50}{7(n+8)}+\frac{3}{2(n+8)^2}.
\end{aligned}
\]

Clearing the denominator and expanding in \(\mathbb Q[n]\) gives identical polynomial coefficient vectors (implemented with `fractions.Fraction` and polynomial multiplication, without a symbolic algebra dependency). The coefficients of the simple poles sum to zero. Consequently, with \(H_m=\sum_{j=1}^{m}j^{-1}\) and \(H_m^{(2)}=\sum_{j=1}^{m}j^{-2}\),

\[
 \sum_{n=0}^{\infty}t_n
 =\left(\sum_{j=5}^8 B_j\right)\zeta(2)
   -\sum_{j=5}^8\left(A_jH_{j-1}+B_jH_{j-1}^{(2)}\right).
\]

The rational sums are exactly \(\sum A_j=0\), \(\sum B_j=960/7\), and
\(-\sum(A_jH_{j-1}+B_jH_{j-1}^{(2)})=-3316139/14700\). Using the classical Basel identity \(\zeta(2)=\pi^2/6\),

\[
\boxed{\sum_{n=0}^{\infty}t_n=\frac{160\pi^2}{7}-\frac{3316139}{14700}.}
\]

The simple-pole limit follows because \(\sum A_j=0\) and \(H_{N+j}-H_{N+5}\to0\) for each fixed \(j\); the square-pole series converges absolutely. For a **rigorous numerical-tail bound**, the nonnegative coefficient comparison

\[
 2n^3+59n^2+583n+1933\le16(n+5)^3
\]

implies \(0<t_n\le(288/7)(n+5)^{-5}\) and, for any integer \(N\ge0\),

\[
0<\sum_{n=N}^{\infty}t_n\le\frac{288}{7}
\left(\frac1{(N+5)^5}+\frac1{4(N+5)^4}\right).
\]

**CONDITIONAL on the unverified geometric reduction in the supplied research note:** If

\[
 P(K_{2,2})+\frac3{9800}=\sum_{n=0}^\infty t_n,
\]

then the exact algebra establishes

\[
 P(K_{2,2})=\frac{160\pi^2}{7}-\frac{6632287}{29400}.
\]

If additionally the independent finite-poset continuum identity
\(p_{4,2}=P(K_{2,2})/5+24937/294000\) holds for the intended probability and normalization, then

\[
 p_{4,2}=\frac{32\pi^2}{7}-\frac{13239637}{294000}.
\]

**OPEN / NOT_RUN:** The original continuum integral, causal comparability normalization, physical probability interpretation, Lean proof of the infinite sum, and the external four-event Lean certificate. Verification of the algebra does **not** establish the integral-to-series equality.

### Reproduction (standard library only)

Run from the repository root after adding the accompanying file:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B tools/verifier/chronos_four_event_series_certificate.py
```

The executable asserts exact polynomial equality over rational coefficients, cancellation and harmonic-sum rational constants, the stated affine reduction, 128 exact rational finite instances, 80-term exact rational Machin-arctangent bounds on π (using alternating-series remainder), an independent 50-term exact rational partial-sum enclosure, and a 2,000-term high-precision numerical comparison enclosed by the stated analytic tail bound. `CONTINUUM_INTEGRAL_IDENTITY := NOT_VERIFIED` and `LEAN_COMPILATION_AND_AXIOMS := NOT_RUN` are intentional truthful statuses.

## Lean import triage

The previously reported Mac audit found 965 tracked Lean files and nine path-based unresolved import candidates. Independent GitHub tree/source inspection confirms the classifications below; it does not establish that every historical module is part of a Lake build target.

| Import candidate | Evidence and classification | In-scope consequence |
|---|---|---|
| `Chronos.Frontier.ZeroArityRepresentationInterface` | Expected source absent; importing `Chronos/Frontier/FinalCarrierObservationExtraction.lean` is at repository top-level (outside `srcDir := "lean"`). The artifact `artifacts/chronos/zero_arity_representation_interface.json` labels the representation target `FRONTIER_OPEN`. | Genuine open representation interface in another source tree, not the observed first `ChronosUrf` failure. |
| `Cyclone.SSKzIntegration` | Expected `lean/Cyclone/SSKzIntegration.lean` absent; importing `lean/Chronos/CycloneBridge.lean` exists. `Cyclone/SSKz.lean` is not an established drop-in replacement for `SSKz_integration`. | Isolated/legacy dependency, no valid alias yet. |
| `Lean` | Standard Lean toolchain module rather than a project source file. | Inventory false positive; not genuinely missing. |
| `Oblivion.CFI2Lift` | Absent under `lean/Oblivion`; six source importers. Expected interfaces include `TwoLift`, whereas the existing `CycloneTwoLift` is a different module containing references to other unresolved definitions. | Genuine dependency; restoring may require new mathematics. |
| `Oblivion.CycleSpace` | Absent under `lean/Oblivion`; four importers use `C1`, `Z1`, `boundary` and module ranks. | Genuine chain-complex definition/proof dependency. |
| `Oblivion.CycloneInvariant` | Absent under `lean/Oblivion`; imported by `Oblivion/CycloneWitness.lean`. | Genuine invariant dependency. |
| `Oblivion.FrontLemma` | Absent at this path; imported by `lean/ChronosUrfRr/Chronos/FrontImport.lean`; alternative `ChronosUrfRr.Oblivion.FrontLemma` exists. The alternative defines a different namespace and marked placeholder semantics. | Potential import typo in legacy wrapper, but type and claim audit required before edit. |
| `Oblivion.Graph` | Absent under `lean/Oblivion`; **nine direct importers**. Existing `ChronosUrfRr/Graph.lean`, `Oblivion/EFEquiv.lean`, and `Oblivion/CodeR.lean` contain separately declared, incompatible `Graph` interfaces, while `Oblivion/CycleDefs.lean` has a different namespaced graph. | **First known secondary-build blocker.** No safe universal alias/replacement established. |
| `chronos_urf_rr.Oblivion.FrontLemma` | Absent; imported by `lean/Chronos_urf_rr.lean`; uppercase `ChronosUrfRr.Oblivion.FrontLemma` exists. Lean module names are case-sensitive. | Historical root/namespace mismatch; not automatically in either configured Lake root. |

External/alias candidate `URF_Core.URF_Axioms_Core` appears in `urf-lean/SpectralGapWitness.lean`. The file is outside the configured `lean` source directory; status within the pinned `urf_core` dependency was **NOT_INSPECTED**. Do not count it as a confirmed missing source within `ChronosUrf`.

### Secondary blockers beyond the missing first module

The existing `lean/Oblivion/TreePathExtension.lean` uses edge tuple selectors on abstract `G.E`, and its `Connected.path_exists` destructuring does not match the `Connected := Nonempty V` definition in `ChronosUrfRr/Graph.lean`. `lean/Oblivion/CycleRank.lean` duplicates the top-level declaration `z1_card_formula`. `lean/Oblivion/CycloneTwoLift.lean` imports only `ChronosUrfRr.Graph` yet refers to `signedLift` and other declarations not defined in that module. These are **source-level risk findings**, not compiler-verified error receipts. Adding an arbitrary `Oblivion.Graph` would not justify promoting the target to PASS.

Dependency spine:

```
ChronosUrf (Lake target)
  -> Oblivion (root)
      -> Oblivion.CycloneSignedLift
          -> Oblivion.Graph [MISSING; first observed build failure]
          -> Oblivion.Beta1 -> Oblivion.Graph
          -> Oblivion.Ball -> Oblivion.Graph
          -> Oblivion.ClosedWalk -> Oblivion.Graph
      -> Oblivion.Tree -> Oblivion.Graph
      -> other historical Oblivion modules

Other source surfaces (not necessarily imported by the target):
  Oblivion.CycleSpace [MISSING] -> CycleRank, CycleBasisOmega, LocalCycleQuotient, CycloneRankInvariant
  Oblivion.CFI2Lift [MISSING] -> CFI/Duplicator/Rank/Witness modules
  Chronos.Frontier.ZeroArityRepresentationInterface [MISSING] -> root-level final frontier
  Cyclone.SSKzIntegration [MISSING] -> Chronos.CycloneBridge
```

## Validation and promotion status

| Check | Status | Basis |
|---|---|---|
| Exact rational partial fractions and harmonic constants | `COMPUTATION_PASS` and mathematical derivation | New standalone certificate executed in an isolated sandbox |
| Exact rational π enclosure and independent exact partial-sum interval | `COMPUTATION_PASS` | 80 alternating arctangent terms per series, 50 exact rational series terms, analytic tail bound |
| High-precision sum with explicit tail bound | `COMPUTATION_PASS` | 2,000 terms, 70-digit decimal arithmetic, analytic upper bound |
| Primary `lake build Chronos` | `INCOMPLETE_TIMEOUT` | Latest authoritative Mac attempt stopped at 1,800 seconds after reported progress `[7631/7655]`, without a reported compiler error; no completed full-library build receipt |
| Secondary `lake build ChronosUrf` | `REPORTED_FAIL` | Missing `lean/Oblivion/Graph.lean` in supplied Mac receipt |
| Codex `ChronosFourEventCertificate.lean` compilation and `#print axioms` | `NOT_RUN` | File exists only at a reported Mac path, not accessible in this audit |
| Repository-wide Python `pytest` | `SINGLE_ATOMIC_RUN_NOT_RUN`; segmented suites PASS | Local Mac executed multiple targeted and continuation suites, including a 636-case tail; those runs do not constitute one atomic full-suite receipt |
| Continuum integral and probability theorem in Lean | `OPEN` | No complete measure-theoretic formalization |
| Local worktree modifications, staging and publication | `15-file candidate; REAL_INDEX_STAGED=0; COMMIT/PUSH/MERGE=NONE` | Mac reported 13 tracked maintenance edits and 2 untracked research files; proposed diff validated in a temporary index while excluding 90 `.venv` changes |

## Minimal remaining obligations

1. Inspect local HEAD, branch, status, protected `.venv`, and existing target paths before adding this candidate.
2. Audit the Mac-only Codex certificate and review patch against the actual checkout; do not equate `lowerCertificate`/`upperCertificate` with a continuum theorem.
3. Resolve the first compatible `Oblivion.Graph` interface **without** inventing placeholders or weakening graph properties; rebuild and stop at the first next error. If the subsystem is legacy/outside the intended target, document a legitimate scoped target rather than silently excluding proofs.
4. Execute the main Lean build, targeted finite Lean certificate and axiom check, and full Python suite with bounded time/resources on the authoritative Mac.
5. For full continuum Lean verification, the first missing mathematically substantive lemma is the **normalized causal-overlap integral equals the stated rational series (including the `3/9800` correction)**. This is distinct from the now independently audited rational-series summation.

No deletion, reset, cache cleanup, checkout, commit, push, or merge is implied by this document.


---

<!-- CHRONOS_TARGETED_VERIFICATION_RECEIPTS_2026_11_23 -->
## Audited targeted-verification receipts — 2026-11-23

**Research scope:** maintenance corrections and exact algebraic four-event certificate only.
**Verified local HEAD:** `605aca6330c7b834c09eae77275763b8a374f864`.
**No full-library success claim.** Primary `lake build Chronos` was terminated by the 1,800-second resource guard with no reported compiler error (`INCOMPLETE_TIMEOUT`); prior 900-second attempts also timed out. The latest trace is included below. `ChronosUrf` is not verified.

**Mathematical boundaries:** continuum four-event integral-to-series reduction `NOT_VERIFIED`; unrestricted Chronos-RR `OPEN`; native marked-boundary/candidate-chord domain identity `OPEN`; zero-arity interface theorem closure `OPEN`; native R1/R2/R3/non-factorisation `OPEN`. The finite certificates do not prove these statements.

**Test accounting:** pytest outcomes below are segmented runs, not a single atomic repository-wide test result. Isolated and continuation tests can overlap; do not sum counts as distinct cases.

**Dependency audit:** 404 distinct direct imports in active `lean/Chronos.lean`, all 404 corresponding Lean sources present. There are 38 compiled direct-import `.olean` files at the checked location; absence of compiled artifacts is not a source-file defect. Transitive dependency completeness and full-library compilation are not established.

- `mathlib` checkout HEAD: `69cbc416b3f58ba11e331db067644d0508e78341`
- `urf_core` checkout HEAD: `ebd274c293a6e7acbe17275f6c3841a3a078c655`
- `lean-toolchain` SHA256: `85b71aa934e019c03eac6ec5ed97526956b4dff51b54c5d558fca8a5b34703e6`
- `lakefile.lean` SHA256: `156e8d0a98fe8f12239d23fe2dc0ae2df7861f7e69486ed7c458c42a9b97cb27`
- `lake-manifest.json` SHA256: `8dbddec98eceb9f9a37e43628c3632bc9b4c86a6a454d69ca68d2ecdeb0e6c59`

#### H41_MODULE

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-h41-targeted.9psom6xq/h41_target_build.log`
SHA256: `b85945e1c1d9430164575c7d01e44a0c37beab1d169a9a9f2329d607d79eaab1`

```text
Build completed successfully (5 jobs).
```

#### H41_PYTEST

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-h41-targeted.9psom6xq/h41_isolated_pytest.log`
SHA256: `19e95f03931508bcb63d5f1f276741db94fd3f8f0399d2690ed306a73c3ba6c7`

```text
..                                                                       [100%]
2 passed in 0.08s
```

#### H41_AXIOMS

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-h41-targeted.9psom6xq/h41_axiom_audit.log`
SHA256: `9064bbe194e6f539eb9673dc2232edb29fc1087c5c1d7b35ac1fe7f5f0f7e4cf`

```text
'Chronos.Frontier.H4_1_FGL_arbitrary_semantic_final_carrier_separating_observable_refuted' does not depend on any axioms
'Chronos.Frontier.H4_1_FGL_arbitrary_semantic_final_carrier_selected_instance_refuted' depends on axioms: [propext]
'Chronos.Frontier.H4_1_FGL_restricted_selected_domain_implies_missing_witness' depends on axioms: [propext]
```

#### R1_PYTEST

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-r1-audit.1wqm2v8c/r1_isolated_pytest.log`
SHA256: `3605abb09038ce24e90d81df8f7c0d87bb6f647a5e016bf461d8a8fcb408f6e9`

```text
.                                                                        [100%]
1 passed in 0.06s
```

#### R1_LEAN_SCOPE

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-r1-audit.1wqm2v8c/r1_lean_scope_audit.log`
SHA256: `0d950628f44cca604f8a7a0aee256e58eabdb8b1e7af3c0e243955d528fab642`

```text
'Chronos.Frontier.markedBoundaryChord_candidateChord_domain_identity' depends on axioms: [propext]
'Chronos.Frontier.audit_nonedge_prevents_placeholder_identity' does not depend on any axioms
```

#### R1_DOWNSTREAM

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-r1-lock-reconcile.evqz62q4/r1_regression.log`
SHA256: `f299cb0ffb4580215f4b9643a2f31cdf09e6c57c46f955b1d1c6a26a088f6fb3`

```text
....                                                                     [100%]
4 passed in 0.30s
```

#### R123_PYTEST

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-r123-verifier.7gli9qkj/r123_pytest.log`
SHA256: `a0ba7f2fb96adfb2c2564a1053a85160f60c5f008ba0c8c06a58a8cb23d1fc2b`

```text
...                                                                      [100%]
3 passed in 0.11s
```

#### R123_BUILD

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-r123-verifier.7gli9qkj/r123_target_build.log`
SHA256: `38c99a3ee9228aa0c978bb6d01cb996654c0e12e873ad2529513a3cbb36bef08`

```text
✔ [3285/3287] Built Chronos.Frontier.R1R2R3SemanticTheoremProofTargets (1.7s)
✔ [3286/3287] Built Chronos.Frontier.RepositoryNativeR1R2R3BindingMissingObject (1.6s)
✔ [3287/3287] Built Chronos.Frontier.R1R2R3IsolatedTargetsConditionalClosure (1.7s)
Build completed successfully (3287 jobs).
```

#### R123_AXIOMS

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-r123-verifier.7gli9qkj/r123_axiom_audit.log`
SHA256: `5787e7102d7e7fc6b4e00c8c72856c0d731aefb535f583458cfcbd9abe8f937a`

```text
'Chronos.Frontier.repository_native_r1_r2_r3_binding_conditional_closure' does not depend on any axioms
'Chronos.Frontier.repository_native_LongChordExclusionInputSurface_instance' does not depend on any axioms
'Chronos.Frontier.repository_native_DiameterSeparationFillingObstructionInputSurface_instance' does not depend on any axioms
'Chronos.Frontier.repository_native_UniformLocalTypeCapacityInputSurface_instance' does not depend on any axioms
```

#### ZERO_ARITY

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-zeroarity-alternative.22gflu8w/zero_arity_tests.log`
SHA256: `f3ff0520e279ec6c149e89699e3211b55be2a422d4179b812a22c9237834275e`

```text
....                                                                     [100%]
4 passed in 0.54s
```

#### PY311_TAIL

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-r123-resume.2voNF53T/pytest.log`
SHA256: `24d550b35259560bc5f83929bcea340f1f9c366347059068dd4bb3f2c0d698d7`

```text
........................................................................ [ 79%]
........................................................................ [ 90%]
............................................................             [100%]
636 passed in 43.07s
```

#### FOUR_EVENT

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-final-preflight.szwb6xmb/four_event_certificate.log`
SHA256: `17e86853e231a0bd9a01b6684769851e9999b76b8e4e04c1dd7459c3fd6befc1`

```text
RATIONAL_PARTIAL_FRACTIONS := PASS
SIMPLE_POLE_CANCELLATION := PASS
FINITE_EXACT_INSTANCES := 128/128 PASS
RATIONAL_PI_INTERVAL := PASS (Machin / alternating remainder)
EXACT_PARTIAL_SUM_TAIL_ENCLOSURE := PASS (N=50)
TAIL_ENCLOSURE := PASS
K22_DECIMAL := 0.0029645419064282944482296570331143854015646825105884676792782591787
P42_DECIMAL := 0.08541263627244212147467994501206505395106123582184558469231823686975
CONTINUUM_INTEGRAL_IDENTITY := NOT_VERIFIED
RESULT := EXACT_ALGEBRA_AND_BOUNDED_NUMERIC_PASS
```

#### PRIMARY_TIMEOUT_LOG

Log: `/var/folders/g7/t7cdygm521zfn6t572ncddgw0000gn/T/chronos-primary-final-continuation.c7rtyn9s/build.log`
SHA256: `5745363c434d36787c6b622ed7a4a6bcb078f4fe56f1c5ede73cc60a2209f5b4`

```text
✔ [7627/7653] Built Mathlib.NumberTheory.Transcendental.Liouville.Residual (7.4s)
✔ [7628/7654] Built Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith (8.8s)
✔ [7629/7654] Built Mathlib.NumberTheory.NumberField.Cyclotomic.Basic (38s)
✔ [7630/7655] Built Mathlib.NumberTheory.Zsqrtd.ToReal (4.7s)
✔ [7631/7655] Built Mathlib.NumberTheory.WellApproximable (12s)
```
