# Test Result: TC-SEC-01 Public Input Validation and State Tamper Resistance

| Field | Value |
|---|---|
| Test case | TC-SEC-01 |
| Requirement(s) | SCM-SR-001, SCM-SR-002, SCM-SR-003, SCM-SR-004, SCM-SR-007 (SCM-SO-1) |
| Executed by | Rishi J Mule (Security Test Engineer) |
| Date | 10-11-2026 |
| Commit tested | 2f6d382 |
| Environment | Windows 11 (10.0.26300), Python 3.11.9, pytest 9.2.0 |
| Result | PASS |

## Steps and observations

| # | Step | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | SCM-SR-001: Boundary and input parameter validation | Domain operations (`Inventory.add`, `Inventory.remove`, `OrderManager.create`, `ShipmentManager.dispatch`) reject non-positive quantities and invalid parameters with `ValueError` before state changes | All invalid boundary inputs (≤ 0 quantities, negative lead times, invalid reliabilities) raise `ValueError`; verified by `test_remove_rejects_non_positive_quantity`, `test_reject_non_positive_quantity`, `test_invalid_quantity`, and `test_order_dataclass_rejects_non_positive_quantity_directly`. State remains unmodified. | PASS |
| 2 | SCM-SR-002: Stock invariants and capacity enforcement | Stock never drops below 0 and never exceeds registered warehouse capacity; exceeding capacity raises `CapacityExceededError`. In arrivals, overflowing shipments stay `IN_TRANSIT` (#70) | `InsufficientStockError` raised on over-withdrawal; `CapacityExceededError` raised on overflow; overflowing arrivals stay in transit without aborting other shipments; verified by `test_remove_too_much_raises`, `test_add_beyond_capacity_raises_and_leaves_stock_unchanged`, and `test_capacity_breach_does_not_abort_other_arrivals`. | PASS |
| 3 | SCM-SR-003: Guarded order lifecycle state machine | Order state transitions follow strict status guards: cancelling a `FULFILLED` order or fulfilling a `CANCELLED` order is prohibited | `ValueError` raised on illegal transitions; terminal orders (`FULFILLED`, `CANCELLED`) are never reprocessed; verified by `test_cancel_rules` and `test_fulfilled_or_cancelled_orders_are_never_reprocessed`. | PASS |
| 4 | SCM-SR-004: Unknown entity reference validation | Unknown entity references (supplier, warehouse, or order IDs) raise `KeyError` prior to mutation | Operations referencing non-existent IDs raise `KeyError`; verified by `test_add_supplier_and_reject_duplicate_and_unknown`, `test_schedule_order_validates_input`, `test_get_unknown_order_raises_key_error`, and `test_set_policy_rejects_unknown_supplier`. | PASS |
| 5 | SCM-SR-007: Defensive copy and snapshot isolation | Calling `Inventory.snapshot()` returns an independent copy that isolates internal state against external mutation | Modifying keys or nested mappings of returned snapshot has zero effect on internal inventory state; verified by `test_snapshot_returns_independent_copy`. | PASS |

## Evidence

- Automated suite: 100 passing tests (`python -m pytest -q`)
- All security test methods passing in `tests/test_inventory.py`, `tests/test_orders.py`, `tests/test_shipments.py`, and `tests/test_simulator.py`
- Zero security invariant violations observed across all 10-day and multi-day simulation runs

## Notes

All automated security tests verified on Python 3.11 with 100% pass rate.

