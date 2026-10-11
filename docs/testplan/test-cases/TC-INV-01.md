### TC-INV-01: Stock Tracking and Warehouse Capacity

| Field | Content |
|---|---|
| TC ID | TC-INV-01 |
| Title | Add and remove stock, reject over-removal and over-capacity additions, unlimited capacity for unregistered warehouses |
| Requirement(s) | SCM-F-001, SCM-F-002 (also supports SCM-SR-001, SCM-SR-002) |
| Type | Functional (unit, boundary-value) |
| Preconditions | 1. Python 3.11 virtual environment with `pip install -r requirements.txt` completed. 2. Repository at commit `b3702ef` (or a later green `main`). 3. Each step starts from a new, empty `Inventory()` from `scm_sim.inventory`. |
| Test data | Made-up IDs as used in the test code: warehouses `WH1`, `WH2`; SKUs `SKU1`, `SKU2` (equivalent to `WH-NORTH` / `WIDGET` in the demo). Quantities: 50, 20, 5, 10, 60, 40, 41, 1 000 000. Capacities: 100 for `WH1` in steps 4–5, 10 for `WH1` in step 6. |
| Objective | Prove that the Inventory records stock correctly, never lets stock fall below 0, and never lets a registered warehouse exceed its capacity, while unregistered warehouses are unlimited. |
| Steps | 1. `add("WH1", "SKU1", 50)`. 2. With 50 in stock, `remove("WH1", "SKU1", 20)`. 3. With 5 in stock, `remove("WH1", "SKU1", 10)`. 4. `register_warehouse("WH1", 100)`; `add("WH1", "SKU1", 60)`; `add("WH1", "SKU2", 40)`; read `total_in_warehouse("WH1")`. 5. `register_warehouse("WH1", 100)`; `add("WH1", "SKU1", 60)`; `add("WH1", "SKU2", 41)`; read `level` of both SKUs and `total_in_warehouse("WH1")`. 6. `register_warehouse("WH1", 10)`; `add("WH2", "SKU1", 1_000_000)`. |
| Expected result | 1. Returns 50. 2. Returns 30. 3. Raises `InsufficientStockError`. 4. The second add returns 40; the warehouse total is exactly 100 (adding up to capacity is allowed). 5. The second add raises `CapacityExceededError`; afterwards `level("WH1", "SKU1") == 60`, `level("WH1", "SKU2") == 0` and the total is 60 (stock unchanged). 6. Returns 1 000 000 (the unregistered `WH2` has no limit). |
| Pass/fail criteria | **Pass** if every step gives exactly the expected return value or exception and all pytest tests listed below pass. **Fail** if any value differs, the wrong exception (or none) is raised, or stock changes after a rejected call. |
| Automated by | `tests/test_inventory.py::test_add_and_level`, `tests/test_inventory.py::test_remove_reduces_stock`, `tests/test_inventory.py::test_remove_too_much_raises`, `tests/test_inventory.py::test_add_up_to_exact_capacity_is_allowed`, `tests/test_inventory.py::test_add_beyond_capacity_raises_and_leaves_stock_unchanged`, `tests/test_inventory.py::test_unregistered_warehouse_has_unlimited_capacity`. Supporting: `test_stockout_detected`, `test_register_warehouse_rejects_non_positive_capacity`, `test_total_in_warehouse_sums_all_skus`, `test_existing_behaviour_unchanged_with_capacity_registered` (quantity 0 rejected with `ValueError`; stockout after removing all stock) |
| Actual result | Pass (CI run #20, commit b3702ef) |
| Status | Passed |

**Coverage note.** Two parts of AC-SCM-F-001 are correct in the code but not yet asserted by an automated test: `remove(…, 0)` raising `ValueError`, and the stock level staying unchanged after `InsufficientStockError`. Both were verified by a manual script against commit `b3702ef` on 11-10-2026. A follow-up PR by the module owner should add these assertions to `tests/test_inventory.py` so that CI checks them on every change.
