# Branch Coverage Report — Final (v1.0)

| Field | Value |
|---|---|
| Report name | Branch Coverage Report |
| Version | Final (v1.0) |
| Prepared by | Rohanth Ganesha C |
| Date | 09-11-2026 |
| Commit tested | f4dc0e8 |
| Environment | Windows 11 (10.0.26300), Python 3.11.9, pytest 9.1.1, pytest-cov 7.1.0 |
| CI note | Verified on Python 3.11 matching CI runner environment. |
| Command | python -m pytest --cov=scm_sim --cov-branch --cov-report=term-missing --cov-report=html:docs/test-reports/branch-coverage/html --cov-report=xml:docs/test-reports/branch-coverage/coverage.xml |

## Result

Combined line + branch coverage: **99%** — 120 total branches, 1 partially covered.

## Per-module coverage

| Module | Branches | Partial | Combined % | Owner |
|---|---|---|---|---|
| src/scm_sim/__init__.py | 0 | 0 | 100% | Rohith |
| src/scm_sim/__main__.py | 10 | 1 | 95% | Rohith |
| src/scm_sim/analytics.py | 20 | 0 | 100% | Pranav |
| src/scm_sim/inventory.py | 16 | 0 | 100% | Rohith |
| src/scm_sim/orders.py | 16 | 0 | 100% | Rohanth |
| src/scm_sim/shipments.py | 22 | 0 | 100% | Rishi |
| src/scm_sim/simulator.py | 36 | 0 | 100% | Rohith |
| **TOTAL** | **120** | **1** | **99%** | |

## Partially covered branches

| File | Branch | Condition not tested | Reason |
|---|---|---|---|
| src/scm_sim/__main__.py | 56->57 | `if __name__ == "__main__":` evaluates to True | Tests import `__main__` under pytest and execute `main()` directly or run subprocess CLI invocations, so the script-mode entry-point execution arc is not evaluated as True in-process. |

## Changes since v1

Combined line + branch coverage increased from 96% (112 branches, 12 partial) to **99%** (120 branches, 1 partial).
- **`analytics.py`**: Branch 83->81 (loop exit) resolved; 100% branch coverage achieved.
- **`inventory.py`**: Branch 57->58 (negative remove validation) resolved via #60; 100% branch coverage achieved.
- **`orders.py`**: Branches 24->25, 61->62, 72->73 (order validation and unknown lookup) resolved via #59 (#84); 100% branch coverage achieved.
- **`simulator.py`**: Branches 103->104, 172->173, 227->228, 243->244, 251->252 (CLI args and simulation validation) resolved via #60; 100% branch coverage achieved.

Exact arcs are also visible in the HTML report: `docs/test-reports/branch-coverage/html/index.html`.
