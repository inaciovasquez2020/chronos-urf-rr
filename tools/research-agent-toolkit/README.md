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
candidate change
    -> dependency closure
    -> scope check
    -> policy check
    -> budget check
    -> exactly one mutation
    -> verifier
    -> pass: preserve
       fail: revert exact mutation and terminate
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
versioned explicit policy, an exact-request scoped signed approval, a verifier
allowlist, and an **explicitly disposable** Git worktree. Its candidate
verification does not commit or merge research files. The normal `rat gate`
policy checks are now applied inside the mutation call as well.

The old arbitrary-subprocess mutation API is disabled; it must not be used to
recover an authoritative checkout. A failed transaction never invokes Git
`reset --hard` or `clean -fd` and never silently deletes outside-scope
artifacts. See `SECURITY_MUTATION_MIGRATION.md` for the deliberate breaking API
change and test obligations.

This is an approval and inventory guard, not an OS sandbox. An allowlisted
verifier can still write outside the disposable worktree. Untrusted verifier
executables require separate sandboxing and independent scrutiny; no safety
claim for an arbitrary verifier follows from these checks.

Ordinary human Git commands are unaffected; no repository-wide hooks are
installed. Human approval is still required before any promotion or merge.
