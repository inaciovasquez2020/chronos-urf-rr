# Legacy `rat mutate`: fail-closed migration candidate (2026-11-09)

Status: ISOLATED CANDIDATE, NOT MERGED OR DEPLOYED. Repository source baseline
for two modified files has been checked against Git object SHAs
`537007b8b3b700dab28d8558730fb59892e3b317` (agent_mutation.py) and
`701c57c125b78020129e8053424bcc2afd7e5e11` (transaction.py).

The original `verified_dependency_subprocess` accepted arbitrary mutation
commands and used repository-wide `reset --hard` / `clean -fd` on failure.
The original agent write entrypoint did not call `engine.evaluate`.

The candidate has three changes:

1. Old `rat mutate` CLI and JSON-RPC calls are **denied by default**, because
   neither presents an authenticated, exact-request authorization token.
2. An explicitly trusted controller can call
   `research_agent_toolkit.hardened_mutation.governed_patch_mutation` with:
   `config_path`, `approval`, `authorization_key`, and `timeout_seconds`.
   The controller, not the research agent, must issue the signed approval.
   Its config must explicitly declare `disposable_worktree_confirmed`,
   `explicit_write_approval`, scope allow/deny patterns, mutation and verifier
   budgets, and exact allowed verifier argv. A real policy evaluation now
   runs against the actual added patch source and paths.
3. `verified_dependency_subprocess` no longer executes mutation commands.
   The separate audited URF-AI guard performs exact-file restoration within an
   **expendable** Git worktree, does not run broad reset/clean, and reports
   preserved unauthorized file residue as an INCOMPLETE result.

This deliberately breaks historical tests asserting that unauthenticated
legacy CLI/server writes succeed. Those tests require **migration to denial
assertions**, plus new signed-approval tests; do not weaken them or introduce
implicit approvals to make tests green. The original unmodified 16-test suite
has NOT BEEN EXECUTED in this isolated research container. Do not merge until
it is run and every intentional contract change is accounted for, and until
proper sandboxing or trusted verifier isolation is reviewed.

The guard does not sandbox verifier processes: an allowlisted subprocess can
read or write outside the disposable worktree, and its side effects are not
independently contained by this implementation. No safety claim for arbitrary
untrusted executable programs follows.

No code changes have been made to the Mac checkout or an existing GitHub PR.
