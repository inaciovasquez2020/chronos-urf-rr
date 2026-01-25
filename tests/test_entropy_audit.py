from chronos.entropy_audit import AuditParams, lower_bound_steps

def test_lower_bound_steps_basic():
    p = AuditParams(n=10, per_step_info_bound_bits=2.0, required_entropy_bits=9.0)
    assert lower_bound_steps(p) >= 5  # 9/2 -> 5 steps

def test_lower_bound_steps_zero_entropy():
    p = AuditParams(n=10, per_step_info_bound_bits=1.0, required_entropy_bits=0.0)
    assert lower_bound_steps(p) == 1
