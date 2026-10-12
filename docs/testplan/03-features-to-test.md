### 3. Features to Be Tested

This section enumerates every feature of the Supply Chain Management Simulator that is to be tested, mapped to the requirement identifiers defined in the Software Requirements Specification. It is the authoritative list of what this Test Plan covers: a requirement that appears in this section is in scope for verification, and a requirement that does not appear here is either out of scope (Test Plan §4) or an objective rather than a testable requirement.

The identifiers below are taken from the Requirements Registry (`docs/requirements-registry.md`) and match SRS §4, §5 and §5.1 exactly. Thirty-two requirements are in scope: 20 functional, 5 non-functional and 7 security requirements, supported by the two security objectives SCM-SO-1 and SCM-SO-2.

#### 3.1 Feature Group A — Inventory Management

Tests the behaviour of the Inventory component (`src/scm_sim/inventory.py`), which owns all stock state.

| Req ID | Feature to be tested | Verifiable behaviour | Component | Test level | Test case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-F-001 | Stock tracking and validated mutation | Quantity is tracked per (warehouse, SKU) pair; `add` and `remove` reject quantities $\le 0$ with `ValueError`; removing more than available raises `InsufficientStockError` and leaves the level unchanged; a never-stocked item reads as level 0. | Inventory | Unit | TC-INV-01 |
| SCM-F-002 | Warehouse capacity enforcement | `register_warehouse` rejects a capacity $\le 0$ with `ValueError`; an `add` that would push the warehouse total past its capacity raises `CapacityExceededError` and leaves stock unchanged; an `add` reaching exactly the capacity succeeds; an unregistered warehouse has unlimited capacity. | Inventory | Unit | TC-INV-01 |
| SCM-F-003 | Per-item stock policy | `StockPolicy` defaults to reorder point 20, reorder quantity 100 and max level 500; negative values and `max_level < reorder_point` are rejected with `ValueError`; `needs_reorder` is true when level $\le$ reorder point; `is_excess` is true only when level $>$ max level. | Inventory | Unit | TC-INV-02 |
| SCM-F-004 | Reorder suggestions and snapshot | `reorder_suggestions()` returns only tracked items at or below their reorder point, each with the policy's reorder quantity, in sorted order; `snapshot()` returns every level as an independent copy that cannot alter internal state. | Inventory | Unit | TC-INV-02 |

#### 3.2 Feature Group B — Order Management

Tests the behaviour of the Order Manager component (`src/scm_sim/orders.py`), which owns the customer order book.

| Req ID | Feature to be tested | Verifiable behaviour | Component | Test level | Test case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-F-010 | Order creation and identifier sequence | `create` rejects a quantity $\le 0$ with `ValueError`; identifiers are allocated sequentially as `ORD-0001`, `ORD-0002`, …; a new order has status `PENDING` and records its creation day. | Order Manager | Unit | TC-ORD-01 |
| SCM-F-011 | Fulfilment and back-ordering | An order is fulfilled in full when stock $\ge$ quantity, with stock reduced, status `FULFILLED` and the fulfilment day recorded; otherwise it becomes `BACKORDERED` with stock unchanged; there is no partial fulfilment. | Order Manager | Unit | TC-ORD-01 |
| SCM-F-012 | Oldest-first retry of open orders | `process_open` retries all `PENDING` and `BACKORDERED` orders in order of creation day and then identifier, and returns only the orders newly fulfilled on this pass. | Order Manager | Unit | TC-ORD-02 |
| SCM-F-013 | Cancellation, lookup and filtering | `cancel` rejects an already `FULFILLED` order with `ValueError` and an unknown identifier with `KeyError`; `get` raises `KeyError` for an unknown identifier; `by_status` returns exactly the orders in the requested status. | Order Manager | Unit | TC-ORD-02 |

#### 3.3 Feature Group C — Shipment and Supplier Management

Tests the behaviour of the Shipment Manager component (`src/scm_sim/shipments.py`), which owns suppliers and inbound shipments.

