"""Fail-closed routing and standalone ECPM certificate verification."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

FILES = {"AnchorInversion.lean", "LEAN.log", "README.md", "SHA256SUMS",
         "VERIFICATION.json", "lake-manifest.json", "lean-toolchain"}
PREFIX = re.compile(r"research/certificates/ecpm_[a-z0-9_]+_[0-9]{8}/")

def classify(entries):
    groups = {}
    if not entries or len(entries) % 2:
        return []
    for status, path in zip(entries[::2], entries[1::2]):
        m = PREFIX.match(path)
        if status != "A" or not m:
            return []
        directory = m.group(0)
        name = path[len(directory):]
        if name not in FILES:
            return []
        groups.setdefault(directory, set()).add(name)
    return sorted(groups) if all(v == FILES for v in groups.values()) else []

def selftest():
    d = "research/certificates/ecpm_anchor_inversion_20261127/"
    entries = [x for f in sorted(FILES) for x in ("A", d + f)]
    assert classify(entries) == [d]
    for bad in ([], entries[:-2], entries + ["M", "lean/Chronos.lean"],
                entries + ["A", "lake-manifest.json"],
                ["M", entries[1]] + entries[2:],
                entries + ["A", d + "extra.py"],
                entries + ["D", "README.md"]):
        assert classify(bad) == []
    print("ROUTER_SELFTEST := PASS")

def route():
    selftest()
    dirs = []
    if os.environ.get("GITHUB_EVENT_NAME") == "pull_request":
        base = os.environ.get("BASE_SHA", "")
        if re.fullmatch(r"[0-9a-f]{40}", base):
            try:
                subprocess.run(["git", "merge-base", "--is-ancestor", base, "HEAD"], check=True)
                data = subprocess.check_output(["git", "diff", "--name-status",
                                                "--no-renames", "-z", base, "HEAD"])
                dirs = classify(data.decode("utf-8").rstrip("\x00").split("\x00"))
            except (subprocess.CalledProcessError, UnicodeError):
                dirs = []
    with open(os.environ["GITHUB_OUTPUT"], "a") as out:
        out.write("mode=" + ("focused" if dirs else "full") + "\n")
        out.write("directories=" + json.dumps(dirs) + "\n")
    print("ROUTE := " + ("FOCUSED" if dirs else "FULL"))

def verify(dirs):
    if not dirs:
        raise SystemExit("NO_CERTIFICATES")
    for directory in dirs:
        if not PREFIX.fullmatch(directory):
            raise SystemExit("INVALID_DIRECTORY")
        d = Path(directory)
        if set(p.name for p in d.iterdir()) != FILES:
            raise SystemExit("UNEXPECTED_FILES")
        for p in d.iterdir():
            if not p.is_file() or p.is_symlink():
                raise SystemExit("NOT_REGULAR_FILE")
        checks = {}
        for line in (d / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split("  ", 1)
            assert name not in checks
            checks[name] = digest
        assert set(checks) == FILES - {"SHA256SUMS"}
        for name, digest in checks.items():
            assert hashlib.sha256((d / name).read_bytes()).hexdigest() == digest
        for name in ("lean-toolchain", "lake-manifest.json"):
            assert (d / name).read_bytes() == Path(name).read_bytes()
        receipt = json.loads((d / "VERIFICATION.json").read_text())
        assert receipt["status"] == "LEAN_VERIFIED_CONDITIONAL"
        assert receipt["compilation"] == "PASS"
        assert receipt["unauthorized_axioms"] == 0
        expected = receipt["axioms"]
        assert len(expected) == receipt["audited_declarations"] >= 31
        source = d / "AnchorInversion.lean"
        # Standalone certificate must not import repository modules.
        for line in source.read_text().splitlines():
            if line.lstrip().startswith("import "):
                assert all(x.startswith("Mathlib.") for x in line.split()[1:])
        result = subprocess.run(["lake", "env", "lean", str(source)],
                                text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=1200)
        print(result.stdout)
        assert result.returncode == 0
        assert not re.search(r"\b(error|warning):", result.stdout)
        assert "sorryAx" not in result.stdout
        allowed = {"propext", "Classical.choice", "Quot.sound"}
        actual = {}
        for name, ax in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", result.stdout):
            assert name not in actual
            used = {x.strip() for x in ax.split(",") if x.strip()}
            assert used <= allowed
            actual[name] = sorted(used)
        assert actual == expected
        print("FOCUSED_ECPM_CERTIFICATE := PASS", directory)

if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("ASSERTIONS_DISABLED")
    if sys.argv[1:] == ["route"]:
        route()
    elif sys.argv[1:] == ["selftest"]:
        selftest()
    elif len(sys.argv) == 3 and sys.argv[1] == "verify":
        verify(json.loads(sys.argv[2]))
    else:
        raise SystemExit("INVALID_MODE")
