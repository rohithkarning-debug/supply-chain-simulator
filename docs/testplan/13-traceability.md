### 13. Test Case Management and Traceability

#### 13.1 Test Case Register

Fifteen test cases are planned. Every one is automated by tests that already exist and pass in CI, except where a manual step is explicitly recorded. The register below is the index; the individual test cases are held in `docs/testplan/test-cases/`.

| TC ID | Title | Covers | Type | Owner | Automation status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| TC-INV-01 | Stock tracking, mutation validation and warehouse capacity | SCM-F-001, SCM-F-002 | Functional | Rohith Karning | Automated (6 pytest tests) |
| TC-INV-02 | Per-item stock policy, reorder suggestions and snapshots | SCM-F-003, SCM-F-004 | Functional | Rohith Karning | Automated (5 pytest tests) |
| TC-ORD-01 | Order creation, sequential identifiers and all-or-nothing fulfilment | SCM-F-010, SCM-F-011 | Functional | Rohanth Ganesha C | Automated (4 pytest tests) |
| TC-ORD-02 | Back-order retry ordering, cancellation rules and status filtering | SCM-F-012, SCM-F-013 | Functional | Rohanth Ganesha C | Automated (3 pytest tests) |
| TC-SHP-01 | Supplier validation and shipment dispatch | SCM-F-020, SCM-F-021 | Functional | Rishi J Mule | Automated (5 pytest tests) |
| TC-SHP-02 | Delay modelling, arrival processing and delay detection | SCM-F-022, SCM-F-023 | Functional | Rishi J Mule | Automated (5 pytest tests) |
| TC-SIM-01 | Daily time-step ordering and automatic replenishment | SCM-F-041, SCM-F-042 | Integration | Rohith Karning | Automated (5 pytest tests) |
| TC-SIM-02 | Scenario configuration, demo detection and CLI behaviour | SCM-F-040, SCM-F-043, SCM-NF-005 | System | Rishi J Mule | Automated (4 pytest tests) |
| TC-ANA-01 | Delayed-shipment and inventory-exception detection | SCM-F-030, SCM-F-031 | Functional | Pranav Achar | Automated (7 pytest tests) |
| TC-ANA-02 | Order metrics, report composition and report formatting | SCM-F-032, SCM-F-033 | Functional | Pranav Achar | Automated (6 pytest tests) |
| TC-REP-01 | Seeded reproducibility of reports and output | SCM-NF-002 | Reliability | Pranav Achar | Mixed: 1 automated pytest test plus a manual CLI comparison |
| TC-COV-01 | Coverage gate and cross-platform portability | SCM-NF-003, SCM-NF-004 | Maintainability | Pranav Achar | Mixed: CI job result plus a manual run on Windows and Linux |
| TC-PERF-01 | Runtime of the 365-day run and the 10-day CLI demo | SCM-NF-001 | Performance | Rohanth Ganesha C | Manual |
| TC-SEC-01 | Input validation, state invariants and reference integrity | SCM-SR-001, SCM-SR-002, SCM-SR-003, SCM-SR-004, SCM-SR-007 | Security | Rishi J Mule | Automated (9 pytest tests across 4 modules) |
| TC-SEC-02 | Branch protection, secrets absence and dependency hygiene | SCM-SR-005, SCM-SR-006 | Security (process) | Rohith Karning | Manual |

#### 13.2 Requirements Traceability Matrix (Requirement to Test Case)

