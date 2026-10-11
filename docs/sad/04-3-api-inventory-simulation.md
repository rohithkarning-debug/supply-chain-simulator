### 4.3 API Design

This section defines the public interface of every code component. For each call it gives the **signature, parameters, return value, exceptions raised and an example**. All examples use made-up data and were executed against the code at commit `b3702ef`; the output shown is the real output. Members whose names start with `_` are private and not part of the API.

#### 4.3.1 Inventory, Simulation Engine and CLI

##### Inventory API (`scm_sim.inventory`)

Conventions: `warehouse` and `sku` are non-empty strings such as `"WH-NORTH"` and `"WIDGET"`; quantities are integers. Every method that raises leaves the inventory unchanged.

**`StockPolicy`**

| Field | Content |
|---|---|
| Signature | `StockPolicy(reorder_point: int = 20, reorder_quantity: int = 100, max_level: int = 500)`, frozen dataclass |
| Parameters | `reorder_point`: reorder when the level is at or below this value. `reorder_quantity`: units to request per reorder. `max_level`: levels above this are excess. |
| Returns | An immutable policy object |
| Raises | `ValueError` if any value is negative, or if `max_level < reorder_point` |

```python
>>> from scm_sim.inventory import Inventory, StockPolicy, InsufficientStockError, CapacityExceededError
>>> StockPolicy()
StockPolicy(reorder_point=20, reorder_quantity=100, max_level=500)
>>> StockPolicy(reorder_point=30, reorder_quantity=150, max_level=20)
Traceback (most recent call last):
ValueError: max_level must be >= reorder_point
```

**`Inventory()`**

| Field | Content |
|---|---|
| Signature | `Inventory()` |
| Parameters | None |
| Returns | A new, empty inventory: no stock, no registered warehouses, no policies |
| Raises | – |

**`level`**

| Field | Content |
|---|---|
| Signature | `level(warehouse: str, sku: str) -> int` |
| Parameters | `warehouse`, `sku`: the item to look up |
| Returns | Current quantity; `0` if the item has never been stocked |
| Raises | – |

```python
>>> inv = Inventory()
>>> inv.level("WH-NORTH", "WIDGET")
0
```

**`register_warehouse`**

| Field | Content |
|---|---|
| Signature | `register_warehouse(warehouse: str, capacity: int) -> None` |
| Parameters | `warehouse`: warehouse ID. `capacity`: maximum total units across all SKUs (> 0). Re-registering replaces the capacity. |
| Returns | `None` |
| Raises | `ValueError` if `capacity <= 0` |

```python
>>> inv.register_warehouse("WH-NORTH", 1200)
>>> inv.register_warehouse("WH-SOUTH", 0)
Traceback (most recent call last):
ValueError: capacity must be positive
```

**`add`**

| Field | Content |
|---|---|
| Signature | `add(warehouse: str, sku: str, qty: int) -> int` |
| Parameters | `qty`: units to add (> 0) |
| Returns | The new level of the item |
| Raises | `ValueError` if `qty <= 0`; `CapacityExceededError` if the warehouse is registered and its total would exceed capacity |

```python
>>> inv.add("WH-NORTH", "WIDGET", 100)
100
>>> inv.add("WH-NORTH", "GIZMO", 1100)
1100
>>> inv.add("WH-NORTH", "GIZMO", 1)
Traceback (most recent call last):
scm_sim.inventory.CapacityExceededError: adding 1 GIZMO would exceed capacity 1200 at WH-NORTH
>>> inv.total_in_warehouse("WH-NORTH")
1200
```

**`remove`**

| Field | Content |
|---|---|
| Signature | `remove(warehouse: str, sku: str, qty: int) -> int` |
| Parameters | `qty`: units to remove (> 0) |
| Returns | The new level of the item |
| Raises | `ValueError` if `qty <= 0`; `InsufficientStockError` if `qty` is greater than the current level |

```python
>>> inv.remove("WH-NORTH", "WIDGET", 30)
70
>>> inv.remove("WH-NORTH", "WIDGET", 71)
Traceback (most recent call last):
scm_sim.inventory.InsufficientStockError: not enough WIDGET at WH-NORTH
>>> inv.level("WH-NORTH", "WIDGET")
70
```

**`is_stockout`**

| Field | Content |
|---|---|
| Signature | `is_stockout(warehouse: str, sku: str) -> bool` |
| Parameters | The item to check |
| Returns | `True` if the level is exactly 0 (including never-stocked items) |
| Raises | – |

