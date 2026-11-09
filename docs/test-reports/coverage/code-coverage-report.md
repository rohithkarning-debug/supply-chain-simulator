# Code Coverage Report — Final (v1.0)

| Field | Value |
|---|---|
| Report name | Code Coverage Report |
| Version | Final (v1.0) |
| Prepared by | Rohanth Ganesha C |
| Date | 09-11-2026 |
| Commit tested | f4dc0e8 |
| Environment | Windows 11 (10.0.26300), Python 3.11.9, pytest 9.1.1, pytest-cov 7.1.0 |
| CI note | Verified on Python 3.11 matching CI runner environment. |
| Command | python -m pytest --cov=scm_sim --cov-report=term-missing --cov-report=html:docs/test-reports/coverage/html |

## Result

Total line coverage: **99%** (469 statements, 1 missed) — 90% target MET (exceeds requirement SCM-NF-003).

## Per-module coverage

| Module | Stmts | Miss | Coverage | Owner |
|---|---|---|---|---|
| src/scm_sim/__init__.py | 1 | 0 | 100% | Rohith |
| src/scm_sim/__main__.py | 33 | 1 | 97% | Rohith |
| src/scm_sim/analytics.py | 67 | 0 | 100% | Pranav |
| src/scm_sim/inventory.py | 59 | 0 | 100% | Rohith |
| src/scm_sim/orders.py | 66 | 0 | 100% | Rohanth |
| src/scm_sim/shipments.py | 88 | 0 | 100% | Rishi |
| src/scm_sim/simulator.py | 155 | 0 | 100% | Rohith |
| **TOTAL** | **469** | **1** | **99%** | |

## Uncovered lines and reasons

| File | Lines | Reason |
|---|---|---|
| src/scm_sim/__main__.py | 57 | Script entry-point invocation `raise SystemExit(main())` within `if __name__ == "__main__":`. Tests import and invoke `main(argv)` directly or spawn subprocesses, so this interpreter script-mode execution line is not hit under in-process coverage. |

## Changes since v1

Statement coverage improved from 97% (425 stmts, 12 missed) to **99%** (469 stmts, 1 missed).
- **`inventory.py`**: 98% -> **100%** (closed missing validation raise on line 58 via #60).
- **`orders.py`**: 95% -> **100%** (closed missing validation and lookup raises on lines 25, 62, 73 via #59, #84).
- **`simulator.py`**: 96% -> **100%** (closed missing validation paths on lines 104, 173, 228, 244-245, 252 via #60).
- **`analytics.py`** & **`shipments.py`**: Maintained **100%** statement coverage after additions in #53 and #79.

## CI enforcement

CI enforces the 90% threshold. `.github/workflows/ci.yml` line 17 runs:

    pytest -v --cov=scm_sim --cov-branch --cov-report=term-missing --cov-report=html --cov-fail-under=90

The test job fails if total coverage drops below 90%.
