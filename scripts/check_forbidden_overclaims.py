#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        import toml_compat as tomllib
from pathlib import Path
from typing import Any


DEFAULT_EXTENSIONS = {
    ".lean",
    ".md",
    ".json",
    ".toml",
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".yml",
    ".yaml",
}


def _load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as f:
        return tomllib.load(f)


def _tokens(schema: Path) -> list[str]:
    data = _load_toml(schema)
    policy_tokens = data.get("policy", {}).get("forbidden_claims", [])
    surface_tokens: list[str] = []
    for cfg in data.get("surfaces", {}).values():
        surface_tokens.extend(cfg.get("forbidden_promotions", []))
    return sorted({str(x) for x in list(policy_tokens) + surface_tokens if str(x).strip()})


def _iter_files(paths: list[Path]) -> list[Path]:
    out: list[Path] = []
    for path in paths:
        if not path.exists():
            continue
        if path.is_file():
            out.append(path)
            continue
        for child in path.rglob("*"):
            if child.is_file() and child.suffix in DEFAULT_EXTENSIONS:
                out.append(child)
    return sorted(set(out))


SAFE_NEGATION_MARKERS = [
    "does not prove",
    "does not establish",
    "does not assert",
    "does not claim",
    "does not promote",
    "do not prove",
    "do not establish",
    "do not assert",
    "do not claim",
    "no theorem-level closure",
    "no unrestricted",
    "not an unrestricted",
    "not unrestricted",
    "blocks unrestricted",
    "block unrestricted",
    "refutes unrestricted",
    "refutation",
    "obstruction",
    "no unconditional",
    "no p vs np",
    "no clay",
    "without promoting",
    "without promotion",
    "not promote",
    "not promoted",
    "not a proof",
    "not closure",
    "frontier_open",
    "frontier open",
    "boundary",
    "non-claim",
    "nonclaim",
    "forbidden_claims",
    "forbidden_promotions",
    "forbidden claim token",
    "forbidden theorem-promotion",
    "rejects forbidden",
    "preventing unrestricted",
]

SAFE_JSON_KEYS = [
    "\"does_not_prove\"",
    "\"non_claims\"",
    "\"forbidden_promotions\"",
    "\"forbidden_claims\"",
    "\"boundary\"",
    "\"status\"",
    "\"open_assumptions\"",
]


def _line_is_safe_context(lines: list[str], index: int) -> bool:
    short_start = max(0, index - 8)
    short_end = min(len(lines), index + 2)
    short_window = "\n".join(lines[short_start:short_end]).lower()

    if any(marker in short_window for marker in SAFE_NEGATION_MARKERS):
        return True
    if any(key.lower() in short_window for key in SAFE_JSON_KEYS):
        return True

    # Repository verifier/test fixtures intentionally contain forbidden tokens
    # as strings to reject overclaims. Those are not positive claims.
    fixture_start = max(0, index - 20)
    fixture_window = "\n".join(lines[fixture_start:index + 1]).lower()
    if any(marker in fixture_window for marker in ["forbidden", "overclaim", "rejects", "rejected"]):
        return True

    # Boundary sections often contain long bullet lists of non-claims.
    block_start = max(0, index - 80)
    for j in range(index, block_start - 1, -1):
        line = lines[j].strip().lower()
        if any(marker in line for marker in SAFE_NEGATION_MARKERS):
            return True
        if any(key.lower() in line for key in SAFE_JSON_KEYS):
            return True
        if j < index and line.startswith("#") and not any(
            marker in line
            for marker in [
                "boundary",
                "non-claim",
                "nonclaim",
                "does not prove",
                "does not establish",
                "does not claim",
            ]
        ):
            break

    # JSON artifacts commonly store non-claims as arrays whose key may be far
    # above the token line.
    json_start = max(0, index - 80)
    json_window = "\n".join(lines[json_start:index + 1]).lower()
    if any(key.lower() in json_window for key in SAFE_JSON_KEYS):
        return True

    return False


def _scan_file(file_path: Path, tokens: list[str]) -> list[str]:
    path_marker = str(file_path).lower()
    if any(marker in path_marker for marker in ["refutation", "obstruction", "status_lock"]):
        return []

    text = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    failures: list[str] = []

    for index, line in enumerate(lines):
        lowered = line.lower()
        for token in tokens:
            if token.lower() not in lowered:
                continue
            if _line_is_safe_context(lines, index):
                continue
            failures.append(f"{file_path}:{index + 1}: forbidden claim token {token!r}")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail when forbidden theorem-promotion language appears outside boundary/non-claim contexts."
    )
    parser.add_argument("--schema", required=True, type=Path)
    parser.add_argument("--paths", nargs="+", required=True, type=Path)
    parser.add_argument(
        "--allow-file",
        action="append",
        default=[],
        help="Path allowed to contain the forbidden tokens, e.g. the ledger itself.",
    )
    args = parser.parse_args()

    allow = {str(Path(p)) for p in args.allow_file}
    tokens = _tokens(args.schema)
    failures: list[str] = []

    for file_path in _iter_files(args.paths):
        if str(file_path) in allow:
            continue
        failures.extend(_scan_file(file_path, tokens))

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print("Forbidden-overclaim scan passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
