### 3.4.4 Analytics Component

#### Component Overview
The **Analytics** component (`scm_sim.analytics`) is the read-only observation layer of the simulator. It transforms the plain state snapshots produced by the domain modules into the operational findings that the Supply Chain Analyst needs: which inbound shipments are late and by how many days, which items are stocked out, low or in excess, and how the order book is performing. It is implemented as seven module-level functions, all of which are **pure**: they read their arguments, return new data structures, and never mutate any argument or any module-level variable. The component holds **no internal state** and is instantiated never — it is used only as a namespace of functions.

#### Architectural Responsibilities
1. **Late-shipment detection (`find_delayed_shipments`):** Compares each shipment's expected arrival day against its actual arrival day when it has been delivered, or against the current simulation day when it is still in transit, and reports only those that are strictly late, ordered worst first.
2. **Inventory health classification (`find_stockouts`, `find_low_stock`, `find_excess`):** Partitions the stock snapshot into three disjoint exception classes using two configurable thresholds — stockouts at exactly zero, low stock in the open interval up to and including the reorder point, and excess strictly above the max level with the surplus quantity reported alongside.
3. **Order performance aggregation (`order_metrics`):** Counts orders per lifecycle status and derives the fill rate as fulfilled orders over eligible orders, rounded to two decimal places.
4. **Report composition (`build_report`):** Combines the outputs of the five classifiers above into a single daily report dictionary with a fixed key set, so that the daily time-step has exactly one artefact to store and print.
5. **Report presentation (`format_report`):** Renders a report dictionary as a stable multi-line text block with one counted section per key and an explicit "No issues" marker for empty sections, so that an absence of problems is visible rather than ambiguous.

#### Public Interface
The component exports exactly seven functions and one type hint convention; it exports no classes, no constants and no exceptions of its own.

| Function | Returns |
| :--- | :--- |
| `find_delayed_shipments(shipments, current_day)` | `list[dict]` with keys `shipment_id`, `sku`, `warehouse_id`, `days_late` |
| `find_stockouts(stock)` | `list[tuple[str, str]]` of `(warehouse_id, sku)` |
| `find_low_stock(stock, reorder_point=20)` | `list[tuple[str, str, int]]` of `(warehouse_id, sku, qty)` |
| `find_excess(stock, max_level=500)` | `list[tuple[str, str, int, int]]` of `(warehouse_id, sku, qty, surplus)` |
| `order_metrics(orders)` | `dict` with keys `total`, `pending`, `fulfilled`, `backordered`, `cancelled`, `fill_rate` |
| `build_report(stock, shipments, orders, current_day, reorder_point=20, max_level=500)` | `dict` with keys `day`, `delayed_shipments`, `stockouts`, `low_stock`, `excess`, `orders` |
| `format_report(report)` | `str` — the rendered multi-line report |

The complete signature, parameter, return and example detail for each call is given in SAD §4.3.4.

#### Inputs and Outputs
- **Inputs:**
  - Stock: the `dict[{(warehouse_id, sku): qty}]` mapping returned by `Inventory.snapshot()` — an independent copy, so Analytics never observes live inventory state.
  - Shipments: a `list` of `Shipment` objects exposing `shipment_id`, `sku`, `warehouse_id`, `expected_day` and `actual_day`. Only these five attributes are read; the Shipment Manager's internal collections are never reached.
  - Orders: a `list` of `Order` objects exposing `status` only. The status may be an `OrderStatus` enumeration member or the equivalent plain string, and both forms may be mixed in one list.
  - Day: the current integer simulation day.
  - Thresholds: `reorder_point` and `max_level`, defaulted to 20 and 500.
- **Outputs:**
  - New lists, dictionaries and strings. Every returned container is freshly allocated, so the caller may store, mutate or discard the result without affecting the simulator.

#### Collaborators and Dependencies
The Analytics component has **no collaborators and no dependencies**. It imports only `from __future__ import annotations` and `from typing import Any` from the Python standard library. It does not import `Inventory`, `OrderManager`, `ShipmentManager` or `Simulation`, and those modules do not import it; the coupling is one-way and expressed entirely through the `Simulation` orchestration layer, which calls `build_report` and `format_report` as steps 5 and 6 of the daily time-step. This satisfies the dependency direction defined in SAD §3.5 (CLI → Simulation → domain modules; analytics depends on nothing) and is what makes the component trivially unit-testable: the test suite constructs stand-ins with `types.SimpleNamespace` rather than building a simulation.

#### Internal State Structures
None. There are no instance attributes, no module-level mutable globals and no caches. Every function is referentially transparent with respect to its arguments, which is why the component contributes no state that could be corrupted and raises no security requirement of its own beyond SCM-SR-007 (returned data is a copy).

