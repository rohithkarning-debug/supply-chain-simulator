### 8. Requirements Traceability Matrix

The Requirements Traceability Matrix (RTM) records, for every requirement defined in this SRS, the section that specifies it, the module that implements it, the test case that verifies it, and the verification status. It is the primary index used during final acceptance to confirm that every requirement in SRS §4, §5 and §5.1 is implemented and verified.

**Status codes**

| Code | Meaning |
| :--- | :--- |
| A | Accepted — the linked test case is automated, has executed, and passed in the CI `test` job on GitHub Actions (CI run #20, commit `b3702ef`, 11-10-2026). |
| N | Not yet verified — the test case is manual, or contains a manual step that has not been executed yet. |

#### 8.1 Functional Requirements

| Req ID | Requirement short | Section ref / Design Spec | Module | Test case(s) | Status (N/P/A) | Comments |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-F-001 | Stock tracking per (warehouse, SKU) with validated add/remove | SRS §4.1; SAD §4.3.1 | `scm_sim.inventory` (`Inventory`) | TC-INV-01 | A | `InsufficientStockError` leaves stock unchanged. |
| SCM-F-002 | Warehouse capacity with `CapacityExceededError` on breach | SRS §4.1; SAD §4.3.1 | `scm_sim.inventory` (`Inventory`) | TC-INV-01 | A | Unregistered warehouses have unlimited capacity. |
| SCM-F-003 | Per-item stock policy; `needs_reorder` / `is_excess` | SRS §4.1; SAD §4.3.1 | `scm_sim.inventory` (`StockPolicy`) | TC-INV-02 | A | Defaults reorder_point 20, reorder_quantity 100, max_level 500. Analytics reuses the 20 / 500 defaults in SCM-F-031. |
| SCM-F-004 | Sorted reorder suggestions and independent stock snapshot | SRS §4.1; SAD §4.3.1 | `scm_sim.inventory` (`Inventory`) | TC-INV-02 | A | `snapshot()` is the input to the analytics stock classifiers; satisfies SCM-SR-007. |
| SCM-F-010 | Create customer orders with sequential `ORD-0001…` IDs | SRS §4.2; SAD §4.3.2 | `scm_sim.orders` (`OrderManager`) | TC-ORD-01 | A | Initial status `PENDING`. |
| SCM-F-011 | Fulfil in full or back-order; no partial fulfilment | SRS §4.2; SAD §4.3.2 | `scm_sim.orders` (`OrderManager`) | TC-ORD-01 | A | Base data for the fill-rate metric in SCM-F-032. |
| SCM-F-012 | Retry open orders oldest-first | SRS §4.2; SAD §4.3.2 | `scm_sim.orders` (`OrderManager`) | TC-ORD-02 | A | Ordering by `created_day`, then `order_id`. |
| SCM-F-013 | Cancel, look up by ID, list by status | SRS §4.2; SAD §4.3.2 | `scm_sim.orders` (`OrderManager`) | TC-ORD-02 | A | Unknown ID raises `KeyError` (SCM-SR-004). |
| SCM-F-020 | Register suppliers with lead time and reliability | SRS §4.3; SAD §4.3.3 | `scm_sim.shipments` (`ShipmentManager`) | TC-SHP-01 | A | Duplicate supplier IDs rejected. |
| SCM-F-021 | Dispatch shipments with sequential `SHP-0001…` IDs | SRS §4.3; SAD §4.3.3 | `scm_sim.shipments` (`ShipmentManager`) | TC-SHP-01 | A | `expected_day = day + lead_time_days`. |
| SCM-F-022 | Model stochastic delays from supplier reliability | SRS §4.3; SAD §4.3.3 | `scm_sim.shipments` (`ShipmentManager`) | TC-SHP-02 | A | Seeded PRNG keeps runs reproducible (SCM-NF-002). |
| SCM-F-023 | Deliver arrivals and list shipments with days late > 0 | SRS §4.3; SAD §4.3.3 | `scm_sim.shipments` (`ShipmentManager`) | TC-SHP-02 | A | Supplies `expected_day` / `actual_day` consumed by SCM-F-030. |
| SCM-F-030 | Report delayed shipments with days late, worst first | SRS §4.4; SAD §4.3.4 | `scm_sim.analytics` (`find_delayed_shipments`) | TC-ANA-01 | A | Uses `actual_day` when delivered, otherwise `current_day`. |
| SCM-F-031 | Report stockouts, low stock and excess with surplus | SRS §4.4; SAD §4.3.4 | `scm_sim.analytics` (`find_stockouts`, `find_low_stock`, `find_excess`) | TC-ANA-01 | A | Boundary values 0 / 20 / 21 and 500 / 501 verified. |
| SCM-F-032 | Order metrics per status and fill rate (2 dp) | SRS §4.4; SAD §4.3.4 | `scm_sim.analytics` (`order_metrics`) | TC-ANA-02 | A | Cancelled orders excluded from the denominator. |
| SCM-F-033 | Build the daily report and format it as readable text | SRS §4.4; SAD §4.3.4 | `scm_sim.analytics` (`build_report`, `format_report`) | TC-ANA-02 | A | Empty sections print "No issues"; satisfies the reporting rule of SCM-NF-005. |
| SCM-F-040 | Configure a scenario | SRS §4.5; SAD §3.4.1 | `scm_sim.simulator` (`Simulation`) | TC-SIM-02 | A | Unknown warehouses and past days rejected. |
| SCM-F-041 | Advance one day in the fixed order and keep every report | SRS §4.5; SAD §4.1 | `scm_sim.simulator` (`Simulation`) | TC-SIM-01 | A | Report construction is step 5 and calls `build_report` (SCM-F-033). |
| SCM-F-042 | Automatic replenishment, trimmed to capacity | SRS §4.5; SAD §4.1 | `scm_sim.simulator` (`Simulation`) | TC-SIM-01 | A | Exactly one dispatch per item while nothing is in transit. |
| SCM-F-043 | Command-line interface with exit code 0 | SRS §4.5; SAD §4.5 | `scm_sim.__main__` | TC-SIM-02 | A | `--days < 1` produces a usage error with exit code 2. |

#### 8.2 Non-Functional Requirements

| Req ID | Requirement short | Section ref / Design Spec | Module | Test case(s) | Status (N/P/A) | Comments |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-NF-001 | 365-day run and 10-day CLI demo each complete in $\le 1.0$ s | SRS §5; SAD §3.1 | `scm_sim.simulator`, `scm_sim.__main__` | TC-PERF-01 | N | Manual timing test with `time` / `Measure-Command`, 3 runs each; to be executed and recorded by 20-10-2026. Measured baselines recorded in SRS §5 are ~0.02 s and ~0.10 s. |
| SCM-NF-002 | Same seed and scenario give identical output on every run and machine | SRS §5; SAD §3.6 | `scm_sim.simulator` (`random.Random(seed)`) | TC-REP-01 | N | Mixed case: the automated part is accepted (A) — `tests/test_simulator.py::test_same_seed_gives_identical_reports` passed in CI run #20. The manual part (running the CLI twice with `--seed 42` and comparing output, then with `--seed 7`) has not been executed, so the overall status is N until it is. |
| SCM-NF-003 | $\ge 90\%$ line coverage of `scm_sim`, all tests pass before merge | SRS §5; SAD §3.6 | `scm_sim` package (all modules) | TC-COV-01 | N | Mixed case: the CI-measured part is accepted (A) — `pytest -v --cov=scm_sim` reported 73 passed and 97% coverage in CI run #20, commit `b3702ef`. Coverage is re-measured on every push to `main` and every PR, so it is continuously satisfied rather than verified once. Status N because the manual portability execution of the same test case is outstanding. |
| SCM-NF-004 | Runs on Python $\ge$ 3.11 on Windows, Linux and macOS, standard library only at runtime | SRS §5; SAD §3.6 | `scm_sim` package; `requirements.txt` | TC-COV-01 | N | Same mixed case as SCM-NF-003: automated on `ubuntu-latest` with Python 3.11 (A); the manual runs on Windows 11 and a local Linux laptop have not been executed yet. `requirements.txt` holds test-only dependencies, satisfying SCM-SR-006. |
| SCM-NF-005 | One documented command to run the demo; counts and "No issues" in every section; `--help` lists all options | SRS §5; SAD §4.5 | `scm_sim.__main__`; `scm_sim.analytics` (`format_report`) | TC-SIM-02 | A | The empty-section rule is implemented by `format_report` (SCM-F-033). |

#### 8.3 Security Objectives and Security Requirements

| Req ID | Requirement short | Section ref / Design Spec | Module | Test case(s) | Status (N/P/A) | Comments |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-SO-1 | **Objective:** integrity of simulation data — stock, order and shipment states can never become invalid, even with bad input | SRS §5.1.1; SAD §3.9 | All domain modules (`Inventory`, `OrderManager`, `ShipmentManager`) | TC-SEC-01 | – | Objective, not directly testable; verified through the SRs below, which are all accepted. |
| SCM-SO-2 | **Objective:** integrity and traceability of the codebase — only reviewed, tested changes reach `main`, each traceable to an author and a PR | SRS §5.1.1; SAD §3.9 | Repository workflow; `.github/workflows/ci.yml` | TC-SEC-02 | N | Objective, not directly testable; enforced procedurally by SCM-SR-005 and SCM-SR-006. The manual branch-protection inspection of TC-SEC-02 is outstanding. |
| SCM-SR-001 | Validate input on every public operation and raise `ValueError` before changing state | SRS §5.1.2; SAD §3.9 | All domain modules; `scm_sim.__main__` | TC-SEC-01 | A | Analytics performs no validation and raises nothing, because it is read-only and holds no state. |
| SCM-SR-002 | Stock never goes below 0 or above a registered capacity; violations raise and leave state unchanged | SRS §5.1.2; SAD §3.9 | `scm_sim.inventory` | TC-SEC-01 | A | `InsufficientStockError` / `CapacityExceededError`. |
| SCM-SR-003 | Guarded order status transitions | SRS §5.1.2; SAD §3.9 | `scm_sim.orders` | TC-SEC-01 | A | `FULFILLED` cannot be cancelled; `FULFILLED` and `CANCELLED` are never re-processed. |
| SCM-SR-004 | Unknown supplier, warehouse or order references raise `KeyError` | SRS §5.1.2; SAD §3.9 | `scm_sim.orders`, `scm_sim.shipments`, `scm_sim.simulator` | TC-SEC-01 | A | Nothing is created implicitly. |
| SCM-SR-005 | `main` is protected: PR required, one non-author approval, `test` check passing, up-to-date branch, no force pushes or deletions | SRS §5.1.2; SAD §3.9 | GitHub branch protection; CI `test` job | TC-SEC-02 | N | Manual process test: direct push to `main` must be rejected, a PR without approval must be unmergeable, and Settings → Branches must show the rules. Not yet executed. |
| SCM-SR-006 | No secrets in the repository; no network calls and no runtime third-party dependencies | SRS §5.1.2; SAD §3.9 | Repository; `requirements.txt` | TC-SEC-02 | N | Verified manually by searching the repository for tokens and checking that `requirements.txt` lists only test dependencies. Not yet executed. |
| SCM-SR-007 | Data returned to callers is a copy; mutating it cannot change internal state | SRS §5.1.2; SAD §3.9 | `scm_sim.inventory` (`snapshot`); `scm_sim.analytics` (`build_report`) | TC-SEC-01 | A | `Inventory.snapshot()` returns an independent copy; `build_report` builds a fresh dictionary that the caller may retain. |

#### 8.4 Coverage Summary

| Requirement set | Total | Accepted (A) | Not yet verified (N) | Objective (–) |
| :--- | :--- | :--- | :--- | :--- |
| Functional requirements (§4) | 20 | 20 | 0 | 0 |
| Non-functional requirements (§5) | 5 | 1 | 4 | 0 |
| Security requirements (§5.1.2) | 7 | 5 | 2 | 0 |
| Security objectives (§5.1.1) | 0 | 0 | 0 | 2 |
| **Total** | **32** | **26** | **6** | **2** |

All 20 functional requirements are accepted. The six requirements carrying status N are all blocked on manual execution rather than on missing verification work: TC-PERF-01 (SCM-NF-001), the manual half of TC-REP-01 (SCM-NF-002), the manual portability half of TC-COV-01 (SCM-NF-003 and SCM-NF-004), and both requirements of TC-SEC-02 (SCM-SR-005 and SCM-SR-006). These are scheduled for completion by 20-10-2026 per Test Plan §7, after which their status moves to A and the accepted count reaches 32 of 32.