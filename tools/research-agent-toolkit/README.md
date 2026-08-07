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
