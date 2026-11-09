# Unit Test Report - Final (v1.0)

| Field | Value |
|---|---|
| Report | Unit Test Report |
| Version | Final (v1.0) |
| Prepared by | Rohanth Ganesha C |
| Date | 09-11-2026 |
| Commit tested | 30702f8 |
| Environment | Windows 11 (10.0.26300), Python 3.11.9, pytest 9.1.1, pytest-cov 7.1.0 |
| Command | python -m pytest -v --durations=10 --junitxml=docs/test-reports/unit/junit.xml |

## 1. Summary
| Total | Passed | Failed | Skipped | Errors | Duration |
|---|---|---|---|---|---|
| 100 | 100 | 0 | 0 | 0 | 1.24s |

## 2. Results by test file
| Test file | Module under test | Owner | Tests | Passed | Failed |
|---|---|---|---|---|---|
| tests/test_inventory.py | scm_sim.inventory | Rohith | 25 | 25 | 0 |
| tests/test_orders.py | scm_sim.orders | Rohanth | 11 | 11 | 0 |
| tests/test_shipments.py | scm_sim.shipments | Rishi | 11 | 11 | 0 |
| tests/test_analytics.py | scm_sim.analytics | Pranav | 29 | 29 | 0 |
| tests/test_simulator.py | scm_sim.simulator, __main__ | Rohith | 21 | 21 | 0 |
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
0.43s call     tests/test_packaging.py::test_installed_scm_sim_command_runs
0.24s call     tests/test_simulator.py::test_cli_runs_as_module
0.02s call     tests/test_simulator.py::test_cli_csv_export
0.01s setup    tests/test_simulator.py::test_cli_csv_export
0.01s call     tests/test_simulator.py::test_cli_csv_and_summary_flags
0.01s setup    tests/test_simulator.py::test_cli_csv_and_summary_flags

(4 durations < 0.005s hidden.  Use -vv to show these durations.)
```

## 5. Changes since v1
Test count increased from 84 to 100 (+16 tests) closing all functional and branch coverage gaps:
- **#53 (Run Summary):** Added 3 tests in `tests/test_analytics.py` (`test_summarize_history_counts_days_and_trend`, `test_summarize_history_empty`, `test_format_summary_text`).
- **#54 (CSV Export):** Added 4 tests in `tests/test_simulator.py` (`test_write_history_csv_one_row_per_day`, `test_cli_csv_export`, `test_cli_csv_and_summary_flags`, `test_cli_reports_unwritable_csv_path`).
- **#59 (Orders Edge Cases):** Added 3 tests in `tests/test_orders.py` (`test_order_dataclass_rejects_non_positive_quantity_directly`, `test_get_unknown_order_raises_key_error`, `test_fulfilled_or_cancelled_orders_are_never_reprocessed`).
- **#60 (Simulator & Inventory Gaps):** Added 2 tests in `tests/test_inventory.py` (`test_remove_rejects_non_positive_quantity`, `test_stock_policy_allows_max_level_equal_to_reorder_point`) and 4 tests in `tests/test_simulator.py` (`test_cli_rejects_zero_days`, `test_set_policy_rejects_unknown_supplier`, `test_run_rejects_negative_days`, `test_replenishment_skips_full_warehouse`).

## 6. Failures and defects
None. 100% pass rate achieved across all 100 automated tests.

## 7. Raw evidence
- junit.xml
- pytest-output.txt
