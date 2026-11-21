# Universality Bridge: SAT-query stress test and input-information no-go theorem

**Date:** 2026-11-09  
**Source:** User-provided *Universality Bridge for Deterministic Polynomial-Time Computation via Normalized k-Tape Transcript Systems*, pp. 2-7.  
**Source SHA-256:** `34096bfa667267624b5b6ad3b76ccb7b0d9eca8e90f129f85ad4b8b9a7eabc30`  
**Operation:** Source-pinned, sandbox-only research. No active Mac checkout or GitHub repositories were changed.  
**Status:** Elementary mathematical results **PROVED on paper, NOT LEAN_VERIFIED**; finite simulations **COMPUTATION_PASS**; unrestricted SAT time lower bound **OPEN**; paired GPT-6 evaluation **NOT_RUN**.

## 1. Universal read-first obstruction (mathematical proposition)

Let `L ⊆ {0,1}*` be **any decidable language** and `X_n` any random variable supported on its n-bit inputs. The input tape of a standard deterministic multitape Turing machine is read-only and the work tapes are initially blank. With the normalized transcript of the source manuscript, `Y_0=c_0`, `Y_(t+1)=(c_t,c_(t+1))`, where `c_t` gives state, head positions and scanned symbols, there exists a *uniform deterministic decider* `N_L` for `L` and a universal linear input-reading phase such that, at a fixed index `r(n) = n + O(1)`, the transcript `Y_<=r(n)` determines the entire initial input `X_n`. Therefore

```
H(X_n | Y_<=r(n)) = 0
I(X_n ; Y_(t+1) | Y_<=t) = 0  for every t >= r(n).
```

**Proof.** `N_L` first copies the read-only input, one symbol per transition, to a blank work tape until it sees the terminator; it then simulates an arbitrary fixed decider for `L` on the stored input. All n input symbols occur as scanned symbols in the first `n+O(1)` normalized transcript frames. Thus the transcript deterministically reconstructs `X_n` and has zero conditional input entropy afterward. The remaining machine computation is a deterministic function of `X_n`; no further *Shannon information about X_n* can be revealed once X_n is known. The copier is a single, length-uniform machine, not separate advice for each input length. QED.

**Meaning.** Every decidable problem, whether computationally cheap or expensive, admits a correct decider that acquires **all** input entropy in O(n) time. Therefore the acquisition of ordinary Shannon information about the original input, taken alone, cannot force superpolynomial SAT decision time. This is a no-go for an *input-information-only* lower-bound strategy, not a theorem that SAT has an efficient algorithm. It leaves open hardness arising from *processing the acquired data*.

**Further corollary (canonical witness).** Let `W(X)` be any deterministic function of a SAT instance X, for example the lexicographically least satisfying assignment, with a sentinel for unsatisfiable instances. Once the read-first transcript determines X, it also determines W(X), so `H(W(X)|Y_<=r(n))=0`, even if computing W(X) from X may require significant resources. Shannon conditional entropy does not measure the computational time needed to extract a deterministic but difficult function of known data. This statement is information-theoretic, not a complexity lower bound for W.

## 2. Stronger per-step bound under the source's exact machine conventions

For a fixed deterministic k-tape machine with **one read-only input tape** over a fixed finite input alphabet Σ and initially blank work tapes, the previous normalized history allows reconstruction of all *work tape contents* and of every input symbol already inspected:

- At t=0, work tapes are blank and the currently scanned input symbol appears in c0.
- If the claim holds through time t, the deterministic transition delta applied to c_t fixes the next state, all head locations and every work-tape write. Hence the subsequent scanned **work symbols** are already known from reconstructed work-tape contents.
- The sole new observation at t+1, if any, is the input symbol under the single read-only head at an **unvisited input cell**. It has at most |Σ| values; a visited cell or known padding symbol contributes no new information.

For fixed input length n (and a fixed known endmarker convention), the conditional support size of `Y_(t+1)` given `Y_<=t` is thus at most `|Σ|`, so:

```
I(X_n ; Y_(t+1) | Y_<=t)
  = H(Y_(t+1) | Y_<=t)
  <= log2 |Σ|.
```

The equality uses that the machine and its complete trace are deterministic functions of X_n. This is **O(1) conditional mutual information per transition**, even though the *explicit length of a frame* that writes binary head positions is O(log n) bits. Those are different notions of bandwidth. For a binary input alphabet, at most one new input bit is exposed per step. End-of-input conventions, multiple read-only tapes, random oracle bits, or additional observation channels must be accounted for separately; this argument does not apply unchanged to those models.

