### 3.5 Architecture Pattern and Rationale

#### 3.5.1 Chosen Pattern: Layered, Modular Architecture in One Package

The simulator uses a **layered, modular architecture** inside a single Python package (`scm_sim`). Each layer has one kind of responsibility, and each module inside a layer owns its own state and rules behind a small public interface.

| Layer | Component(s) | Responsibility | May depend on |
|---|---|---|---|
| Presentation | CLI (`__main__.py`) | Parse command-line options; print the day-by-day log and the final report | Orchestration |
| Orchestration | Simulation Engine (`simulator.py`) | Hold the scenario; run the discrete daily time step; call the domain modules in a fixed order; keep the report history | Domain, Analytics |
| Domain | Inventory (`inventory.py`), Order Manager (`orders.py`), Shipment Manager (`shipments.py`) | Own supply-chain state (stock, orders, shipments) and enforce its rules | Inventory only |
| Analytics | Analytics (`analytics.py`) | Pure functions that turn a stock snapshot, shipments and orders into a report; never change state | Nothing |

**Dependency rule.** Dependencies point one way: **CLI → Simulation Engine → domain modules and Analytics**. Within the domain layer, the Order Manager and the Shipment Manager depend only on Inventory, and never on each other. Analytics depends on nothing in the package; it reads plain data handed to it. There are no cyclic imports, and the source code confirms this (`orders.py` and `shipments.py` import only `scm_sim.inventory`; `analytics.py` imports no `scm_sim` module).

**Time model.** Inside the orchestration layer the system is a **discrete time-step simulation**: time advances in whole days, and every day runs the same five stages in the same order (arrivals → today's orders → back-order retry → replenishment → report; see §3.4.1 and §4.1).

**Shared state.** The only state shared between domain modules is the single `Inventory` object, passed to the `OrderManager` and `ShipmentManager` constructors. The Simulation Engine decides *when* each manager reads or changes it.

#### 3.5.2 Rationale

| Driver | How the pattern addresses it |
|---|---|
| **Parallel team development** (four people, one module each) | Each domain and analytics module was specified with a fixed interface, built and unit-tested on its own feature branch, and merged independently (PRs #2, #3, #5, #6). The Simulation Engine was integrated last (PR #7) without changing any other module. |
| **Testability** (SCM-NF-003) | Lower layers do not depend on higher ones, so every module is tested in isolation: Inventory with no other module, the managers with a real `Inventory`, Analytics with simple stand-in objects. Integration and CLI behaviour are tested once in `test_simulator.py`. Result: 73 tests, 97% coverage. |
| **Correct event ordering** (SCM-F-041) | Only `Simulation.step()` calls the domain modules during a run, so the order of events within a day is defined, documented and tested in one place. |
| **Determinism and reproducibility** (SCM-NF-002) | Randomness is confined to one seeded `random.Random` in the Shipment Manager, and every loop iterates in a sorted or insertion order. A discrete time step has no timing or threading effects. |
| **Data integrity** (SCM-SO-1, SCM-SR-001, SCM-SR-002) | Each domain module validates input and protects its own invariants, and Analytics is read-only and receives a copy of stock. A bug in reporting cannot corrupt simulation state. |
| **Simplicity and portability** (SCM-NF-004) | One package, standard library only, no services to deploy. It runs anywhere Python 3.11 runs. |
| **Understandability for evaluation** | The layers correspond one-to-one with the problem statement: manage inventory, orders and shipments (domain), simulate movement over time (orchestration), identify delays, stockouts and excess (analytics). |

#### 3.5.3 Alternatives Considered and Rejected

| Alternative | Advantages | Reasons for rejection |
|---|---|---|
| **(a) Event-driven / message-queue simulation** (e.g. a discrete-event library such as SimPy, with events scheduled at arbitrary times) | More realistic timing (events within a day, continuous lead times); scales to many concurrent processes | Adds a third-party runtime dependency, which violates the standard-library-only constraint. Ordering of simultaneous events becomes implicit, which makes tests harder to write and read and makes deterministic results harder to guarantee. Daily granularity is sufficient for the problem statement. |
| **(b) Web application with a database** (REST back end, persistent storage, browser front end) | Multi-user access, persistent scenarios, graphical dashboards | Out of scope for a simulator. Adds deployment, configuration and a large security surface (authentication, injection, network exposure) with no benefit to the problem statement. Much slower to test, and data would no longer be reproducible from a seed alone. |

#### 3.5.4 Consequences and Trade-offs

**Positive**

- Modules are small and independently testable; each team member could own and defend one module.
- Behaviour is fully reproducible from the seed and the scenario.
- No installation beyond Python is needed to run the simulator.

**Negative / accepted trade-offs** (tracked in §4.6 Open Issues)

- **Coarse time.** All events in a day happen in a fixed order rather than at specific times; for example, today's new orders are served before older back-orders are retried.
- **One threshold in Analytics.** Analytics reports use one global low-stock and excess threshold, while Inventory supports per-item policies, because the Analytics interface was fixed before integration.
- **Orchestrator responsibility.** Some safeguards live only in the Simulation Engine (trimming reorders to capacity, rejecting unknown warehouses); code that uses the domain modules directly does not get them.
- **In-memory only.** Scenarios must be built in Python code; there is no file input, and results are not saved after the program ends.
