    # Independent Verification

    ## Fresh verification path
    ```bash
    git clone https://github.com/inaciovasquez2020/chronos-urf-rr.git
    cd chronos-urf-rr
    python3 -m pytest -q
grep -RInE 'sorry|admit|axiom' URF/Lean || true
    ```

    ## Expected outcome
    - Commands complete without hidden local dependencies.
    - Any theorem-level claim must still be checked against the explicit status file.
