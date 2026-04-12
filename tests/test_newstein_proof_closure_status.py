from pathlib import Path

def test_newstein_proof_closure_status_locked():
    s = Path("docs/status/NEWSTEIN_PROOF_CLOSURE_STATUS.md").read_text()
    required = [
        "# Newstein Proof Closure Status",
        "### 1. Ledger closure",
        "- COMPLETE",
        "### 2. Reduction closure",
        "### 3. Proof closure",
        "- INCOMPLETE",
        "### Rooted-ball branch",
        "### Fiber quotient-rank branch",
        "### Fiber-to-global branch",
        "### Global assembly branch",
        "### Complexity branch",
        "## Proof-closure criterion",
        "## Repository-level conclusion",
        "## Minimal remaining object",
        "Each ledgered theorem must be replaced by an actual proof object or verified theorem implementation.",
    ]
    for item in required:
        assert item in s

def test_newstein_proof_replacement_queue_locked():
    s = Path("docs/math/NEWSTEIN_PROOF_REPLACEMENT_QUEUE.md").read_text()
    required = [
        "# Newstein Proof Replacement Queue",
        "## Replacement order",
        "### 1. Rooted-ball branch",
        "NEWSTEIN_LOCAL_TRIANGLE_GENERATION_THEOREM",
        "NEWSTEIN_ROOTED_BALL_TRIVIALIZATION_THEOREM",
        "### 2. Fiber quotient-rank branch",
        "NEWSTEIN_FIBER_RANK_GAP_THEOREM",
        "### 3. Fiber-to-global branch",
        "NEWSTEIN_DIRECT_SUM_EMBEDDING",
        "### 4. Global assembly branch",
        "NEWSTEIN_NON_FACTORIZATION_CONSEQUENCE",
        "### 5. Complexity branch",
        "NEWSTEIN_TRANSCRIPT_LOWER_BOUND",
        "## Replacement rule",
    ]
    for item in required:
        assert item in s
