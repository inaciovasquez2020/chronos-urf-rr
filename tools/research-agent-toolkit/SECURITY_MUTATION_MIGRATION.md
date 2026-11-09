# Research Agent Toolkit: fail-closed write-boundary migration

Status: **DRAFT / SECURITY REVIEW OPEN**. This note describes the proposed
migration in PR #1338; do not treat test success as independent security
approval or merge authorization.

## Contracts

- Legacy `rat mutate` CLI, tool-server mutation without credentials, the generic
  `verified_mutation` callback, and `verified_dependency_subprocess` deny writes.
- A separately trusted controller may issue an exact-request HMAC approval for
  a disposable, initially clean Git worktree and a provenance-scoped patch.
  The patch is subject to the original toolkit policy engine and a trusted
  SQLite approval ledger **outside** the worktree. Consumption is atomic and
  occurs before the attempted write; failed attempts do not return tokens.
- All user-supplied external verifier execution is **forbidden**. The two
  internal options are `RAT_INTERNAL_DIFF_CHECK` and
  `RAT_INTERNAL_PYTHON_SYNTAX`. These check structural validity, not theorem
  correctness or claims of mathematical proof.
- Successful staging returns **nonzero code 4**, status
  `STRUCTURAL_CANDIDATE_NOT_PROMOTED` at the guard and adapter phase
  `STRUCTURAL_STAGED_UNVERIFIED`, with `preserved=False`. The candidate **does
  remain modified** in the disposable worktree. No automatic commit or
  promotion is authorized.
- Preflight inspects staged/unstaged/untracked/ignored files **and** tracked
  Git index flags (`git ls-files -v -z`). Noncanonical index flags, including
  `skip-worktree` and `assume-unchanged`, cause fail-closed denial even when
  `git status` reports clean.
- No `git reset --hard`, `git clean -fd`, checkout, or broad deletion is used
  for error recovery. Unauthorized side effects must be reported, not erased.

## Inline Lean probe authorization boundary

The `modules` argument to `governed_patch_mutation` is **fail-closed denied**.
`exact_lean_dependencies` can invoke `lake env lean` and load project code.
A separately authorized, precomputed exact dependency graph pathway does not yet
exist. Theorem-module mutations remain blocked until that pathway is reviewed.
This denial neither runs Lean nor claims mathematical verification.

## Remaining trust boundaries

A SQLite transaction does **not** prevent privileged ledger replacement or
rollback. The signing key and ledger storage must be protected under a
genuinely trusted principal. No operating-system sandbox or safety guarantee
for arbitrary Python callbacks, untrusted verifiers, or external command
execution is supplied. Thus automated write execution and merge require a
separate independent security review and explicit authorization.

## Regression gates

The dedicated workflow runs the migrated original toolkit suite, adversarial
mutation tests, index-flag tests, URF-AI tests, and paired evaluation fixtures.
A successful *structural* check is never a proof certificate, irrespective
of the workflow's green status. The finite mathematics cases remain
source-specific and should not be relabeled as Lean verification.
