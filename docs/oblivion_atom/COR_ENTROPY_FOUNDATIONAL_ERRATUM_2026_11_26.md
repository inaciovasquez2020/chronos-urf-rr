# COR and EntropyDepth foundational mathematical erratum

Date: 2026-11-26. Base commit 964afae98ff6938a6c2faf22d8275ab667c402bc. Paper proofs and counterexamples; Lean NOT_RUN; independent novelty NOT_ESTABLISHED. Frozen historical files, existing Lean declarations and artifacts are preserved. This note supersedes the specific unsupported or false claims identified below.

## 1. Global cycle rank is not bounded by the number of local types

The actual definition in docs/oblivion_atom/formal_definitions.md is COR_R(G)=dim_F2 Z_R(G), where Z_R is the span of all cycles contained in induced radius-R balls. Distinct embeddings of the same template may be independent vectors in the global edge space.

For m>=3 let G_m be the Cartesian product C_m square K_3. This is a connected simple degree-four graph on 3m vertices, with 6m edges, and its full cycle rank is 3m+1. Independent rotations and permutations of the factors act transitively on vertices, so every isomorphism-invariant rooted neighborhood type is the same, for every k and R. The m triangular fibers have pairwise disjoint edge supports, so they are independent and contained in radius-one balls. Thus COR_R(G_m)>=m for every R>=1. For degree bound four, every positive-radius finite threshold in the claimed homogeneous-graph rigidity lemma fails. If radius zero is allowed, a positive threshold can make the implication vacuous. This is not a refutation of separately defined maximum-per-ball cycle rank, or of a quotient of the global edge space identifying embeddings.

The proof in proofs/oblivion_atom/COR_type_collapse_lemma.md incorrectly bounds the dimension of the span of embedded vectors by the number of templates. Even genuine rooted ball isomorphism, stronger than logical equivalence, does not imply that bound. The explicit constants based only on template count fail for the same reason.

## 2. Exact COR spectrum of the counterexample family

For nonnegative integral R:
- R=0: COR=0.
- R=1: COR=6 for m=3, and COR=m for m>=4.
- R>=2: COR=3m when m>2R+1; COR=3m+1 when m<=2R+1.

Proof. At radius one with m>=4 the ball consists of the fiber triangle with two pendant vertices. For m=3 its two factor triangles meet at the root; the three triangles of each factor direction have disjoint edge supports, yielding six independent cycles. At radius at least two, include all m fiber triangles and two squares per base edge, connecting layer 0 to layers 1 and 2. Every square is contained in a radius-two ball. The longitudinal edge in layer 1 or 2 identifies its unique chosen square, so these 2m squares and m triangles are jointly independent. Project edge chains onto C_m by taking each longitudinal edge to its base edge and each fiber edge to zero. The induced map on cycle spaces is surjective, because a longitudinal cycle in one layer maps to the generator of Z_1(C_m). Hence its kernel has dimension 3m. If m>2R+1 the projection of each ball lies within a proper induced path in C_m, so any cycle supported there maps to zero. This gives the matching upper bound 3m. If m<=2R+1 a full longitudinal cycle lies within an R-ball centered in its layer, giving the remaining independent dimension.

