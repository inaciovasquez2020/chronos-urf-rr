def test_exhaustive_validation():
    from itertools import combinations, repeat

    from research_agent_toolkit.adaptive_radius import (
        RadiusAuditor,
        BinaryBasis,
        IncompleteAudit,
    )


    def independent_span_dimension(vertices, edges, radius):
        """Compute the entire span explicitly, without Gaussian elimination."""

        span = {0}
        cutoff = min(len(edges), 2 * radius + 1)

        for size in range(1, cutoff + 1):
            for indices in combinations(range(len(edges)), size):
                degrees = [0] * len(vertices)
                vector = 0

                for index in indices:
                    a, b = edges[index]
                    degrees[a] += 1
                    degrees[b] += 1
                    vector |= 1 << index

                if any(d % 2 for d in degrees):
                    continue

                if vector not in span:
                    span.update({
                        value ^ vector for value in span
                    })

        size = len(span)

        assert size > 0
        assert size & (size - 1) == 0

        return size.bit_length() - 1


    graphs = 0
    checks = 0

    for n in range(6):
        vertices = list(range(n))
        possible = list(combinations(vertices, 2))

        for mask in range(1 << len(possible)):
            edges = [
                edge for i, edge in enumerate(possible)
                if mask & (1 << i)
            ]

            graph = RadiusAuditor(vertices, edges)

            for radius in range(n + 1):
                actual = graph.audit(radius)["local_dimension"]

                expected = independent_span_dimension(
                    vertices, edges, radius
                )

                assert actual == expected, (
                    vertices, edges, radius, actual, expected
                )

                checks += 1

            graphs += 1

    assert graphs == 1100
    assert checks == 6505

    print("INDEPENDENT_SPAN_GRAPHS:", graphs)
    print("INDEPENDENT_SPAN_COMPARISONS:", checks)
    print("INDEPENDENT_LINEAR_ALGEBRA := PASS")


    def must_raise(error, action):
        try:
            action()
        except error:
            return
        raise AssertionError("Expected exception was not raised")


    must_raise(
        IncompleteAudit,
        lambda: RadiusAuditor(range(100), [], max_vertices=10)
    )

    must_raise(
        IncompleteAudit,
        lambda: RadiusAuditor(
            range(10),
            combinations(range(10), 2),
            max_edges=5
        )
    )

    must_raise(
        IncompleteAudit,
        lambda: RadiusAuditor(
            repeat(0), [], max_work=100
        )
    )

    must_raise(
        IncompleteAudit,
        lambda: RadiusAuditor(
            [0, 1], repeat((0, 1)), max_work=100
        )
    )

    must_raise(
        ValueError,
        lambda: RadiusAuditor([0, "vertex"], [])
    )

    must_raise(
        ValueError,
        lambda: RadiusAuditor([True], [])
    )

    must_raise(
        ValueError,
        lambda: RadiusAuditor([], [], max_work=-1)
    )

    ticks = [0]

    def budget():
        ticks[0] += 1
        if ticks[0] > 1:
            raise IncompleteAudit("Elimination limit")

    basis = BinaryBasis(budget)
    basis.add(3)

    must_raise(
        IncompleteAudit,
        lambda: basis.add(3)
    )

    print("ELIMINATION_GUARD := PASS")
    print("UNBOUNDED_INPUT_GUARDS := PASS")
    print("INVALID_INPUT_GUARDS := PASS")

    graph = RadiusAuditor(
        ["claim", "proof", "evidence"],
        [
            ("claim", "proof"),
            ("proof", "evidence"),
            ("evidence", "claim"),
        ]
    )

    assert graph.audit(1)["local_dimension"] == 1

    print("NAMED_DEPENDENCY_GRAPH := PASS")
    print("AI_RADIUS_HARDENING := COMPUTATION_PASS")
