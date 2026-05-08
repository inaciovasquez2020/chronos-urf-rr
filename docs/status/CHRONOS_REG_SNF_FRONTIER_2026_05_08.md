# Chronos Reg-SNF Frontier

status: FRONTIER_OPEN

theorem_closure: false

## Weakest Missing Lemma

Reg-SNF:

```text
Carrier Admissibility implies Registered Subdominant Normal Form.
Formal statement:
∀ admissible C, ∃ r ∈ R, ∀ b,λ:
  ∃ injective φ_{b,λ} : T_C(b,λ) → T_r(b,λ)
Equivalent capacity form:
∀ admissible C, ∃ r ∈ R, ∀ b,λ:
  |T_C(b,λ)| ≤ |T_r(b,λ)|
Dependency Position
Reg-SNF
⇒ Carrier Registry Exhaustiveness
⇒ Uniform Carrier Subdominance, assuming Reg-Sub-Uniform
⇒ Non-Factorization, assuming Rank-Image-Bound
⇒ Chronos-RR depth lower bound, assuming Depth Bridge
Boundary
This artifact states the weakest missing lemma only.
It does not prove Reg-SNF.
It does not prove Carrier Registry Exhaustiveness.
It does not prove Uniform Carrier Subdominance.
It does not prove Non-Factorization.
It does not prove Chronos-RR closure, H4.1/FGL closure, P vs NP, or theorem-level closure.