| Req ID | Feature to be tested | Verifiable behaviour | Component | Test level | Test case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-F-020 | Supplier registration and validation | `Supplier` rejects `lead_time_days < 0` and a `reliability` outside $[0.0, 1.0]$ with `ValueError`; `add_supplier` rejects a duplicate identifier with `ValueError` and an unknown identifier on dispatch with `KeyError`. | Shipment Manager | Unit | TC-SHP-01 |
| SCM-F-021 | Dispatch and identifier sequence | `dispatch` creates a shipment with status `IN_TRANSIT`, identifier `SHP-0001`, `SHP-0002`, …, and `expected_day = day + supplier.lead_time_days`; a quantity $\le 0$ raises `ValueError`; `in_transit()` returns only shipments not yet delivered. | Shipment Manager | Unit | TC-SHP-01 |
| SCM-F-022 | Stochastic delay model | When no explicit delay is given, a PRNG draw exceeding the supplier's reliability adds `rng.randint(1, 3)` days to the arrival day and a draw within reliability adds none; `reliability = 1.0` is never delayed; an explicit `delay` overrides the random draw. | Shipment Manager | Unit | TC-SHP-02 |
| SCM-F-023 | Arrival processing and late detection | Every `IN_TRANSIT` shipment whose arrival day is reached is delivered, adding stock through `Inventory.add`, setting status `DELIVERED` and recording the actual day; a shipment is never delivered before its arrival day; `delayed(current_day)` returns shipments whose `days_late` exceeds 0, whether still in transit or already delivered late. | Shipment Manager | Unit / Integration | TC-SHP-02, TC-SIM-01 |

#### 3.4 Feature Group D — Analytics and Reporting

Tests the behaviour of the Analytics component (`src/scm_sim/analytics.py`), the read-only observation layer owned by the Dev Lead.

| Req ID | Feature to be tested | Verifiable behaviour | Component | Test level | Test case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-F-030 | Delayed-shipment detection | `days_late` is the delivered shipment's actual day, or the current day while in transit, minus the expected day; only `days_late > 0` is reported; on-time and early arrivals are excluded; the result is ordered most-late first with a deterministic tie-break. | Analytics | Unit | TC-ANA-01 |
| SCM-F-031 | Inventory health classification | A stockout is a quantity of exactly 0; low stock is $0 < qty \le$ reorder point (20 included, 0 and 21 excluded); excess is $qty >$ max level (500 excluded, 501 included) and reports the surplus; each class is returned sorted, and caller-supplied thresholds override the 20 / 500 defaults. | Analytics | Unit | TC-ANA-01 |
| SCM-F-032 | Order metrics and fill rate | Status counts for `PENDING`, `FULFILLED`, `BACKORDERED` and `CANCELLED` are correct and `total` equals the list length; fill rate is $\text{round}(\text{fulfilled} \div (\text{total} − \text{cancelled}),\ 2)$; it is 0.0 when there are no eligible orders; enumeration members and plain strings are accepted, including mixed in one list. | Analytics | Unit | TC-ANA-02 |
| SCM-F-033 | Report composition and formatting | `build_report` returns a dictionary whose key set is exactly `{day, delayed_shipments, stockouts, low_stock, excess, orders}` and forwards caller thresholds; `format_report` emits the day header, one counted section per key, one line per item, and the text `No issues` for every empty section. | Analytics | Unit | TC-ANA-02 |

#### 3.5 Feature Group E — Simulation Engine and Command-Line Interface

Tests the orchestration layer and its user-facing entry point.

| Req ID | Feature to be tested | Verifiable behaviour | Component | Test level | Test case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-F-040 | Scenario configuration | Suppliers, warehouses with capacity, per-item policies linked to a supplier, initial stock and orders scheduled for future days can all be configured; a day in the past, a quantity $\le 0$ and an unknown warehouse are each rejected with the appropriate exception. | Simulation Engine | System | TC-SIM-02 |
| SCM-F-041 | Daily time-step and report retention | `step` advances the day counter and executes arrivals, today's orders, back-order retry, replenishment and report construction in that fixed order; `run(days)` returns one report per day and `run(-1)` raises `ValueError`. | Simulation Engine | Integration | TC-SIM-01 |
| SCM-F-042 | Automatic replenishment | Exactly one replenishment is dispatched per item that needs reorder while nothing is in transit for it; the quantity is trimmed so that on-hand plus in-transit stock never exceeds the warehouse capacity. | Simulation Engine | Integration | TC-SIM-01 |
| SCM-F-043 | Command-line interface | `python -m scm_sim --days N --seed S` runs the demo, prints the day-by-day log and the final report, and exits with code 0; `--days` below 1 produces a usage error with exit code 2. | CLI | System | TC-SIM-02 |

#### 3.6 Feature Group F — Non-Functional and Cross-Cutting Features

