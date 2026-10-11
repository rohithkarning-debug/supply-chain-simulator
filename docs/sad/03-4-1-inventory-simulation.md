### 3.4 Component Descriptions

Each component below is described by its responsibility, the interface it provides and the interfaces it requires, its internal data, its key design decisions, and the requirements and tests it traces to. Detailed call-by-call API definitions are in §4.3.

#### 3.4.1 Inventory, Simulation Engine, CLI and CI Pipeline

##### Inventory

| Item | Description |
|---|---|
| File / owner | `src/scm_sim/inventory.py` / Rohith Karning |
| Layer | Domain |
| Responsibility | Single source of truth for stock: quantity per (warehouse, SKU), total capacity per warehouse, and a stock policy per item. Decides whether an item needs a reorder or holds excess stock. |
| Provided interface | `Inventory`: `level`, `add`, `remove`, `is_stockout`, `register_warehouse`, `total_in_warehouse`, `set_policy`, `get_policy`, `needs_reorder`, `is_excess`, `reorder_suggestions`, `snapshot`. `StockPolicy` (frozen dataclass). Exceptions `InsufficientStockError`, `CapacityExceededError`. |
| Required interface | None. Inventory imports no other `scm_sim` module. |
| Used by | Order Manager (`level`, `remove`), Shipment Manager (`add`), Simulation Engine (set-up, `reorder_suggestions`, `total_in_warehouse`, `snapshot`) |
| Requirements | SCM-F-001, SCM-F-002, SCM-F-003, SCM-F-004; supports SCM-SR-001, SCM-SR-002, SCM-SR-007 |
| Tests | `tests/test_inventory.py` (20 test functions, 23 test runs including parametrised cases); TC-INV-01, TC-INV-02 |

**Internal data**

| Attribute | Type | Content |
|---|---|---|
| `_stock` | `dict[(warehouse, sku), int]` | Current quantity of each item. A key is created the first time the item is stocked and kept even when its quantity falls to 0, so a stockout stays visible in snapshots. |
| `_capacity` | `dict[warehouse, int]` | Capacity of each registered warehouse. A warehouse with no entry has unlimited capacity. |
| `_policies` | `dict[(warehouse, sku), StockPolicy]` | Explicit policies. `get_policy` returns `StockPolicy()` (20 / 100 / 500) for items without one. |

**Key design decisions**

1. **Check before change.** `add` validates the quantity and the capacity, and `remove` validates the quantity and the available stock, *before* updating `_stock`. A rejected call therefore leaves stock exactly as it was (SCM-SR-002).
2. **Capacity is total units per warehouse.** `add` compares `total_in_warehouse(warehouse) + qty` with the capacity, so all SKUs share one limit. Adding exactly up to capacity is allowed.
3. **Immutable policies.** `StockPolicy` is a frozen dataclass that validates itself in `__post_init__` (no negative values; `max_level ≥ reorder_point`). A policy is changed by replacing it with `set_policy`, never by editing it.
4. **Deterministic suggestions.** `reorder_suggestions` covers every *tracked* item (stocked at least once, or with a policy) and is sorted by warehouse and then SKU. This makes replenishment order, and therefore shipment IDs, reproducible (SCM-NF-002).
5. **Copies out, never references.** `snapshot()` returns `dict(self._stock)`, a new dictionary, so readers such as Analytics cannot change stock (SCM-SR-007).

**Constraints and limitations.** Capacity is enforced only when stock is added; registering a capacity below the stock already held is accepted. Warehouses and SKUs are not registered centrally, so an unknown warehouse simply has 0 stock and no capacity limit at this level. The Simulation Engine adds the warehouse-existence check (SCM-SR-004).

##### Simulation Engine

