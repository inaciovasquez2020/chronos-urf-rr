# URF-AI candidate in Research Agent Toolkit

**Status:** isolated read-only research candidate, not a deployed autonomous agent or a formal proof engine.

## Target and provenance

- Target: `inaciovasquez2020/chronos-urf-rr`, `tools/research-agent-toolkit/urf-ai/`.
- GitHub main HEAD observed before staging: `3ce354779eb9039aef4d1153317f2535ed39fecd` (2026-11-09).
- Original source: isolated `urf_ai_candidate_20261109` container candidate; **not** a GitHub commit.
- Compatible Python version: >=3.11; no runtime Python package dependencies.
- Existing Research Agent Toolkit 0.2.0 is **not overwritten or fully integrated** by the additive stage.
- Repository publication: **NOT_PUSHED** until authorized and validated against current base.

## Run without installing packages

From `tools/research-agent-toolkit/urf-ai`:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_*.py' -v
PYTHONPATH=paired_eval PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s paired_eval -p 'test_*.py' -v
python3 -m urf_ai bridge_reconstruction
python3 -m urf_ai benchmark
# From the repository root, optional policy-gated source-file adapter:
# python3 tools/research-agent-toolkit/urf-ai/tools/rat_readonly.py \
#   --repo-root . \
#   --config tools/research-agent-toolkit/examples/toolkit.json \
#   --source tools/research-agent-toolkit/README.md \
#   --case bridge_reconstruction
```

Source-specific PDF audit is **NOT_RUN** unless the user supplies the original PDF. To run separately, provide `--source /absolute/path/to/PDF`; do not publish the private source file automatically. The included receipts are reproducibility records from earlier isolated tests, **not live replays**.

A paired GPT-6 experiment has **NOT_RUN**. Running `paired_eval/paired_gpt6.py run` incurs paid API calls and requires explicit opt-in and credentials. Previously generated `public_fixture_suite_20261109.json` is public regression data and **must not be called unseen**. For a valid future benchmark, generate a fresh private suite and keep it sealed until both arms finish.

## Scope, controls, and non-claims

- `urf_ai/guard.py` is a **candidate guarded mutation adapter** for an explicitly disposable, clean Git worktree with separate HMAC approval and verifier allowlist. It is not a process sandbox; it cannot guarantee safety from an untrusted verifier binary or side effects outside the worktree. Do not invoke it on the authoritative Mac checkout.
- `urf_ai/evidence.py` verifies signed receipt *records* and exact claim bindings; this does not independently run Lean or establish mathematical truth.
- `urf_ai/csts.py` implements a strict **subset** of CSTS; not complete CSTS v0.1 conformance, durable audit storage, or trustworthy external attestation.
- `urf_ai/assistant.py` is a deterministic, curated, read-only adapter, **not** an LLM or a trained model. `tools/rat_readonly.py` additionally applies the existing RAT policy engine to an existing, explicitly selected repository source path, hashes it, and returns a curated research note, without approving theorem promotion.
- The legacy `rat mutate` and `verified_dependency_subprocess` paths in upstream Research Agent Toolkit 0.2.0 remain unsafe without a separately reviewed integration: they do not enforce the policy gate and may use `git reset --hard` / `git clean -fd`. **Do not run them** on a valuable checkout. Adding this subtree does not fix those entrypoints.
- A P≠NP proof, unrestricted SAT lower bound, and Lean validation remain OPEN / NOT_RUN.

## Safe next integration obligation

First replace/disable the existing write routes and update their tests under a separate, source-matched patch, then rerun the original toolkit suite plus this suite. Require PR review and CI before exposing agent mutation. Until then, use only the read-only CLI and benchmark. No original repository file is deleted, overwritten, or staged in this additive integration.
