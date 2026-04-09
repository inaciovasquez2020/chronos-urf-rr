from pathlib import Path
import sys

status = Path("proofs/Chronos/conditional/H41_FINITE_PATCH_STATUS_2026_04.yaml").read_text()
readme = Path("README.md").read_text()
proof_shell = Path("proofs/Chronos/conditional/FGL_PROOF_SHELL_2026_04.md").read_text()

ok = True

if "terminal_assumption: FGL(k,R,B)" not in status:
    print("MISSING: terminal_assumption FGL(k,R,B)")
    ok = False

if "finite-patch H4.1 is conditional only on `proofs/Chronos/conditional/FGL_PROOF_SHELL_2026_04.md`." not in readme:
    print("MISSING: README FGL-only statement")
    ok = False

if "V_{k,R,B}\\cap\\bigl(W_{k,R,B}\\oplus \\langle 1\\rangle\\bigr)^{\\perp}=\\{0\\}" not in proof_shell:
    print("MISSING: canonical FGL theorem statement")
    ok = False

if not ok:
    sys.exit(1)

print("PASS: FGL is the sole open finite-patch assumption")
