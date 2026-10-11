# Requirements Registry: Supply Chain Management Simulator

This registry is the single source of truth for every requirement, security objective and test case ID used in the SRS, SAD and Test Plan; IDs must not be changed or added without telling Rohith.

## 5. Requirements registry (fixed IDs; don't change or add without telling Rohith)

All IDs use the prefix **`SCM-`**. Acceptance criteria IDs are `AC-SCM-F-001`, etc.

### 5.1 Functional requirements (20)

| ID | Requirement (short) | Priority | Owner | Test case |
|---|---|---|---|---|
| SCM-F-001 | Track stock per (warehouse, SKU); add/remove units; quantity must be > 0; removing more than available raises `InsufficientStockError` and leaves stock unchanged | High | Rohith | TC-INV-01 |
| SCM-F-002 | Register a warehouse capacity (> 0); an add that would push the warehouse total over capacity raises `CapacityExceededError` and leaves stock unchanged; unregistered warehouses are unlimited | High | Rohith | TC-INV-01 |
| SCM-F-003 | Per-item stock policy (reorder point 20, reorder quantity 100, max level 500 by default; invalid values rejected); `needs_reorder` when level ≤ reorder point; `is_excess` when level > max level | High | Rohith | TC-INV-02 |
| SCM-F-004 | Produce a sorted list of reorder suggestions for every tracked item at/below its reorder point, and an independent snapshot of all stock levels | Medium | Rohith | TC-INV-02 |
| SCM-F-010 | Create customer orders (customer, warehouse, SKU, quantity > 0, day) with sequential IDs `ORD-0001…` and initial status PENDING | High | Rohanth | TC-ORD-01 |
| SCM-F-011 | Fulfil an order in full when stock ≥ quantity (stock reduced, FULFILLED, fulfilment day recorded); otherwise BACKORDERED with stock unchanged; no partial fulfilment | High | Rohanth | TC-ORD-01 |
| SCM-F-012 | Retry all PENDING and BACKORDERED orders oldest-first (created day, then ID) and return the newly fulfilled ones | High | Rohanth | TC-ORD-02 |
| SCM-F-013 | Cancel an order unless it is FULFILLED; look up an order by ID (unknown → `KeyError`); list orders by status | Medium | Rohanth | TC-ORD-02 |
| SCM-F-020 | Register suppliers with ID, name, lead time (≥ 0 days) and on-time reliability (0.0–1.0); duplicate IDs rejected | High | Rishi | TC-SHP-01 |
| SCM-F-021 | Dispatch a shipment from a supplier to a warehouse with sequential IDs `SHP-0001…`; expected day = dispatch day + lead time; unknown supplier or quantity ≤ 0 rejected | High | Rishi | TC-SHP-01 |
| SCM-F-022 | Model delays: if a seeded random draw exceeds the supplier's reliability, add 1–3 days to the arrival day; reliability 1.0 is never delayed | High | Rishi | TC-SHP-02 |
| SCM-F-023 | On or after its arrival day, deliver each in-transit shipment (stock added, DELIVERED, actual day recorded) and list shipments whose days late > 0 | High | Rishi | TC-SHP-02 |
| SCM-F-030 | Report delayed shipments with days late (actual day if delivered, else current day, minus expected day), sorted most-late first | High | Pranav | TC-ANA-01 |
| SCM-F-031 | Report stockouts (qty = 0), low stock (0 < qty ≤ reorder point) and excess inventory (qty > max level, with surplus) | High | Pranav | TC-ANA-01 |
| SCM-F-032 | Compute order metrics: counts per status and fill rate = fulfilled ÷ (total − cancelled), 2 dp, 0.0 when there are no eligible orders | Medium | Pranav | TC-ANA-02 |
| SCM-F-033 | Build a daily report (day, delayed shipments, stockouts, low stock, excess, orders) and format it as readable text, printing "No issues" for empty sections | Medium | Pranav | TC-ANA-02 |
| SCM-F-040 | Configure a scenario: suppliers, warehouses with capacity, per-item policies linked to a supplier, initial stock, and customer orders scheduled for future days (past days, quantity ≤ 0 and unknown warehouses rejected) | High | Rohith | TC-SIM-02 |
| SCM-F-041 | Advance the simulation one day at a time in the fixed order: arrivals → today's orders → back-order retry → replenishment → report; keep every daily report | High | Rohith | TC-SIM-01 |
| SCM-F-042 | Automatically dispatch one replenishment per item that needs reorder and has none in transit, trimmed so on-hand + in-transit stock never exceeds warehouse capacity | High | Rohith | TC-SIM-01 |
| SCM-F-043 | Command-line interface `python -m scm_sim --days N --seed S` runs the demo, prints a day-by-day log and the final report, and exits with code 0 (`--days < 1` → usage error) | Medium | Rohith | TC-SIM-02 |