The earlier source-specific audit already corrected the source's chain-rule identity:

```
H(X) = I(X;Y0) + sum_t I(X;Y_(t+1)|Y_<=t) + H(X|Y_<=T).
```

Combining these identities still yields only a **linear** identification bound, since the input is fully inspectable in linear time.

## 3. A SAT-specific worst-case linear lower bound, not a P-vs-NP result

For m independent input sign bits `b ∈ {0,1}^m`, encode the fixed one-variable CNF:

```
F_b = (z) AND C1 AND ... AND Cm,
Ci  = (z) if bi=0, else (not z).
```

Exactly one of the 2^m sign strings is satisfiable: `b=0^m`. On the all-zero input, flipping any single sign bit changes SAT from true to false. Any deterministic correct sign-bit query decision tree must inspect **all m positions** on that input: if it skipped bit i, it could not distinguish 0^m from the input with bit i flipped. A scanner stopping at the first 1 achieves worst-case m queries. Thus the **restricted-family deterministic query complexity is exactly m**.

Under the **uniform distribution on sign strings**, the straightforward scanner examines bit i if the first i-1 bits are zero, so

```
E[queries] = sum_(i=1)^m 2^(-(i-1)) = 2(1 - 2^(-m)).
H(SAT(F_b)) = h2(2^(-m)) -> 0,
```

where `h2(p)=-p log2 p-(1-p)log2(1-p)` is binary entropy. The exact worst-case query lower bound **grows linearly**, while the average query cost approaches 2 and the entropy of the answer tends to 0. The mathematical result is standard decision-tree sensitivity in a particularly simple CNF representation. Its sign-bit representation has one propositional variable but m independent input bits; it is **not** an m-variable SAT lower bound.

This distinguishes worst-case computation from distributional Shannon information. The same m-bit input can be read in O(m) time, after which Shannon information about the input is exhausted regardless of how the eventual decision is calculated.

## 4. Executable verification and adversarial tests

Implementation is in the isolated candidate only:

- `urf_ai/sat_query_boundary.py`: independent truth-assignment CNF oracle, early-exit sign scanner, exact rational mean query count, transcript-fiber entropy, concrete deterministic two-tape copier with source-form `Y0` and `Y_(t+1)` frames, and fail-closed status evaluator.
- `tests/test_sat_query_boundary.py`: finite sweeps `m=1..12`, copier `n=1..10`, invalid inputs, overclaiming and malformed witness mutations, and read-only adapter integration.
- `tools/run_sat_query_boundary_audit.py`: reproducible source-SHA-pinned receipt generator, writes only to standard output.
- `receipts/sat_query_boundary_20261109.json`: detailed fixed-input receipt.

Observed finite bounds:

```
SUM_(m=1)^12 2^m = 8190 independent CNF instances checked
m = 1..12: restricted-family SAT count = 1, worst-case queries = m
m = 1..12: exact E[queries] = 2(1 - 2^(-m))
n = 1..10: concrete copier prefix transcript fibers exhaustively checked
n = 1..10: work tape contents independently reconstructed from transcript
n = 1..10: H(X|Y_<=t) = n - min(n,t+1)
no proof status promotion from any finite fixture
```

All candidate tests together: **59 + 12 = 71 Python unittest checks passed** in the sandbox; no Lean toolchain or separate GPT-6 model invocation was used. One earlier run hit a stale `total=9` assertion after adding two benchmark cases; only the expectation was repaired, and the full suite then passed.

## 5. Weakest remaining obligation and next genuine mathematical frontier

A universal lower bound on **input-reading or Shannon information acquisition** is not a suitable target for a superpolynomial SAT time theorem, because `N_SAT` reads the full input in `O(n)` time. Any successful replacement must bound a **computational** resource under a genuine uniform model after the input is fully available—for instance some rigorously specified circuit/proof/refinement complexity that every correct SAT decider is required to realize, with a justified reduction to total runtime.

That universal bridge is presently **OPEN**. Establishing superpolynomial post-read time for *all* correct SAT deciders would itself settle a major complexity open problem. Results for resolution, restricted circuits, or specially constrained algorithms are not automatically universal. A computationally bounded information or indistinguishability measure might be relevant, but no such SAT-hardness theorem has been established by this case.

**Claude:** not consulted; no precise lemma currently offers a justified large expected gain beyond the identified open obstruction. **Codex:** not invoked; the finite isolated checks do not justify major proof integration yet. **Git/Mac:** unchanged. **Publication:** none.
