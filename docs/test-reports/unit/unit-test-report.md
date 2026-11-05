# Unit Test Report - v1

| Field | Value |
|---|---|
| Report | Unit Test Report |
| Version | v1 (testing week) |
| Prepared by | Rohanth Ganesha C |
| Date | 05-11-2026 |
| Commit tested | 2cceca8 |
| Environment | Windows 11 (10.0.26300), Python 3.11.9, pytest 9.1.1, pytest-cov 7.1.0 |
| Command | python -m pytest -v --durations=10 --junitxml=docs/test-reports/unit/junit.xml |

## 1. Summary
| Total | Passed | Failed | Skipped | Errors | Duration |
|---|---|---|---|---|---|
| 84 | 84 | 0 | 0 | 0 | 1.18s |

## 2. Results by test file
| Test file | Module under test | Owner | Tests | Passed | Failed |
|---|---|---|---|---|---|
| tests/test_inventory.py | scm_sim.inventory | Rohith | 23 | 23 | 0 |
| tests/test_orders.py | scm_sim.orders | Rohanth | 8 | 8 | 0 |
| tests/test_shipments.py | scm_sim.shipments | Rishi | 11 | 11 | 0 |
| tests/test_analytics.py | scm_sim.analytics | Pranav | 26 | 26 | 0 |
| tests/test_simulator.py | scm_sim.simulator, __main__ | Rohith | 13 | 13 | 0 |
| tests/test_packaging.py | pyproject / scm-sim command | Rohith | 3 | 3 | 0 |

## 3. Results by test case
| TC-ID | Test file | Result |
|---|---|---|
| TC-INV-01, TC-INV-02 | test_inventory.py | PASS |
| TC-ORD-01, TC-ORD-02 | test_orders.py | PASS |
| TC-SHP-01, TC-SHP-02 | test_shipments.py | PASS |
| TC-ANA-01, TC-ANA-02 | test_analytics.py | PASS |
| TC-SIM-01, TC-SIM-02, TC-REP-01 (automated part) | test_simulator.py | PASS |
| TC-SEC-01 | test_inventory.py, test_orders.py, test_shipments.py, test_simulator.py | PASS |

## 4. Slowest tests
```
0.37s call     tests/test_packaging.py::test_installed_scm_sim_command_runs
0.19s call     tests/test_simulator.py::test_cli_runs_as_module

(8 durations < 0.005s hidden.  Use -vv to show these durations.)
```

## 5. Failures and defects
None.

## 6. Raw evidence
- junit.xml
- pytest-output.txt