#### Key Algorithms
1. **Days-late computation.** For each shipment the component selects `end_day = actual_day if actual_day is not None else current_day`, then `days_late = end_day − expected_day`, and retains only entries where `days_late > 0`. Selecting on `is not None` rather than truthiness matters: a shipment delivered on day 0 records `actual_day = 0`, which must be treated as delivered rather than as in transit.
2. **Ordering.** The delayed list is sorted on the key `(-days_late, shipment_id)`. The negated `days_late` gives descending lateness, and `shipment_id` is included as a deterministic tie-break so that two shipments that are equally late always appear in the same order between runs — required by SCM-NF-002. The three stock classifiers use Python's `sorted` on tuple literals, which sorts first by `warehouse_id` and then by `sku`, giving a stable, human-readable ordering for free.
3. **Threshold comparison.** The low-stock test is the strict-and-inclusive pair `0 < qty <= reorder_point` and the excess test is the strict `qty > max_level`. Together with the exact test `qty == 0` for stockouts, the three classes are disjoint and together cover every non-negative quantity, so no item is ever reported twice or omitted.
4. **Status normalisation.** Each order status is read as `getattr(o.status, "value", o.status)`, which unwraps an enumeration member to its string value and passes a plain string through unchanged. The resulting value is then looked up in the fixed counts dictionary, so a status outside the four known values is ignored rather than raising — Analytics never fails on data it does not recognise.
5. **Fill rate.** `fill_rate = round(fulfilled / (total − cancelled), 2)` when `total − cancelled > 0`, and `0.0` otherwise. Cancelling an order removes the demand rather than counting it as a service failure, so cancelled orders are excluded from the denominator; the guarded division prevents `ZeroDivisionError` both for an empty order book and for an order book in which every order has been cancelled.

#### Design Decisions and Alternatives Considered
| Decision | Rationale | Alternative rejected |
| :--- | :--- | :--- |
| **Pure functions in one module, rather than an `Analytics` class with methods** | Analytics needs no identity, no configuration and no lifetime. Pure functions can be imported and called directly, are trivially testable in isolation, and cannot leak state between the many daily reports the Simulation retains. | An `Analytics` class instance mirroring the other components would have added an empty constructor and an object whose only state would be unused; it would also have forced the Simulation to own an instance it never reads from. |
| **Thresholds supplied as function parameters rather than read from `StockPolicy`** | This keeps the component dependency-free and makes the thresholds explicit and visible at every call site. It also allows a report to be computed with different thresholds from the ones in force, which is what the Analytics tests exercise. | Reading the per-item `StockPolicy` held by `Inventory` would have coupled Analytics to the Inventory component and to its data structures, and would have changed the signature and semantics of three of the seven functions. The consequence of this decision — one global threshold for all items, where Inventory holds per-item policies — is recorded as a known limitation in SAD §4.6. |
| **Tuples rather than small objects for stock findings** | `(warehouse_id, sku)` and its extensions are hashable, sortable, cheap to compare in tests and print directly. No attribute access or constructor is needed. | A `StockAlert` dataclass would be more self-describing but would add a class, a constructor and no behaviour; the reporting code would still destructure it field by field. |
| **Reports returned as `dict` and rendered separately** | Keeping `build_report` and `format_report` apart means the data and the presentation can be verified and consumed independently: the Simulation stores the dictionaries, the CLI and tests render text. | Rendering inside `build_report` would destroy the structured data, preventing the Simulation from retaining comparable day-by-day reports and making the reproducibility test in TC-REP-01 impossible. |
| **Graceful handling of unknown order statuses** | Ignoring an unrecognised status keeps `order_metrics` total and prevents a malformed order from aborting the whole daily report, which the Simulator would surface as a hard failure at day *n*. | Raising on an unknown status would be stricter, but Analytics is read-only and has no way to repair the data; failing the entire run over a single unexpected value is a worse outcome for an observational component. |

#### Traceability to Requirements
- **Functional Requirements:** SCM-F-030 (`find_delayed_shipments`), SCM-F-031 (`find_stockouts`, `find_low_stock`, `find_excess`), SCM-F-032 (`order_metrics`), SCM-F-033 (`build_report`, `format_report`).
- **Non-Functional Requirements:** SCM-NF-002 (deterministic ordering makes same-seed runs identical), SCM-NF-005 (`format_report` prints a count per section and "No issues" for empty sections), SCM-NF-003 (contributes to the measured coverage of the `scm_sim` package).
- **Security Requirements:** SCM-SR-007 only, and satisfied by construction — every returned list, tuple and dictionary is newly allocated, so a caller that mutates a report cannot change any internal state. The component performs no input validation and raises no exceptions because it mutates nothing: every operation it offers is safe to apply to any argument it can be given, so SCM-SR-001 has nothing to enforce here.

#### Known Limitations
1. **A single global threshold pair.** `find_low_stock` and `find_excess` take one `reorder_point` and one `max_level` for the whole snapshot, whereas Inventory holds a `StockPolicy` per (warehouse, SKU) item. A scenario whose items have different policies will be reported against the global defaults unless the caller overrides them.
2. **No history or trend.** Each call analyses a single point in time. The component reports the state on one day and holds no notion of a previous day, so it cannot itself compute a trend, an average delay or a time-to-resolution; any such figure would have to be derived by a caller comparing retained reports.
3. **Tuple-heavy output.** The stock classifiers return positional tuples, which are compact and cheap but not self-describing at the call site; a caller must remember the field order of each return type.
4. **No persistence or export.** Reports exist only as in-memory dictionaries and strings; they are printed by the CLI and retained by the Simulation but cannot be written to a file or read back later.
5. **Edge case not special-cased.** A shipment with `actual_day` recorded as day 0 is correctly treated as delivered because the code tests `is not None`, but this is the only such guard and a reader must know why; there is no general notion of "sentinel" values in the interface.