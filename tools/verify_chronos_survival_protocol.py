from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/status/CHRONOS_SURVIVAL_PROTOCOL.md"

REQUIRED = [
    "Status: Repository-governance protocol",
    "executable artifact for local-computation, refinement-depth, and status-normalized rigidity claims",
    "solved theorem",
    "closed executable surface",
    "certified frontier",
    "conditional result",
    "open obstruction",
    "`chronos-urf-rr` must not imply that an open theorem is solved",
    "The durable contribution of `chronos-urf-rr` is the conversion of refinement-depth and local-computation claims into auditable, executable, status-normalized artifacts.",
    "Do not expand Chronos merely by adding new terminology.",
]

def main() -> None:
    if not DOC.exists():
        raise SystemExit("missing docs/status/CHRONOS_SURVIVAL_PROTOCOL.md")
    text = DOC.read_text()
    for needle in REQUIRED:
        if needle not in text:
            raise SystemExit(f"missing required text: {needle}")
    print("chronos survival protocol verified")

if __name__ == "__main__":
    main()