The matrix below traces every requirement in the registry to the test case or cases that verify it. It is the test-side counterpart of the RTM in SRS §8.

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
| SCM-F-032 | Order metrics and fill rate to 2 dp | §4.4 | TC-ANA-02 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-033 | Daily report composition and formatting | §4.4 | TC-ANA-02 | Unit | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-040 | Scenario configuration with validation | §4.5 | TC-SIM-02 | System | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-041 | Fixed-order daily step and report retention | §4.5 | TC-SIM-01 | Integration | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-042 | Automatic trimmed replenishment | §4.5 | TC-SIM-01 | Integration | Pass (CI run #20, `b3702ef`) | A |
| SCM-F-043 | CLI with exit code 0 and usage error at 2 | §4.5 | TC-SIM-02 | System | Pass (CI run #20, `b3702ef`) | A |
| SCM-NF-001 | 365-day run and 10-day CLI demo each $\le 1.0$ s | §5 | TC-PERF-01 | Performance | Not run | N |
| SCM-NF-002 | Same seed and scenario give identical output | §5 | TC-REP-01 | Reliability | Automated part Pass (CI run #20, `b3702ef`); manual CLI comparison not run | N |
| SCM-NF-003 | $\ge 90\%$ coverage, all tests pass before merge | §5 | TC-COV-01 | Maintainability | Automated part Pass — 73 passed, 97% coverage (CI run #20, `b3702ef`) | N |
| SCM-NF-004 | Runs on Windows, Linux, macOS; standard library only | §5 | TC-COV-01 | Portability | Automated on `ubuntu-latest`; manual Windows and Linux runs not run | N |
| SCM-NF-005 | One documented command; counts and "No issues"; `--help` | §5 | TC-SIM-02 | System | Pass (CI run #20, `b3702ef`) | A |
| SCM-SR-001 | Input validation before any state change | §5.1.2 | TC-SEC-01 | Security | Pass (CI run #20, `b3702ef`) | A |
| SCM-SR-002 | Stock invariants and unchanged state on violation | §5.1.2 | TC-SEC-01 | Security | Pass (CI run #20, `b3702ef`) | A |
| SCM-SR-003 | Guarded order status transitions | §5.1.2 | TC-SEC-01 | Security | Pass (CI run #20, `b3702ef`) | A |
| SCM-SR-004 | Unknown references rejected with `KeyError` | §5.1.2 | TC-SEC-01 | Security | Pass (CI run #20, `b3702ef`) | A |
| SCM-SR-005 | Protected `main` branch rules | §5.1.2 | TC-SEC-02 | Security (process) | Not run | N |
| SCM-SR-006 | No secrets, no network calls, no runtime dependencies | §5.1.2 | TC-SEC-02 | Security (process) | Not run | N |
| SCM-SR-007 | Returned data is an independent copy | §5.1.2 | TC-SEC-01 | Security | Pass (CI run #20, `b3702ef`) | A |

The two security objectives require no test case of their own: SCM-SO-1 is evidenced by the accepted results for SCM-SR-001 to SCM-SR-004 and SCM-SR-007, and SCM-SO-2 is evidenced by SCM-SR-005 and SCM-SR-006 once TC-SEC-02 has been executed.

#### 13.3 Reverse Traceability (Test Case to Requirement and Automation)

| TC ID | Requirements | Automated by | Manual part |
| :--- | :--- | :--- | :--- |
| TC-INV-01 | SCM-F-001, SCM-F-002 | `tests/test_inventory.py`: `test_add_and_level`, `test_remove_reduces_stock`, `test_remove_too_much_raises`, `test_add_up_to_exact_capacity_is_allowed`, `test_add_beyond_capacity_raises_and_leaves_stock_unchanged`, `test_unregistered_warehouse_has_unlimited_capacity` | – |
| TC-INV-02 | SCM-F-003, SCM-F-004 | `tests/test_inventory.py`: `test_stock_policy_rejects_invalid_values`, `test_needs_reorder_at_boundary`, `test_is_excess_only_above_max_level`, `test_reorder_suggestions_sorted_and_only_tracked_items`, `test_snapshot_returns_independent_copy` | – |
| TC-ORD-01 | SCM-F-010, SCM-F-011 | `tests/test_orders.py`: `test_create_order_id_sequence`, `test_invalid_quantity`, `test_fulfil_enough_stock`, `test_backorder_when_short` | – |
| TC-ORD-02 | SCM-F-012, SCM-F-013 | `tests/test_orders.py`: `test_backorder_later_fulfilled_by_process_open`, `test_oldest_first_priority`, `test_cancel_rules` | – |
| TC-SHP-01 | SCM-F-020, SCM-F-021 | `tests/test_shipments.py`: `test_supplier_validation`, `test_add_supplier_and_reject_duplicate_and_unknown`, `test_expected_day_calculated_from_lead_time`, `test_shipment_id_sequence_and_in_transit_filtering`, `test_reject_non_positive_quantity` | – |
| TC-SHP-02 | SCM-F-022, SCM-F-023 | `tests/test_shipments.py`: `test_on_time_arrival_adds_stock`, `test_delayed_shipment_not_delivered_early`, `test_delayed_detection_both_in_transit_late_and_delivered_late`, `test_reliability_one_means_never_delayed`, `test_probabilistic_delay_with_zero_reliability` | – |
| TC-SIM-01 | SCM-F-041, SCM-F-042 | `tests/test_simulator.py`: `test_step_advances_day_counter`, `test_shipment_arrives_after_lead_time_and_increases_stock`, `test_large_order_is_backordered_then_fulfilled_after_replenishment`, `test_low_stock_triggers_exactly_one_reorder_while_in_transit`, `test_reorder_is_trimmed_to_fit_warehouse_capacity` | – |
| TC-SIM-02 | SCM-F-040, SCM-F-043, SCM-NF-005 | `tests/test_simulator.py`: `test_schedule_order_validates_input`, `test_demo_detects_delay_stockout_backorder_and_excess`, `test_cli_main_runs`, `test_cli_runs_as_module` | – |
| TC-ANA-01 | SCM-F-030, SCM-F-031 | `tests/test_analytics.py`: `test_in_transit_late_uses_current_day`, `test_delivered_late_uses_actual_day_not_current_day`, `test_on_time_and_early_are_excluded`, `test_sorted_by_days_late_descending`, `test_stockouts_only_exact_zero_and_sorted`, `test_low_stock_boundaries_zero_excluded_and_20_included`, `test_excess_boundaries_500_excluded_and_501_included` | – |
| TC-ANA-02 | SCM-F-032, SCM-F-033 | `tests/test_analytics.py`: `test_fill_rate_excludes_cancelled_orders`, `test_fill_rate_is_zero_with_no_orders`, `test_enum_and_string_statuses_can_be_mixed`, `test_build_report_has_all_keys`, `test_format_report_has_section_headers_and_counts`, `test_format_report_prints_no_issues_for_empty_sections` | – |
| TC-REP-01 | SCM-NF-002 | `tests/test_simulator.py::test_same_seed_gives_identical_reports` | Run the CLI twice with `--seed 42` and compare the output; then run with `--seed 7` and confirm the delays differ |
| TC-COV-01 | SCM-NF-003, SCM-NF-004 | CI `test` job (`pytest -v --cov=scm_sim`): 73 passed, 97% coverage | Run the suite and the demo on Windows 11 and on a Linux laptop |
| TC-PERF-01 | SCM-NF-001 | – | Time `build_demo().run(365)` and the 10-day CLI demo with `time` / `Measure-Command`, 3 runs each |
| TC-SEC-01 | SCM-SR-001, SCM-SR-002, SCM-SR-003, SCM-SR-004, SCM-SR-007 | `tests/test_inventory.py` (`test_remove_too_much_raises`, `test_add_beyond_capacity_raises_and_leaves_stock_unchanged`, `test_stock_policy_rejects_invalid_values`, `test_snapshot_returns_independent_copy`), `tests/test_orders.py` (`test_invalid_quantity`, `test_cancel_rules`), `tests/test_shipments.py` (`test_supplier_validation`, `test_add_supplier_and_reject_duplicate_and_unknown`), `tests/test_simulator.py` (`test_schedule_order_validates_input`) | – |
| TC-SEC-02 | SCM-SR-005, SCM-SR-006 | – | Attempt a direct push to `main`; attempt to merge a PR without approval; inspect Settings → Branches; search the repository for tokens and secrets; check `requirements.txt` for test-only dependencies |

#### 13.4 Coverage Analysis

| Metric | Value |
| :--- | :--- |
| Requirements in the registry | 32 (20 functional, 5 non-functional, 7 security) |
| Requirements traced to at least one test case | 32 |
| Requirements with an accepted result (status A) | 26 |
| Requirements awaiting manual execution (status N) | 6 (SCM-NF-001, SCM-NF-002, SCM-NF-003, SCM-NF-004, SCM-SR-005, SCM-SR-006) |
| Requirements untraced | 0 |
| Test cases planned | 15 |
| Test cases fully automated | 11 |
| Test cases mixed (automated plus manual) | 2 (TC-REP-01, TC-COV-01) |
| Test cases fully manual | 2 (TC-PERF-01, TC-SEC-02) |
| Test items under test | 7 (Test Plan §2) |
| Test items with at least one test case | 7 |
| Requirements per test case (average) | 2.1 |
| Highest-requirement test case | TC-SEC-01 (5 security requirements) |

**Analysis.** Forward traceability is complete: every requirement in the registry is exercised by at least one planned test case, and the automation named for each test case exists in `tests/`. Reverse traceability is also complete: every test case names at least one requirement, so no testing effort is spent without a stated purpose. The only outstanding items are the manual executions, all of which concern properties that no automated test can observe — elapsed time, a second operating system, and repository branch-protection settings. These are scheduled for 20-10-2026 (Test Plan §7), after which the six status N requirements move to A and the exit criteria in §5.4 are fully satisfied.