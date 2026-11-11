# Replica-overlap to sampling-profile transfer (2026-11-11)

## Mathematical theorem
Let P be any finite poset, A,B order ideals of the same size n, and k≤n. Define Q_k(A) and Q_k(B) as the distributions of unlabelled induced k-point posets sampled uniformly without replacement from A and B. Put r=|A\B|=|B\A|=|A△B|/2. Then

d_TV(Q_k(A),Q_k(B)) ≤ 1 - binom(n-r,k)/binom(n,k) ≤ min(1,kr/n).

The binomial expression is understood to be zero if n-r<k. Proof: Couple both k-subsets by using the same uniform k-subset of the n-r common elements on the event that the random k-subset lies wholly in the intersection. The complementary event has probability 1-binom(n-r,k)/binom(n,k). A union bound gives ≤ kr/n. Causal-order types agree on the intersection.

For independent uniformly chosen linear extensions of P, let I_n,J_n denote the prefixes and D(P,n)=E[|I_n△J_n| | P]. The same coupling gives

E[d_TV(Q_k(I_n),Q_k(J_n)) | P] ≤ k D(P,n)/(2n).

Therefore, if E[D(P_N,n_N)]/n_N→0 along any sequence with n_N≥k, then induced k-point sampling profiles of two independent prefix histories converge together in mean total variation. This is a *history-robustness* theorem, not a proof of convergence to a Minkowski poset limit.

## Validation
Standalone standard-library script chronos_replica_sampling_transfer_audit.py: 56,088 exact checks on all transitive closures from naturally oriented edge patterns through N=5, comparing distinct prefix ideals, k≤3. PASS. No claim of exhaustive geometric 4D sampling checks. Mac repo build NOT_RUN. Lean NOT_RUN. Independent human mathematical review OPEN.

## Open question
Determine whether normalized replica disagreement tends to zero for uniformly linear-extended four-dimensional Minkowski sprinklings at fixed positive prefix fraction, or prove a positive asymptotic lower bound. Even that answer does not settle the iterated n-after-N Minkowski uniform-tail sampling limit.

Research staging only: no merge, no physical emergence claim.