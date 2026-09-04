#!/usr/bin/env python3
"""Run the accumulation Newton audit with collinear hull vertices merged."""
from __future__ import annotations

import verify_gfe_corrected_finite_beta_horizon_exceptional_accumulation_growth as audit


def merged_upper_hull(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    hull: list[tuple[int, int]] = []
    for point in points:
        while len(hull) >= 2:
            x0, y0 = hull[-2]
            x1, y1 = hull[-1]
            x2, y2 = point
            lhs = (y1 - y0) * (x2 - x1)
            rhs = (y2 - y1) * (x1 - x0)
            if lhs <= rhs:
                hull.pop()
            else:
                break
        hull.append(point)
    return hull


audit.upper_hull = merged_upper_hull

if __name__ == "__main__":
    audit.main()
