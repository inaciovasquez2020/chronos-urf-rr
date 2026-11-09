"""Bounded adversarial SAT-query fixtures for the Universality Bridge audit.

This is an exact *restricted-family* deterministic query model, not a proof of
unrestricted SAT time hardness, a neural model, or a Lean proof.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import log2


def valid_signs(signs: str) -> bool:
    return type(signs) is str and 1 <= len(signs) <= 12 and set(signs) <= {"0", "1"}


def cnf(signs: str) -> tuple[tuple[int, ...], ...]:
    """F_b = (z) AND each (z) if bit=0, or (not z) if bit=1.

    The only variable has index 1. Each sign is an independently variable
    bit in an otherwise fixed-width CNF representation.
    """
    if not valid_signs(signs):
        raise ValueError("signs must have 1..12 binary entries")
    return ((1,),) + tuple((1,) if s == "0" else (-1,) for s in signs)


def brute_sat(signs: str) -> bool:
    clauses = cnf(signs)
    return any(all(any(((lit > 0) == value) for lit in clause) for clause in clauses)
               for value in (False, True))


def scan_sat(signs: str) -> tuple[bool, int]:
    if not valid_signs(signs):
        raise ValueError("invalid input")
    for i, bit in enumerate(signs, start=1):
        if bit == "1":
            return False, i
    return True, len(signs)


def sat_family_receipt(m: int) -> dict:
    """Exhaustive independent CNF truth-table vs early-exit sign scanner."""
    if type(m) is not int or not 1 <= m <= 12:
        raise ValueError("finite enumeration guard: 1 <= m <= 12")
    xs = ("".join(t) for t in product("01", repeat=m))
    count = 0
    sat = 0
    query_sum = 0
    worst = 0
    for bits in xs:
        ans, qs = scan_sat(bits)
        assert ans == brute_sat(bits)
        sat += int(ans)
        count += 1
        query_sum += qs
        worst = max(worst, qs)
    zero = "0" * m
    sensitivity = sum(brute_sat(zero) != brute_sat(zero[:i] + "1" + zero[i+1:])
                      for i in range(m))
    expected = Fraction(query_sum, count)
    analytic = Fraction(2 * (2**m - 1), 2**m)
    assert expected == analytic
    assert sat == 1 and sensitivity == m and worst == m
    p = 1 / count
    output_entropy_bits = -p * log2(p) - (1-p) * log2(1-p) if m >= 2 else 1.0
    return {
        "m": m,
        "encoded_instances": count,
        "sat_instances": sat,
        "unsat_instances": count - sat,
        "all_positive_is_sat": brute_sat(zero),
        "all_positive_sensitivity": sensitivity,
        "deterministic_query_lower_bound": m,
        "matching_worst_case_scan_queries": worst,
        "uniform_mean_scan_queries_numerator": expected.numerator,
        "uniform_mean_scan_queries_denominator": expected.denominator,
        "sat_output_entropy_bits_approx": output_entropy_bits,
        "bound_scope": "m_input_sign_bits_one_propositional_variable_1CNF_not_general_SAT_time",
    }


def eager_read_entropy(n: int, visited: int, extra_steps: int = 0) -> dict:
    """Uniform n-bit input; deterministic read-first abstract TM schedule.

    Initial frame Y0 observes cell 0; after n distinct observations the input is
    fully known. Additional deterministic input-independent bookkeeping steps
    do not increase H(X | observations). They can be expensive computationally.
    """
    if (type(n) is not int or type(visited) is not int or type(extra_steps) is not int
            or not 1 <= n <= 12 or not 0 <= visited <= n or not 0 <= extra_steps <= 4096):
        raise ValueError("finite/reproducibility resource guard")
    fibers: dict[str, int] = {}
    for tup in product("01", repeat=n):
        bits = "".join(tup)
        transcript = bits[:visited]
        fibers[transcript] = fibers.get(transcript, 0) + 1
    assert len(fibers) == 2**visited
    assert set(fibers.values()) == {2**(n-visited)}
    return {
        "input_bits": n,
        "distinct_input_cells_observed": visited,
        "additional_deterministic_compute_steps": extra_steps,
        "input_entropy_bits": n,
        "conditional_input_entropy_bits": n-visited,
        "input_information_acquired_bits": visited,
        "full_reconstruction_from_observations": visited == n,
        "additional_information_after_full_read_bits": 0 if visited == n else None,
        "classification": "DETERMINISTIC_QUERY_OBSERVATION_NOT_TM_RUNTIME_PROOF",
    }


def evaluate_sat_query_response(response: object, case_id: str) -> dict:
    """Reject arbitrary prose, fake completions, and out-of-scope statements."""
    def fail(msg: str) -> dict:
        return {"case": case_id, "pass": False, "reason": msg}
    if type(response) is not dict or response.get("case_id") != case_id:
        return fail("invalid response identity")
    if case_id == "bridge_sat_sign_query":
        if set(response) != {"case_id", "status", "witness", "missing_obligation"}:
            return fail("closed-world schema failure")
        if (response.get("status") != "RESTRICTED_QUERY_LOWER_BOUND_ONLY"
                or response.get("missing_obligation") != "UNRESTRICTED_SAT_TIME_LOWER_BOUND"):
            return fail("unsupported status or missing boundary")
        w = response.get("witness")
        if type(w) is not dict or set(w) != {"m", "all_positive_signs"}:
            return fail("invalid witness schema")
        m = w.get("m")
        if type(m) is not int or not 2 <= m <= 12 or w.get("all_positive_signs") != "0"*m:
            return fail("witness does not bind to all-positive CNF")
        r = sat_family_receipt(m)
        return {"case": case_id, "pass": r["deterministic_query_lower_bound"] == m,
                "reason": "exact restricted-CNF sensitivity/query lower bound", "audit": r}
    if case_id == "bridge_eager_read_no_go":
        if set(response) != {"case_id", "status", "witness", "missing_obligation"}:
            return fail("closed-world schema failure")
        if (response.get("status") != "INPUT_INFORMATION_EXHAUSTED_IN_LINEAR_TIME"
                or response.get("missing_obligation") != "TASK_SPECIFIC_COMPUTATION_LOWER_BOUND_REQUIRED"):
            return fail("invalid conclusion or attempted theorem promotion")
        w = response.get("witness")
        if type(w) is not dict or set(w) != {"input_bits", "read_steps", "postprocessing_steps"}:
            return fail("invalid witness schema")
        n = w.get("input_bits")
        if type(n) is not int or w.get("read_steps") != n:
            return fail("read bound not linear/exact")
        try:
            r = eager_read_entropy(n, n, w.get("postprocessing_steps"))
        except (TypeError, ValueError):
            return fail("guard failure")
        return {"case": case_id, "pass": r["conditional_input_entropy_bits"] == 0,
                "reason": "all information exhausted during linear input scan", "audit": r}
    return fail("unknown case")


SAT_QUERY_CASES = frozenset({"bridge_sat_sign_query", "bridge_eager_read_no_go"})


def copy_machine_history(bits: str, t: int) -> tuple:
    """Actual normalized frames for a fixed deterministic two-tape copier.

    Tape 1 is read-only with end marker '_'; work tape initially all '_'.
    State qcopy reads a bit b, writes b to work tape, advances both heads;
    on the end marker it enters qhalt without moving. The displayed scanned
    work symbol is '_', because each work cell is reached for the first time.
    A normalized Y0=c0, Y_(i+1)=(c_i,c_(i+1)) is returned.
    """
    if not valid_signs(bits) or type(t) is not int or not 0 <= t <= len(bits) + 1:
        raise ValueError("invalid copier input/time")
    n = len(bits)
    configurations = []
    for i in range(n+1):
        configurations.append(("qcopy", (i, i), (bits[i] if i < n else "_", "_")))
    configurations.append(("qhalt", (n, n), ("_", "_")))
    return (configurations[0],) + tuple((configurations[i], configurations[i+1]) for i in range(t))


def copy_machine_work_at(bits: str, t: int) -> str:
    """The actual nonblank work tape after t copier transitions."""
    if not valid_signs(bits) or type(t) is not int or not 0 <= t <= len(bits)+1:
        raise ValueError("invalid copier time")
    return bits[:min(t,len(bits))]


def reconstruct_work_from_transcript(history: tuple) -> str:
    """Recover the copier's work tape from its observed transition frames."""
    if not isinstance(history, tuple) or not history:
        raise ValueError("empty or invalid history")
    reconstructed=[]
    for i, transition in enumerate(history[1:]):
        if not isinstance(transition, tuple) or len(transition)!=2:
            raise ValueError("bad transition frame")
        old,_new=transition
        if old[0] == 'qcopy' and old[2][0] in '01':
            reconstructed.append(old[2][0])
    return ''.join(reconstructed)


