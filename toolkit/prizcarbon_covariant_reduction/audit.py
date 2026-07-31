"""Repository and history audit for a concrete odd-parity reduction chain."""

from __future__ import annotations

import argparse
import bisect
import collections
import datetime as dt
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Optional, Sequence


TEXT_SUFFIXES = {
    ".lean",
    ".py",
    ".md",
    ".json",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

EXCLUDED_DIRS = {
    ".git",
    ".lake",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".mypy_cache",
    ".pytest_cache",
}

SELF_PATH_PREFIXES = {
    "toolkit/prizcarbon_covariant_reduction",
    "tools/run_prizcarbon_covariant_reduction_toolkit.py",
    "tests/test_prizcarbon_covariant_reduction_toolkit.py",
}

DECLARATION_RE = re.compile(
    r"^\s*(?:theorem|lemma|def|structure|class|abbrev|inductive)\s+"
    r"([A-Za-z0-9_'.]+)"
)

IMPORT_RE = re.compile(
    r"^\s*import\s+([A-Za-z0-9_.]+)\s*$"
)

CONDITIONAL_MARKERS = (
    "proposed",
    "conditional",
    "carrier",
    "candidate",
    "target",
    "interface",
    "assumption",
    "assumed",
    "hypothesis",
    "boundary",
    "unproved",
    "not claimed",
    "does not assert",
    "does not prove",
    "placeholder",
)


@dataclass(frozen=True)
class Stage:
    key: str
    label: str
    terms: tuple[str, ...]
    required: bool = True


STAGES = (
    Stage(
        "covariant_action",
        "Covariant action and variational origin",
        (
            "covariant action",
            "action density",
            "euler lagrange",
            "first variation",
            "second variation",
            "quadratic action",
        ),
    ),
    Stage(
        "background_specialization",
        "Schwarzschild background specialization",
        (
            "schwarzschild",
            "background equation",
            "background solution",
            "static spherical background",
        ),
    ),
    Stage(
        "odd_parity_variables",
        "Odd-parity perturbation variables",
        (
            "odd parity",
            "axial perturbation",
            "regge wheeler odd parity",
        ),
    ),
    Stage(
        "gauge_invariant_master",
        "Gauge-invariant master variable",
        (
            "gauge invariant",
            "master field",
            "master variable",
            "moncrief",
            "cunningham price",
        ),
    ),
    Stage(
        "harmonic_reduction",
        "Spherical-harmonic reduction",
        (
            "spherical harmonic",
            "harmonic decomposition",
            "harmonic mode",
            "multipole",
            "ell two",
        ),
    ),
    Stage(
        "quadratic_variation",
        "Odd-parity quadratic action",
        (
            "quadratic action",
            "second variation",
            "twice varied",
            "action hessian",
            "odd parity action",
        ),
    ),
    Stage(
        "master_equation",
        "Concrete master differential equation",
        (
            "master equation",
            "regge wheeler equation",
            "regge wheeler operator",
            "wave equation",
            "second derivative",
        ),
    ),
    Stage(
        "coordinate_bridge",
        "Areal-radius and tortoise-coordinate bridge",
        (
            "tortoise",
            "r star",
            "areal radius",
            "schwarzschild coordinate",
            "radial coordinate",
        ),
    ),
    Stage(
        "potential_identification",
        "Master-potential coefficient identification",
        (
            "regge wheeler potential",
            "potential coefficient",
            "coefficient match",
            "mass radius coefficient",
            "potential identification",
        ),
    ),
    Stage(
        "scalar_residual_bridge",
        "Bridge to proposed scalar residual",
        (
            "proposed prizcarbon scalar euler lagrange residual",
            "scalar residual",
            "scalar residual comparison",
            "coefficient mismatch",
        ),
    ),
    Stage(
        "geometric_curvature",
        "Geometric-curvature realization",
        (
            "geometric curvature",
            "curvature realization",
            "weyl tensor",
            "weyl curvature",
            "regge wheeler tensor",
        ),
        required=False,
    ),
)

CRITICAL_GAP_ORDER = (
    "quadratic_variation",
    "master_equation",
    "coordinate_bridge",
    "potential_identification",
    "geometric_curvature",
)


def normalize_text(text: str) -> str:
    expanded = re.sub(
        r"([a-z0-9])([A-Z])",
        r"\1 \2",
        text,
    )
    expanded = re.sub(
        r"([A-Z]+)([A-Z][a-z])",
        r"\1 \2",
        expanded,
    )
    expanded = re.sub(
        r"[^A-Za-z0-9]+",
        " ",
        expanded,
    )
    return " ".join(expanded.lower().split())


def contains_conditional_marker(text: str) -> bool:
    normalized = normalize_text(text)
    return any(
        marker in normalized
        for marker in CONDITIONAL_MARKERS
    )


def match_stage(line: str, stage: Stage) -> Optional[str]:
    normalized_line = normalize_text(line)

    for term in stage.terms:
        normalized_term = normalize_text(term)

        if normalized_term in normalized_line:
            return normalized_term

    return None


def run_git(
    root: Path,
    arguments: Sequence[str],
    timeout: int = 60,
) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *arguments],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
    )

    if completed.returncode != 0:
        return ""

    return completed.stdout.strip()


