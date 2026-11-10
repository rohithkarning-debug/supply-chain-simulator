### 13. Test Case Management and Traceability

#### 13.1 Test Case Register

Fifteen test cases are documented. Automated cases run in CI; mixed and manual cases include their execution evidence in the individual test-case records. The register below is the index; the individual test cases are held in `docs/testplan/test-cases/`.

| TC ID | Title | Covers | Type | Owner | Automation status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-INV-01 | Stock tracking, mutation validation and warehouse capacity | SCM-F-001, SCM-F-002, SCM-SR-001, SCM-SR-002 | Functional | Rohith Karning | Automated (see §13.3) |
| TC-INV-02 | Per-item stock policy, reorder suggestions and snapshots | SCM-F-003, SCM-F-004, SCM-SR-001, SCM-SR-007 | Functional | Rohith Karning | Automated (see §13.3) |
| TC-ORD-01 | Order creation, sequential identifiers and all-or-nothing fulfilment | SCM-F-010, SCM-F-011 | Functional | Rohanth Ganesha C | Automated (see §13.3) |
| TC-ORD-02 | Back-order retry ordering, cancellation rules and status filtering | SCM-F-012, SCM-F-013 | Functional | Rohanth Ganesha C | Automated (see §13.3) |
| TC-SHP-01 | Supplier validation and shipment dispatch | SCM-F-020, SCM-F-021 | Functional | Rishi J Mule | Automated (see §13.3) |
| TC-SHP-02 | Delay modelling, arrival processing and delay detection | SCM-F-022, SCM-F-023 | Functional | Rishi J Mule | Automated (see §13.3) |
| TC-SIM-01 | Daily time-step ordering and automatic replenishment | SCM-F-023, SCM-F-041, SCM-F-042 | Integration | Rohith Karning | Automated (see §13.3) |
| TC-SIM-02 | Scenario configuration, demo detection and CLI behaviour | SCM-F-034, SCM-F-040, SCM-F-043, SCM-F-044, SCM-NF-005 | System | Rishi J Mule | Automated (see §13.3) |
| TC-ANA-01 | Delayed-shipment and inventory-exception detection | SCM-F-030, SCM-F-031 | Functional | Pranav Achar | Automated (see §13.3) |
| TC-ANA-02 | Order metrics, report composition, formatting and run summary | SCM-F-032, SCM-F-033, SCM-F-034 | Functional | Pranav Achar | Automated (see §13.3) |
| TC-REP-01 | Seeded reproducibility of reports and output | SCM-NF-002 | Reliability | Pranav Achar | Mixed: 1 automated pytest test plus a manual CLI comparison |
| TC-COV-01 | Coverage gate and cross-platform portability | SCM-NF-003, SCM-NF-004 | Maintainability | Pranav Achar | Mixed: CI job result plus a manual run on Windows and Linux |
| TC-PERF-01 | Runtime of the 365-day run and the 10-day CLI demo | SCM-NF-001 | Performance | Rohanth Ganesha C | Manual |
| TC-SEC-01 | Input validation, state invariants and reference integrity | SCM-SR-001, SCM-SR-002, SCM-SR-003, SCM-SR-004, SCM-SR-007 | Security | Rishi J Mule | Automated (9 pytest tests across 4 modules) |
| TC-SEC-02 | Branch protection, secrets absence and dependency hygiene | SCM-SR-005, SCM-SR-006 | Security (process) | Rohith Karning | Manual |

#### 13.2 Requirements Traceability Matrix (Requirement to Test Case)

The matrix below traces every requirement in the registry to the test case or cases that verify it. It is the test-side counterpart of the RTM in SRS §8.

**Status codes:** A = accepted with passing evidence; P = partially validated because some required evidence is outstanding; N = not verified because required evidence is absent.

