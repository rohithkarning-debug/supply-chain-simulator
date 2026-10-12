### 3.8 Traceability to Requirements

This section maps every requirement defined in the Software Requirements Specification to the architectural component that implements it, using the component names defined in SAD §3.3 and listed in SAD §3.4. It is the design-side counterpart of the Requirements Traceability Matrix in SRS §8: SRS §8 traces every requirement to its test case, and this section traces every requirement to the code that satisfies it. Together they close the loop from requirement to design to verification, and a requirement that appears in neither table is treated as unimplemented.

#### 3.8.1 Functional Requirements

| Req ID | Requirement short | Primary component | Supporting component(s) | Design section | Test case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-F-001 | Stock per (warehouse, SKU), validated add and remove | **Inventory** (`scm_sim.inventory`) | – | SAD §3.4.1, §4.3.1 | TC-INV-01 |
| SCM-F-002 | Warehouse capacity with `CapacityExceededError` | **Inventory** (`scm_sim.inventory`) | Simulation Engine (registers capacities) | SAD §3.4.1, §4.3.1 | TC-INV-01 |
| SCM-F-003 | Per-item stock policy, `needs_reorder`, `is_excess` | **Inventory** (`StockPolicy`) | Analytics (reuses the same default thresholds) | SAD §3.4.1, §4.3.1 | TC-INV-02 |
| SCM-F-004 | Sorted reorder suggestions and stock snapshot | **Inventory** (`scm_sim.inventory`) | Analytics (consumes the snapshot) | SAD §3.4.1, §4.3.1 | TC-INV-02 |
| SCM-F-010 | Create orders with sequential `ORD-0001…` IDs | **Order Manager** (`scm_sim.orders`) | – | SAD §3.4.2, §4.3.2 | TC-ORD-01 |
| SCM-F-011 | Fulfil in full or back-order, no partial fulfilment | **Order Manager** (`scm_sim.orders`) | Inventory (stock check and deduction) | SAD §3.4.2, §4.3.2 | TC-ORD-01 |
| SCM-F-012 | Retry open orders oldest-first | **Order Manager** (`scm_sim.orders`) | Simulation Engine (invokes the retry pass) | SAD §3.4.2, §4.3.2 | TC-ORD-02 |
| SCM-F-013 | Cancel, look up by ID, list by status | **Order Manager** (`scm_sim.orders`) | – | SAD §3.4.2, §4.3.2 | TC-ORD-02 |
| SCM-F-020 | Register suppliers with lead time and reliability | **Shipment Manager** (`scm_sim.shipments`) | – | SAD §3.4.3, §4.3.3 | TC-SHP-01 |
| SCM-F-021 | Dispatch shipments with sequential `SHP-0001…` IDs | **Shipment Manager** (`scm_sim.shipments`) | – | SAD §3.4.3, §4.3.3 | TC-SHP-01 |
| SCM-F-022 | Model stochastic delays from supplier reliability | **Shipment Manager** (`scm_sim.shipments`) | Simulation Engine (supplies the seeded `random.Random`) | SAD §3.4.3, §4.3.3 | TC-SHP-02 |
| SCM-F-023 | Deliver arrivals; list shipments with days late > 0 | **Shipment Manager** (`scm_sim.shipments`) | Inventory (receives the delivered stock) | SAD §3.4.3, §4.3.3 | TC-SHP-02 |
| SCM-F-030 | Report delayed shipments with days late, worst first | **Analytics** (`scm_sim.analytics`) | Shipment Manager (supplies `expected_day` / `actual_day`) | SAD §3.4.4, §4.3.4 | TC-ANA-01 |
| SCM-F-031 | Report stockouts, low stock and excess with surplus | **Analytics** (`scm_sim.analytics`) | Inventory (supplies the stock snapshot) | SAD §3.4.4, §4.3.4 | TC-ANA-01 |
| SCM-F-032 | Order metrics per status and fill rate | **Analytics** (`scm_sim.analytics`) | Order Manager (supplies the orders) | SAD §3.4.4, §4.3.4 | TC-ANA-02 |
| SCM-F-033 | Build the daily report and format it as readable text | **Analytics** (`scm_sim.analytics`) | Simulation Engine and CLI (consume the report) | SAD §3.4.4, §4.3.4 | TC-ANA-02 |
| SCM-F-040 | Configure a scenario | **Simulation Engine** (`scm_sim.simulator`) | Inventory, Shipment Manager, Order Manager | SAD §3.4.1, §4.3.1 | TC-SIM-02 |
| SCM-F-041 | Advance one day in the fixed order, keep every report | **Simulation Engine** (`scm_sim.simulator`) | Analytics (builds the report at step 5) | SAD §3.4.1, §4.1 | TC-SIM-01 |
| SCM-F-042 | Automatic replenishment trimmed to capacity | **Simulation Engine** (`scm_sim.simulator`) | Inventory (`reorder_suggestions`), Shipment Manager (`dispatch`) | SAD §3.4.1, §4.1 | TC-SIM-01 |
| SCM-F-043 | Command-line interface, exit code 0 | **CLI** (`scm_sim.__main__`) | Simulation Engine (`build_demo`, `run`) | SAD §3.4.1, §4.5 | TC-SIM-02 |

