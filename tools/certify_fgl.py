#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from fractions import Fraction
from pathlib import Path
from typing import Any, List, Sequence, Tuple


Matrix = List[List[Any]]


@dataclass(frozen=True)
class Field:
    name: str
    p: int | None = None

    @staticmethod
    def parse(name: str) -> "Field":
        s = name.strip()
        if s in {"Q", "QQ", "Rational", "rationals"}:
            return Field("Q", None)

        m = re.fullmatch(r"(?:GF|Fp|F_p)\((\d+)\)", s)
        if m:
            p = int(m.group(1))
            if p < 2:
                raise ValueError("field characteristic must be prime >= 2")
            return Field(f"GF({p})", p)

        m = re.fullmatch(r"GF(\d+)", s)
        if m:
            p = int(m.group(1))
            if p < 2:
                raise ValueError("field characteristic must be prime >= 2")
            return Field(f"GF({p})", p)

        raise ValueError(f"unsupported field: {name}")

    def elt(self, x: Any) -> Any:
        if self.p is None:
            if isinstance(x, Fraction):
                return x
            if isinstance(x, int):
                return Fraction(x)
            if isinstance(x, str):
                return Fraction(x)
            return Fraction(x)

        if isinstance(x, str):
            if "/" in x:
                q = Fraction(x)
                num = q.numerator % self.p
                den = q.denominator % self.p
                return (num * pow(den, -1, self.p)) % self.p
            return int(x) % self.p

        if isinstance(x, Fraction):
            num = x.numerator % self.p
            den = x.denominator % self.p
            return (num * pow(den, -1, self.p)) % self.p

        return int(x) % self.p

    def zero(self) -> Any:
        return Fraction(0) if self.p is None else 0

    def one(self) -> Any:
        return Fraction(1) if self.p is None else 1

    def add(self, a: Any, b: Any) -> Any:
        if self.p is None:
            return a + b
        return (a + b) % self.p

    def sub(self, a: Any, b: Any) -> Any:
        if self.p is None:
            return a - b
        return (a - b) % self.p

    def mul(self, a: Any, b: Any) -> Any:
        if self.p is None:
            return a * b
        return (a * b) % self.p

    def neg(self, a: Any) -> Any:
        if self.p is None:
            return -a
        return (-a) % self.p

    def inv(self, a: Any) -> Any:
        if a == self.zero():
            raise ZeroDivisionError("division by zero")
        if self.p is None:
            return 1 / a
        return pow(a % self.p, -1, self.p)

    def div(self, a: Any, b: Any) -> Any:
        return self.mul(a, self.inv(b))

    def is_zero(self, a: Any) -> bool:
        return a == self.zero()

    def out(self, a: Any) -> Any:
        if self.p is None:
            return str(a)
        return int(a)


@dataclass(frozen=True)
class FGLCertificate:
    field: str
    basis_size: int
    test_count: int
    witness_count: int
    rank_T: int
    rank_N: int
    rank_NK: int
    kernel_dim_T: int
    kernel_contained_in_witness: bool
    annihilates_witness: bool
    quotient_rank_valid: bool
    status: str


def normalize_matrix(A: Sequence[Sequence[Any]], F: Field) -> Matrix:
    if A is None:
        return []
    return [[F.elt(x) for x in row] for row in A]


def transpose(A: Matrix) -> Matrix:
    if not A:
        return []
    return [list(row) for row in zip(*A)]


def zero_col_matrix(rows: int) -> Matrix:
    return [[] for _ in range(rows)]


def validate_rectangular(A: Matrix, name: str) -> None:
    if not A:
        return
    n = len(A[0])
    for i, row in enumerate(A):
        if len(row) != n:
            raise ValueError(f"{name} row {i} has length {len(row)} but expected {n}")


def hcat(A: Matrix, B: Matrix) -> Matrix:
    if not A and not B:
        return []
    if not A:
        return B
    if not B:
        return A
    if len(A) != len(B):
        raise ValueError(f"row count mismatch in hcat: {len(A)} vs {len(B)}")
    return [ra + rb for ra, rb in zip(A, B)]


def matmul(A: Matrix, B: Matrix, F: Field) -> Matrix:
    if not A:
        return []
    if not B:
        return [[] for _ in range(len(A))]
    validate_rectangular(A, "A")
    validate_rectangular(B, "B")
    if len(A[0]) != len(B):
        raise ValueError(f"inner dimension mismatch: {len(A[0])} vs {len(B)}")

    BT = transpose(B)
    out: Matrix = []
    for row in A:
        out_row = []
        for col in BT:
            s = F.zero()
            for a, b in zip(row, col):
                s = F.add(s, F.mul(a, b))
            out_row.append(s)
        out.append(out_row)
    return out


def is_zero_matrix(A: Matrix, F: Field) -> bool:
    return all(F.is_zero(x) for row in A for x in row)


