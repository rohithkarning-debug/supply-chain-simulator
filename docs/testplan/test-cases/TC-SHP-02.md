| Field | Content |
| :--- | :--- |
| **TC ID** | TC-SHP-02 |
| **Title** | Stochastic Delay Modeling, Inbound Physical Receiving, and Delay Detection |
| **Requirement(s)** | SCM-F-022, SCM-F-023 |
| **Type** | Functional |
| **Objective** | Verify that supplier reliability governs delay probabilities, that shipments are received into inventory only on or after their arrival day via `Inventory.add()`, and that `delayed()` accurately detects both in-transit late and delivered late shipments. |
| **Preconditions** | An initialized `Inventory` instance and an instantiated `ShipmentManager`. |
| **Test data** | Suppliers `SUP-01` (reliability=1.0, lead_time=2), `SUP-SLOW` (reliability=0.0, lead_time=2); destination `WH-01`; item `SKU-01`; quantities 40, 75, 100; explicit delays 0 and 2. |
| **Steps** | 1. Dispatch with `delay=0` on day 1 (arrival day 3) and call `process_arrivals(2)` and `process_arrivals(3)`. Verify stock and status.<br>2. Dispatch with `delay=2` on day 1 (expected day 3, arrival day 5). Call `process_arrivals(3)` and verify shipment is not delivered early.<br>3. Inspect `days_late()` across days 1 to 5, querying `ShipmentManager.delayed()`.<br>4. Dispatch 20 shipments from `SUP-01` (`reliability=1.0`) across distinct PRNG seeds without explicit delay arguments.<br>5. Dispatch from `SUP-SLOW` (`reliability=0.0`) and verify delay values. |
| **Expected result** | On-time shipments deliver on expected day, incrementing inventory and setting status `DELIVERED`; delayed shipments do not arrive early; `delayed()` flags in-transit late shipments on day 4 and delivered late shipments on day 5; reliability 1.0 never delays; reliability 0.0 experiences delays in {1, 2, 3}. |
| **Pass/fail criteria** | **Pass** if stock is updated solely via `inventory.add()`, arrival timing is strictly respected, and all delay calculations evaluate correctly; **Fail** if premature delivery occurs, inventory is corrupted, or delays are miscalculated. |
| **Automated by** | `tests/test_shipments.py::test_on_time_arrival_adds_stock`<br>`tests/test_shipments.py::test_delayed_shipment_not_delivered_early`<br>`tests/test_shipments.py::test_delayed_detection_both_in_transit_late_and_delivered_late`<br>`tests/test_shipments.py::test_reliability_one_means_never_delayed`<br>`tests/test_shipments.py::test_probabilistic_delay_with_zero_reliability` |
| **Actual result** | Pass (CI run #20, commit `b3702ef`) |
| **Status** | Passed |
