# Branch Coverage Report — v1

| Field | Value |
|---|---|
| Report name | Branch Coverage Report |
| Version | v1 |
| Prepared by | Pranav |
| Date | 2026-11-05 |
| Commit tested | 3354d63 |
| Environment | Linux 6.18.55-2-cachyos-lts, Python 3.14.9 |
| Command | python -m pytest --cov=scm_sim --cov-branch --cov-report=term-missing --cov-report=html:docs/test-reports/branch-coverage/html --cov-report=xml:docs/test-reports/branch-coverage/coverage.xml |

## Result

Combined line + branch coverage: 96% — 112 total branches, 12 partially covered.

## Per-module coverage

| Module | Branches | Partial | Combined % | Owner |
|---|---|---|---|---|
| src/scm_sim/__init__.py | 0 | 0 | 100% | TODO |
| src/scm_sim/__main__.py | 6 | 2 | 85% | TODO |
| src/scm_sim/analytics.py | 18 | 1 | 99% | TODO |
| src/scm_sim/inventory.py | 16 | 1 | 97% | TODO |
| src/scm_sim/orders.py | 16 | 3 | 92% | TODO |
| src/scm_sim/shipments.py | 22 | 0 | 100% | TODO |
| src/scm_sim/simulator.py | 34 | 5 | 94% | TODO |
| TOTAL | 112 | 12 | 96% | |

## Partially covered branches

| File | Branch | Condition not tested | Reason |
|---|---|---|---|
| src/scm_sim/analytics.py | 83->81 | loop fall-through | TODO |
| src/scm_sim/__main__.py | 19 | one branch | TODO |
| src/scm_sim/__main__.py | 31 | one branch | TODO |
| src/scm_sim/inventory.py | 58 | one branch | TODO |
| src/scm_sim/orders.py | 25 | one branch | TODO |
| src/scm_sim/orders.py | 62 | one branch | TODO |
| src/scm_sim/orders.py | 73 | one branch | TODO |
| src/scm_sim/simulator.py | 104 | one branch | TODO |
| src/scm_sim/simulator.py | 173 | one branch | TODO |
| src/scm_sim/simulator.py | 228 | one branch | TODO |
| src/scm_sim/simulator.py | 244-245 | one branch | TODO |
| src/scm_sim/simulator.py | 252 | one branch | TODO |
