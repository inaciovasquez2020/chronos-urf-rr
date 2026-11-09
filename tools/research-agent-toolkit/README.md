# Research Agent Toolkit

A standalone, deterministic toolkit for AI-assisted research repositories.

It combines eight capabilities:

1. **Dependency scanner** — Python AST, Lean imports/declarations, shell source edges, and literal repository-file references.
2. **Scope constraints** — allow/deny path rules before a mutation is accepted.
3. **Budgets** — hard caps on mutations, failed verifications, tool calls, and arbitrary counters.
4. **Policy engine** — rejects forbidden proof/code patterns and out-of-scope changes.
5. **Approval gates** — classifies proposed actions as ALLOW, VERIFY, or DENY.
6. **Observability** — append-only JSONL spans/events for agent actions and verifier results.
7. **Session receipts** — compact, machine-readable summaries of decisions, mutations, tests, and outcomes.
8. **Local document index** — deterministic hashed-vector indexing/search in SQLite; PDF extraction is enabled when PyMuPDF is installed.

Additional utilities:

- **Builder profile** from trace/session logs.
- **Calendar export** of research events to `.ics`.
- **Fine-tune manifest generator** for preparing JSONL training data without claiming or performing model training.

The baseline package uses only Python's standard library. Optional PDF extraction uses `PyMuPDF` (`fitz`) when available.

## Core invariant

```text
candidate change -> provenance closure -> scope/policy/budget checks
    -> trusted signed single-use authorization (external durable ledger)
    -> exactly one patch in disposable worktree
    -> internal diff/syntax check ONLY (not a theorem verifier)
    -> STRUCTURAL_STAGED_UNVERIFIED: nonzero status, no proof claim
       OR failure / constrained exact-file recovery
```

## Quick start

```bash
python -m pip install -e .
rat scan . --out dependency-graph.json
rat gate --config examples/toolkit.json --action modify --paths src/example.py
rat index --db research.db README.md
rat search --db research.db "dependency graph verifier"
```

## Boundary

This package enforces workflow invariants. It does not prove mathematical claims, validate scientific interpretation, or certify correctness beyond the verifiers you explicitly invoke.


## Agent research-file write contract (security quarantine)

**Legacy automatic writes are DISABLED by default.** The CLI command `rat
mutate` and JSON-RPC tool-server `mutate` keep their names but now fail closed:
without a trusted signed approval they do not change files. The old contract
that unconditionally applied a patch and restored clean HEAD is superseded.

Only a **separately trusted approval controller** may call
`research_agent_toolkit.hardened_mutation.governed_patch_mutation` with a
versioned explicit policy, a scoped HMAC authorization, an external durable
approval ledger, an internal-check allowlist, and an **explicitly disposable**
Git worktree. Only `RAT_INTERNAL_DIFF_CHECK` and
`RAT_INTERNAL_PYTHON_SYNTAX` are accepted: no caller-supplied verifier command
is executed. The normal `rat gate` policy checks run within this mutation call.

A candidate may remain modified in the disposable worktree after internal
structural checks; this is NOT mathematical verification. The guard reports
`STRUCTURAL_CANDIDATE_NOT_PROMOTED` with return code 4. The toolkit adapter
reports `preserved=False`, `phase=STRUCTURAL_STAGED_UNVERIFIED`, and return
code 4. A nonzero staging result must not be promoted to a proof/CI PASS.

The old arbitrary-subprocess mutation API is disabled; it must not be used to
recover an authoritative checkout. A failed transaction never invokes Git
`reset --hard` or `clean -fd` and never silently deletes outside-scope
artifacts. See `SECURITY_MUTATION_MIGRATION.md` for the deliberate breaking API
change and test obligations.

This is an approval and inventory guard, not an OS sandbox. Untrusted
verifier executables are prohibited, not sandboxed. The ledger and HMAC key
must be controlled by a distinct trusted principal; same-UID replacement or
rollback of that state is outside the guarantee. Git index flags that hide
tracked modifications (`skip-worktree`, `assume-unchanged`) cause preflight
denial. Independent security review is REQUIRED before enabling automated
writes or merging.

Ordinary human Git commands are unaffected; no repository-wide hooks are
installed. Human approval is still required before any promotion or merge.
