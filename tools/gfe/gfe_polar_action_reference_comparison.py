from __future__ import annotations

"""Exact comparison of an integrated in-memory action against the 81-slot report."""
import hashlib
import re
from pathlib import Path
import sympy as sp
from sympy.core.function import AppliedUndef


def compare_integrated_action_to_report(action, coordinates, report_path):
    t, r, theta, phi = coordinates
    if action.has(theta, phi):
        raise ValueError("integrated action still depends on angular coordinates")
    M_atoms = [z for z in action.free_symbols if z.name == "M"]
    r_atoms = [z for z in action.free_symbols if z.name == "r"]
    if len(M_atoms) != 1 or len(r_atoms) != 1:
        raise ValueError("could not uniquely identify M and r in integrated expression")
    M, r_symbol = M_atoms[0], r_atoms[0]

    jet_symbols = {}
    replacements = {}
    for derivative in sorted(action.atoms(sp.Derivative), key=lambda z: len(z.variables), reverse=True):
        base = derivative.expr
        if not isinstance(base, AppliedUndef):
            continue
        name = base.func.__name__
        counts = dict(derivative.variable_count)
        suffix = []
        for variable, label in ((t, "t"), (r, "r")):
            suffix.extend([label] * counts.pop(variable, 0))
        if counts:
            raise ValueError(f"unsupported derivative variables in jet {derivative}: {counts}")
        jet_name = name + ("_" + "_".join(suffix) if suffix else "")
        jet_symbols.setdefault(jet_name, sp.Symbol(jet_name))
        replacements[derivative] = jet_symbols[jet_name]
    for function in action.atoms(AppliedUndef):
        name = function.func.__name__
        jet_symbols.setdefault(name, sp.Symbol(name))
        replacements[function] = jet_symbols[name]
    canonical_action = sp.expand(action.xreplace(replacements))

    report = Path(report_path).read_text(encoding="utf-8")
    section = report.index("## Exact angularly integrated coefficient")
    start = report.index("```text\n", section) + len("```text\n")
    end = report.index("\n```", start)
    lines = report[start:end].splitlines()
    if len(lines) != 81:
        raise ValueError(f"reference table has {len(lines)} slots, expected 81")

    reference_terms = []
    for number, line in enumerate(lines, 1):
        match = re.match(r"^\((.*)\)\*\((.*)\)(?: \+)?$", line)
        if not match:
            raise ValueError(f"could not parse reference slot {number}")
        coefficient_text, monomial_text = match.groups()
        coefficient = sp.sympify(coefficient_text, locals={"M": M, "r": r_symbol})
        monomial = sp.Integer(1)
        factors = re.findall(r"([A-Za-z][A-Za-z0-9_]*)(?:\*\*(\d+))?", monomial_text)
        for name, power in factors:
            jet_symbols.setdefault(name, sp.Symbol(name))
            monomial *= jet_symbols[name] ** (int(power) if power else 1)
        reference_terms.append(coefficient * monomial)
    reference_action = sp.expand(sum(reference_terms))

    variables = sorted(jet_symbols.values(), key=lambda z: z.name)
    residual = sp.Poly(sp.expand(canonical_action - reference_action), *variables, domain="EX")
    nonzero = []
    for powers, coefficient in residual.terms():
        reduced = sp.factor(sp.cancel(sp.together(coefficient)))
        if reduced != 0:
            monomial = "*".join(
                f"{variable}^{power}" for variable, power in zip(variables, powers) if power
            ) or "1"
            nonzero.append({"monomial": monomial, "residual": str(reduced)})
    integrated_srepr = sp.srepr(action)
    report_bytes = report.encode("utf-8")
    return {
        "passed": not nonzero,
        "reference_slot_count": len(lines),
        "nonzero_residual_count": len(nonzero),
        "nonzero_residuals": nonzero,
        "integrated_sha256_srepr": hashlib.sha256(integrated_srepr.encode("utf-8")).hexdigest(),
        "reference_sha256": hashlib.sha256(report_bytes).hexdigest(),
    }