| Req ID | Requirement short | SRS section | Test case(s) | Test level | Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-F-001 | Stock per (warehouse, SKU) with validated add/remove | §4.1 | TC-INV-01 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-002 | Warehouse capacity with `CapacityExceededError` | §4.1 | TC-INV-01 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-003 | Per-item policy, `needs_reorder`, `is_excess` | §4.1 | TC-INV-02 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-004 | Reorder suggestions and independent snapshot | §4.1 | TC-INV-02 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-010 | Order creation with sequential IDs | §4.2 | TC-ORD-01 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-011 | Fulfil in full or back-order, no partial fulfilment | §4.2 | TC-ORD-01 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-012 | Retry open orders oldest-first | §4.2 | TC-ORD-02 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-013 | Cancel, look up by ID, list by status | §4.2 | TC-ORD-02 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-020 | Supplier registration with lead time and reliability | §4.3 | TC-SHP-01 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-021 | Dispatch with sequential IDs and expected day | §4.3 | TC-SHP-01 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-022 | Stochastic delay model from reliability | §4.3 | TC-SHP-02 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-023 | Arrival processing and late-shipment listing | §4.3 | TC-SHP-02, TC-SIM-01 | Unit, Integration | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-030 | Delayed shipments with days late, worst first | §4.4 | TC-ANA-01 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-031 | Stockouts, low stock and excess with surplus | §4.4 | TC-ANA-01 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-032 | Order metrics and fill rate to 2 dp | §4.4 | TC-ANA-02 | Unit | Pass (final unit-test report: 100 tests, commit `30702f8`) | A |
| SCM-F-033 | Daily report composition and formatting | §4.4 | TC-ANA-02 | Unit | Pass (final unit-test report: 100 tests, commit `30702f8`) | A |
| SCM-F-034 | Multi-day run summary and `--summary` display | §4.4 | TC-ANA-02, TC-SIM-02 | Unit, System | Pass (final unit-test report: 100 tests, commit `30702f8`; E5 is recorded in the System Validation Report) | A |
| SCM-F-040 | Scenario configuration with validation | §4.5 | TC-SIM-02 | System | Pass (final unit-test report: 100 tests, commit `30702f8`) | A |
| SCM-F-041 | Fixed-order daily step and report retention | §4.5 | TC-SIM-01 | Integration | Pass (final unit-test report: 100 tests, commit `30702f8`) | A |
| SCM-F-042 | Automatic trimmed replenishment | §4.5 | TC-SIM-01 | Integration | Pass (final unit-test report: 100 tests, commit `30702f8`) | A |
| SCM-F-043 | CLI with exit code 0 and usage error at 2 | §4.5 | TC-SIM-02 | System | Pass (final unit-test report: 100 tests, commit `30702f8`) | A |
| SCM-F-044 | Daily metrics CSV export with `--csv PATH` | §4.5 | TC-SIM-02 | System | Pass (final unit-test report: 100 tests, commit `30702f8`; E6 is recorded in the System Validation Report) | A |
| SCM-NF-001 | 365-day run and 10-day CLI demo each $\le 1.0$ s | §5 | TC-PERF-01 | Performance | Pass; three measured trials for each run on Windows 11 / Python 3.11.9 | A |
| SCM-NF-002 | Same seed and scenario give identical output | §5 | TC-REP-01 | Reliability | Pass; automated report equality and manual CLI comparisons recorded | A |
| SCM-NF-003 | $\ge 90\%$ line coverage, all tests pass before merge | §5 | TC-COV-01 | Maintainability | Pass; 100 tests, 99.79% line, 99.17% branch, 99.66% combined coverage | A |
| SCM-NF-004 | Runs on Windows, Linux, macOS; standard library only | §5 | TC-COV-01 | Portability | Windows and Linux tested; macOS not tested | P |
| SCM-NF-005 | One documented command; counts and "No issues"; `--help` | §5 | TC-SIM-02 | System | Pass; package command, summary/CSV options and CLI behavior verified | A |
| SCM-SR-001 | Input validation before any state change | §5.1.2 | TC-INV-01, TC-INV-02, TC-SEC-01 | Security | Pass (CI run #20, `b3702ef`) | A |
| SCM-SR-002 | Stock invariants and unchanged state on violation | §5.1.2 | TC-INV-01, TC-SEC-01 | Security | Pass (CI run #20, `b3702ef`) | A |
| SCM-SR-003 | Guarded order status transitions | §5.1.2 | TC-SEC-01 | Security | Pass (CI run #20, `b3702ef`) | A |
| SCM-SR-004 | Unknown references rejected with `KeyError` | §5.1.2 | TC-SEC-01 | Security | Pass (CI run #20, `b3702ef`) | A |
| SCM-SR-005 | Protected `main` branch rules | §5.1.2 | TC-SEC-02 | Security (process) | Pass; branch rules, push rejection and blocked merge recorded in `docs/testplan/results/TC-SEC-02.md` | A |
| SCM-SR-006 | No secrets, no network calls, no runtime dependencies | §5.1.2 | TC-SEC-02 | Security (process) | Pass; repository scans and dependency inspection recorded in `docs/testplan/results/TC-SEC-02.md` | A |
| SCM-SR-007 | Returned data is an independent copy | §5.1.2 | TC-INV-02, TC-SEC-01 | Security | Pass (CI run #20, `b3702ef`) | A |

The two security objectives require no test case of their own: SCM-SO-1 is evidenced by the accepted results for SCM-SR-001 to SCM-SR-004 and SCM-SR-007, and SCM-SO-2 is evidenced by the accepted results for SCM-SR-005 and SCM-SR-006.

The `CI run #20` entries above preserve the original baseline evidence (73 automated tests). The final suite result is 100 / 100 passed, as recorded in the [final unit-test report](../test-reports/unit/unit-test-report.md); final line and branch coverage evidence is recorded in the [coverage reports](../test-reports/coverage/code-coverage-report.md) and [branch-coverage report](../test-reports/branch-coverage/branch-coverage-report.md).

#### 13.3 Reverse Traceability (Test Case to Requirement and Automation)

| TC ID | Requirements | Automated by | Manual part |
| :--- | :--- | :--- | :--- |
| TC-INV-01 | SCM-F-001, SCM-F-002, SCM-SR-001, SCM-SR-002 | `tests/test_inventory.py`: `test_add_and_level`, `test_remove_reduces_stock`, `test_remove_too_much_raises`, `test_remove_rejects_non_positive_quantity`, `test_add_up_to_exact_capacity_is_allowed`, `test_add_beyond_capacity_raises_and_leaves_stock_unchanged`, `test_unregistered_warehouse_has_unlimited_capacity`; supporting: `test_stockout_detected`, `test_register_warehouse_rejects_non_positive_capacity`, `test_total_in_warehouse_sums_all_skus`, `test_existing_behaviour_unchanged_with_capacity_registered` | – |
| TC-INV-02 | SCM-F-003, SCM-F-004, SCM-SR-001, SCM-SR-007 | `tests/test_inventory.py`: `test_stock_policy_rejects_invalid_values`, `test_needs_reorder_at_boundary`, `test_is_excess_only_above_max_level`, `test_reorder_suggestions_sorted_and_only_tracked_items`, `test_snapshot_returns_independent_copy`; supporting: `test_stock_policy_defaults`, `test_stock_policy_allows_max_level_equal_to_reorder_point`, `test_get_policy_returns_default_when_unset`, `test_set_policy_is_per_warehouse_and_sku`, `test_reorder_suggestions_empty_for_new_inventory` | – |
| TC-ORD-01 | SCM-F-010, SCM-F-011 | `tests/test_orders.py`: `test_create_order_id_sequence`, `test_invalid_quantity`, `test_fulfil_enough_stock`, `test_backorder_when_short`, `test_rejected_order_does_not_consume_an_id`, `test_order_dataclass_rejects_non_positive_quantity_directly` | – |
| TC-ORD-02 | SCM-F-012, SCM-F-013 | `tests/test_orders.py`: `test_backorder_later_fulfilled_by_process_open`, `test_oldest_first_priority`, `test_cancel_rules`, `test_get_unknown_order_raises_key_error`, `test_fulfilled_or_cancelled_orders_are_never_reprocessed`; `tests/test_simulator.py`: `test_older_backorder_is_served_before_new_order_on_same_day` | – |
| TC-SHP-01 | SCM-F-020, SCM-F-021 | `tests/test_shipments.py`: `test_supplier_validation`, `test_add_supplier_and_reject_duplicate_and_unknown`, `test_expected_day_calculated_from_lead_time`, `test_shipment_id_sequence_and_in_transit_filtering`, `test_reject_non_positive_quantity` | – |
| TC-SHP-02 | SCM-F-022, SCM-F-023 | `tests/test_shipments.py`: `test_on_time_arrival_adds_stock`, `test_delayed_shipment_not_delivered_early`, `test_delayed_detection_both_in_transit_late_and_delivered_late`, `test_reliability_one_means_never_delayed`, `test_probabilistic_delay_with_zero_reliability`, `test_capacity_breach_does_not_abort_other_arrivals`; `tests/test_simulator.py`: `test_blocked_arrival_is_logged_and_delivered_once_space_frees` | – |
| TC-SIM-01 | SCM-F-023, SCM-F-041, SCM-F-042 | `tests/test_simulator.py`: `test_step_advances_day_counter`, `test_shipment_arrives_after_lead_time_and_increases_stock`, `test_large_order_is_backordered_then_fulfilled_after_replenishment`, `test_low_stock_triggers_exactly_one_reorder_while_in_transit`, `test_reorder_is_trimmed_to_fit_warehouse_capacity`, `test_older_backorder_is_served_before_new_order_on_same_day` | – |
| TC-SIM-02 | SCM-F-034, SCM-F-040, SCM-F-043, SCM-F-044, SCM-NF-005 | `tests/test_simulator.py`: `test_schedule_order_validates_input`, `test_demo_detects_delay_stockout_backorder_and_excess`, `test_cli_main_runs`, `test_cli_main_summary_flag`, `test_metrics_rows_has_one_flat_row_per_day`, `test_cli_csv_export`, `test_cli_csv_and_summary_flags`, `test_cli_rejects_zero_days`, `test_cli_runs_as_module`; `tests/test_packaging.py`: `test_installed_scm_sim_command_runs`, `test_pyproject_declares_scm_sim_console_script`, `test_package_has_no_runtime_dependencies` | – |
| TC-ANA-01 | SCM-F-030, SCM-F-031 | `tests/test_analytics.py`: `test_in_transit_late_uses_current_day`, `test_delivered_late_uses_actual_day_not_current_day`, `test_on_time_and_early_are_excluded`, `test_in_transit_not_yet_due_is_excluded`, `test_arrival_on_day_zero_is_not_treated_as_in_transit`, `test_sorted_by_days_late_descending`, `test_stockouts_only_exact_zero_and_sorted`, `test_low_stock_boundaries_zero_excluded_and_20_included`, `test_low_stock_respects_custom_reorder_point`, `test_excess_boundaries_500_excluded_and_501_included`, `test_excess_surplus_with_custom_max_level`, `test_empty_stock_gives_empty_results`, `test_low_stock_and_excess_use_each_items_own_policy`, `test_items_without_policy_fall_back_to_global_thresholds`, `test_build_report_passes_policies_through`; `tests/test_simulator.py`: `test_report_uses_per_item_policy_thresholds` | – |
| TC-ANA-02 | SCM-F-032, SCM-F-033, SCM-F-034 | `tests/test_analytics.py`: `test_order_metrics_counts_with_string_statuses`, `test_order_metrics_accepts_enum_statuses`, `test_enum_and_string_statuses_can_be_mixed`, `test_fill_rate_excludes_cancelled_orders`, `test_fill_rate_is_zero_with_no_orders`, `test_fill_rate_is_zero_when_all_cancelled`, `test_build_report_has_all_keys`, `test_build_report_contents`, `test_build_report_passes_custom_thresholds_through`, `test_format_report_has_section_headers_and_counts`, `test_format_report_prints_no_issues_for_empty_sections`, `test_summarize_run_and_format`, `test_summarize_run_empty_history`, `test_order_metrics_unknown_status` | – |
| TC-REP-01 | SCM-NF-002 | `tests/test_simulator.py::test_same_seed_gives_identical_reports` | Run the CLI twice with `--seed 42` and compare the output; then run with `--seed 7` and confirm the delays differ |
| TC-COV-01 | SCM-NF-003, SCM-NF-004 | CI `test` job (`pytest -v --cov=scm_sim --cov-branch --cov-fail-under=90`): 100 tests passed; 99.79% line, 99.17% branch, 99.66% combined coverage | Windows 11 and Linux tested; macOS not tested |
| TC-PERF-01 | SCM-NF-001 | – | Time `build_demo().run(365)` and the 10-day CLI demo with `time` / `Measure-Command`, 3 runs each |
| TC-SEC-01 | SCM-SR-001, SCM-SR-002, SCM-SR-003, SCM-SR-004, SCM-SR-007 | `tests/test_inventory.py`: `test_remove_rejects_non_positive_quantity`, `test_remove_too_much_raises`, `test_register_warehouse_rejects_non_positive_capacity`, `test_add_beyond_capacity_raises_and_leaves_stock_unchanged`, `test_stock_policy_rejects_invalid_values`, `test_snapshot_returns_independent_copy`; `tests/test_orders.py`: `test_invalid_quantity`, `test_rejected_order_does_not_consume_an_id`, `test_order_dataclass_rejects_non_positive_quantity_directly`, `test_get_unknown_order_raises_key_error`, `test_cancel_rules`, `test_fulfilled_or_cancelled_orders_are_never_reprocessed`; `tests/test_shipments.py`: `test_supplier_validation`, `test_add_supplier_and_reject_duplicate_and_unknown`, `test_reject_non_positive_quantity`; `tests/test_simulator.py`: `test_schedule_order_validates_input`, `test_set_policy_rejects_unknown_supplier` | – |
| TC-SEC-02 | SCM-SR-005, SCM-SR-006 | – | Attempt a direct push to `main`; attempt to merge a PR without approval; inspect Settings → Branches; search the repository for tokens and secrets; check `requirements.txt` for test-only dependencies |

#### 13.4 Coverage Analysis

| Metric | Value |
| :--- | :--- |
| Requirements in the registry | 34 (22 functional, 5 non-functional, 7 security) |
| Requirements traced to at least one test case | 34 |
| Functional requirements | 22 total; 22 accepted |
| Non-functional requirements | 5 total; 4 accepted, 1 partially validated |
| Security requirements | 7 total; 7 accepted |
| Total requirement status | 34 total; 33 accepted, 1 partially validated, 0 not verified |
| Requirements untraced | 0 |
| Test cases planned | 15 |
| Test cases fully automated | 11 |
| Test cases mixed (automated plus manual) | 2 (TC-REP-01, TC-COV-01) |
| Test cases fully manual | 2 (TC-PERF-01, TC-SEC-02) |
| Test items under test | 7 (Test Plan §2) |
| Test items with at least one test case | 7 |
| Requirements per test case (average) | 2.7 (40 requirement-to-test-case links / 15 cases) |
| Highest-requirement test cases | TC-SIM-02 and TC-SEC-01 (5 requirements each) |

**Analysis.** Forward and reverse traceability are complete: all 34 requirements map to at least one of the 15 test cases, and all test cases map to requirements. Thirty-three requirements are accepted; SCM-NF-004 remains partially validated because macOS was not tested. Rishi's final System Validation Report was merged in PR #89 and records E1–E6: E1–E4 exercise SCM-F-043 (CLI invocation), E5 exercises SCM-F-034 (run summary), and E6 exercises SCM-F-044 (daily metrics CSV export). These are results recorded in the report; the manual E1–E6 runs were not independently repeated during this audit.