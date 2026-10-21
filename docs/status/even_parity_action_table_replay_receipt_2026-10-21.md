# Action-table replay receipt

Status: `ACTION_TABLE_CONSISTENCY_REPLAY_PASS; METRIC_TO_CURVATURE_CLEAN_REPLAY_NOT_RUN`

Replay script: `tools/replay_even_parity_action_table.py` (runs with Python 3 and SymPy).

Checks performed by parsing the 81 monomials printed in the derivation report and reconstructing the second-jet Hessian:

- 81 action terms parse successfully.
- Parsed action is homogeneous quadratic in perturbation jets.
- Coefficient of `(H2_t_t)^2` is `+3*M*r/(2*(r-2*M)^2)`.
- Coefficient of `(K_t_t)^2` is `-3*M*r/(2*(r-2*M)^2)`.
- Coefficient of `(H0_r_r)^2` is `+3*M*(r-2*M)^2/(2*r^3)`.
- The top 3x3 Hessian block has zero determinant and every 2x2 minor vanishes.
- The reconstructed six-variable Hessian has rank 4 at the generic sample `M=2, r=5`.

Interpretation: this independently checks internal consistency of the published action table and Hessian formulas. It does not regenerate the metric inverse, Christoffel symbols, curvature operator, angular integration, or Euler–Lagrange equations from the metric. Therefore it is not the clean metric-to-action replay needed to certify the derivation end-to-end.