import importlib.util
from pathlib import Path

import numpy as np
import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "radiative-rigidity" / "pca_rank1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("radiative_rigidity_pca_rank1", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


pca_rank1 = load_module()


def test_radiative_rigidity_is_rank1_accepts_outer_product_matrix():
    u = np.array([1.0, 2.0, 3.0])
    v = np.array([4.0, 5.0])
    assert pca_rank1.is_rank1(np.outer(u, v))


def test_radiative_rigidity_is_rank1_rejects_rank2_identity_matrix():
    assert not pca_rank1.is_rank1(np.eye(2))


def test_radiative_rigidity_is_rank1_rejects_non_2d_input():
    with pytest.raises(ValueError, match="2D array"):
        pca_rank1.is_rank1([1.0, 2.0, 3.0])
