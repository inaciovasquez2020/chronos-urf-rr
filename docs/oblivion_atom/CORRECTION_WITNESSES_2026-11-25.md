# Mathematical erratum — local span and witness extraction

Base: `fe829fb3fd29ca687db376f60420708526a6132b`.

## [docs/oblivion_atom/theory/cycle_local_rigidity_constants.tex](../../docs/oblivion_atom/theory/cycle_local_rigidity_constants.tex)

The per-ball rank bound is valid for connected radius-$R$ balls, but the global span bound is false. Even if all rooted balls are isomorphic, their embedded cycle spaces need not coincide. For even $m\ge6$, the connected vertex-transitive degree-four toroidal grid $C_m\square C_m$ contains $m^2/4$ vertex-disjoint unit squares in radius-two balls. Their edge vectors are linearly independent. Thus $C_2(G)\ge m^2/4$ while $T_r(G)=1$ for every $r,k$. The global constant bound is refuted.

## [docs/oblivion_atom/theory/cycle_witness_extraction.tex](../../docs/oblivion_atom/theory/cycle_witness_extraction.tex)

The proof's arbitrary-basis inference is invalid: a basis vector of a sum need not belong to any constituent subspace. Instead let $U_v=\iota_{v*}Z_1(B_R(v))$, choose a basis of each $U_v$, and extract a maximal independent subset of their finite union. This is a basis of $W=\sum_v U_v$, because the union spans $W$. Assign each chosen vector to a ball containing it. This proves the stated vector count when vertex repetitions are allowed. If distinct centers are required and $D=\max_v\dim U_v>0$, each center can support at most $D$ chosen independent vectors; hence at least $\lceil C_R(G)/D\rceil$ distinct centers occur. Selecting one assigned vector at each center gives independent vectors with distinct supporting centers. The stronger distinct-center count $C_R(G)$ is not established. In fact for $G=K_5$, $R=1$, the rank is six but there are only five vertices, so that count is false in general.

The corrected basis argument is a paper proof, not a new Lean certificate. Historical text and existing verification artifacts are retained. No PDF changes.