| Item | Description |
|---|---|
| File / owner | `src/scm_sim/simulator.py` / Rohith Karning |
| Layer | Orchestration |
| Responsibility | Holds one scenario and advances it one day at a time. Wires Inventory, Order Manager, Shipment Manager and Analytics together, controls the order of events inside a day, replenishes stock automatically and keeps the history of daily reports. Provides the ready-made demo scenario. |
| Provided interface | `Simulation`: `add_supplier`, `add_warehouse`, `set_policy`, `add_stock`, `schedule_order`, `step`, `run`, `final_summary`, `all_orders`; attributes `day`, `history`, `logs`, `inventory`, `orders`, `shipments`. Functions `build_demo(seed)` and `describe_day(log, report)`. Dataclasses `ScheduledOrder` and `DayLog`. |
| Required interface | Inventory, Order Manager, Shipment Manager (public methods only), Analytics `build_report` and `format_report`, standard library `random.Random` |
| Used by | CLI; tests in `tests/test_simulator.py` |
| Requirements | SCM-F-040, SCM-F-041, SCM-F-042; supports SCM-NF-002, SCM-SR-001, SCM-SR-004 |
| Tests | `tests/test_simulator.py` (10 test functions); TC-SIM-01, TC-SIM-02, TC-REP-01 |

**Internal data**

| Attribute | Type | Content |
|---|---|---|
| `day` | `int` | Last simulated day; 0 before the first step |
| `inventory`, `orders`, `shipments` | `Inventory`, `OrderManager`, `ShipmentManager` | Created in the constructor. Both managers share the same `Inventory`; the Shipment Manager receives `random.Random(seed)`. |
| `_warehouses` | `dict[warehouse, capacity]` | Registered warehouses (used for validation and capacity trimming) |
| `_suppliers` | `dict[supplier_id, Supplier]` | Registered suppliers (used to validate `set_policy`) |
| `_item_supplier` | `dict[(warehouse, sku), supplier_id]` | The one supplier that replenishes each item |
| `_schedule` | `dict[day, list[ScheduledOrder]]` | Future customer demand; a day's entry is removed when that day is simulated |
| `history` | `list[dict]` | One Analytics report per simulated day, in order |
| `logs` | `list[DayLog]` | One event record per simulated day, in order |

**The daily step.** `step()` increments `day`, then runs five stages in a fixed order:

| Stage | Call(s) | Why at this point |
|---|---|---|
| 1. Arrivals | `shipments.process_arrivals(day)` | Goods that arrive today can be used today. |
| 2. Today's orders | `orders.create(…)` then `orders.try_fulfil(order, day)` for each scheduled order | Demand is served from the stock now on hand; each fulfilment removes stock before the next one is checked. |
| 3. Back-order retry | `orders.process_open(day)` | Any arrival stock left after today's orders goes to waiting orders, oldest first. |
| 4. Replenishment | `_replenish(day)` using `inventory.reorder_suggestions()`, `shipments.in_transit()`, `shipments.dispatch(…)` | Reorder decisions see the end-of-day stock after all demand. |
| 5. Report | `build_report(inventory.snapshot(), shipments.delayed(day), all_orders(), day, …)` | The report shows the final state of the day. |

**Replenishment algorithm (`_replenish`).** For each `(warehouse, sku, reorder_quantity)` from `reorder_suggestions()` (sorted): skip the item if it has no assigned supplier or already has a shipment in transit; otherwise compute `free = capacity − total_in_warehouse(warehouse) − units in transit to that warehouse − units dispatched earlier in this step`, set `quantity = min(reorder_quantity, free)`, and dispatch only if `quantity > 0`. Stock only increases through arrivals, so a shipment that fitted when dispatched still fits when it arrives, and `CapacityExceededError` cannot be raised during `process_arrivals`.

**Key design decisions**

1. **One orchestrator.** All cross-module calls during a run happen in `step()`; no domain component calls another except through the shared Inventory. Event order is therefore defined and testable in one place.
2. **Validate at the boundary.** `schedule_order` rejects past days, quantities ≤ 0 and unknown warehouses before queuing anything; `set_policy` and `add_stock` reject unknown warehouses and suppliers with `KeyError`. Invalid demand never reaches the Order Manager.
3. **Public interfaces only.** The engine gets every order via `by_status` over all `OrderStatus` values (sorted by ID), and late shipments via `delayed(day)`. It never reads another module's private attributes.
4. **Reproducibility.** The only randomness is the seeded generator passed to the Shipment Manager; all iteration orders are sorted or insertion-ordered. Same seed and scenario give identical `history` (SCM-NF-002).
5. **Global report thresholds.** The constructor's `reorder_point` and `max_level` (defaults 20 and 500) are passed to `build_report`, because Analytics accepts one threshold for all items. Replenishment itself uses the per-item policies.

