# Branch Coverage Report — v1

| Field | Value |
|---|---|
| Report name | Branch Coverage Report |
| Version | v1 |
| Prepared by | Pranav Hareesh Achar |
| Date | 2026-11-05 |
| Commit tested | 3354d63 |
| Environment | Linux 6.18.55-2-cachyos-lts, Python 3.14.9 |
| CI note | CI runs Python 3.11; statement counts differ slightly on 3.14. |
| Command | python -m pytest --cov=scm_sim --cov-branch --cov-report=term-missing --cov-report=html:docs/test-reports/branch-coverage/html --cov-report=xml:docs/test-reports/branch-coverage/coverage.xml |

## Result

Combined line + branch coverage: 96% — 112 total branches, 12 partially covered.

## Per-module coverage

| Module | Branches | Partial | Combined % | Owner |
|---|---|---|---|---|
| src/scm_sim/__init__.py | 0 | 0 | 100% | Rohith |
| src/scm_sim/__main__.py | 6 | 2 | 85% | Rohith |
| src/scm_sim/analytics.py | 18 | 1 | 99% | Pranav |
| src/scm_sim/inventory.py | 16 | 1 | 97% | Rohith |
| src/scm_sim/orders.py | 16 | 3 | 92% | Rohanth |
| src/scm_sim/shipments.py | 22 | 0 | 100% | Rishi |
| src/scm_sim/simulator.py | 34 | 5 | 94% | Rohith |
| TOTAL | 112 | 12 | 96% | |

## Partially covered branches

| File | Branch | Condition not tested | Reason |
|---|---|---|---|
| src/scm_sim/__main__.py | 18->19 | if __name__ == "__main__" evaluates to True | Tests import the module under pytest and never execute it as a script. |
| src/scm_sim/__main__.py | 30->31 | second entry-point guard inside __main__ | Same — script-mode path never taken in the test suite. |
| src/scm_sim/analytics.py | 83->81 | loop back-edge (early exit / iteration-count path) | No test drives the loop through an exit other than normal end-of-data. |
| src/scm_sim/inventory.py | 57->58 | input-validation raise path | No test passes invalid input to trigger the raise on line 58. |
| src/scm_sim/orders.py | 24->25 | input-validation raise path | No test triggers the raise on line 25. |
| src/scm_sim/orders.py | 61->62 | input-validation raise path | No test triggers the raise on line 62. |
| src/scm_sim/orders.py | 72->73 | input-validation raise path | No test triggers the raise on line 73. |
| src/scm_sim/simulator.py | 103->104 | input-validation raise path | No test triggers the raise on line 104. |
| src/scm_sim/simulator.py | 172->173 | input-validation raise path | No test triggers the raise on line 173. |
| src/scm_sim/simulator.py | 227->228 | input-validation raise path | No test triggers the raise on line 228. |
| src/scm_sim/simulator.py | 243->244 | input-validation raise path | No test triggers the raise on line 244. |
| src/scm_sim/simulator.py | 251->252 | input-validation raise path | No test triggers the raise on line 252. |

Exact arcs are also visible in the HTML report: docs/test-reports/branch-coverage/html/index.html.