Finite corroboration (container Python 3.13.5, not Mac): the earlier unsupported 312-check receipt is withdrawn. Two actual executions of the exact verifier produced byte-identical logs. It checked all 390 combinations m=3..80 and R=0..4 against the full formula; 464 binary linear subspaces through dimension five; 13,130 exact class marginal comparisons; 464 optimal decision-tree computations; 3,876 exact entropy identity distributions; 2,198 exhaustive small-graph packing cases; and 3,297 power-graph color/cover cases. Source and log are preserved in [URF-Core at commit cf314c9390dfbac2e3f0ad100eb7c372f1bd1ad7](https://github.com/inaciovasquez2020/urf-core/tree/cf314c9390dfbac2e3f0ad100eb7c372f1bd1ad7/research/certificates/foundational_audit_20261126). Source Git blob 8e6e170deceda441a317933214464a38c6045d45, log Git blob 9c2e874e1c98a659eb73291773ca036b2dcd907e; source SHA256 70246207a9063fea2d61a1b206eec3355c231d7218d1ac1c7fb72bac89e75300. Run python3 -B urf_foundations_audit.py without optimization. A 90-second alarm exits nonzero on timeout. Finite evidence only; Lean NOT_RUN.

## 3. General replacement: packing gives linear rank

Let G have n>0 vertices, maximum degree at most D, and let M(D,2R) bound the size of any radius-2R ball, for example sum_{j=0}^{2R} D^j with the j=0 term defined as 1. Let S be the set of centers whose induced R-balls contain a cycle. Greedily select a center from S and remove all remaining centers within distance 2R. Each selection removes at most M centers; therefore at least ceil(|S|/M) centers are selected. Their R-balls are pairwise vertex-disjoint by the triangle inequality. Choose one cycle per selected ball. The cycles have disjoint nonempty edge supports, so they are independent in the global F2 cycle space. Consequently
COR_R(G) >= ceil(|S|/M(D,2R)).
Also COR_R(G) <= beta_1(G) <= |E(G)| <= Dn/2.
In particular on any vertex-transitive bounded-degree family at fixed R, either every ball is acyclic and COR=0, or COR=Theta(n) on those members with a cyclic ball. The same conclusion holds for isomorphic rooted balls, or a class in which the relevant local cycle-existence property is uniform. Mere FO^k equivalence is not assumed to detect cycle existence.

## 4. Expander and lift claims

The Lcake=COR identity is valid by definition (both are the dimension of the sum of embedded local cycle spaces). However the universal bounded-degree-expander O(1) claim is false. Take a fixed-degree regular spectral expander family H_n and form H_n square K_3. It is regular of degree d+2, and its combinatorial Laplacian is L_H tensor I + I tensor L_K3. Eigenvectors are tensor products, so its smallest nonzero eigenvalue is min(lambda_2(L_H),3), uniformly positive. Yet each of the n triangle fibers contributes one independent radius-one cycle; COR_R>=n for R>=1. This is a counterexample even for connected spectral expanders. The reported empirical counts may describe the tested family only. High-girth graphs with girth>2R+1 have acyclic R-balls: any non-tree edge of a BFS tree in a ball would give a fundamental cycle of length <=2R+1. Thus high girth, not expansion alone, suffices for COR_R=0.

The random-lift TODO asserting extensive fixed-radius COR from a cyclic base is not established by a base cycle alone. For the connected base C_l, l>=3, any n-sheet cover is a disjoint union of cycles of lengths l times the cycle lengths of the monodromy permutation. Under independent uniform edge permutations the monodromy is uniform in S_n. At fixed R, only components of length <=2R+1 can contribute. For each j<=floor((2R+1)/l), the expected number of j-cycles of a uniform permutation is 1/j (count j-subsets, cyclic orderings and arbitrary remaining permutations). Hence expected COR is at most the fixed harmonic sum over those j; by Markov's inequality COR/n converges to zero in probability. This refutes the general cyclic-base claim for this uniform cover model, not every possible lift distribution or an increasing-R regime.

## 5. Correct entropy-to-depth transfer

For fixed finite hidden X and nested observations S_t, H(X|S_t)-H(X|S_{t+1})=I(X;S_{t+1}|S_t). A global per-round cap c>0 gives T >= (H(X|S_0)-H(X|S_T))/c. The COR hypothesis alone does not specify a distribution or terminal recovery criterion. If X is uniform on a specified F2 cycle space of rank h, H(X)=h bits; a linear lower bound follows when h=Omega(n), initial transcript is independent, full recovery is necessary, and the cap is constant. For merely deciding a Boolean function, full recovery is not implied. If the input is n bits, no telescoping fixed-input Shannon entropy budget can exceed n bits; obtaining Omega(n log n) rounds requires a different justified target entropy scale, a smaller per-round cap, or another lower-bound mechanism. The historical patch amplification claim is not established by the cited bridge. A linear lower bound is compatible with polynomial time.

The historical unconditional equivalence of evolving marginal configuration entropy loss and transcript gain is false in general: erase uniform n-bit state while the transcript stays constant. State entropy drops n bits; observed information gain is zero. The fixed-hidden-variable identity above is retained. No conclusion is asserted about independently verified Lean results.

## 6. Clause-dual distance and actual XOR-SAT decision

In the clause-dual manuscript the minimum nonzero support d is defined only if ker(A^T) is nonzero (or an explicit infinity convention is used). A parity-one coset for w in ker(A^T) is unsatisfiable for Ax=b; the parity-zero coset need not be satisfiable when there are other independent dual constraints. Thus distinguishing the two parity-conditioned distributions is not automatically distinguishing satisfiable from unsatisfiable instances.

A separate exact theorem fixes this. Let U=im(A) be a proper linear subspace of F2^m, D=U^perp, d=min_{0!=w in D} |supp(w)|. Compare uniform b in U with uniform b in its complement. For any T of size<d, the coordinate projection U -> F2^T is surjective: otherwise a nonzero functional on F2^T annihilates the projection and extends by zeros to a dual vector of weight<d. Uniform b in U therefore has uniform T-marginal. Since the full uniform law is a mixture of the two class laws with nonzero weights, the complement also has uniform T-marginal. In an adaptive coordinate query tree with independent seed and no other input-dependent information, fixing the seed makes every leaf with fewer than d distinct queries a partial-assignment cylinder. Its probabilities agree under the two laws. Hence fewer than d total distinct queries on every path give zero distinguishing bias. Conversely query the support of a weight-d dual vector: reject on parity one, accept otherwise. Parity is zero on U and one on exactly 2^{m-1} inputs outside U; thus balanced-class success exceeds 1/2. The exact minimum worst-case query budget for positive bias is d, or ceil(d/q) completed rounds when q>0 queries may be made per round.

For zero-error deterministic decision on all inputs, let J be the union of the supports of all dual vectors. On b=0, every coordinate j in J must be read: flipping an unread such coordinate gives e_j not in U with the same execution path. Conversely reading J suffices to evaluate all dual constraints. The exact deterministic worst-case coordinate-query complexity is |J|, including 0 when D is trivial. This result is separate from the parity-wall correction in PR #1385; it assumes explicit coordinate access, not unrestricted FO locality or arbitrary aggregation. No polynomial-time separation follows.

## Inspected source blobs

- docs/oblivion_atom/formal_definitions.md: a51c3e634a59acffb10f14e3eabf341609f21278
- proofs/oblivion_atom/COR_type_collapse_lemma.md: 520bf060c54a553104824ba0a8091d00f935a4e8
- docs/oblivion_atom/explicit_COR_constant.md: 389fd83d79741258f63590a102acf753176fd0e7
- docs/oblivion_atom/constant_c_kDeltaR_spec.md: 5ba7aa62b92e1e6bf6756e9c1d17bcc682301702
- docs/oblivion_atom/lcake_oblivion_integration.md: 65080a1afdbe8433d14f19e7be7a8faf3cb714e4
- docs/oblivion_atom/TODO_formal_closure.md: e6666097f336888eb70220ca664be066d17e9cf7
- docs/oblivion_atom/cor_entropydepth_bridge.md: d1a77571256797aabe69a0fefcdd4c50b4e69568
- docs/oblivion_atom/entropydepth_lower_bound.md: d6ffaaaecec67abb5959a3b93e5012e2598cdc1d
- docs/final_walls.md: f0d46ae545aa24eb105f6563c15d76402cd0d9fc
- docs/referee/PROVEN_RESULTS.md: 51e1ab25292317f623ed4185a77752dd80427fb1
- manuscripts/chronos_core/ClauseDualDistanceEntropyDepth.tex: a77b20ff8898be2537730d7549c3259d2af507c3

Historical certificates and their source declarations are not modified. These corrections concern the stated mathematical models; unrestricted TRAP, P vs NP, and transfer to unrelated physical or topological claims remain OPEN.
