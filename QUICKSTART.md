# Chronos URF RR Quickstart

This is the shortest path from clone to a first successful local verification pass.

## Requirements

- `git`
- `bash`
- `python3`
- Lean 4 with `lake`

## 1. Clone

```bash
git clone https://github.com/inaciovasquez2020/chronos-urf-rr.git
cd chronos-urf-rr
```

## 2. Check tools

```bash
python3 --version
git --version
lake --version
lean --version
```

## 3. Run canonical checks

```bash
lake build
[ -d tests ] && python3 -m pytest -q
```

## 4. Review the main executable surfaces

- `README.md`
- `STATUS.md`
- `STATUS_SNAPSHOT.md`
- `URF_STATUS.md`
- `OPEN_INPUTS_REGISTRY.md`
- `docs/`

## 5. Next steps

- detailed setup: `docs/SETUP_GUIDE.md`
- contribution policy: `CONTRIBUTING.md`
