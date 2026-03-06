# toolkit/oblivion/scripts/gf2_csr.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Tuple, Dict
import numpy as np

try:
    from scipy.sparse import csr_matrix
except Exception as e:
    raise RuntimeError("scipy is required: pip install scipy") from e


@dataclass(frozen=True)
class GF2CSR:
    A: "csr_matrix"  # uint8 data, arithmetic interpreted mod 2

    @property
    def shape(self) -> Tuple[int, int]:
        return self.A.shape

    def mv(self, v: np.ndarray) -> np.ndarray:
        v = v.astype(np.uint8, copy=False)
        y = self.A.dot(v)
        return (y & 1).astype(np.uint8)

    def mm(self, X: np.ndarray) -> np.ndarray:
        X = X.astype(np.uint8, copy=False)
        Y = self.A.dot(X)
        return (Y & 1).astype(np.uint8)


def build_incidence_gf2_csr(
    n_rows: int,
    n_cols: int,
    ones: Iterable[Tuple[int, int]],
) -> GF2CSR:
    rows: List[int] = []
    cols: List[int] = []
    for r, c in ones:
        if r < 0 or r >= n_rows or c < 0 or c >= n_cols:
            raise ValueError(f"Index out of bounds: ({r},{c}) in shape {(n_rows,n_cols)}")
        rows.append(r)
        cols.append(c)

    data = np.ones(len(rows), dtype=np.uint8)
    A = csr_matrix((data, (np.array(rows), np.array(cols))), shape=(n_rows, n_cols), dtype=np.uint8)
    A.sum_duplicates()
    A.data &= 1  # mod 2
    A.eliminate_zeros()
    return GF2CSR(A=A)
