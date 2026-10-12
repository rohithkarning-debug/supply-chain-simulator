### 4.3.4 Analytics API (`scm_sim.analytics`)

The Analytics component exports seven module-level functions and no classes. Every function is **pure**: it reads only its arguments, allocates and returns new containers, and never mutates an argument, never touches module-level state and never raises an exception of its own. The component imports only `from __future__ import annotations` and `from typing import Any` from the Python standard library, and depends on no other component — the coupling is entirely through the data the caller passes in (SAD §3.4.4).

**A note on the Raises column.** Every entry below reads "None". This is accurate and deliberate: Analytics mutates nothing, so it has no state to protect and therefore performs no input validation. `find_low_stock` will accept a negative `reorder_point` and simply return an empty list; `format_report` will raise `KeyError` only if handed a dictionary that is missing a key, which is a programming error in the caller rather than bad data from the simulation. Domain components such as `Inventory` and `ShipmentManager` validate aggressively (SCM-SR-001); Analytics is deliberately not one of them, and must not be described as if it were.

| # | Function | Purpose |
| :--- | :--- | :--- |
| 1 | `find_delayed_shipments(shipments, current_day)` | Detect shipments that are later than their expected arrival day. |
| 2 | `find_stockouts(stock)` | Detect items whose quantity is exactly zero. |
| 3 | `find_low_stock(stock, reorder_point=20)` | Detect items at or below the reorder point but above zero. |
| 4 | `find_excess(stock, max_level=500)` | Detect items above the max level, with the surplus quantity. |
| 5 | `order_metrics(orders)` | Count orders per status and compute the fill rate. |
| 6 | `build_report(stock, shipments, orders, current_day, reorder_point=20, max_level=500)` | Compose findings 1–5 into one daily report dictionary. |
| 7 | `format_report(report)` | Render a report dictionary as readable multi-line text. |

---

#### 1. `find_delayed_shipments(shipments, current_day)`

- **Signature:** `find_delayed_shipments(shipments: list[Any], current_day: int) -> list[dict[str, Any]]`
- **Parameters:**
  - `shipments` (`list`): The shipments to inspect. Each element need only expose the attributes `shipment_id` (`str`), `sku` (`str`), `warehouse_id` (`str`), `expected_day` (`int`) and `actual_day` (`int` or `None`). Any object with those attributes works, which is why the tests pass stand-ins built with `types.SimpleNamespace`. Passing the result of `ShipmentManager.in_transit()` plus the delivered shipments covers the whole run.
  - `current_day` (`int`): The current simulation day, used as the reference point for every shipment that has not yet been delivered.
- **Returns:** A `list` of `dict`, one per late shipment, each with exactly the keys `shipment_id`, `sku`, `warehouse_id` and `days_late`. A shipment is included **if and only if** `days_late > 0`, where `days_late` is computed as `actual_day − expected_day` for a delivered shipment and `current_day − expected_day` for one still in transit. The list is sorted by `days_late` descending, with `shipment_id` ascending as a deterministic tie-break. Returns an empty list when nothing is late.
- **Raises:** None.
- **Example:**
```python
from scm_sim.analytics import find_delayed_shipments

delayed = find_delayed_shipments(shipments, current_day=4)
for d in delayed:
    print(f"{d['shipment_id']}: {d['sku']} to {d['warehouse_id']}, "
          f"{d['days_late']} day(s) late")
# SHP-0001: WIDGET to WH-NORTH, 1 day(s) late
```
- **Notes:** A shipment arriving exactly on its expected day, or before it, is never reported. The delivered branch selects on `actual_day is not None` rather than on truthiness, so a shipment that arrived on day 0 is correctly treated as delivered rather than as perpetually in transit.

---

#### 2. `find_stockouts(stock)`

- **Signature:** `find_stockouts(stock: dict[tuple[str, str], int]) -> list[tuple[str, str]]`
- **Parameters:**
  - `stock` (`dict`): The stock snapshot keyed by `(warehouse_id, sku)`. Pass the result of `Inventory.snapshot()`, which is an independent copy.