```python
>>> inv.is_stockout("WH-NORTH", "WIDGET"), inv.is_stockout("WH-SOUTH", "GADGET")
(False, True)
```

**`total_in_warehouse`**

| Field | Content |
|---|---|
| Signature | `total_in_warehouse(warehouse: str) -> int` |
| Parameters | `warehouse`: warehouse ID |
| Returns | Sum of the levels of all SKUs in that warehouse |
| Raises | – |

```python
>>> inv.total_in_warehouse("WH-NORTH")
1170
```

**`set_policy` / `get_policy`**

| Field | Content |
|---|---|
| Signature | `set_policy(warehouse: str, sku: str, policy: StockPolicy) -> None`; `get_policy(warehouse: str, sku: str) -> StockPolicy` |
| Parameters | `policy`: the policy for that item; replaces any previous one |
| Returns | `None` / the item's policy, or `StockPolicy()` if none was set |
| Raises | – |

```python
>>> inv.set_policy("WH-NORTH", "WIDGET", StockPolicy(reorder_point=80, reorder_quantity=150, max_level=500))
>>> inv.get_policy("WH-NORTH", "WIDGET").reorder_quantity
150
>>> inv.get_policy("WH-SOUTH", "GADGET")
StockPolicy(reorder_point=20, reorder_quantity=100, max_level=500)
```

**`needs_reorder` / `is_excess`**

| Field | Content |
|---|---|
| Signature | `needs_reorder(warehouse: str, sku: str) -> bool`; `is_excess(warehouse: str, sku: str) -> bool` |
| Parameters | The item to check |
| Returns | `needs_reorder`: `level <= policy.reorder_point`. `is_excess`: `level > policy.max_level`. |
| Raises | – |

```python
>>> inv.needs_reorder("WH-NORTH", "WIDGET")
True
>>> inv.is_excess("WH-NORTH", "GIZMO")
True
```

**`reorder_suggestions`**

| Field | Content |
|---|---|
| Signature | `reorder_suggestions() -> list[tuple[str, str, int]]` |
| Parameters | None |
| Returns | `(warehouse, sku, reorder_quantity)` for every tracked item (ever stocked, or with a policy) that needs a reorder, sorted by warehouse then SKU |
| Raises | – |

```python
>>> inv.reorder_suggestions()
[('WH-NORTH', 'WIDGET', 150)]
```

**`snapshot`**

| Field | Content |
|---|---|
| Signature | `snapshot() -> dict[tuple[str, str], int]` |
| Parameters | None |
| Returns | A new dictionary `{(warehouse, sku): qty}` of all tracked stock; changing it does not change the inventory |
| Raises | – |

```python
>>> snap = inv.snapshot()
>>> snap
{('WH-NORTH', 'WIDGET'): 70, ('WH-NORTH', 'GIZMO'): 1100}
>>> snap[("WH-NORTH", "WIDGET")] = 0
>>> inv.level("WH-NORTH", "WIDGET")
70
```

##### Simulation Engine API (`scm_sim.simulator`)

Conventions: day 0 is set-up time and the first `step()` simulates day 1. Set-up methods may also be called between steps.

**`Simulation`**

| Field | Content |
|---|---|
| Signature | `Simulation(seed: int = 42, reorder_point: int = 20, max_level: int = 500)` |
| Parameters | `seed`: seed of the `random.Random` that draws shipment delays. `reorder_point`, `max_level`: the global low-stock and excess thresholds used in Analytics reports (replenishment uses per-item policies). |
| Returns | A simulation at `day == 0` with an empty `Inventory`, `OrderManager` and `ShipmentManager` (exposed as `inventory`, `orders`, `shipments`), and empty `history` and `logs` |
| Raises | – |

```python
>>> from scm_sim.simulator import Simulation, build_demo, describe_day
>>> sim = Simulation(seed=42)
>>> sim.day, sim.history
(0, [])
```

**`add_supplier`**

| Field | Content |
|---|---|
| Signature | `add_supplier(supplier_id: str, name: str, lead_time_days: int = 2, reliability: float = 1.0) -> Supplier` |
| Parameters | `lead_time_days`: base delivery time (≥ 0). `reliability`: probability of on-time arrival, 0.0–1.0. |
| Returns | The registered `Supplier` |
| Raises | `ValueError` if `lead_time_days < 0`, `reliability` is outside [0, 1], or the ID is already registered |

```python
>>> sim.add_supplier("SUP-RELIABLE", "Reliable Parts Ltd", lead_time_days=2, reliability=1.0)
Supplier(supplier_id='SUP-RELIABLE', name='Reliable Parts Ltd', lead_time_days=2, reliability=1.0)
```