def is_self_path(relative: str) -> bool:
    return any(
        relative == prefix
        or relative.startswith(prefix + "/")
        for prefix in SELF_PATH_PREFIXES
    )


def iter_text_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        relative_path = path.relative_to(root)
        relative = str(relative_path)

        if is_self_path(relative):
            continue

        if any(
            part in EXCLUDED_DIRS
            for part in relative_path.parts
        ):
            continue

        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        try:
            if path.stat().st_size > 2_000_000:
                continue
        except OSError:
            continue

        yield path


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines()
    except OSError:
        return []


def declaration_positions(
    lines: Sequence[str],
) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []

    for index, line in enumerate(lines):
        match = DECLARATION_RE.match(line)

        if match:
            result.append((index, match.group(1)))

    return result


def declaration_scope(
    lines: Sequence[str],
    positions: Sequence[tuple[int, str]],
    line_index: int,
) -> tuple[Optional[str], str]:
    if not positions:
        start = max(0, line_index - 4)
        end = min(len(lines), line_index + 5)
        return None, "\n".join(lines[start:end])

    indexes = [entry[0] for entry in positions]
    position = bisect.bisect_right(
        indexes,
        line_index,
    ) - 1

    if position < 0:
        start = max(0, line_index - 4)
        end = min(len(lines), line_index + 5)
        return None, "\n".join(lines[start:end])

    start, declaration = positions[position]
    end = (
        positions[position + 1][0]
        if position + 1 < len(positions)
        else len(lines)
    )

    return declaration, "\n".join(lines[start:end])


def module_from_path(
    root: Path,
    path: Path,
) -> Optional[str]:
    if path.suffix != ".lean":
        return None

    parts = list(
        path.relative_to(root).with_suffix("").parts
    )

    if parts and parts[0] == "lean":
        parts = parts[1:]

    return ".".join(parts)


def collect_import_graph(
    root: Path,
    files: Sequence[Path],
) -> tuple[dict[str, set[str]], dict[str, str]]:
    graph: dict[str, set[str]] = collections.defaultdict(set)
    module_paths: dict[str, str] = {}

    for path in files:
        module = module_from_path(root, path)

        if module is None:
            continue

        module_paths[module] = str(path.relative_to(root))
        graph.setdefault(module, set())

        for line in read_lines(path):
            match = IMPORT_RE.match(line)

            if match:
                graph[module].add(match.group(1))

    return dict(graph), module_paths


def undirected_graph(
    graph: Mapping[str, set[str]],
) -> dict[str, set[str]]:
    result: dict[str, set[str]] = collections.defaultdict(set)

    for source, targets in graph.items():
        result.setdefault(source, set())

        for target in targets:
            result[source].add(target)
            result[target].add(source)

    return dict(result)


def shortest_connection(
    graph: Mapping[str, set[str]],
    starts: set[str],
    targets: set[str],
) -> list[str]:
    if not starts or not targets:
        return []

    queue = collections.deque(sorted(starts))
    previous: dict[str, Optional[str]] = {
        start: None
        for start in starts
    }

    found: Optional[str] = None

    while queue:
        current = queue.popleft()

        if current in targets:
            found = current
            break

        for neighbor in sorted(graph.get(current, set())):
            if neighbor in previous:
                continue

            previous[neighbor] = current
            queue.append(neighbor)

    if found is None:
        return []

    path: list[str] = []
    cursor: Optional[str] = found

    while cursor is not None:
        path.append(cursor)
        cursor = previous[cursor]

    path.reverse()
    return path


def history_subject_hits(
    root: Path,
    stage: Stage,
    history_lines: Sequence[str],
    limit: int,
) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []

    for line in history_lines:
        if "\t" not in line:
            continue

        commit, subject = line.split("\t", 1)
        normalized_subject = normalize_text(subject)

        if not any(
            normalize_text(term) in normalized_subject
            for term in stage.terms
        ):
            continue

        results.append(
            {
                "commit": commit,
                "subject": subject,
            }
        )

        if len(results) >= limit:
            break

    return results


