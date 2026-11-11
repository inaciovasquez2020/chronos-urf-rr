# Weighted barrier-rank sandwich and a refuted count-only shortcut

Date: 2026-11-11. Status: PROVED (finite posets, direct proof); COMPUTATION_PASS (independent exact audit); 4D asymptotics OPEN; Lean NOT_RUN; independent review OPEN.

## Definitions

Let P be a finite poset of N events and x minimal. Put U={y:x<y}, u=|U|>0, and A=P\({x}∪U), a=|A|. Let Q=P\{x}. For a fixed linear extension alpha of A and beta=(beta_1,...,beta_u) of U, put

c_j=max {rank_alpha(z): z∈A and z<beta_i for some i<=j}, with max(empty)=0.

**Important:** c_j is a CUMULATIVE maximum, not a count or the rank of predecessors of beta_j alone. It is nondecreasing. A valid interleaving has its j-th U symbol after at least c_j A symbols.

Let W(alpha,beta) be the number of valid interleavings (computed by the barrier DP). Choose (alpha,beta) with probability proportional to W(alpha,beta). Set

C_1 = E_weighted[c_1], C_u=E_weighted[c_u].

Let B_x denote the rank of the first strict successor of x in a uniform linear extension of Q; let Delta_x=E[B_x]-N/(u+1).

## Theorem: correct rank-sensitive two-sided inequality

For each fixed (alpha,beta), the constant barriers (c_1,...,c_1) and (c_u,...,c_u) bound c coordinatewise. Conditioning the uniform-shuffle distributive lattice on stronger barrier constraints stochastically delays the first U. Under a constant barrier r, the first-U rank has mean

  E[B_const(r)] = r + (N-r)/(u+1) = (N+r*u)/(u+1).

Averaging with **W(alpha,beta)** weights gives

  [u/(u+1)] C_1 <= Delta_x <= [u/(u+1)] C_u,

and therefore the corrected first-birth probability bounds

  (u+1)/(N+u*C_u) <= Pr_P(x first) <= (u+1)/(N+u*C_1).

This is a finite-poset theorem. It is exact when all valid barriers are constant (notably when u=1). It can improve the previously proved crude size-only bounds, but is not uniform-in-N geometric control: C_u can approach a.

## Explicit refutation of tempting count-only upper bound on Delta

Take four elements with relations 0<2 and 1<2; 3 is isolated. Candidate x=0. Then U={2}, A={1,3}, u=1, and only one A element (1) is a predecessor of U. However, the internal A linear extensions are (1,3) with barrier c=1 and two valid interleavings, and (3,1) with barrier c=2 and one valid interleaving.

Thus C_1=C_u=(2*1+1*2)/3=4/3, E[B]=8/3, and

  Pr(x first)=3/8;  Delta_x=2/3.

The invalid shortcut C_u<= number of A elements preceding some U would give C_u<=1, incorrectly predicting Pr(x first)>=2/5. Since 3/8<2/5, **the count-only shortcut is REFUTED**.

This counterexample does NOT refute the previously published lower bound Pr(x first)>=1/(N-u)=1/3, which remains true.

## Independent exact certificates

- Reran existing local barrier certificate: 2,121 finite-poset / candidate checks PASS.
- New standalone standard-library Python: all forward-edge transitive closures with N=2,3,4,5, every eligible minimal event: 1,761 exact rank-sensitive sandwich checks PASS.
- In 224 of those cases, the invalid count-only improvement was refuted; 501 cases had nonzero interval width between the correct bounds.
- All first-birth probabilities crosschecked against independent full-poset linear-extension enumeration.
- N=6 extension and 4D asymptotics NOT_RUN. No resource failure counted as pass.

## Next mathematical obstruction

Estimate the W-weighted **rank** of geometrically required external predecessors in 4D Minkowski sprinklings. Their number alone is insufficient; even a single predecessor may appear late among incomparable events. The full barrier distribution and its completion-weight bias remain OPEN.

Repository staging only: no Lean kernel verification, no independent novelty claim, no 4D sampling convergence, no emergent-gravity theorem.
