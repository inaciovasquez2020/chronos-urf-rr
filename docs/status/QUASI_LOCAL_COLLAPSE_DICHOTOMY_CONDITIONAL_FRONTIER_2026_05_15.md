# Quasi-Local Collapse Dichotomy Conditional Frontier

Status: CONDITIONAL_FRONTIER_FRAMEWORK_ONLY

Source: uploaded frontier formulation. :contentReference[oaicite:1]{index=1}

## Object

`QuasiLocalCollapseDichotomy`

## AdmissibleEinsteinMatterData

An admissible datum is a tuple `(Sigma, h, K, Phi)` satisfying:

- `Sigma` is a smooth connected noncompact 3-manifold.
- `h` is a Riemannian asymptotically flat metric.
- `K` is a symmetric extrinsic-curvature tensor.
- `Phi` is an Einstein-matter field in the maximal Cauchy development.
- The Hamiltonian and momentum constraints hold.
- The dominant energy condition holds.
- ADM mass is finite.
- There is no past trapped boundary.
- Generic nondegeneracy is assumed.

## Covariant objects

For maximal Cauchy development `(M,g,Phi)` and compact region `R subset M`:

- `D_plus(R)` is the future causal/domain-of-dependence region used by the frontier.
- `C_partial(R,epsilon)` is a covariant quasi-local boundary-capacity placeholder.
- `QL_CollapseGate(R)` is a conditional quasi-local collapse predicate.

## Conditional statements

### Statement I

`CosmicCensorship and HoopConjecture imply QL_CollapseGate(R) implies TrappedSurface(D_plus(R)).`

### Statement II

`CosmicCensorship implies not QL_CollapseGate(R) implies NoVisibleNakedSingularity(D_plus(R), Scri_plus).`

## Boundary

Conditional surface only.

Does not prove:

- unrestricted `QL_CollapseGate`
- unrestricted nonspherical collapse exclusion
- Cosmic Censorship
- Hoop Conjecture
- unrestricted `UniversalBoundaryCompactness`
- unrestricted Chronos-RR
- H4.1/FGL
- P vs NP
- any Clay-problem closure

## Next restricted targets

1. Prove the spherical Misner-Sharp threshold version.
2. Encode an axisymmetric perturbative version.
3. Replace `QL_CollapseGate` by an explicit Hawking-energy sufficient condition.
4. Keep Cosmic Censorship and Hoop Conjecture as explicit assumptions.
