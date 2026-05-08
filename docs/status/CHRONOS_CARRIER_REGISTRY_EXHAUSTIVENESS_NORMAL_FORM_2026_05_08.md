# Chronos Carrier Registry Exhaustiveness Normal Form

status: FRONTIER_OPEN

theorem_closure: false

## Target Normal Form

For every admissible local/refinement carrier `C`, there must exist a registered simulator carrier `r` such that for every fiber `b` and scale `λ`,

```text
|T_C(b, λ)| ≤ |T_r(b, λ)|
Registered Subdominant Classes
The current registry permits the following simulator normal-form classes:
constant_capacity
log_capacity
linear_capacity
affine_high_capacity
n_log_n_capacity
quadratic_deficient_capacity
Forbidden Boundary Classes
The following classes are not admissible normal forms:
obstruction_oracle_capacity
obstruction_plus_one_capacity
Reason: they encode obstruction space at full rank or higher.
Missing Theorem
Carrier Registry Exhaustiveness Theorem:
Every admissible carrier has a transcript normal form dominated by one of the registered subdominant classes.
Boundary
This artifact states the normal-form target only.
It does not prove registry exhaustiveness.
It does not prove Uniform Carrier Subdominance.
It does not prove Chronos-RR closure, Chronos depth lower bound, H4.1/FGL closure, P vs NP, or theorem-level closure.
