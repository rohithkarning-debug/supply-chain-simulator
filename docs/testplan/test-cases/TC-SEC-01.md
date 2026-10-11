| Field | Content |
| :--- | :--- |
| **TC ID** | TC-SEC-01 |
| **Title** | Public Input Validation, Invariant Enforcement, and State Tamper Resistance |
| **Requirement(s)** | SCM-SR-001, SCM-SR-002, SCM-SR-003, SCM-SR-004, SCM-SR-007 |
| **Type** | Security |
| **Objective** | Verify that domain operations reject invalid boundary parameters before mutating state, enforce warehouse capacity and non-negative stock invariants, guard order lifecycles against invalid status changes, reject unknown IDs with `KeyError`, and return immutable independent snapshots. |
| **Preconditions** | Initialized `Inventory`, `OrderManager`, `ShipmentManager`, and `Simulation` instances. |
| **Test data** | Negative quantities (-10, 0); negative lead times (-1); invalid reliabilities (-0.1, 1.5); non-existent entity IDs (`SUP-999`, `ORD-999`, `WH-999`); warehouse capacity 100 with stock addition of 101. |
| **Steps** | 1. Attempt adding and removing non-positive quantities in Inventory, Orders, and Shipments.<br>2. Attempt removing more units than available in warehouse stock.<br>3. Attempt adding units exceeding registered warehouse capacity.<br>4. Attempt cancelling a FULFILLED order and re-fulfilling a CANCELLED order.<br>5. Attempt dispatching and scheduling orders referencing unknown supplier and warehouse IDs.<br>6. Mutate the dictionary returned by `Inventory.snapshot()` and verify internal `_stock`. |
| **Expected result** | `ValueError` raised for invalid parameters with state left unchanged; `InsufficientStockError` and `CapacityExceededError` raised with inventory intact; `cancel()` on FULFILLED raises `ValueError`; unknown entity references raise `KeyError`; mutating returned snapshot has zero effect on internal inventory. |
| **Pass/fail criteria** | **Pass** if all invalid input vectors are rejected, state invariants remain uncompromised, and snapshots are independent; **Fail** if state corruption, silent mutation, or unhandled crashes occur. |
| **Automated by** | `tests/test_inventory.py::test_remove_too_much_raises`<br>`tests/test_inventory.py::test_add_beyond_capacity_raises_and_leaves_stock_unchanged`<br>`tests/test_inventory.py::test_stock_policy_rejects_invalid_values`<br>`tests/test_inventory.py::test_snapshot_returns_independent_copy`<br>`tests/test_orders.py::test_invalid_quantity`<br>`tests/test_orders.py::test_cancel_rules`<br>`tests/test_shipments.py::test_supplier_validation`<br>`tests/test_shipments.py::test_add_supplier_and_reject_duplicate_and_unknown`<br>`tests/test_simulator.py::test_schedule_order_validates_input` |
| **Actual result** | Pass (CI run #20, commit `b3702ef`) |
| **Status** | Passed |
