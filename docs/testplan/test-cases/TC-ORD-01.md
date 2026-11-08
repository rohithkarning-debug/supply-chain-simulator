### Test Case Specification: TC-ORD-01

| Field | Content |
|---|---|
| **TC ID** | TC-ORD-01 |
| **Title** | Order Creation, Sequential Identification, and Inventory Fulfillment Validation |
| **Requirement(s)** | SCM-F-010, SCM-F-011 |
| **Type** | Functional |
| **Preconditions** | Initialized `Inventory` instance; `OrderManager` bound to the inventory; warehouse `WH-NORTH` has either sufficient or deficient stock of SKU `WIDGET`. |
| **Test data** | Customer: `C-ACME`, Warehouse: `WH-NORTH`, SKU: `WIDGET`, Quantities: `10`, `5`, `0`, `-5`, Day: `1` |
| **Objective** | Verify sequential ID generation, negative/zero quantity rejection without sequence gap, atomic inventory deduction upon fulfillment, and backorder transition on stock shortage. |
| **Steps** | 1. Call `mgr.create("C-ACME", "WH-NORTH", "WIDGET", 10, day=1)` and `mgr.create("C-ACME", "WH-NORTH", "WIDGET", 5, day=1)`.<br>2. Attempt to create an order with quantity `0`.<br>3. Add 20 units of `WIDGET` to `WH-NORTH`, create order for 10 units, call `try_fulfil(order, day=1)`.<br>4. Reset stock to 5 units, create order for 10 units, call `try_fulfil(order, day=1)`.<br>5. Call `create` with quantity 0 and −5 (each raises `ValueError`), then create two valid orders and verify their allocated IDs.<br>6. Construct an `Order` dataclass directly with quantity 0. |
| **Expected result** | 1. Orders receive sequential IDs `ORD-0001` and `ORD-0002` with status `PENDING`.<br>2. Creation with quantity 0 raises `ValueError`.<br>3. When stock is 20, `try_fulfil` returns `True`, status becomes `FULFILLED`, `fulfilled_day=1`, stock decreases to 10.<br>4. When stock is 5, `try_fulfil` returns `False`, status becomes `BACKORDERED`, stock remains 5 without partial fulfillment.<br>5. Both invalid calls raise `ValueError`; subsequent valid orders receive `ORD-0001` and `ORD-0002` — rejected calls do not consume sequence IDs.<br>6. Direct instantiation with non-positive quantity raises `ValueError` in `Order.__post_init__`. |
| **Pass/fail criteria** | Pass if all returned IDs, exceptions, statuses, and stock levels match expectations; Fail if quantity 0 is accepted, partial fulfillment occurs, or IDs are non-sequential. |
| **Automated by** | `tests/test_orders.py::test_create_order_id_sequence`<br>`tests/test_orders.py::test_invalid_quantity`<br>`tests/test_orders.py::test_fulfil_enough_stock`<br>`tests/test_orders.py::test_backorder_when_short`<br>`tests/test_orders.py::test_rejected_order_does_not_consume_an_id`<br>`tests/test_orders.py::test_order_dataclass_rejects_non_positive_quantity_directly` |
| **Actual result** | Pass (all automated tests pass; commit `b3702ef` and PR #68) |
| **Status** | Passed |

Updated 08-11-2026: Invalid quantity no longer consumes an order ID (#68); added steps 5–6, test_rejected_order_does_not_consume_an_id, and test_order_dataclass_rejects_non_positive_quantity_directly to Automated by (#59).
