#!/usr/bin/env python3
"""Certify that the flagship-sector growing connection coefficient is finite.

Sector: M=1, beta=5/2, omega=i/4, ell=2, lambda=6.

This gate deliberately proves only well-defined finiteness of C_grow, not its
value or nonvanishing.  It composes two already-certified facts:

* the Borel-Laplace physical horizon branch continues uniquely to every finite
  real r>2; and
* on the quantitative infinity tail r>=4096 there is an actual invertible
  six-channel fundamental matrix Phi_inf and a connection vector

      C_phys = Phi_inf(r)^(-1) Y_phys(r)

  independent of r on the common exterior domain.

At the finite reference radius r=4096, Y_phys(4096) is therefore a finite
six-vector and Phi_inf(4096) is an invertible finite 6x6 matrix.  Hence
C_phys is an element of C^6 and its first component C_grow is a finite complex
scalar.  No numerical enclosure or nonzero conclusion is asserted here.
"""
from __future__ import annotations

import ast
import contextlib
import io

import verify_gfe_corrected_exceptional_accumulation_exterior_continuation as exterior
import verify_gfe_corrected_exceptional_accumulation_exterior_infinity_projection_interface as projection


def run_gate(module) -> str:
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        module.main()
    output = buffer.getvalue()
    print(output, end="")
    return output


def certified_line(output: str, prefix: str) -> str:
    marker = prefix + " := "
    for line in output.splitlines():
        if line.startswith(marker):
            return line[len(marker):]
    raise AssertionError(f"missing certified output line: {prefix}")


def main() -> None:
    exterior_output = run_gate(exterior)
    if "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_CONTINUATION_CERTIFIED" not in exterior_output:
        raise AssertionError("finite-radius physical continuation dependency did not certify")
    if certified_line(exterior_output, "PHYSICAL_EXTERIOR_CONTINUATION") != (
        "unique to every finite r>2"
    ):
        raise AssertionError("physical finite-radius continuation statement changed")

    projection_output = run_gate(projection)
    if "GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_EXTERIOR_INFINITY_PROJECTION_INTERFACE_CERTIFIED" not in projection_output:
        raise AssertionError("infinity projection dependency did not certify")
    if certified_line(projection_output, "PHYSICAL_EXTERIOR_BRANCH") != (
        "unique reconstructed horizon solution continued to every finite r>2"
    ):
        raise AssertionError("projection gate detached from the physical exterior branch")
    if certified_line(projection_output, "ACTUAL_INFINITY_BASIS") != (
        "six-channel fundamental matrix from the certified asymptotic-integration gate"
    ):
        raise AssertionError("actual infinity fundamental basis statement changed")
    if certified_line(projection_output, "CONNECTION_DEFINITION") != (
        "C_phys=Phi_inf(r)^(-1)Y_phys(r); independent of r on the common exterior domain"
    ):
        raise AssertionError("connection-vector definition changed")
    if certified_line(projection_output, "QUANTITATIVE_NORMAL_FORM_TAIL_START") != "r >= 4096":
        raise AssertionError("quantitative common-tail reference radius changed")

    names = ast.literal_eval(certified_line(projection_output, "CONNECTION_COEFFICIENT_VECTOR"))
    expected_names = [
        "C_grow",
        "C_decay",
        "C_plus_low",
        "C_plus_high",
        "C_minus_low",
        "C_minus_high",
    ]
    if names != expected_names:
        raise AssertionError(f"connection coefficient ordering changed: {names}")

    reference_radius = 4096
    if not reference_radius > 2:
        raise AssertionError("reference radius left the physical exterior")

    print("GFE_CORRECTED_EXCEPTIONAL_ACCUMULATION_CGROW_FINITENESS_CERTIFIED")
    print("SECTOR := M=1; beta=5/2; omega=I/4; ell=2; lambda=6")
    print(f"REFERENCE_RADIUS := {reference_radius}")
    print("PHYSICAL_STATE_AT_REFERENCE := Y_phys(4096) is a well-defined finite six-vector by unique finite-radius continuation")
    print("INFINITY_BASIS_AT_REFERENCE := Phi_inf(4096) is an invertible finite 6x6 fundamental matrix on the certified common tail")
    print("CONNECTION_VECTOR_AT_REFERENCE := C_phys=Phi_inf(4096)^(-1)Y_phys(4096) is an element of C^6")
    print("CGROW_FINITENESS := C_grow is the first component of C_phys and is a finite complex scalar")
    print("CGROW_LIMIT_INTERPRETATION := the normalized growing-channel coefficient is well-defined through the certified infinity basis")
    print("BOUNDARY := no numerical value, sign, nonvanishing, bounded physical solution, or global exceptional-mode conclusion is claimed")


if __name__ == "__main__":
    main()