- **Returns:** A `list` of `(warehouse_id, sku)` tuples for every item whose quantity is **exactly** 0, sorted ascending (by `warehouse_id`, then `sku`). An item with any positive quantity — including 1 — is not a stockout and is not returned. Returns an empty list for an empty snapshot.
- **Raises:** None.
- **Example:**
```python
from scm_sim.analytics import find_stockouts

find_stockouts({("WH-NORTH", "WIDGET"): 0, ("WH-NORTH", "GADGET"): 1})
# [('WH-NORTH', 'WIDGET')]
```

---

#### 3. `find_low_stock(stock, reorder_point=20)`

- **Signature:** `find_low_stock(stock: dict[tuple[str, str], int], reorder_point: int = 20) -> list[tuple[str, str, int]]`
- **Parameters:**
  - `stock` (`dict`): The stock snapshot keyed by `(warehouse_id, sku)`.
  - `reorder_point` (`int`, default `20`): The inclusive upper bound of the low-stock band. The default matches the default `StockPolicy(reorder_point=20)`.
- **Returns:** A `list` of `(warehouse_id, sku, qty)` tuples for every item where $0 < qty \le$ `reorder_point`, sorted ascending by `warehouse_id` then `sku`. A quantity of 0 is **excluded** — that is a stockout, reported by `find_stockouts`, not low stock. A quantity of exactly `reorder_point` is **included**. Returns an empty list when no item is in the band.
- **Raises:** None.
- **Example:**
```python
from scm_sim.analytics import find_low_stock

find_low_stock({("WH-NORTH", "GADGET"): 1, ("WH-NORTH", "GIZMO"): 20,
                ("WH-NORTH", "BOLT"): 21})
# [('WH-NORTH', 'GADGET', 1), ('WH-NORTH', 'GIZMO', 20)]

find_low_stock({("WH-NORTH", "BOLT"): 21}, reorder_point=21)
# [('WH-NORTH', 'BOLT', 21)]
```

---

#### 4. `find_excess(stock, max_level=500)`

- **Signature:** `find_excess(stock: dict[tuple[str, str], int], max_level: int = 500) -> list[tuple[str, str, int, int]]`
- **Parameters:**
  - `stock` (`dict`): The stock snapshot keyed by `(warehouse_id, sku)`.
  - `max_level` (`int`, default `500`): The exclusive lower bound of the excess band. The default matches the default `StockPolicy(max_level=500)`.
- **Returns:** A `list` of `(warehouse_id, sku, qty, surplus)` tuples for every item where `qty > max_level`, sorted ascending by `warehouse_id` then `sku`. `surplus` is computed as `qty − max_level`, i.e. the quantity held above the threshold. A quantity of exactly `max_level` is **excluded**. Returns an empty list when no item exceeds the threshold.
- **Raises:** None.
- **Example:**
```python
from scm_sim.analytics import find_excess

find_excess({("WH-NORTH", "GIZMO"): 500, ("WH-NORTH", "BOLT"): 501})
# [('WH-NORTH', 'BOLT', 501, 1)]

find_excess({("WH-NORTH", "WIDGET"): 120}, max_level=100)
# [('WH-NORTH', 'WIDGET', 120, 20)]
```

---

#### 5. `order_metrics(orders)`

- **Signature:** `order_metrics(orders: list[Any]) -> dict[str, Any]`
- **Parameters:**
  - `orders` (`list`): The orders to aggregate. Each element need only expose a `status` attribute. Pass the list returned by `OrderManager.by_status(...)`, or the manager's full order list.
- **Returns:** A `dict` with exactly the keys `total`, `pending`, `fulfilled`, `backordered`, `cancelled` and `fill_rate`. `total` is the length of the supplied list; the four status counts correspond to `OrderStatus.PENDING`, `FULFILLED`, `BACKORDERED` and `CANCELLED`. `fill_rate` is $\text{round}(\text{fulfilled} \div (\text{total} − \text{cancelled}),\ 2)$, or `0.0` when `total − cancelled` is not greater than 0. Status values are accepted as `OrderStatus` enumeration members, as plain strings, or as a mix of the two within one list; a status value outside the four known names is ignored rather than raising.
- **Raises:** None.
- **Example:**
```python
from scm_sim.orders import OrderStatus
from scm_sim.analytics import order_metrics

m = order_metrics(orders)   # FULFILLED, FULFILLED, PENDING, CANCELLED
m["total"]        # 4
m["fulfilled"]    # 2
m["fill_rate"]    # 0.67  -> round(2 / (4 - 1), 2)

order_metrics([])["fill_rate"]   # 0.0
```