### 5.2 Non-functional requirements (owner: Rohanth)

| ID | Requirement | Category | Priority | Test case |
|---|---|---|---|---|
| SCM-NF-001 | A 365-day run of the demo scenario completes in ≤ 1 s, and the 10-day CLI demo (including interpreter start-up) in ≤ 1 s, on a standard laptop with Python 3.11 (measured baseline: ~0.02 s and ~0.1 s) | Performance | Medium | TC-PERF-01 |
| SCM-NF-002 | Same seed + same scenario → identical daily reports and output on every run and machine | Reliability / Reproducibility | High | TC-REP-01 |
| SCM-NF-003 | ≥ 90% line coverage of `scm_sim`, measured by pytest-cov on every CI run; all tests must pass before merge | Maintainability | High | TC-COV-01 |
| SCM-NF-004 | Runs on Python ≥ 3.11 on Windows, Linux and macOS using only the standard library at runtime (pytest only for testing) | Portability | Medium | TC-COV-01 |
| SCM-NF-005 | A new user can run the demo with one documented command; every report section shows a count and "No issues" when empty; `--help` lists all options | Usability | Medium | TC-SIM-02 |

### 5.3 Security (owner: Rishi)

| ID | Item | Priority | Test case |
|---|---|---|---|
| SCM-SO-1 | **Objective: integrity of simulation data.** Stock, order and shipment states can never become invalid (negative stock, over-capacity warehouse, impossible status changes), even with bad input | – | – |
| SCM-SO-2 | **Objective: integrity and traceability of the codebase.** Only reviewed, tested changes reach `main`, and every change is traceable to an author and a PR | – | – |
| SCM-SR-001 | All public operations validate input (quantities > 0, lead time ≥ 0, reliability in [0, 1], valid policies, capacity > 0, future days) and raise `ValueError` **before** changing any state | High | TC-SEC-01 |
| SCM-SR-002 | Stock can never go below 0 or above a registered warehouse capacity; violating operations raise `InsufficientStockError` / `CapacityExceededError` and leave state unchanged | High | TC-SEC-01 |
| SCM-SR-003 | Order status changes are guarded: FULFILLED orders can't be cancelled; FULFILLED and CANCELLED orders are never re-processed | High | TC-SEC-01 |
| SCM-SR-004 | References to unknown suppliers, warehouses or orders are rejected with `KeyError`; nothing is created implicitly | High | TC-SEC-01 |
| SCM-SR-005 | `main` is protected: PR required, 1 approval from a non-author, required `test` check passing, branch up to date, force pushes and deletions blocked, rules applied to admins | High | TC-SEC-02 |
| SCM-SR-006 | No secrets or credentials in the repository; the simulator makes no network calls and has no runtime third-party dependencies | Medium | TC-SEC-02 |
| SCM-SR-007 | Data returned to callers (snapshots, reports) is a copy; modifying it can't change internal state | Medium | TC-SEC-01 |

### 5.4 Test cases (15)

Every test case is **automated by existing pytest tests** (column "Automated by"). Actual result = Pass, from CI run #20 on commit `b3702ef` (11-10-2026), unless stated.

