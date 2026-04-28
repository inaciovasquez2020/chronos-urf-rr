import subprocess
import sys


CHECKS = [
    "tools/verify_urf_repository_status_export.py",
    "tools/verify_urf_status_language_guard.py",
]


def run_check(path):
    result = subprocess.run(
        [sys.executable, path],
        check=True,
        text=True,
        capture_output=True,
    )

    output = result.stdout.strip()
    if output:
        print(output)


def main():
    for path in CHECKS:
        run_check(path)

    print("URF status suite PASS")


if __name__ == "__main__":
    main()
