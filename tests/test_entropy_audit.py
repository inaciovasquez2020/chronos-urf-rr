import sys
import os

# Force local path inclusion for CI environment
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chronos.entropy_audit import AuditParams, lower_bound_steps


def test_chronos_non_amplification():
    params = AuditParams(threshold=0.5, depth_limit=10)
    result = lower_bound_steps(params, initial_entropy=0.2)
    assert 0 <= result <= params.depth_limit


def test_entropy_depth_invariant():
    params = AuditParams(threshold=0.1, depth_limit=5)
    result = lower_bound_steps(params, initial_entropy=0.8)
    assert result <= params.depth_limit
