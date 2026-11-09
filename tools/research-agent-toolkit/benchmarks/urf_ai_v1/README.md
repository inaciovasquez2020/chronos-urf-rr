# URF-AI research benchmark v1 (experimental)

**Status:** BOUNDED_REGRESSION_ONLY — **NOT** an independent, blind AI-comparison result.

This is a dependency-free deterministic regression set for mathematical claim boundaries, counterexamples, evidence provenance, and *synthetic* confidentiality decisions. The 14 public tests cover normalized Turing-machine transcript reconstruction, the Shannon initial-information correction, expected-vs-pointwise information, aggregate output capacity, and receipts that do not constitute independently replayed proofs.

All provenance/privacy fixtures are **synthetic**. No unreleased research archive, private filename, private digest, or validation record is included. Repository publication of this scaffold must not be interpreted as permission to publish any real private research data.

## From the `tools/research-agent-toolkit` directory

```bash
PYTHONPATH=src python3 -B -m research_agent_toolkit.urf_ai_benchmark --selftest
PYTHONPATH=src python3 -B -m research_agent_toolkit.urf_ai_benchmark --export-tasks /tmp/urf_ai_tasks.json --seed 451
PYTHONPATH=src python3 -B -m unittest discover -s tests -p 'test_urf_ai_benchmark.py' -v
```

For model responses (once independently collected), `--evaluate candidate.json --seed 451` scores a single candidate; `--compare ordinary.json urf_assisted.json --seed 451` computes paired diagnostic differences. Do **not** supply the Python scorer, expected verdicts, or this repository to a model claiming a blind trial. The public scorer contains answer logic and can be used only for engineering diagnostics. Distinct, undisclosed held-out problems and separately isolated sessions are required for a credible efficacy experiment.

## Input and output contract

Task fixture: `tasks_seed451.json`. Candidate JSON must be a list of `{id, status, issue_code, witness}` objects with the witness fields requested by each task. The evaluator independently checks the finite oracle. Boolean and integer witness values are type-distinct; unknown statuses are rejected; recognized proof-claim labels and their case/whitespace variants are counted as unsupported proof promotions when their certificates are not valid. Unauthorized extra fields are rejected. Missing, duplicate, or malformed submissions never produce a perfect score.

The comparison does not run an AI, access a model endpoint, authenticate third-party certificates, inspect real confidential data, verify a Lean theorem, or certify SAT complexity lower bounds.

## Scientific boundaries

- `REFUTED_AS_STATED`: local transcript without the input does not reconstruct unread tape cells.
- `PROVED_UNDER_ASSUMPTIONS`: input-assisted reconstruction is just ordinary deterministic simulation; the corrected entropy identity includes `I(X;Y0)`. A fixed-machine local frame has conditional next-step information at most `k log2|Gamma|` bits.
- `CONDITIONAL` and `NOT_IMPLIED`: information bounds do not imply superpolynomial SAT hardness; special variants require exact premises.
- `RECEIPT_ONLY` and `PRIVATE_BLOCKED`: signatures, hashes and recorded status are not independent theorem proofs or publication permission.

**Gate:** Finite benchmark diagnostics are not certificates of unrestricted mathematical theorems or evidence of general URF-AI effectiveness.

This subproject is deliberately kept out of the toolkit's mutation path. It adds no agent write route, alters no policy/rollback contract, and does not grant permission to change any admitted research chain. Future source edits to admitted research chains must go through the existing governed `rat mutate` interface.
