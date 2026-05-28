# Gravity Pull-Push Actual-Value Test

Status: FINITE_ACTUAL_VALUE_ACCOUNTING_TEST_ONLY

Date: 2026-05-28

This adds a finite pull-push accounting test with Lean-checked actual values.

Actual values:

- empty: pull 0, push 0, pull residual 0, push residual 0, total 0
- balanced: pull 7, push 7, pull residual 0, push residual 0, total 14
- pull-dominant: pull 13, push 5, pull residual 8, push residual 0, total 18
- push-dominant: pull 4, push 9, pull residual 0, push residual 5, total 13

Does not prove: physical repulsive gravity.
Does not prove: new gravitational force law.
Does not prove: Einstein-matter PDE well-posedness.
Does not prove: collapse theorem.
Does not prove: black-hole formation theorem.
Does not prove: cosmic censorship.
Does not prove: hoop conjecture.
Does not prove: dark matter replacement.
Does not prove: gravity closure.
Does not prove: unrestricted QL_CollapseGate.
Does not prove: unrestricted UniversalBoundaryCompactness.
Does not prove: unrestricted Chronos-RR.
Does not prove: unrestricted H4.1/FGL.
Does not prove: P vs NP.
Does not prove: Clay problem.
