# Quantitative nonprojectivity of fresh 4D Minkowski samples under order-invariant growth

Date: 2026-11-11. Paper theorem: PROVED. Exact rational certificate: COMPUTATION_PASS. Novelty: NOT_ESTABLISHED. Lean: NOT_RUN. Large-prefix Minkowski k-sample limit: OPEN.

## Finite order-invariant growth and the prefix operator

For an order-invariant causal-set growth process, let ν_n be the distribution on **unlabeled** n-element posets at birth stage n. Order-invariance means that conditional on the n-event unlabeled causal order, every valid linear extension is equally likely as its birth order. Therefore ν_2=T ν_3, where T is the Markov kernel deleting the final element of a uniformly random linear extension of an unlabeled three-element poset.

In the order (chain,fork,merge,single-edge,antichain), the two-element comparability probabilities under T are (1,0,1,1/3,0). These numbers follow by independent enumeration of all valid permutations and their initial two-event restrictions.

Let Q_n be the law of the causal order of n **independent, uniformly volume-sprinkled** points of one four-dimensional Minkowski Alexandrov interval. Exact normalized volume moments E[s]=1/20, E[s²]=1/105, E[sf]=1/2100 give

Q_3 = (1/350,9/350,9/350,33/175,53/70).

Thus Q_2(comparable)=1/10, while (TQ_3)(comparable)=16/175. Since the two-point state space has just comparable/incomparable classes,

δ := TV(Q_2,TQ_3)=3/350.

## Theorem: quantitative unavoidable finite-stage error

For ANY order-invariant birth process (finite or infinite), with its two- and three-event unlabeled marginal laws ν_2,ν_3,

TV(ν_2,Q_2) + TV(ν_3,Q_3) >= 3/350,

and therefore

max(TV(ν_2,Q_2), TV(ν_3,Q_3)) >= 3/700.

Proof: projectivity ν_2=Tν_3, the triangle inequality, and total-variation contraction under the Markov kernel T:

TV(Q_2,TQ_3)
<= TV(Q_2,ν_2)+TV(Tν_3,TQ_3)
<= TV(Q_2,ν_2)+TV(ν_3,Q_3).

This is exact and requires no continuum or N→∞ assumption.

## Sharpness for the two-stage minimax constraint

Put ε=3/700. Modify Q_3 by transferring ε mass from the three-event antichain type to the three-event merge type. The resulting valid law ν_3 is

(chain,fork,merge,single,antichain)
=(1/350,9/350,3/100,33/175,527/700).

Choose a uniformly random natural extension of a ν_3-sampled poset, then take its initial two-event prefix. This is an order-invariant **finite three-event growth process**, and ν_2(comparable)=67/700. Hence

TV(ν_2,Q_2)=3/700, TV(ν_3,Q_3)=3/700.

The bound is therefore sharp for **two-stage compatibility**. This construction does NOT prove attainability within a single infinite order-invariant process at all stages.

## Scope and interpretation

- Exact fresh Minkowski-sprinkling laws Q_n are NOT stage-by-stage projective under uniform linear-extension prefix deletion, and no order-invariant process can match them all exactly.
- Even approximating Q_2 and Q_3 simultaneously forces the explicit nonzero error above.
- This **does not** rule out an order-invariant process whose **uniform k-subsets of its n-event prefixes** converge to Q_k as n→∞ for each fixed k. Uniform subsets and initial birth prefixes are different sampling operators.
- It does not establish CSG applicability or a general no-go theorem for the user's uniform-extension limit construction. CSG and order-invariance have different hypotheses.
- Existing paper: Brightwell and Luczak, *Order-invariant measures on causal sets*, Annals of Applied Probability 21 (2011), DOI 10.1214/10-AAP736. This quantitative finite-stage observation is not asserted novel.

## Verification

Standard-library exact-rational certificate: chronos_order_invariant_projectivity_gap_20261111.py; source SHA256 12c0d72cdd4a701886bc23f9d85854a93ca385dfdd770e520921cef03e05601d; checks all five 3-event posets via independent permutation enumeration and constructs the sharp two-stage witness. Local run: PASS.

Research staging only. PR #1347 preserved; no merge, Lean compilation, or Mac local-tree inspection.
