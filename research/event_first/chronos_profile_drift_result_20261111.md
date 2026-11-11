# Event-first Chronos–URF–RR: exact causal-profile drift certificate

Status: PROVED (finite combinatorics), COMPUTATION_PASS (bounded exact tests), asymptotic four-dimensional Minkowski convergence OPEN. Novelty not established. No Lean verification.

## Statement

For a finite poset P of size N, fix any natural linear extension x_1,...,x_N and let I_m={x_1,...,x_m}. Fix 2<=k<=m. Let F_{m,k} denote the probability vector on unlabeled k-poset types obtained by uniform sampling a k-subset of I_m. Let G_{m,k} be the analogous type vector obtained by adjoining the new event x_{m+1} to a uniform (k-1)-subset of I_m.

Then componentwise:

F_{m+1,k} = (1-k/(m+1)) F_{m,k} + (k/(m+1)) G_{m,k}.

Proof: C(m,k)/C(m+1,k)=1-k/(m+1) of uniform k-subsets exclude x_{m+1}; k/(m+1) contain it. Split the sample accordingly.

In a random finite 4D Minkowski diamond sprinkling, sample N i.i.d. volume-uniform points and choose a uniformly random linear extension. Uniform sampling of k points from the entire N-sprinkling has the same law Q_k^(4) as k fresh i.i.d. sprinkled points. Consequently:

Q_k^(4) - E[F_{n,k}] = sum_{m=n}^{N-1} (k/(m+1)) E[G_{m,k}-F_{m,k}].

The total-variation bound follows by triangle inequality:

d_TV(E[F_{n,k}],Q_k^(4)) <= sum_{m=n}^{N-1} (k/(m+1)) E[d_TV(G_{m,k},F_{m,k})].

Thus an absolute weighted-drift tail vanishing in the iterated limit n->infinity after limsup N->infinity is sufficient for Minkowski induced-order sampling convergence. Signed drift cancellation means it is not necessary. The exact signed identity itself is a necessary-and-sufficient reformulation at each finite N.

## Pair observable

Let R_m=# comparable pairs in I_m and p_m=R_m/C(m,2). For new maximal event v=x_{m+1}, d_m=# ancestors of v among the first m events (= all ancestors of v). Then

p_{m+1} - p_m = (2/(m+1))(d_m/m - p_m).

For finite sprinklings, E[p_N]=1/10 in 4D, so

1/10 - E[p_n] = sum_{m=n}^{N-1}(2/(m+1))(E[d_m/m]-E[p_m]).

The one-step drift is not guaranteed nonnegative: in the three-point fork (past masks [0,1,1]), a uniformly selected natural extension yields p_2=1, p_3=2/3.

## Validation and boundaries

Standalone standard-library Python script `chronos_profile_drift_audit_20261111.py` validates the general vector identity for k=2,3,4 where permitted, individual linear extensions, and the telescoping identity under uniform extension averaging. All forward-edge configurations on n=2..5 vertices were transitively closed and tested: 69,182 exact rational assertions PASS. This verifies finite combinatorial implementation only, not the sampling-limit theorem.

Primary literature context: Brightwell and Luczak, Order-Invariant Measures on Causal Sets, Annals of Applied Probability 21 (2011), DOI 10.1214/10-AAP736; De Loof, De Meyer and De Baets, Exploiting the Lattice of Ideals Representation of a Poset (2006), DOI 10.3233/FUN-2006-712-309. No priority or independent review claims.

OPEN: prove or refute vanishing of the signed Minkowski weighted-drift tail for every fixed k. OPEN: metric-free selecting law and gravitational dynamics. No repo merge permitted by this certificate.