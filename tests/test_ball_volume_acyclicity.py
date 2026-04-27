from tools.verify_ball_volume_acyclicity import certify, volume_bound


def test_old_two_r_cycle_bound_has_triangle_counterexample():
    cert = certify(
        3,
        [(0, 1), (1, 2), (2, 0)],
        root=0,
        radius=1,
        delta_bound=2,
    )
    assert cert.girth == 3
    assert cert.ball_cardinality == 3
    assert cert.ball_acyclic is False
    assert cert.old_two_r_bound_counterexample is True


def test_volume_bound_degree_cases():
    assert volume_bound(0, 10) == 1
    assert volume_bound(1, 0) == 1
    assert volume_bound(1, 5) == 2
    assert volume_bound(2, 3) == 7
    assert volume_bound(3, 2) == 10


def test_girth_gt_ball_card_implies_ball_acyclic_on_cycle6_radius1():
    cert = certify(
        6,
        [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)],
        root=0,
        radius=1,
        delta_bound=2,
    )
    assert cert.girth == 6
    assert cert.ball_cardinality == 3
    assert cert.hypothesis_girth_gt_ball_card is True
    assert cert.ball_acyclic is True


def test_bounded_degree_volume_certificate_on_path():
    cert = certify(
        5,
        [(0, 1), (1, 2), (2, 3), (3, 4)],
        root=2,
        radius=2,
        delta_bound=2,
    )
    assert cert.girth is None
    assert cert.ball_cardinality == 5
    assert cert.ball_acyclic is True
    assert cert.ball_cardinality <= cert.volume_bound