def audit_repository(
    root: Path,
    *,
    include_history: bool = False,
    history_limit: int = 10,
    max_matches_per_stage: int = 120,
) -> dict[str, object]:
    root = root.resolve()
    files = list(iter_text_files(root))

    raw_matches: dict[str, list[dict[str, object]]] = {
        stage.key: []
        for stage in STAGES
    }

    stage_modules: dict[str, set[str]] = {
        stage.key: set()
        for stage in STAGES
    }

    for path in files:
        relative = str(path.relative_to(root))
        lines = read_lines(path)
        positions = declaration_positions(lines)
        module = module_from_path(root, path)

        for line_index, line in enumerate(lines):
            for stage in STAGES:
                matched_term = match_stage(line, stage)

                if matched_term is None:
                    continue

                declaration, scope = declaration_scope(
                    lines,
                    positions,
                    line_index,
                )

                classification_text = "\n".join(
                    (
                        relative,
                        declaration or "",
                        scope,
                    )
                )

                tier = (
                    "conditional"
                    if contains_conditional_marker(
                        classification_text
                    )
                    else "unqualified"
                )

                raw_matches[stage.key].append(
                    {
                        "path": relative,
                        "line": line_index + 1,
                        "declaration": declaration,
                        "snippet": line.strip()[:300],
                        "matched_term": matched_term,
                        "tier": tier,
                    }
                )

                if module:
                    stage_modules[stage.key].add(module)

    history_lines: list[str] = []

    if include_history:
        history_lines = run_git(
            root,
            [
                "log",
                "--all",
                "-n",
                "2500",
                "--format=%H%x09%s",
            ],
        ).splitlines()

    stage_reports: dict[str, dict[str, object]] = {}

    for stage in STAGES:
        matches = raw_matches[stage.key]

        conditional_count = sum(
            1
            for match in matches
            if match["tier"] == "conditional"
        )

        unqualified_count = (
            len(matches) - conditional_count
        )

        if not matches:
            status = "absent"
        elif unqualified_count == 0:
            status = "conditional_only"
        else:
            status = "unqualified_evidence"

        stage_files = sorted(
            {
                str(match["path"])
                for match in matches
            }
        )

        stage_reports[stage.key] = {
            "label": stage.label,
            "required": stage.required,
            "status": status,
            "total_match_count": len(matches),
            "conditional_match_count": conditional_count,
            "unqualified_match_count": unqualified_count,
            "file_count": len(stage_files),
            "files": stage_files,
            "matches": matches[:max_matches_per_stage],
            "history_hits": (
                history_subject_hits(
                    root,
                    stage,
                    history_lines,
                    history_limit,
                )
                if include_history
                else []
            ),
        }

    import_graph, module_paths = collect_import_graph(
        root,
        files,
    )

    connected_graph = undirected_graph(import_graph)

    action_to_master = shortest_connection(
        connected_graph,
        stage_modules["covariant_action"],
        stage_modules["master_equation"],
    )

    master_to_scalar = shortest_connection(
        connected_graph,
        stage_modules["master_equation"],
        stage_modules["scalar_residual_bridge"],
    )

    strongest_gap = next(
        (
            key
            for key in CRITICAL_GAP_ORDER
            if stage_reports[key]["status"]
            != "unqualified_evidence"
        ),
        "NONE_DETECTED_BY_HEURISTIC",
    )

    required_keys = [
        stage.key
        for stage in STAGES
        if stage.required
    ]

    concrete_chain_ready = all(
        stage_reports[key]["status"]
        == "unqualified_evidence"
        for key in required_keys
    )

    scores: dict[str, int] = collections.Counter()

    for stage in STAGES:
        stage_weight = (
            5
            if stage.key in CRITICAL_GAP_ORDER
            else 1
        )

        for match in raw_matches[stage.key]:
            tier_weight = (
                2
                if match["tier"] == "unqualified"
                else 1
            )

            scores[str(match["path"])] += (
                stage_weight * tier_weight
            )

    top_candidate_files = [
        {
            "path": path,
            "score": score,
        }
        for path, score in sorted(
            scores.items(),
            key=lambda item: (-item[1], item[0]),
        )[:30]
    ]

    strongest_gap_evidence = (
        stage_reports[strongest_gap]["matches"][:20]
        if strongest_gap in stage_reports
        else []
    )

    return {
        "schema_version": 4,
        "generated_utc": (
            dt.datetime.now(dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat()
        ),
        "repository_root": str(root),
        "repository_head": (
            run_git(root, ["rev-parse", "HEAD"])
            or "UNKNOWN"
        ),
        "scanned_file_count": len(files),
        "stages": stage_reports,
        "critical_gap_order": list(CRITICAL_GAP_ORDER),
        "strongest_gap": strongest_gap,
        "strongest_gap_evidence": strongest_gap_evidence,
        "concrete_chain_ready": concrete_chain_ready,
        "import_connectivity": {
            "action_to_master_modules": action_to_master,
            "action_to_master_paths": [
                module_paths.get(module, module)
                for module in action_to_master
            ],
            "master_to_scalar_modules": master_to_scalar,
            "master_to_scalar_paths": [
                module_paths.get(module, module)
                for module in master_to_scalar
            ],
        },
        "top_candidate_files": top_candidate_files,
        "claim_boundary": (
            "Keyword evidence, declaration classification, Git history, "
            "import connectivity, compilation, and CI do not establish "
            "a covariant odd-parity reduction or physical theorem."
        ),
        "required_next_object": (
            "An explicit theorem derived from the encoded covariant action "
            "whose Schwarzschild odd-parity quadratic variation yields the "
            "gauge-invariant master differential equation and identifies "
            "its potential coefficient with the scalar residual."
        ),
    }


def render_markdown(report: Mapping[str, object]) -> str:
    lines = [
        "# Prizcarbon Covariant Odd-Parity Reduction Audit",
        "",
        f"- Repository head: `{report['repository_head']}`",
        f"- Scanned files: `{report['scanned_file_count']}`",
        f"- Concrete chain ready: `{report['concrete_chain_ready']}`",
        f"- Strongest gap: `{report['strongest_gap']}`",
        "",
        "## Stage inventory",
        "",
        "| Stage | Status | Files | Matches |",
        "|---|---:|---:|---:|",
    ]

    stages = report["stages"]
    assert isinstance(stages, Mapping)

    for stage in STAGES:
        entry = stages[stage.key]
        assert isinstance(entry, Mapping)

        lines.append(
            "| "
            f"{stage.label} | "
            f"`{entry['status']}` | "
            f"{entry['file_count']} | "
            f"{entry['total_match_count']} |"
        )

    lines.extend(
        [
            "",
            "## Strongest-gap evidence",
            "",
        ]
    )

    evidence = report["strongest_gap_evidence"]
    assert isinstance(evidence, list)

    if not evidence:
        lines.append("- No current-tree evidence found.")
    else:
        for match in evidence:
            declaration = (
                f" `{match['declaration']}`"
                if match.get("declaration")
                else ""
            )

            lines.append(
                "- "
                f"`{match['path']}:{match['line']}` "
                f"[{match['tier']}]"
                f"{declaration} — "
                f"{match['snippet']}"
            )

    lines.extend(
        [
            "",
            "## Import connectivity",
            "",
        ]
    )

    connectivity = report["import_connectivity"]
    assert isinstance(connectivity, Mapping)

    for title, key in (
        (
            "Action evidence to master-equation evidence",
            "action_to_master_paths",
        ),
        (
            "Master-equation evidence to scalar bridge",
            "master_to_scalar_paths",
        ),
    ):
        path = connectivity[key]
        assert isinstance(path, list)

        if path:
            lines.append(
                f"- {title}: "
                + " → ".join(
                    f"`{item}`"
                    for item in path
                )
            )
        else:
            lines.append(f"- {title}: no import path found")

    lines.extend(
        [
            "",
            "## Top candidate files",
            "",
        ]
    )

    candidates = report["top_candidate_files"]
    assert isinstance(candidates, list)

    for candidate in candidates[:20]:
        lines.append(
            f"- `{candidate['score']}` — "
            f"`{candidate['path']}`"
        )

    lines.extend(
        [
            "",
            "## Required next theorem object",
            "",
            str(report["required_next_object"]),
            "",
            "## Claim boundary",
            "",
            str(report["claim_boundary"]),
            "",
        ]
    )

    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--markdown-out", type=Path)
    parser.add_argument("--history", action="store_true")
    parser.add_argument(
        "--history-limit",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--max-matches-per-stage",
        type=int,
        default=120,
    )

    args = parser.parse_args(argv)

    report = audit_repository(
        args.repo,
        include_history=args.history,
        history_limit=args.history_limit,
        max_matches_per_stage=args.max_matches_per_stage,
    )

    if args.json_out:
        args.json_out.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        args.json_out.write_text(
            json.dumps(
                report,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    if args.markdown_out:
        args.markdown_out.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        args.markdown_out.write_text(
            render_markdown(report),
            encoding="utf-8",
        )

    print(
        "RESULT := covariant odd-parity deep audit completed"
    )
    print(
        f"REPOSITORY_HEAD := {report['repository_head']}"
    )
    print(
        f"SCANNED_FILES := {report['scanned_file_count']}"
    )
    print(
        "CONCRETE_CHAIN_READY := "
        f"{str(report['concrete_chain_ready']).upper()}"
    )
    print(
        f"STRONGEST_GAP := {report['strongest_gap']}"
    )

    stages = report["stages"]
    assert isinstance(stages, Mapping)

    for stage in STAGES:
        entry = stages[stage.key]
        assert isinstance(entry, Mapping)

        print(
            "STAGE := "
            f"{stage.key} | "
            f"{entry['status']} | "
            f"files={entry['file_count']} | "
            f"matches={entry['total_match_count']}"
        )

    print(f"BOUNDARY := {report['claim_boundary']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
