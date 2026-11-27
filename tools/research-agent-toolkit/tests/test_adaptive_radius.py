def test_exhaustive_validation():
    from itertools import combinations
    from research_agent_toolkit.adaptive_radius import (
        RadiusAuditor,
        IncompleteAudit,
        independent_oracle,
    )

    graphs = 0
    checks = 0


    def cycle(n):
        return [(i, (i + 1) % n) for i in range(n)]


    print("=== EXHAUSTIVE INDEPENDENT ORACLE ===")

    for n in range(6):
        vertices = list(range(n))
        possible = list(combinations(vertices, 2))

        for mask in range(1 << len(possible)):
            edges = [
                e for i, e in enumerate(possible)
                if mask & (1 << i)
            ]

            graph = RadiusAuditor(vertices, edges)
            previous = 0

            for radius in range(n + 1):
                result = graph.audit(radius)
                expected = independent_oracle(
                    vertices, edges, radius
                )

                local = result["local_dimension"]

                assert local == expected, (
                    vertices, edges, radius,
                    result, expected
                )

                assert local >= previous
                previous = local
                checks += 1

            assert previous == graph.dimension()
            graphs += 1

    print("LABELED_GRAPHS:", graphs)
    print("EXACT_RADIUS_CHECKS:", checks)
    print("INDEPENDENT_ORACLE := PASS")


    print("=== ADVERSARIAL NETWORKS ===")

    for n in range(3, 65):
        graph = RadiusAuditor(range(n), cycle(n))

        for radius in range(n // 2 + 1):
            expected = int(2 * radius + 1 >= n)
            actual = graph.audit(radius)

            assert actual["local_dimension"] == expected

    print("CYCLE_THRESHOLD_TESTS := PASS")


    tree = RadiusAuditor(
        range(64),
        [(i, i + 1) for i in range(63)]
    )

    assert tree.dimension() == 0
    assert tree.audit(0)["coverage"] is None
    assert tree.adaptive(4)["status"] == "SATURATED"

    print("ACYCLIC_BOUNDARY := PASS")


    disconnected = RadiusAuditor(
        range(9),
        cycle(3) + [
            (a + 3, b + 3)
            for a, b in cycle(6)
        ]
    )

    assert disconnected.dimension() == 2
    assert disconnected.audit(1)["local_dimension"] == 1
    assert disconnected.audit(3)["local_dimension"] == 2

    print("DISCONNECTED_COMPONENTS := PASS")


    try:
        RadiusAuditor(
            range(20), cycle(20),
            max_work=1
        ).audit(1)
    except IncompleteAudit:
        print("RESOURCE_GUARD := PASS")
    else:
        raise AssertionError("Resource guard failed")


    try:
        RadiusAuditor([0], [(0, 0)])
    except ValueError:
        print("INVALID_GRAPH_REJECTION := PASS")
    else:
        raise AssertionError("Invalid graph accepted")


    print("=== AI STRUCTURAL AUDIT DEMONSTRATION ===")

    graph = RadiusAuditor(
        range(12),
        cycle(12) + [(0, 3), (3, 6), (6, 9)]
    )

    for entry in graph.adaptive(6)["profile"]:
        print(entry)

    print("ADAPTIVE_RADIUS_ENGINE := COMPUTATION_PASS")
