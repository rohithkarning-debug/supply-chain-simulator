### 2. Test Items

#### 2.1 Basis of Testing

The items subject to test are the seven components of the Supply Chain Management Simulator as built and merged into `main` at commit **`b3702ef`** (11-10-2026). The system is a Python 3.11 command-line application whose source lives in the `src/scm_sim/` package, whose automated tests live in `tests/`, and whose continuous verification runs as the `test` job of the GitHub Actions workflow `.github/workflows/ci.yml`. Every item below is a module or a repository-level process artefact that is exercised by at least one planned test case in Test Plan §13.

At that commit the baseline is **73 automated tests passing with 97% line coverage of `scm_sim`**, CI green. These figures are recorded here so that the later test report can be compared against a fixed baseline rather than against an expectation formed after the fact.

#### 2.2 Test Items

| # | Test item | Source file | Owner | Responsibility under test | Requirements | Test cases |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| T1 | **Inventory** | `src/scm_sim/inventory.py` | Rohith Karning | Stock levels per (warehouse, SKU); validated `add` and `remove`; registered warehouse capacities and the `CapacityExceededError` invariant; per-item `StockPolicy` with `needs_reorder` and `is_excess`; sorted reorder suggestions; independent stock snapshots. | SCM-F-001, SCM-F-002, SCM-F-003, SCM-F-004; SCM-SR-002, SCM-SR-007 | TC-INV-01, TC-INV-02, TC-SEC-01 |
| T2 | **Order Manager** | `src/scm_sim/orders.py` | Rohanth Ganesha C | Customer order creation with sequential `ORD-0001…` identifiers; all-or-nothing fulfilment; back-ordering when stock is short; oldest-first retry of open orders; cancellation, lookup by ID and listing by status. | SCM-F-010, SCM-F-011, SCM-F-012, SCM-F-013; SCM-SR-003, SCM-SR-004 | TC-ORD-01, TC-ORD-02, TC-SEC-01 |
| T3 | **Shipment Manager** | `src/scm_sim/shipments.py` | Rishi J Mule | Supplier registration with lead time and reliability; dispatch with sequential `SHP-0001…` identifiers; stochastic delay modelling from the seeded PRNG; arrival processing into inventory; listing of in-transit and late shipments. | SCM-F-020, SCM-F-021, SCM-F-022, SCM-F-023; SCM-SR-001, SCM-SR-004 | TC-SHP-01, TC-SHP-02, TC-SEC-01 |
| T4 | **Analytics** | `src/scm_sim/analytics.py` | Pranav Achar | Detection of delayed shipments with days late, ordered worst first; classification of stockouts, low stock and excess inventory against configurable thresholds; order metrics and fill rate; daily report composition and text formatting. | SCM-F-030, SCM-F-031, SCM-F-032, SCM-F-033; SCM-NF-002, SCM-NF-005 | TC-ANA-01, TC-ANA-02 |
| T5 | **Simulation Engine** | `src/scm_sim/simulator.py` | Rohith Karning | Scenario configuration; the fixed-order daily time-step (arrivals → today's orders → back-order retry → replenishment → report); retention of every daily report; automatic trimmed replenishment; the built-in demo scenario; seeded reproducibility of a whole run. | SCM-F-040, SCM-F-041, SCM-F-042; SCM-NF-001, SCM-NF-002 | TC-SIM-01, TC-SIM-02, TC-REP-01, TC-PERF-01 |
| T6 | **CLI** | `src/scm_sim/__main__.py` | Rohith Karning | Command-line entry point `python -m scm_sim --days N --seed S`; day-by-day log and final report output; exit code 0 on success; usage error with exit code 2 for an invalid `--days` value; `--help` listing all options. | SCM-F-043; SCM-NF-005 | TC-SIM-02, TC-PERF-01 |
| T7 | **CI Pipeline** | `.github/workflows/ci.yml` | Rohith Karning | Execution of the whole suite with `pytest -v --cov=scm_sim` on every push to `main` and every pull request; publication of the required `test` check; enforcement of the protected-`main` rules that make merging conditional on it. | SCM-NF-003; SCM-SR-005, SCM-SR-006 | TC-COV-01, TC-SEC-02 |

#### 2.3 Items Not Under Test

The following are explicitly excluded from the test items, with the reasons recorded in Test Plan §4: the Python interpreter and standard-library internals (including the statistical behaviour of `random`, which is trusted rather than verified); the internals of pytest, pytest-cov and GitHub Actions; and any GUI, web interface, database or authentication layer, none of which exist in this system. The test baseline for all items is commit `b3702ef`; any change to that baseline requires the affected items to be re-tested.

#### 2.4 Test Item Interfaces

The items are verified through their public interfaces, which are documented in SAD §4.3. The interfaces below are the contract each test case relies on; a change to any of them invalidates the corresponding test case and requires it to be updated in the same change.

| Test item | Interfaces exercised by the test cases |
| :--- | :--- |
| T1 Inventory | `Inventory()`, `level`, `add`, `remove`, `register_warehouse`, `total_in_warehouse`, `set_policy`, `get_policy`, `needs_reorder`, `is_excess`, `reorder_suggestions`, `snapshot`, `StockPolicy` |
| T2 Order Manager | `OrderManager(inventory)`, `create`, `get`, `try_fulfil`, `process_open`, `cancel`, `by_status`, `OrderStatus` |
| T3 Shipment Manager | `Supplier(...)`, `ShipmentManager(inventory, rng)`, `add_supplier`, `dispatch`, `process_arrivals`, `in_transit`, `delayed`, `ShipmentStatus`, `Shipment.days_late` |
| T4 Analytics | `find_delayed_shipments`, `find_stockouts`, `find_low_stock`, `find_excess`, `order_metrics`, `build_report`, `format_report` |
| T5 Simulation Engine | `Simulation(seed, reorder_point, max_level)`, `add_supplier`, `add_warehouse`, `set_policy`, `add_stock`, `schedule_order`, `step`, `run`, `final_summary`, `build_demo` |
| T6 CLI | `python -m scm_sim --days N --seed S`, `--help`, process exit code |
| T7 CI Pipeline | GitHub Actions job `test` on `ubuntu-latest` with Python 3.11; GitHub branch protection settings for `main` |