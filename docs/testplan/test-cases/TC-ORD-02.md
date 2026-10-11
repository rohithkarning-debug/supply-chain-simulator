### Test Case Specification: TC-ORD-02

| Field | Content |
|---|---|
| **TC ID** | TC-ORD-02 |
| **Title** | FIFO Backorder Reprocessing, Fulfillment Priority, and Order Cancellation Rules |
| **Requirement(s)** | SCM-F-012, SCM-F-013 |
| **Type** | Functional |
| **Preconditions** | Initialized `OrderManager` and `Inventory`; orders in `BACKORDERED` or `PENDING` states; inventory restocked or exhausted. |
| **Test data** | Customers: `C-ACME`, `C-BETA`; Warehouse: `WH-NORTH`; SKU: `WIDGET`; Quantities: `10`, `10`; Days: `1`, `2`, `3` |
| **Objective** | Verify that `process_open()` prioritizes older orders over newer orders when stock is constrained, correctly sets status to `FULFILLED`, and enforces cancellation guards preventing cancellation of fulfilled orders. |
| **Steps** | 1. Create order 1 on day 1 (qty 10) and order 2 on day 2 (qty 10). Attempt fulfillment with 0 stock; verify both are `BACKORDERED`.<br>2. Add 15 units of `WIDGET` to warehouse on day 3.<br>3. Call `mgr.process_open(day=3)`.<br>4. Attempt to cancel an active unfulfilled order.<br>5. Attempt to cancel an already fulfilled order. |
| **Expected result** | 1. Both orders marked `BACKORDERED`.<br>2. When 15 units are available, `process_open(day=3)` fulfills the older order (Day 1) and leaves the newer order (Day 2) `BACKORDERED`. Stock reduces to 5 units.<br>3. Cancelling an unfulfilled order succeeds with status `CANCELLED`.<br>4. Cancelling a `FULFILLED` order raises `ValueError`. |
| **Pass/fail criteria** | Pass if older orders are prioritized strictly over newer orders during constrained stock replenishment and cancellation rules are enforced; Fail if newer order is fulfilled first or fulfilled order is cancelled. |
| **Automated by** | `tests/test_orders.py::test_backorder_later_fulfilled_by_process_open`<br>`tests/test_orders.py::test_oldest_first_priority`<br>`tests/test_orders.py::test_cancel_rules` |
| **Actual result** | Pass (CI run #20, commit `b3702ef`) |
| **Status** | Passed |
