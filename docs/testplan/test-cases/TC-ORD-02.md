### Test Case Specification: TC-ORD-02

| Field | Content |
|---|---|
| **TC ID** | TC-ORD-02 |
| **Title** | FIFO Backorder Reprocessing, Fulfillment Priority, and Order Cancellation Rules |
| **Requirement(s)** | SCM-F-012, SCM-F-013 |
| **Type** | Functional |
| **Preconditions** | Initialized `OrderManager` and `Inventory`; orders in `BACKORDERED` or `PENDING` states; inventory restocked or exhausted. |
| **Test data** | Customers: `C-ACME`, `C-BETA`; Warehouse: `WH-NORTH`; SKU: `WIDGET`; Quantities: `10`, `10`; Days: `1`, `2`, `3` |
| **Objective** | Verify that `process_open()` prioritizes older orders over newer orders when stock is constrained, existing back-orders are retried before today's new demand, correctly sets status to `FULFILLED`, enforces cancellation guards preventing cancellation of fulfilled orders, and rejects unknown order IDs or reprocessing fulfilled/cancelled orders. |
| **Steps** | 1. Create order 1 on day 1 (qty 10) and order 2 on day 2 (qty 10). Attempt fulfillment with 0 stock; verify both are `BACKORDERED`.<br>2. Add 15 units of `WIDGET` to warehouse on day 3.<br>3. Call `mgr.process_open(day=3)`.<br>4. Attempt to cancel an active unfulfilled order.<br>5. Attempt to cancel an already fulfilled order.<br>6. Look up an unknown order ID `ORD-0042` with `get`.<br>7. Fulfill one order and cancel another, then call `try_fulfil` on both again on a later day.<br>8. In simulation, retry open back-orders before today's new orders when fresh stock arrives on the same day. |
| **Expected result** | 1. Both orders marked `BACKORDERED`.<br>2. When 15 units are available, `process_open(day=3)` fulfills the older order (Day 1) and leaves the newer order (Day 2) `BACKORDERED`. Stock reduces to 5 units.<br>3. Cancelling an unfulfilled order succeeds with status `CANCELLED`.<br>4. Cancelling a `FULFILLED` order raises `ValueError`.<br>5. `mgr.get("ORD-0042")` raises `KeyError`.<br>6. Calling `try_fulfil` on already FULFILLED or CANCELLED order returns `False` and leaves stock unchanged (SCM-SR-003).<br>7. In simulation step, existing back-orders are retried and filled before today's new demand is processed. |
| **Pass/fail criteria** | Pass if older orders are prioritized strictly over newer orders during constrained stock replenishment, cancellation rules are enforced, unknown IDs raise KeyError, and re-fulfilling finished orders returns False without stock deduction; Fail if newer order is fulfilled first or fulfilled order is cancelled. |
| **Automated by** | `tests/test_orders.py::test_backorder_later_fulfilled_by_process_open`<br>`tests/test_orders.py::test_oldest_first_priority`<br>`tests/test_orders.py::test_cancel_rules`<br>`tests/test_orders.py::test_get_unknown_order_raises_key_error`<br>`tests/test_orders.py::test_fulfilled_or_cancelled_orders_are_never_reprocessed`<br>`tests/test_simulator.py::test_older_backorder_is_served_before_new_order_on_same_day` |
| **Actual result** | Pass. Final automated suite: 100 tests passed. See [final unit-test report](../../test-reports/unit/unit-test-report.md). |
| **Status** | Passed |

Updated 08-11-2026: Open back-orders are now retried before today's new orders (#69); updated steps and expected results, and added `test_get_unknown_order_raises_key_error`, `test_fulfilled_or_cancelled_orders_are_never_reprocessed`, and `test_older_backorder_is_served_before_new_order_on_same_day` to Automated by (#59). Final suite evidence reconciled 09-11-2026.