**`add_warehouse`**

| Field | Content |
|---|---|
| Signature | `add_warehouse(warehouse_id: str, capacity: int) -> None` |
| Parameters | `capacity`: total units across all SKUs (> 0) |
| Returns | `None` |
| Raises | `ValueError` if `capacity <= 0` |

```python
>>> sim.add_warehouse("WH-NORTH", capacity=1200)
```

**`set_policy`**

| Field | Content |
|---|---|
| Signature | `set_policy(warehouse_id: str, sku: str, supplier_id: str, policy: StockPolicy \| None = None) -> None` |
| Parameters | `supplier_id`: the one supplier that replenishes this item. `policy`: thresholds; `None` means `StockPolicy()`. |
| Returns | `None` |
| Raises | `KeyError` if the warehouse or the supplier has not been added |

```python
>>> sim.set_policy("WH-NORTH", "WIDGET", "SUP-RELIABLE", StockPolicy(20, 150, 500))
>>> sim.set_policy("WH-NORTH", "WIDGET", "SUP-UNKNOWN")
Traceback (most recent call last):
KeyError: "Unknown supplier: 'SUP-UNKNOWN'"
```

**`add_stock`**

| Field | Content |
|---|---|
| Signature | `add_stock(warehouse_id: str, sku: str, quantity: int) -> int` |
| Parameters | `quantity`: units to place in stock (> 0) |
| Returns | The new level of the item |
| Raises | `KeyError` if the warehouse has not been added; `ValueError` if `quantity <= 0`; `CapacityExceededError` if capacity would be exceeded |

```python
>>> sim.add_stock("WH-NORTH", "WIDGET", 30)
30
```

**`schedule_order`**

| Field | Content |
|---|---|
| Signature | `schedule_order(day: int, customer_id: str, warehouse_id: str, sku: str, quantity: int) -> None` |
| Parameters | `day`: the future day on which the order is created (> current `day`). `quantity`: units ordered (> 0). |
| Returns | `None`; the demand is queued until that day |
| Raises | `ValueError` if `day <= sim.day` or `quantity <= 0`; `KeyError` if the warehouse has not been added |

```python
>>> sim.schedule_order(1, "C-ACME", "WH-NORTH", "WIDGET", 25)
>>> sim.schedule_order(2, "C-BOLT", "WH-NORTH", "WIDGET", 40)
>>> sim.schedule_order(1, "C-ACME", "WH-EAST", "WIDGET", 5)
Traceback (most recent call last):
KeyError: "Unknown warehouse: 'WH-EAST'"
```

**`step`**

| Field | Content |
|---|---|
| Signature | `step() -> dict` |
| Parameters | None |
| Returns | The Analytics report for the new day, with keys `day`, `delayed_shipments`, `stockouts`, `low_stock`, `excess`, `orders`. The report is also appended to `history`, and a `DayLog` to `logs`. |
| Raises | – (validation happens when the scenario is configured) |
| Behaviour | Increments `day`, then: (1) `process_arrivals`; (2) create and `try_fulfil` today's scheduled orders; (3) `process_open`; (4) replenish each item needing a reorder with nothing in transit, trimmed to capacity; (5) `build_report`. |

```python
>>> report = sim.step()
>>> report["day"], report["low_stock"], report["orders"]["fulfilled"]
(1, [('WH-NORTH', 'WIDGET', 5)], 1)
>>> [(s.shipment_id, s.sku, s.quantity, s.expected_day) for s in sim.logs[0].reorders]
[('SHP-0001', 'WIDGET', 150, 3)]
```

**`run`**

| Field | Content |
|---|---|
| Signature | `run(days: int) -> list[dict]` |
| Parameters | `days`: number of further days to simulate (≥ 0) |
| Returns | The reports of those days, in order |
| Raises | `ValueError` if `days < 0` |

```python
>>> [r["day"] for r in sim.run(2)]
[2, 3]
>>> sim.orders.get("ORD-0002").status.value, sim.orders.get("ORD-0002").fulfilled_day
('FULFILLED', 3)
```

**`final_summary`**

| Field | Content |
|---|---|
| Signature | `final_summary() -> str` |
| Parameters | None |
| Returns | The latest report formatted by Analytics `format_report`; if no day has been simulated, a report for day 0 |
| Raises | – |

```python
>>> print(sim.final_summary().splitlines()[0])
=== Supply Chain Report: Day 3 ===
```

