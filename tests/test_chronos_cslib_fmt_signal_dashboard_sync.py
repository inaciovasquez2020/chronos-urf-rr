import subprocess


def test_chronos_cslib_fmt_signal_dashboard_sync():
    subprocess.run(
        [
            "python3",
            "-B",
            "tools/verify_chronos_cslib_fmt_signal_dashboard_sync.py",
        ],
        check=True,
    )