---

#### 6. `build_report(stock, shipments, orders, current_day, reorder_point=20, max_level=500)`

- **Signature:** `build_report(stock: dict[tuple[str, str], int], shipments: list[Any], orders: list[Any], current_day: int, reorder_point: int = 20, max_level: int = 500) -> dict[str, Any]`
- **Parameters:**
  - `stock` (`dict`): The stock snapshot, forwarded unchanged to `find_stockouts`, `find_low_stock` and `find_excess`.
  - `shipments` (`list`): The shipments to inspect, forwarded to `find_delayed_shipments`.
  - `orders` (`list`): The orders to aggregate, forwarded to `order_metrics`.
  - `current_day` (`int`): The simulation day. It is stored under `day` **and** used as the reference point for in-transit lateness.
  - `reorder_point` (`int`, default `20`): Forwarded to `find_low_stock`.
  - `max_level` (`int`, default `500`): Forwarded to `find_excess`.
- **Returns:** A new `dict` with exactly six keys: `day` (the `current_day` as given), `delayed_shipments`, `stockouts`, `low_stock`, `excess` and `orders` (the dictionary from `order_metrics`). Because the dictionary is freshly allocated on every call, the caller — the Simulation Engine — may retain every daily report for the whole run and compare them later.
- **Raises:** None.
- **Example:**
```python
from scm_sim.analytics import build_report

report = build_report(inv.snapshot(), in_transit + delivered, orders, current_day=4)
sorted(report.keys())
# ['day', 'delayed_shipments', 'excess', 'low_stock', 'orders', 'stockouts']
report["day"]            # 4
```
- **Notes:** This is the only Analytics entry point the Simulation Engine calls directly; the five classifier functions are used through it in a run, and directly in tests and ad-hoc analysis.

---

#### 7. `format_report(report)`

- **Signature:** `format_report(report: dict[str, Any]) -> str`
- **Parameters:**
  - `report` (`dict`): A report dictionary as returned by `build_report`. All six keys must be present; a missing key raises `KeyError`, which indicates a caller error rather than invalid simulation data.
- **Returns:** A `str` containing newline-separated lines. The first line is the header `=== Supply Chain Report: Day N ===`. Five sections follow, each preceded by a blank line and headed `Section name (count)`, in this fixed order: `Delayed shipments`, `Stockouts`, `Low stock`, `Excess` and `Orders`. When a section is empty the line `  No issues` is printed in place of item listings; when it is non-empty one `  - …` line is printed per item. The `Orders` section always prints two lines — a status breakdown and `  fill rate: <value>`.
- **Raises:** None for a well-formed report; `KeyError` if a required key is absent.
- **Example:**
```python
from scm_sim.analytics import build_report, format_report

print(format_report(build_report({}, [], [], current_day=1)))
# === Supply Chain Report: Day 1 ===
#
# Delayed shipments (0)
#   No issues
#
# Stockouts (0)
#   No issues
#
# Low stock (0)
#   No issues
#
# Excess (0)
#   No issues
#
# Orders (0)
#   pending 0, fulfilled 0, backordered 0, cancelled 0
#   fill rate: 0.0
```

#### 7.1 Data Formats Consumed and Produced

| Argument | Expected shape | Example | Produced by |
| :--- | :--- | :--- | :--- |
| `stock` | `dict[{(warehouse_id, sku): int}]` | `{("WH-NORTH", "WIDGET"): 0}` | `Inventory.snapshot()` |
| `shipments` | `list` of objects with `shipment_id`, `sku`, `warehouse_id`, `expected_day`, `actual_day` | `Shipment(id="SHP-0001", expected_day=3, actual_day=None)` | `ShipmentManager.in_transit()` / delivered shipments |
| `orders` | `list` of objects with `status` (`OrderStatus` or `str`) | `Order(id="ORD-0001", status=OrderStatus.FULFILLED)` | `OrderManager.by_status(...)` |
| `current_day` | `int`, the simulation day | `4` | `Simulation` day counter |
| `report` | `dict` with the six report keys | see `build_report` | `build_report` |