| Req ID | Feature to be tested | Verifiable behaviour | Component | Test level | Test case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-NF-001 | Performance | A 365-day run of the demo scenario and the 10-day CLI demo including interpreter start-up each complete within 1 s. | Simulation Engine, CLI | Performance (manual) | TC-PERF-01 |
| SCM-NF-002 | Reproducibility | The same seed with the same scenario produces identical daily reports and identical output on every run and on every host. | Simulation Engine, Analytics | Reliability (automated + manual) | TC-REP-01 |
| SCM-NF-003 | Coverage and pre-merge gate | The CI `test` job reports $\ge 90\%$ line coverage of `scm_sim` on every push to `main` and every pull request, and all tests pass before a merge is permitted. | CI Pipeline | Maintainability (automated) | TC-COV-01 |
| SCM-NF-004 | Portability and dependency constraint | The simulator runs on Python $\ge$ 3.11 on Windows, Linux and macOS using only the standard library at runtime, with third-party packages required for testing alone. | All modules, `requirements.txt` | Portability (automated + manual) | TC-COV-01 |
| SCM-NF-005 | Usability of the demo | A new user runs the demo with one documented command; every report section shows a count and prints "No issues" when empty; `--help` lists all options. | CLI, Analytics | System | TC-SIM-02 |

#### 3.7 Feature Group G — Security

The two security objectives are not themselves testable; the features tested are the security requirements through which they are achieved.

| Req ID | Feature to be tested | Verifiable behaviour | Component | Test level | Test case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-SO-1 | *Objective:* integrity of simulation data | Achieved through SCM-SR-001 to SCM-SR-004 and SCM-SR-007 below; verified by TC-SEC-01 across all domain modules. | Inventory, Order Manager, Shipment Manager | Security | TC-SEC-01 |
| SCM-SO-2 | *Objective:* integrity and traceability of the codebase | Achieved through SCM-SR-005 and SCM-SR-006 below; verified by TC-SEC-02 against the repository and its branch-protection settings. | CI Pipeline, repository | Security (process) | TC-SEC-02 |
| SCM-SR-001 | Input validation before state change | Every public operation rejects invalid arguments — quantities $\le 0$, lead time $< 0$, reliability outside $[0,1]$, invalid policies, capacity $\le 0$, past days — with `ValueError` raised **before** any state changes. | All domain modules, Simulation | Security | TC-SEC-01 |
| SCM-SR-002 | Stock integrity invariants | Stock never falls below 0 or rises above a registered warehouse capacity; a violating operation raises `InsufficientStockError` or `CapacityExceededError` and leaves state unchanged. | Inventory | Security | TC-SEC-01 |
| SCM-SR-003 | Guarded order status transitions | A `FULFILLED` order cannot be cancelled; `FULFILLED` and `CANCELLED` orders are never re-processed by a retry pass. | Order Manager | Security | TC-SEC-01 |
| SCM-SR-004 | Rejection of unknown references | A reference to an unknown supplier, warehouse or order raises `KeyError`, and nothing is created implicitly as a side effect. | Order Manager, Shipment Manager, Simulation | Security | TC-SEC-01 |
| SCM-SR-005 | Protected `main` branch | A pull request is required to change `main`; at least one approval from a non-author is needed; the required `test` check must pass; the branch must be up to date; force pushes and deletions are blocked; the rules apply to administrators. | Repository, CI Pipeline | Security (process) | TC-SEC-02 |
| SCM-SR-006 | No secrets and no runtime dependencies | The repository contains no secrets or credentials; the simulator makes no network calls and has no runtime third-party dependency, with `requirements.txt` holding test-only packages. | All modules, repository | Security (process) | TC-SEC-02 |
| SCM-SR-007 | Returned data is a copy | Data returned to callers — snapshots and reports — is an independent copy, so modifying it cannot change internal state. | Inventory, Analytics | Security | TC-SEC-01 |

#### 3.8 Summary of Feature Coverage

| Feature group | Functional | Non-functional | Security | Total |
| :--- | :--- | :--- | :--- | :--- |
| A — Inventory Management | 4 | 0 | 0 | 4 |
| B — Order Management | 4 | 0 | 0 | 4 |
| C — Shipment and Supplier Management | 4 | 0 | 0 | 4 |
| D — Analytics and Reporting | 4 | 0 | 0 | 4 |
| E — Simulation Engine and CLI | 4 | 0 | 0 | 4 |
| F — Non-Functional and Cross-Cutting | 0 | 5 | 0 | 5 |
| G — Security | 0 | 0 | 7 requirements (+ 2 objectives) | 7 |
| **Total** | **20** | **5** | **7** | **32** |

All 32 requirements of the SRS are assigned to a feature group and to at least one test case. The 15 test cases of Test Plan §13 therefore between them cover every requirement in the registry; none is left unverified and none is verified without a requirement to justify it.