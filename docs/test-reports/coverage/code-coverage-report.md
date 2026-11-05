# Code Coverage Report — v1

| Field | Value |
|---|---|
| Report name | Code Coverage Report |
| Version | v1 |
| Prepared by | Pranav Hareesh Achar |
| Date | 2026-11-05 |
| Commit tested | 3354d63 |
| Environment | Linux 6.18.55-2-cachyos-lts, Python 3.14.9 |
| CI note | CI runs Python 3.11; statement counts differ slightly on 3.14. |
| Command | python -m pytest --cov=scm_sim --cov-report=term-missing --cov-report=html:docs/test-reports/coverage/html |

## Result

Total line coverage: 97% (425 statements, 12 missed) — 90% target MET.

## Per-module coverage

| Module | Stmts | Miss | Coverage | Owner |
|---|---|---|---|---|
| src/scm_sim/__init__.py | 1 | 0 | 100% | Rohith |
| src/scm_sim/__main__.py | 20 | 2 | 90% | Rohith |
| src/scm_sim/analytics.py | 58 | 0 | 100% | Pranav |
| src/scm_sim/inventory.py | 59 | 1 | 98% | Rohith |
| src/scm_sim/orders.py | 60 | 3 | 95% | Rohanth |
| src/scm_sim/shipments.py | 78 | 0 | 100% | Rishi |
| src/scm_sim/simulator.py | 149 | 6 | 96% | Rohith |
| TOTAL | 425 | 12 | 97% | |

## Uncovered lines and reasons

| File | Lines | Reason |
|---|---|---|
| src/scm_sim/__main__.py | 19, 31 | Inside the if __name__ == "__main__" entry-point guard; tests import the module under pytest and never run it as a script. |
| src/scm_sim/inventory.py | 58 | Input-validation error path (raise) not triggered by any test. |
| src/scm_sim/orders.py | 25, 62, 73 | Input-validation error paths (raise ValueError/KeyError) not triggered by any test. |
| src/scm_sim/simulator.py | 104, 173, 228, 244-245, 252 | Input-validation error paths (raise) not triggered by any test. |

## CI enforcement

CI enforces the 90% threshold. .github/workflows/ci.yml line 17 runs:

    pytest -v --cov=scm_sim --cov-branch --cov-report=term-missing --cov-report=html --cov-fail-under=90

The test job fails if total coverage drops below 90%.