**Demo scenario (`build_demo(seed=42)`).** Suppliers `SUP-RELIABLE` (lead time 2, reliability 1.0) and `SUP-FLAKY` (lead time 2, reliability 0.3); warehouses `WH-NORTH` (capacity 1200) and `WH-SOUTH` (capacity 500); items `WIDGET` and `GIZMO` at `WH-NORTH`, `GADGET` and `WIDGET` at `WH-SOUTH`; 14 orders from customers `C-ACME`, `C-BOLT`, `C-CORE` and `C-DYNA` over days 1–10. It is designed to show every condition Analytics detects: `GADGET` at `WH-SOUTH` sells out on day 2 and a day 3 order is back-ordered; `SUP-FLAKY` shipments arrive late; `GIZMO` starts at 650 against a max level of 500.

##### CLI

| Item | Description |
|---|---|
| File / owner | `src/scm_sim/__main__.py` / Rohith Karning |
| Layer | Presentation |
| Responsibility | Command-line entry point: parses options, runs the demo scenario and prints the day-by-day log and the final report |
| Provided interface | `python -m scm_sim [--days N] [--seed S]` (defaults 10 and 42); function `main(argv=None) -> int` |
| Required interface | Simulation Engine `build_demo`, `Simulation.run`, `Simulation.logs`, `Simulation.final_summary`, `describe_day`; standard library `argparse` |
| Requirements | SCM-F-043, SCM-NF-005 |
| Tests | `test_cli_main_runs`, `test_cli_runs_as_module` in `tests/test_simulator.py`; TC-SIM-02 |

**Behaviour.** `main` parses the arguments with `argparse`; a `--days` value below 1 is reported with `parser.error`, which prints the usage and exits with code 2, and non-integer values are rejected by `argparse` in the same way. It then prints a header line, one block per day produced by `describe_day` (arrivals, fulfilled orders, back-orders, back-orders filled, reorders, and a `flags:` summary line), a blank line and the formatted final report, and returns 0. `main` takes an optional `argv` list so tests can call it directly without starting a new process.

**Design decisions.** The CLI contains no business logic; it only connects the user to the Simulation Engine, so all behaviour it shows is already covered by the engine's tests. Output is plain text, so it can be compared between runs to check reproducibility (TC-REP-01).

##### CI Pipeline

| Item | Description |
|---|---|
| File / owner | `.github/workflows/ci.yml` / Rohith Karning |
| Layer | Development infrastructure (not part of the runtime product) |
| Responsibility | Run the full automated test suite with coverage on every change proposed to, or merged into, `main`, and provide the required status check that gates merging |
| Triggers | `push` to `main`; `pull_request` targeting `main` |
| Job | `test` on `ubuntu-latest`: `actions/checkout@v4` → `actions/setup-python@v5` (Python 3.11) → `pip install -r requirements.txt` → `pytest -v --cov=scm_sim` |
| Requirements | SCM-NF-003, SCM-SR-005; supports SCM-NF-004 (Linux run) and SCM-SO-2 |
| Evidence | 20 of 20 workflow runs successful up to run #20 on commit `b3702ef` (11-10-2026): 73 tests passed, 97% line coverage |

**Design decisions.** The job name `test` is configured as a required status check in the branch protection rule for `main`, so a pull request cannot be merged until the suite passes on its latest commit. Running on Linux in CI while developers use Windows gives a cross-platform check on every change. Coverage is measured and printed on every run; the 90% target of SCM-NF-003 is checked by reading that report (TC-COV-01), because the workflow does not set a `--cov-fail-under` limit.
