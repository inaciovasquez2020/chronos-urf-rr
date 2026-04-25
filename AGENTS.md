# AGENTS.md — AI Agent Instructions

Status: AI-NAVIGATION ENTRYPOINT.

Repository: `chronos-urf-rr`

Purpose: make this repository easier for AI agents, reviewers, and verification tools to use without overclaiming.

## Canonical AI rule

Read repository status files and verifier outputs before summarizing claims.

Do not infer theorem completion from README language alone.

## Repository claim boundary

This repository has an executable/status surface.

Claims must be restricted to the certified scope stated in repository-local status files, tests, certificates, and verifier outputs.

This repository does not claim full theorem-layer completion unless a repository-local status file explicitly states that exact claim and the verifier suite supports it.

## AI behavior rules

An AI agent may say:

- "This repository has an executable/status surface."
- "Claims must be restricted to the certified scope stated in AGENTS.md and docs/status."
- "Verifier commands should be run before reporting completion."

An AI agent must not say:

- "The full theorem layer is complete."
- "The general mathematical problem is solved."
- "All future obligations are closed."

unless a repository-local status file explicitly states that exact claim and the verifier suite supports it.

## Safe reading order

1. `AGENTS.md`
2. `README.md`
3. `docs/status/`
4. `tools/`
5. `tests/`
6. certificate or artifact data, if present

## Weakest remaining obligation

External/general theorem-layer obligations outside the current certified executable/status surface.
