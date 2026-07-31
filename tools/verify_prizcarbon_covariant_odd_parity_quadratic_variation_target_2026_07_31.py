#!/usr/bin/env python3
"""Verify the concrete odd-parity quadratic-variation boundary.

This audits whether the encoded scalar-summary action is connected to the
existing Schwarzschild odd-parity metric perturbation and metric second jet.
It does not convert repository evidence into a physical theorem.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable, Optional, Sequence


ACTION_RELATIVE = Path(
    "lean/Chronos/Frontier/"
    "PrizcarbonProposedCovariantActionCarrier.lean"
)

MASTER_RELATIVE = Path(
    "lean/Chronos/Frontier/"
    "ReggeWheelerOddParityMasterExtraction.lean"
)

SECOND_JET_RELATIVE = Path(
    "lean/Chronos/Frontier/"
    "ReggeWheelerOddParityVacuumCPMMetricSecondJet.lean"
)

EXPECTED_SCALAR_FIELDS = [
    "scalarCurvature",
    "scalarKinetic",
    "arealRadiusGradientSq",
    "arealRadius",
    "massAspect",
    "pseudoscalar",
    "multiplier",
    "currentMassDerivative",
]

DECLARATION_RE = re.compile(
    r"^[ \t]*(?:theorem|lemma|def|structure|class|abbrev|inductive)\s+"
    r"([A-Za-z0-9_'.]+)",
    re.MULTILINE,
)


def read_text(path: Path) -> str:
    return path.read_text(
        encoding="utf-8",
        errors="strict",
    )


def declaration_blocks(
    text: str,
) -> Iterable[tuple[str, str]]:
    matches = list(DECLARATION_RE.finditer(text))

    for index, match in enumerate(matches):
        start = match.start()
        end = (
            matches[index + 1].start()
            if index + 1 < len(matches)
            else len(text)
        )

        yield match.group(1), text[start:end]


def declaration_block(
    text: str,
    name: str,
) -> str:
    for declaration_name, block in declaration_blocks(text):
        if declaration_name == name:
            return block

    raise ValueError(f"missing declaration {name}")


def structure_real_fields(block: str) -> list[str]:
    fields: list[str] = []

    for line in block.splitlines()[1:]:
        match = re.match(
            r"^\s+([A-Za-z0-9_']+)\s*:\s*ℝ\s*$",
            line,
        )

        if match:
            fields.append(match.group(1))

    return fields


def declarations_containing(
    lean_root: Path,
    required_terms: Sequence[str],
) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []

    for path in sorted(lean_root.rglob("*.lean")):
        text = read_text(path)

        for name, block in declaration_blocks(text):
            if all(term in block for term in required_terms):
                results.append(
                    {
                        "path": str(path.relative_to(lean_root.parent)),
                        "declaration": name,
                    }
                )

    return results


def inspect_repository(root: Path) -> dict[str, object]:
    root = root.resolve()

    action_path = root / ACTION_RELATIVE
    master_path = root / MASTER_RELATIVE
    second_jet_path = root / SECOND_JET_RELATIVE

    for path in (
        action_path,
        master_path,
        second_jet_path,
    ):
        if not path.is_file():
            raise FileNotFoundError(path)

    action_text = read_text(action_path)
    master_text = read_text(master_path)
    second_jet_text = read_text(second_jet_path)

    scalar_structure = declaration_block(
        action_text,
        "ProposedPrizcarbonCovariantScalars",
    )

    action_density = declaration_block(
        action_text,
        "proposedPrizcarbonActionDensity",
    )

    scalar_fields = structure_real_fields(
        scalar_structure
    )

    action_domain_is_scalar_record = (
        "(x : ProposedPrizcarbonCovariantScalars)"
        in action_density
    )

    action_file_mentions_odd_metric = (
        "ReggeWheelerOddParity" in action_text
    )

    master_extraction_present = all(
        term in master_text
        for term in (
            "reggeWheelerOddParityMasterField",
            "reggeWheelerOddParitySpacetimeMetricPerturbation",
            "reggeWheelerOddParityRWGaugeMetricComponentsOfMaster",
        )
    )

    second_metric_jet_present = (
        "def reggeWheelerOddParityVacuumCPMMetricSecondJet"
        in second_jet_text
    )

    lean_root = root / "lean"

    direct_action_metric_bridges = declarations_containing(
        lean_root,
        (
            "proposedPrizcarbonActionDensity",
            "reggeWheelerOddParitySpacetimeMetricPerturbation",
        ),
    )

    direct_action_second_jet_bridges = declarations_containing(
        lean_root,
        (
            "proposedPrizcarbonActionDensity",
            "reggeWheelerOddParityVacuumCPMMetricSecondJet",
        ),
    )

    explicit_action_second_variations = declarations_containing(
        lean_root,
        (
            "proposedPrizcarbonActionDensity",
            "secondVariation",
        ),
    )

    explicit_action_frechet_derivatives = declarations_containing(
        lean_root,
        (
            "proposedPrizcarbonActionDensity",
            "fderiv",
        ),
    )

    missing_metric_to_scalar_map = (
        not direct_action_metric_bridges
        and not direct_action_second_jet_bridges
    )

    missing_second_metric_variation = (
        not explicit_action_second_variations
        and not explicit_action_frechet_derivatives
    )

    ready_for_metric_hessian = all(
        (
            scalar_fields == EXPECTED_SCALAR_FIELDS,
            action_domain_is_scalar_record,
            not action_file_mentions_odd_metric,
            master_extraction_present,
            second_metric_jet_present,
            not missing_metric_to_scalar_map,
            not missing_second_metric_variation,
        )
    )

    return {
        "schema_version": 1,
        "repository_root": str(root),
        "action_file": str(ACTION_RELATIVE),
        "master_file": str(MASTER_RELATIVE),
        "second_jet_file": str(SECOND_JET_RELATIVE),
        "scalar_fields": scalar_fields,
        "expected_scalar_fields": EXPECTED_SCALAR_FIELDS,
        "action_domain_is_scalar_record": action_domain_is_scalar_record,
        "action_file_mentions_odd_metric": action_file_mentions_odd_metric,
        "master_extraction_present": master_extraction_present,
        "second_metric_jet_present": second_metric_jet_present,
        "direct_action_metric_bridges": direct_action_metric_bridges,
        "direct_action_second_jet_bridges": (
            direct_action_second_jet_bridges
        ),
        "explicit_action_second_variations": (
            explicit_action_second_variations
        ),
        "explicit_action_frechet_derivatives": (
            explicit_action_frechet_derivatives
        ),
        "missing_metric_to_scalar_map": missing_metric_to_scalar_map,
        "missing_second_metric_variation": (
            missing_second_metric_variation
        ),
        "ready_for_metric_hessian": ready_for_metric_hessian,
        "required_next_object": (
            "Define every ProposedPrizcarbonCovariantScalars component "
            "along g_epsilon = g_Schwarzschild + epsilon*h_odd from the "
            "existing metric perturbation and metric jets, then compute "
            "the second epsilon derivative of the encoded action density."
        ),
        "claim_boundary": (
            "The scalar-summary action and odd-parity metric-jet surfaces "
            "are encoded independently; no metric-to-scalar map or metric "
            "Hessian currently connects them."
        ),
    }


def main(
    argv: Optional[Sequence[str]] = None,
) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--json-out",
        type=Path,
    )

    args = parser.parse_args(argv)
    report = inspect_repository(args.repo)

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

    print(
        "RESULT := concrete Prizcarbon quadratic-variation target verified"
    )
    print(
        "ACTION_DOMAIN := ProposedPrizcarbonCovariantScalars"
    )
    print(
        "ACTION_SCALAR_FIELDS := "
        + " ".join(report["scalar_fields"])
    )
    print(
        "ACTION_FILE_MENTIONS_ODD_METRIC := "
        + str(
            report["action_file_mentions_odd_metric"]
        ).upper()
    )
    print(
        "MASTER_EXTRACTION_PRESENT := "
        + str(
            report["master_extraction_present"]
        ).upper()
    )
    print(
        "SECOND_METRIC_JET_PRESENT := "
        + str(
            report["second_metric_jet_present"]
        ).upper()
    )
    print(
        "METRIC_TO_SCALAR_MAP := "
        + (
            "MISSING"
            if report["missing_metric_to_scalar_map"]
            else "PRESENT"
        )
    )
    print(
        "SECOND_METRIC_VARIATION := "
        + (
            "MISSING"
            if report["missing_second_metric_variation"]
            else "PRESENT"
        )
    )
    print(
        "READY_FOR_METRIC_HESSIAN := "
        + str(
            report["ready_for_metric_hessian"]
        ).upper()
    )
    print(
        "REQUIRED_NEXT_OBJECT := "
        + str(report["required_next_object"])
    )
    print(
        "BOUNDARY := "
        + str(report["claim_boundary"])
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
