# Chronos Repository-Native Zero-Arity Carrier Migration Target — 2026-05-11

Status: FRONTIER_OPEN / REPOSITORY_NATIVE_INTERFACE_REDUCTION_ONLY.

This artifact replaces the local `CarrierData` dependency with an abstract repository-native interface target.

Formal theorem:

- `zero_arity_carrier_exhaustiveness_from_repository_native_interface`

The theorem proves that zero-arity carrier exhaustiveness follows from the following explicit repository-native obligations:

1. native `Carrier`;
2. native `Registry`;
3. native arity map;
4. native carrier-to-registry map;
5. native registry generation relation;
6. native registry finiteness predicate;
7. native zero-arity representation predicate;
8. native finite represented atom predicate;
9. carrier registry generation;
10. finite carrier registry;
11. zero-arity representation from arity zero;
12. finite represented atom from finite registry.

Boundary:

- This is a repository-native interface reduction only.
- This does not prove that the current Chronos repository-native `Carrier` satisfies the interface.
- This does not prove that the current Chronos repository-native `Registry` satisfies the interface.
- This is not unrestricted Chronos-RR closure.
- This is not H4.1/FGL closure.
- This is not UniversalFiberEntropyGap closure.
- This is not P vs NP closure.
- This is not Clay-problem closure.

Next weakest missing object:

`RepositoryNativeZeroArityInterface` instantiated by the active Chronos repository-native `Carrier` and `Registry`.
