# Event-first spacetime: isolated research staging (2026-11-11)

Base: PR #1347 exact commit `abef2b3e61dcb24a3ebb65ad0df7a76f63d4869f`.
Status: RESEARCH / NOT PROMOTED / NO LEAN VERIFICATION / OUTSIDE REVIEW OPEN.

## Scope and scope locks

- The referenced PR contains a restricted conformal four-dimensional causal-diamond identifiability result, not a metric-free emergence theorem.
- The later calculations investigate finite causal orders, consistent stochastic growth, linear-extension prefix sampling, and replica disagreement.
- Mathematical and computational claims in conversation-derived reports require audit against the attached source scripts before promotion. An attempted all-scripts validation batch timed out; syntactic parsing of 20 Python scripts passed. No Mac run is claimed.
- All-N Minkowski sampling convergence, an intrinsic selecting law, matter/gravity dynamics, and global five-dimensional claims remain OPEN.
- No axioms, Lean proofs, independent security review, or independent mathematical review have been claimed on this branch.

## Verified elementary finite-poset identity

For a finite poset P, a uniformly chosen linear extension, and a prefix of n elements, let q(x)=Pr(x in prefix | P). Let I,J be independent prefixes from two independent uniform linear extensions. Then

  E[|I △ J| | P] = 2 Σ_x q(x)(1-q(x)) = 2(n - Σ_x q(x)^2).

For any deterministic order ideal A,

  E[|I △ A| | P] = Σ_{x in A}(1-q(x)) + Σ_{x not in A}q(x).

Because q(x)≥q(y) whenever x<y, the threshold {x:q(x)>1/2} is an ideal and minimizes the expected mismatch. Writing R for that minimum and D for replica disagreement,

  D/2 ≤ R ≤ D.

The best n-element deterministic ideal R_n obeys D/2 ≤ R ≤ R_n ≤ D. These identities are finite combinatorics, not a spacetime emergence theorem.

## Open decisive boundary

For P_N obtained from uniformly sprinkled points in a fixed 4D Minkowski causal diamond, and n/N→α in (0,1), determine the asymptotics of

  E[D(P_N,n)]/n.

Even a positive lower bound would refute deterministic-ideal concentration only; it would NOT alone refute convergence of uniformly sampled prefix suborders to Minkowski statistics.

## Research-file inventory uploaded for independent audit

All 30 conversation-produced standalone Python scripts and Markdown reports are now staged individually in `research/event_first/` on this isolated branch, GitHub tree checked at commit `dbca15c9c5d12a409d142257961066782965700f`. The chat archive `chronos_event_first_research_20261111.zip` (SHA-256: `d0897c4629cbf1cde063682267448bfdf14240da5972d46bcfbe763992c88b8e`; 52,473 bytes) remains a separate downloadable backup; archive is NOT stored in Git. Presence in the branch is NOT verification or publication.

## Release gates

- Inspect actual Mac working tree, status, HEAD, untracked and unpushed research before local integration.
- Reproduce individual exact computations with CPU/time/state guards and reconcile contradictions.
- Compile proposed Lean declarations with repository-pinned toolchain, audit axioms, and obtain independent mathematical review.
- Do not merge into main or PR #1347 until separately approved.