def copy_machine_entropy_regression(n: int) -> dict:
    """Exhaustive transcript-fiber partitions for a concrete 2-tape machine."""
    if type(n) is not int or not 1 <= n <= 10:
        raise ValueError('copy simulator guard 1..10')
    xs=(''.join(tup) for tup in product('01',repeat=n))
    # For each observation time, determine fiber sizes independent of formulas.
    groups=[{} for _ in range(n+2)]
    for x in xs:
        for t in range(n+2):
            h=copy_machine_history(x,t)
            fiber=groups[t]
            fiber[h]=fiber.get(h,0)+1
            assert reconstruct_work_from_transcript(h)==copy_machine_work_at(x,t)
    residual=[]
    for t,g in enumerate(groups):
        seen=min(n,t+1)
        assert len(g)==2**seen and set(g.values())=={2**(n-seen)}
        residual.append(n-seen)
    return {'input_bits':n,'history_times':list(range(n+2)),
            'conditional_entropy_bits':residual,
            'per_transition_information_bits':[residual[t]-residual[t+1]
                                               for t in range(n+1)],
            'full_input_recovered_by_transcript_at_time':n-1,
            'work_contents_reconstructed_from_transcript':True,
            'source_model':'deterministic_two_tape_read_only_input_work_copier'}