**`all_orders`**

| Field | Content |
|---|---|
| Signature | `all_orders() -> list[Order]` |
| Parameters | None |
| Returns | Every order created so far, in order-ID order |
| Raises | – |

```python
>>> [(o.order_id, o.customer_id, o.status.value) for o in sim.all_orders()]
[('ORD-0001', 'C-ACME', 'FULFILLED'), ('ORD-0002', 'C-BOLT', 'FULFILLED')]
```

**`build_demo`**

| Field | Content |
|---|---|
| Signature | `build_demo(seed: int = 42) -> Simulation` |
| Parameters | `seed`: passed to `Simulation` |
| Returns | A ready-to-run scenario at day 0: suppliers `SUP-RELIABLE` (1.0) and `SUP-FLAKY` (0.3), warehouses `WH-NORTH` (1200) and `WH-SOUTH` (500), SKUs `WIDGET`, `GADGET` and `GIZMO`, and 14 orders over days 1–10 |
| Raises | – |

```python
>>> demo = build_demo(seed=42)
>>> reports = demo.run(10)
>>> reports[-1]["delayed_shipments"][0]
{'shipment_id': 'SHP-0001', 'sku': 'GADGET', 'warehouse_id': 'WH-SOUTH', 'days_late': 1}
>>> reports[-1]["excess"]
[('WH-NORTH', 'GIZMO', 600, 100)]
```

**`describe_day`**

| Field | Content |
|---|---|
| Signature | `describe_day(log: DayLog, report: dict) -> str` |
| Parameters | One day's `DayLog` and its report |
| Returns | A multi-line, human-readable summary of the day, ending with a `flags:` line |
| Raises | – |

```python
>>> print(describe_day(demo.logs[2], reports[2]))
Day 3:
  fulfilled ORD-0006: 45 WIDGET from WH-NORTH
  BACKORDER ORD-0005: 30 GADGET from WH-SOUTH
  flags: 0 delayed, 1 stockout, 0 low, 1 excess | fill rate 0.83
```

**Data types**

| Type | Fields |
|---|---|
| `ScheduledOrder` (frozen dataclass) | `customer_id: str`, `warehouse_id: str`, `sku: str`, `quantity: int` |
| `DayLog` (dataclass) | `day: int`, `delivered: list[Shipment]`, `fulfilled: list[Order]`, `backordered: list[Order]`, `backorders_filled: list[Order]`, `reorders: list[Shipment]` |

##### CLI API (`scm_sim.__main__`)

**Command line**

| Field | Content |
|---|---|
| Signature | `python -m scm_sim [-h] [--days DAYS] [--seed SEED]` (with `PYTHONPATH=src`, or run from `src/`) |
| Parameters | `--days`: days to simulate, integer ≥ 1, default 10. `--seed`: random seed, integer, default 42. `-h`/`--help`: show usage and exit. |
| Returns | Exit code 0; prints a header line, one block per day and the final report to standard output |
| Raises | Usage error on standard error with exit code 2 if `--days < 1` or a value is not an integer |

```
$ PYTHONPATH=src python -m scm_sim --days 0
usage: scm_sim [-h] [--days DAYS] [--seed SEED]
scm_sim: error: --days must be at least 1
```

**`main`**

| Field | Content |
|---|---|
| Signature | `main(argv: list[str] \| None = None) -> int` |
| Parameters | `argv`: argument list; `None` reads `sys.argv` |
| Returns | `0` on success |
| Raises | `SystemExit(2)` on a usage error (raised by `argparse`) |

```python
>>> from scm_sim.__main__ import main
>>> main(["--days", "1", "--seed", "42"])
Supply Chain Simulator demo: 1 day(s), seed 42
<BLANKLINE>
Day 1:
  fulfilled ORD-0001: 30 WIDGET from WH-NORTH
  fulfilled ORD-0002: 25 WIDGET from WH-SOUTH
  flags: 0 delayed, 0 stockout, 0 low, 1 excess | fill rate 1.0
<BLANKLINE>
=== Supply Chain Report: Day 1 ===
<BLANKLINE>
Delayed shipments (0)
  No issues
<BLANKLINE>
Stockouts (0)
  No issues
<BLANKLINE>
Low stock (0)
  No issues
<BLANKLINE>
Excess (1)
  - WH-NORTH / GIZMO: 650 (surplus 150)
<BLANKLINE>
Orders (2)
  pending 0, fulfilled 2, backordered 0, cancelled 0
  fill rate: 1.0
0
```
