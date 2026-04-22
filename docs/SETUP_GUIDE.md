# Setup Guide

This guide is for contributors who want a reliable local environment for Chronos URF RR.

## Prerequisites

```bash
python3 --version
git --version
lake --version
lean --version
```

Recommended baseline:

- Python 3.10 or newer
- Git
- Lean 4 with `lake`
- POSIX shell environment

## Clone

```bash
git clone https://github.com/inaciovasquez2020/chronos-urf-rr.git
cd chronos-urf-rr
```

## Optional virtual environment

```bash
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install --upgrade pip
```

## Verification

```bash
lake build
[ -d tests ] && python3 -m pytest -q
```

## Recommended edit loop

```bash
git pull --ff-only origin main
lake build
[ -d tests ] && python3 -m pytest -q
git status --short
```

## Related files

- `QUICKSTART.md`
- `CONTRIBUTING.md`
- `README.md`
- `STATUS.md`
- `STATUS_SNAPSHOT.md`
- `URF_STATUS.md`
- `OPEN_INPUTS_REGISTRY.md`
