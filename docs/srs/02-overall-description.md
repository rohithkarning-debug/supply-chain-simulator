## 2. Overall Description

### 2.1 Product Perspective

The Supply Chain Management Simulator is a **new, self-contained Python program**. It is not part of a larger product and does not connect to any external system. It is distributed as the Python package `scm_sim` (source in `src/scm_sim/`) and is started from a terminal.

Internally the product is organised as a layered set of modules inside one package:

| Layer | Component (file) | Role |
|---|---|---|
| Presentation | CLI (`__main__.py`) | Parses `--days` and `--seed`, runs the demo, prints the day-by-day log and the final report |
| Orchestration | Simulation Engine (`simulator.py`) | Holds the scenario, advances time one day per step, and calls the domain modules in a fixed order |
| Domain | Inventory (`inventory.py`), Order Manager (`orders.py`), Shipment Manager (`shipments.py`) | Each owns its own state and business rules; Order Manager and Shipment Manager change stock only through the shared Inventory |
| Analytics | Analytics (`analytics.py`) | Pure functions that read plain data (stock snapshot, shipments, orders) and produce reports without changing any state |

Development is supported by a **CI Pipeline** (`.github/workflows/ci.yml`) that runs the full pytest suite on every push to `main` and every pull request.

Goods flow through the simulated network as follows:

```
Supplier --(shipment, lead time + possible delay)--> Warehouse --(customer order)--> Customer
```

### 2.2 Major Product Functions

The system shall provide the following major functions (detailed in §4):

1. **Inventory management** (§4.1): track stock per (warehouse, SKU), enforce warehouse capacity, apply per-item stock policies, suggest reorders and provide stock snapshots.
2. **Order management** (§4.2): create customer orders, fulfil them in full or back-order them, retry back-orders oldest first, cancel orders and list orders by status.
3. **Shipment and supplier management** (§4.3): register suppliers, dispatch shipments, model delays from supplier reliability using a seeded random generator, deliver arrivals into inventory and list delayed shipments.
4. **Analytics and reporting** (§4.4): detect delayed shipments, stockouts, low stock and excess inventory; compute order metrics and fill rate; build and format a daily report.
5. **Simulation engine and CLI** (§4.5): configure a scenario, advance it one day at a time in a fixed event order, replenish stock automatically, keep the daily report history, and run a built-in demo from the command line.

### 2.3 User Classes and Characteristics

| User class | Description | Technical expertise | Main interactions |
|---|---|---|---|
| **Supply Chain Analyst** (primary) | Configures a scenario, runs the simulation and reads reports to find delays, stockouts and excess inventory | Basic Python and command-line use | Runs `python -m scm_sim`, or builds a `Simulation` in Python and calls `run(days)` and `final_summary()` |
| **Instructor / Evaluator** | Runs the CLI demo and the test suite to assess the system against the problem statement | Comfortable with a terminal and pytest | Runs `python -m scm_sim --days 10 --seed 42` and `pytest -v --cov=scm_sim` |
| **Developer** (team member) | Extends modules, writes tests, opens and reviews pull requests | Python 3.11, pytest, Git/GitHub | Edits `src/scm_sim/`, runs tests locally, pushes feature branches, uses CI results |
| **System timer** (secondary actor) | The daily step. Each step triggers arrivals, order fulfilment, back-order retries, replenishment and reporting | n/a (part of the system) | `Simulation.step()` |

The following are **simulated entities, not human actors**: **Supplier** (sends replenishment shipments), **Warehouse** (stores stock up to its capacity) and **Customer** (places orders, identified by IDs such as `C-ACME`).

### 2.4 Operating Environment

| Item | Requirement |
|---|---|
| Runtime | Python 3.11 or later (developed and tested with Python 3.11.9) |
| Operating systems | Windows 10/11, Linux and macOS |
| Runtime libraries | Python standard library only (`dataclasses`, `enum`, `random`, `argparse`, `typing`) |
| Test tools | pytest ≥ 8.0 and pytest-cov ≥ 5.0 (listed in `requirements.txt`; not needed to run the simulator) |
| CI environment | GitHub Actions, job `test` on `ubuntu-latest` with Python 3.11 |
| Hardware | Any machine able to run Python 3.11; no special hardware |
| Network | None at runtime |

### 2.5 Design and Implementation Constraints

1. **Standard library only at runtime.** No third-party packages may be imported by `src/scm_sim/`; pytest and pytest-cov are test-only dependencies.
2. **In-memory data.** All state (stock, policies, orders, shipments, reports) lives in Python objects for the length of one run. There is no file, database or network storage.
3. **Deterministic with a seed.** The only source of randomness is one `random.Random(seed)` instance passed to the Shipment Manager. The same seed and scenario must produce identical results on every run and machine.
4. **Discrete daily time step.** Time advances in whole days; there is no continuous or real-time clock.
5. **Package layout.** Source code lives in `src/scm_sim/` and tests in `tests/`. There is no packaging configuration (`pyproject.toml`), so the CLI is run from `src/` or with `PYTHONPATH=src`.
6. **Team and process.** The system is built by a 4-person team within one semester. Each module has one owner. All changes reach `main` only through a reviewed pull request with a passing `test` CI check.
7. **Python language level.** Code uses type hints and dataclasses compatible with Python 3.11.

### 2.6 Assumptions and Dependencies

**Assumptions**

1. Each (warehouse, SKU) item is replenished by **exactly one supplier**, assigned when its stock policy is set.
2. **Delays only make shipments later.** A shipment never arrives before its expected day; a delay adds 1–3 days.
3. **Customer demand is known in advance.** Orders are scheduled for specific future days before or during the run; the system does not forecast demand.
4. Orders are fulfilled **in full or not at all** (no partial shipments to customers).
5. Suppliers have unlimited stock; only lead time and reliability limit them.
6. Stock moves only between a supplier and a warehouse, and from a warehouse to a customer; there are no transfers between warehouses.
7. Capacity is measured in units summed over all SKUs in a warehouse; all units take the same space.

**Dependencies**

1. A Python 3.11+ interpreter on the user's machine.
2. pytest and pytest-cov for running the automated tests.
3. GitHub and GitHub Actions for version control, code review and CI.
4. The companion documents: SAD v1.0 (design) and Test Plan v1.0 (verification), and the requirements registry `docs/requirements-registry.md`.
