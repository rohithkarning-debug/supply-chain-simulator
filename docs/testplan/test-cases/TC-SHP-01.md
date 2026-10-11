| Field | Content |
| :--- | :--- |
| **TC ID** | TC-SHP-01 |
| **Title** | Supplier Validation, Identifier Sequencing, and Dispatch Lead-Time Computation |
| **Requirement(s)** | SCM-F-020, SCM-F-021 |
| **Type** | Functional |
| **Objective** | Verify that supplier registration enforces ID uniqueness and parameter constraints, that shipments generate sequential IDs formatted as `SHP-XXXX`, and that expected arrival days correctly reflect dispatch day plus supplier lead time. |
| **Preconditions** | An initialized `Inventory` instance and an instantiated `ShipmentManager`. |
| **Test data** | Suppliers `SUP-01` (lead_time_days=2, reliability=1.0), `SUP-02` (lead_time_days=3); warehouse `WH-01`; SKU `SKU-01`; quantity=50; dispatch day=2. |
| **Steps** | 1. Instantiate `Supplier` with valid and invalid bounds (lead_time < 0, reliability < 0.0 or > 1.0).<br>2. Register `SUP-01` with `ShipmentManager.add_supplier()` and attempt duplicate registration.<br>3. Dispatch a shipment with an unregistered supplier ID `SUP-999`.<br>4. Dispatch two shipments with positive quantities from `SUP-01` and verify generated IDs.<br>5. Dispatch with quantity `<= 0` and verify exception handling.<br>6. Dispatch from `SUP-02` (lead time 3) on day 2 and verify `expected_day`. |
| **Expected result** | Invalid parameters and duplicate supplier registrations raise `ValueError`; unknown supplier dispatches raise `KeyError`; non-positive quantities raise `ValueError`; generated shipment IDs follow `SHP-0001`, `SHP-0002`; `expected_day` strictly equals `2 + 3 = 5`. |
| **Pass/fail criteria** | **Pass** if all assertions hold and exceptions are raised without state mutation; **Fail** if invalid parameters are accepted, IDs collide, or `expected_day` is miscalculated. |
| **Automated by** | `tests/test_shipments.py::test_supplier_validation`<br>`tests/test_shipments.py::test_add_supplier_and_reject_duplicate_and_unknown`<br>`tests/test_shipments.py::test_expected_day_calculated_from_lead_time`<br>`tests/test_shipments.py::test_shipment_id_sequence_and_in_transit_filtering`<br>`tests/test_shipments.py::test_reject_non_positive_quantity` |
| **Actual result** | Pass (CI run #20, commit `b3702ef`) |
| **Status** | Passed |
