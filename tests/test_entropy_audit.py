import sys
import os
import pytest

# Force local path inclusion for CI environment
# This line tells Python: "Look one folder up to find the packages"
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# This is the line I was referring to — it imports the Chronos logic specifically
from chronos.entropy_audit import AuditParams, lower_bound_steps

def test_chronos_non_amplification():
    """
    S0 Witness: Verifies that the Chronos operator respects the 
    Structural Non-Amplification principle.
    """
    params = AuditParams(threshold=0.5, depth_limit=10)
    
    # Simulate a structural audit where entropy remains bounded
    result = lower_bound_steps(params, initial_entropy=0.2)
    
    # Verification: Entropy should not exceed the URF-defined wall
    assert result <= params.depth_limit
    assert result >= 0

def test_entropy_depth_invariant():
    """
    S0 Witness: Verifies that the EntropyDepth invariant holds 
    under temporal operator shifts.
    """
    params = AuditParams(threshold=0.1, depth_limit=5)
    
    # A system with high initial entropy should be flagged or capped
    result = lower_bound_steps(params, initial_entropy=0.8)
    
    # In a rigid framework, the depth invariant is the upper bound
    assert result <= params.depth_limit

if __name__ == "__main__":
    pytest.main()