def rref(A: Matrix, F: Field) -> Tuple[Matrix, List[int]]:
    A = [row[:] for row in A]
    validate_rectangular(A, "A")
    if not A:
        return A, []

    m = len(A)
    n = len(A[0])
    pivots: List[int] = []
    r = 0

    for c in range(n):
        pivot = None
        for i in range(r, m):
            if not F.is_zero(A[i][c]):
                pivot = i
                break

        if pivot is None:
            continue

        A[r], A[pivot] = A[pivot], A[r]
        scale = A[r][c]
        A[r] = [F.div(x, scale) for x in A[r]]

        for i in range(m):
            if i != r and not F.is_zero(A[i][c]):
                factor = A[i][c]
                A[i] = [F.sub(x, F.mul(factor, y)) for x, y in zip(A[i], A[r])]

        pivots.append(c)
        r += 1
        if r == m:
            break

    return A, pivots


def rank(A: Matrix, F: Field) -> int:
    if not A:
        return 0
    _, pivots = rref(A, F)
    return len(pivots)


def nullspace_basis_columns(A: Matrix, F: Field) -> Matrix:
    validate_rectangular(A, "A")
    if not A:
        raise ValueError("cannot infer ambient dimension from empty test matrix")

    R, pivots = rref(A, F)
    n = len(A[0])
    pivot_set = set(pivots)
    free_cols = [j for j in range(n) if j not in pivot_set]

    if not free_cols:
        return zero_col_matrix(n)

    cols: List[List[Any]] = []

    for free in free_cols:
        x = [F.zero() for _ in range(n)]
        x[free] = F.one()

        for row_index, pivot_col in enumerate(pivots):
            x[pivot_col] = F.neg(R[row_index][free])

        cols.append(x)

    return transpose(cols)


def load_instance(path: Path) -> tuple[Field, Matrix, Matrix]:
    data = json.loads(path.read_text(encoding="utf-8"))
    F = Field.parse(data["field"])

    if "test_matrix_basis_by_test" in data:
        shell_M = normalize_matrix(data["test_matrix_basis_by_test"], F)
        validate_rectangular(shell_M, "test_matrix_basis_by_test")
        T = transpose(shell_M)
    elif "test_matrix_test_by_basis" in data:
        T = normalize_matrix(data["test_matrix_test_by_basis"], F)
        validate_rectangular(T, "test_matrix_test_by_basis")
    else:
        raise ValueError("missing test_matrix_basis_by_test or test_matrix_test_by_basis")

    if not T:
        raise ValueError("test matrix must have at least one row")

    basis_size = len(T[0])
    N = normalize_matrix(data.get("witness_matrix", []), F)

    if not N:
        N = zero_col_matrix(basis_size)
    else:
        validate_rectangular(N, "witness_matrix")
        if len(N) != basis_size:
            raise ValueError(f"witness_matrix must have {basis_size} rows, got {len(N)}")

    return F, T, N


def certify(T: Matrix, N: Matrix, F: Field) -> FGLCertificate:
    basis_size = len(T[0])
    test_count = len(T)
    witness_count = len(N[0]) if N and N[0] else 0

    K = nullspace_basis_columns(T, F)

    rank_T = rank(T, F)
    rank_N = rank(N, F)
    rank_NK = rank(hcat(N, K), F)

    TN = matmul(T, N, F)
    annihilates_witness = is_zero_matrix(TN, F)

    kernel_dim_T = basis_size - rank_T
    kernel_contained = rank_NK == rank_N
    quotient_rank_valid = annihilates_witness and rank_T == basis_size - rank_N

    status = "Proved" if kernel_contained else "Conditional"

    return FGLCertificate(
        field=F.name,
        basis_size=basis_size,
        test_count=test_count,
        witness_count=witness_count,
        rank_T=rank_T,
        rank_N=rank_N,
        rank_NK=rank_NK,
        kernel_dim_T=kernel_dim_T,
        kernel_contained_in_witness=kernel_contained,
        annihilates_witness=annihilates_witness,
        quotient_rank_valid=quotient_rank_valid,
        status=status,
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: tools/certify_fgl.py artifacts/fgl/finite_patch_matrices.json [output.json]", file=sys.stderr)
        return 2

    src = Path(sys.argv[1])
    if not src.exists():
        print(f"MISSING: {src}", file=sys.stderr)
        return 2

    dst = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path("artifacts/fgl/fgl_certificate.json")

    F, T, N = load_instance(src)
    cert = certify(T, N, F)

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(asdict(cert), indent=2) + "\n", encoding="utf-8")

    print(json.dumps(asdict(cert), indent=2))

    return 0 if cert.kernel_contained_in_witness else 10


if __name__ == "__main__":
    raise SystemExit(main())