| TC ID | Covers | Type | Owner | Automated by (tests/…) |
|---|---|---|---|---|
| TC-INV-01 | F-001, F-002 | Functional | Rohith | `test_inventory.py`: `test_add_and_level`, `test_remove_reduces_stock`, `test_remove_too_much_raises`, `test_add_up_to_exact_capacity_is_allowed`, `test_add_beyond_capacity_raises_and_leaves_stock_unchanged`, `test_unregistered_warehouse_has_unlimited_capacity` |
| TC-INV-02 | F-003, F-004 | Functional | Rohith | `test_inventory.py`: `test_stock_policy_rejects_invalid_values`, `test_needs_reorder_at_boundary`, `test_is_excess_only_above_max_level`, `test_reorder_suggestions_sorted_and_only_tracked_items`, `test_snapshot_returns_independent_copy` |
| TC-SIM-01 | F-041, F-042 | Integration | Rohith | `test_simulator.py`: `test_step_advances_day_counter`, `test_shipment_arrives_after_lead_time_and_increases_stock`, `test_large_order_is_backordered_then_fulfilled_after_replenishment`, `test_low_stock_triggers_exactly_one_reorder_while_in_transit`, `test_reorder_is_trimmed_to_fit_warehouse_capacity` |
| TC-SIM-02 | F-040, F-043, NF-005 | System | Rishi | `test_simulator.py`: `test_schedule_order_validates_input`, `test_demo_detects_delay_stockout_backorder_and_excess`, `test_cli_main_runs`, `test_cli_runs_as_module` |
| TC-ORD-01 | F-010, F-011 | Functional | Rohanth | `test_orders.py`: `test_create_order_id_sequence`, `test_invalid_quantity`, `test_fulfil_enough_stock`, `test_backorder_when_short` |
| TC-ORD-02 | F-012, F-013 | Functional | Rohanth | `test_orders.py`: `test_backorder_later_fulfilled_by_process_open`, `test_oldest_first_priority`, `test_cancel_rules` |
| TC-PERF-01 | NF-001 | Performance | Rohanth | Manual: time `build_demo().run(365)` and the 10-day CLI demo (`time` / `Measure-Command`), 3 runs each |
| TC-COV-01 | NF-003, NF-004 | Maintainability | Pranav | CI `test` job (`pytest -v --cov=scm_sim`): 73 passed, 97% coverage; manual run on Windows + Linux |
| TC-SHP-01 | F-020, F-021 | Functional | Rishi | `test_shipments.py`: `test_supplier_validation`, `test_add_supplier_and_reject_duplicate_and_unknown`, `test_expected_day_calculated_from_lead_time`, `test_shipment_id_sequence_and_in_transit_filtering`, `test_reject_non_positive_quantity` |
| TC-SHP-02 | F-022, F-023 | Functional | Rishi | `test_shipments.py`: `test_on_time_arrival_adds_stock`, `test_delayed_shipment_not_delivered_early`, `test_delayed_detection_both_in_transit_late_and_delivered_late`, `test_reliability_one_means_never_delayed`, `test_probabilistic_delay_with_zero_reliability` |
| TC-SEC-01 | SR-001, SR-002, SR-003, SR-004, SR-007 | Security | Rishi | `test_inventory.py` (`test_remove_too_much_raises`, `test_add_beyond_capacity_raises_and_leaves_stock_unchanged`, `test_stock_policy_rejects_invalid_values`, `test_snapshot_returns_independent_copy`), `test_orders.py` (`test_invalid_quantity`, `test_cancel_rules`), `test_shipments.py` (`test_supplier_validation`, `test_add_supplier_and_reject_duplicate_and_unknown`), `test_simulator.py` (`test_schedule_order_validates_input`) |
| TC-SEC-02 | SR-005, SR-006 | Security (process) | Rohith | Manual: try a direct push to `main` (must be rejected); open a PR without approval (merge blocked); check Settings → Branches; search repo for secrets/tokens; check `requirements.txt` has test-only deps |
| TC-ANA-01 | F-030, F-031 | Functional | Pranav | `test_analytics.py`: `test_in_transit_late_uses_current_day`, `test_delivered_late_uses_actual_day_not_current_day`, `test_on_time_and_early_are_excluded`, `test_sorted_by_days_late_descending`, `test_stockouts_only_exact_zero_and_sorted`, `test_low_stock_boundaries_zero_excluded_and_20_included`, `test_excess_boundaries_500_excluded_and_501_included` |
| TC-ANA-02 | F-032, F-033 | Functional | Pranav | `test_analytics.py`: `test_fill_rate_excludes_cancelled_orders`, `test_fill_rate_is_zero_with_no_orders`, `test_enum_and_string_statuses_can_be_mixed`, `test_build_report_has_all_keys`, `test_format_report_has_section_headers_and_counts`, `test_format_report_prints_no_issues_for_empty_sections` |
| TC-REP-01 | NF-002 | Reliability | Pranav | `test_simulator.py`: `test_same_seed_gives_identical_reports`; manual: run CLI twice with `--seed 42` and compare output (identical), then `--seed 7` (different delays) |

**Test case format** (one file per test case: `docs/testplan/test-cases/TC-XXX-NN.md`):

| Field | Content |
|---|---|
| TC ID | TC-ORD-01 |
| Title | … |
| Requirement(s) | SCM-F-010, SCM-F-011 |
| Type | Functional / Integration / System / Performance / Security / Reliability / Maintainability |
| Preconditions | … |
| Test data | … (made-up IDs: `WH-NORTH`, `WIDGET`, `C-ACME`) |
| Objective | One sentence: what this test proves |
| Steps | 1. … 2. … |
| Expected result | … (measurable) |
| Pass/fail criteria | Pass if …; fail if … |
| Automated by | `tests/test_orders.py::test_fulfil_enough_stock`, … |
| Actual result | Pass (CI run #20, commit b3702ef), or "Not run" for manual cases not yet executed |
| Status | Passed / Not run |