#### 3.8.2 Non-Functional Requirements

| Req ID | Requirement short | Primary component | Supporting component(s) | Design section | Test case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| SCM-NF-001 | 365-day run and 10-day CLI demo each in $\le 1.0$ s | **Simulation Engine** (`scm_sim.simulator`) | CLI (`scm_sim.__main__`), whole `scm_sim` package | SAD §3.1, §3.6 | TC-PERF-01 |
| SCM-NF-002 | Same seed and scenario give identical output | **Simulation Engine** (`scm_sim.simulator`) | Shipment Manager (injected PRNG), Analytics (deterministic ordering) | SAD §3.6 | TC-REP-01 |
| SCM-NF-003 | $\ge 90\%$ line coverage, all tests pass before merge | **CI Pipeline** (`.github/workflows/ci.yml`) | All five source modules | SAD §3.4.1, §3.6 | TC-COV-01 |
| SCM-NF-004 | Runs on Python $\ge$ 3.11 on Windows, Linux and macOS, standard library only | All five source modules | CI Pipeline (verifies one of the three platforms automatically) | SAD §3.6 | TC-COV-01 |
| SCM-NF-005 | One documented command; counts and "No issues" in every report section; `--help` | **CLI** (`scm_sim.__main__`) | Analytics (`format_report`) | SAD §4.5 | TC-SIM-02 |

#### 3.8.3 Security Requirements

The two security objectives are architectural in nature and are realised through the components and controls below rather than implemented by any single component.

| Req ID | Requirement short | Primary component(s) | Design section | Test case |
| :--- | :--- | :--- | :--- | :--- |
| SCM-SO-1 | **Objective:** integrity of simulation data | Inventory, Order Manager, Shipment Manager (all three enforce their invariants) | SAD §3.4.1, §3.4.2, §3.4.3, §4.4 | TC-SEC-01 |
| SCM-SO-2 | **Objective:** integrity and traceability of the codebase | CI Pipeline and the protected-`main` workflow; Developer (authoring and reviewing pull requests) | SAD §3.9 | TC-SEC-02 |
| SCM-SR-001 | Validate input on every public operation before mutating state | Inventory, Order Manager, Shipment Manager, Simulation Engine | SAD §4.4 | TC-SEC-01 |
| SCM-SR-002 | Stock never below 0 or above a registered capacity | Inventory | SAD §3.4.1, §4.4 | TC-SEC-01 |
| SCM-SR-003 | Guarded order status transitions | Order Manager | SAD §3.4.2, §4.4 | TC-SEC-01 |
| SCM-SR-004 | Unknown supplier, warehouse or order references raise `KeyError` | Order Manager, Shipment Manager, Simulation Engine | SAD §4.4 | TC-SEC-01 |
| SCM-SR-005 | `main` is protected: PR, non-author approval, passing `test` check, no force pushes | CI Pipeline and the repository branch-protection settings | SAD §3.9 | TC-SEC-02 |
| SCM-SR-006 | No secrets; no network calls; no runtime third-party dependencies | All five source modules (`requirements.txt`) | SAD §3.6, §3.9 | TC-SEC-02 |
| SCM-SR-007 | Returned data is a copy; mutating it cannot change internal state | Inventory (`snapshot`), Analytics (`build_report`) | SAD §3.4.1, §3.4.4 | TC-SEC-01 |

#### 3.8.4 Reverse Coverage (Component to Requirements)

| Component | Requirements implemented | Requirements it supports but does not own |
| :--- | :--- | :--- |
| **Inventory** | SCM-F-001, SCM-F-002, SCM-F-003, SCM-F-004 | SCM-SR-002, SCM-SR-007 |
| **Order Manager** | SCM-F-010, SCM-F-011, SCM-F-012, SCM-F-013 | SCM-SR-003, SCM-SR-004 |
| **Shipment Manager** | SCM-F-020, SCM-F-021, SCM-F-022, SCM-F-023 | SCM-SR-004, SCM-SR-006 |
| **Analytics** | SCM-F-030, SCM-F-031, SCM-F-032, SCM-F-033 | SCM-SR-007, SCM-NF-002, SCM-NF-005 |
| **Simulation Engine** | SCM-F-040, SCM-F-041, SCM-F-042 | SCM-SR-001, SCM-NF-001, SCM-NF-002 |
| **CLI** | SCM-F-043 | SCM-NF-005 |
| **CI Pipeline** | SCM-NF-003 | SCM-SR-005, SCM-SR-006, SCM-NF-004 |

Every one of the 32 requirement IDs (20 functional, 5 non-functional, 7 security) appears in exactly one "primary component" cell above, and every component in the component diagram of SAD §3.3 implements at least one requirement. No component is orphaned and no requirement is unimplemented.