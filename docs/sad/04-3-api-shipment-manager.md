### 4.3.3 Shipment Manager API

The `scm_sim.shipments` module provides classes and enumerations for managing suppliers, dispatching goods, and tracking physical shipments.

---

#### 1. `ShipmentStatus`
* **Signature:** `class ShipmentStatus(str, Enum)`
* **Description:** Lifecycle state enumeration for shipments. Inherits from `str` to enable direct string comparison and JSON serialization.
* **Enumeration Members:**
  - `IN_TRANSIT = "IN_TRANSIT"`
  - `DELIVERED = "DELIVERED"`

---

#### 2. `Supplier`
* **Signature:** `Supplier(supplier_id: str, name: str, lead_time_days: int = 2, reliability: float = 1.0)`
* **Parameters:**
  - `supplier_id` (*str*): Unique alphanumeric identifier for the supplier.
  - `name` (*str*): Descriptive name of the supplier company.
  - `lead_time_days` (*int*, optional): Baseline transit duration in simulated days. Default is 2. Must be `>= 0`.
  - `reliability` (*float*, optional): On-time arrival probability in range `[0.0, 1.0]`. Default is 1.0.
* **Returns:** Initialized `Supplier` dataclass instance.
* **Raises:**
  - `ValueError`: If `lead_time_days < 0` or if `reliability` is outside `[0.0, 1.0]`.
* **Example:**
  ```python
  from scm_sim.shipments import Supplier

  supplier = Supplier(
      supplier_id="SUP-FLAKY",
      name="Flaky Logistics Inc",
      lead_time_days=3,
      reliability=0.75,
  )
  ```

---

#### 3. `Shipment`
* **Signature:** `Shipment(shipment_id: str, supplier_id: str, warehouse_id: str, sku: str, quantity: int, dispatch_day: int, expected_day: int, arrival_day: int, actual_day: Optional[int] = None, status: ShipmentStatus = ShipmentStatus.IN_TRANSIT)`
* **Parameters:**
  - `shipment_id` (*str*): Unique shipment tracking ID (e.g., `"SHP-0001"`).
  - `supplier_id` (*str*): Originating supplier ID.
  - `warehouse_id` (*str*): Destination warehouse ID.
  - `sku` (*str*): Stock Keeping Unit code.
  - `quantity` (*int*): Number of units shipped. Must be `> 0`.
  - `dispatch_day` (*int*): Simulation day when shipment was dispatched.
  - `expected_day` (*int*): Scheduled arrival day (`dispatch_day + lead_time_days`).
  - `arrival_day` (*int*): Actual day the shipment will arrive (`expected_day + delay`).
  - `actual_day` (*Optional[int]*, optional): Day when shipment was physically received and added to inventory. Default is `None`.
  - `status` (*ShipmentStatus*, optional): Current lifecycle status. Default is `ShipmentStatus.IN_TRANSIT`.
* **Returns:** Initialized `Shipment` dataclass instance.
* **Raises:**
  - `ValueError`: If `quantity <= 0`.
* **Example:**
  ```python
  from scm_sim.shipments import Shipment, ShipmentStatus

  shp = Shipment(
      shipment_id="SHP-0001",
      supplier_id="SUP-RELIABLE",
      warehouse_id="WH-NORTH",
      sku="WIDGET",
      quantity=100,
      dispatch_day=1,
      expected_day=3,
      arrival_day=3,
  )
  ```

---

#### 4. `Shipment.delay_days` (Property)
* **Signature:** `@property def delay_days(self) -> int`
* **Parameters:** None.
* **Returns:** *int*: Number of days delayed past `expected_day` if delivered (`max(0, actual_day - expected_day)`); returns `0` if status is not `DELIVERED` or `actual_day is None`.
* **Raises:** None.
* **Example:**
  ```python
  print(shp.delay_days)  # 0 (while in transit)
  ```

---

#### 5. `Shipment.days_late(current_day: int)`
* **Signature:** `days_late(current_day: int) -> int`
* **Parameters:**
  - `current_day` (*int*): Current simulation day index.
* **Returns:** *int*: If `DELIVERED`, returns `self.delay_days`. If `IN_TRANSIT`, returns `max(0, current_day - self.expected_day)`.
* **Raises:** None.
* **Example:**
  ```python
  # Dispatched day 1, expected day 3. On day 4 while in transit:
  print(shp.days_late(4))  # 1
  ```

---

#### 6. `ShipmentManager.__init__`
* **Signature:** `ShipmentManager(inventory: Inventory, rng: Optional[random.Random] = None)`
* **Parameters:**
  - `inventory` (*Inventory*): Reference to the shared `Inventory` system instance.
  - `rng` (*Optional[random.Random]*, optional): Seeded pseudorandom number generator. Defaults to `random.Random(42)`.
* **Returns:** Initialized `ShipmentManager` instance.
* **Raises:** None.
* **Example:**
  ```python
  import random
  from scm_sim.inventory import Inventory
  from scm_sim.shipments import ShipmentManager

  inv = Inventory()
  mgr = ShipmentManager(inventory=inv, rng=random.Random(42))
  ```

---

#### 7. `ShipmentManager.add_supplier`
* **Signature:** `add_supplier(supplier: Supplier) -> None`
* **Parameters:**
  - `supplier` (*Supplier*): The supplier dataclass instance to register.
* **Returns:** `None`.
* **Raises:**
  - `ValueError`: If a supplier with `supplier.supplier_id` is already registered.
* **Example:**
  ```python
  mgr.add_supplier(Supplier("SUP-01", "Acme Supplier", lead_time_days=2))
  ```

---

#### 8. `ShipmentManager.dispatch`
* **Signature:** `dispatch(supplier_id: str, warehouse_id: str, sku: str, quantity: int, day: int, delay: Optional[int] = None) -> Shipment`
* **Parameters:**
  - `supplier_id` (*str*): Registered supplier identifier.
  - `warehouse_id` (*str*): Destination warehouse identifier.
  - `sku` (*str*): Product SKU code.
  - `quantity` (*int*): Positive integer quantity to ship (`> 0`).
  - `day` (*int*): Current simulation dispatch day.
  - `delay` (*Optional[int]*, optional): Explicit delay in days. If `None`, delay is sampled via `self.rng`.
* **Returns:** *Shipment*: Newly created shipment instance with ID `SHP-0001`, `SHP-0002`, etc.
* **Raises:**
  - `KeyError`: If `supplier_id` is not registered.
  - `ValueError`: If `quantity <= 0`.
* **Example:**
  ```python
  shp = mgr.dispatch("SUP-01", "WH-NORTH", "WIDGET", quantity=50, day=1)
  print(shp.shipment_id, shp.expected_day, shp.arrival_day)
  ```

---

#### 9. `ShipmentManager.process_arrivals`
* **Signature:** `process_arrivals(day: int) -> List[Shipment]`
* **Parameters:**
  - `day` (*int*): Current simulation day index.
* **Returns:** *List[Shipment]*: All shipments delivered today whose `arrival_day <= day` and were previously `IN_TRANSIT`.
* **Raises:**
  - `CapacityExceededError`: Propagated from `Inventory.add()` if receiving units exceeds warehouse capacity.
* **Example:**
  ```python
  delivered = mgr.process_arrivals(day=3)
  for s in delivered:
      print(f"Received {s.quantity} of {s.sku} at {s.warehouse_id}")
  ```

---

#### 10. `ShipmentManager.in_transit`
* **Signature:** `in_transit() -> List[Shipment]`
* **Parameters:** None.
* **Returns:** *List[Shipment]*: Filtered list of all shipments currently in `ShipmentStatus.IN_TRANSIT`.
* **Raises:** None.
* **Example:**
  ```python
  active_shipments = mgr.in_transit()
  ```

---

#### 11. `ShipmentManager.delayed`
* **Signature:** `delayed(current_day: int) -> List[Shipment]`
* **Parameters:**
  - `current_day` (*int*): Current simulation day index.
* **Returns:** *List[Shipment]*: List of all shipments with `days_late(current_day) > 0` (both in-transit late and delivered late).
* **Raises:** None.
* **Example:**
  ```python
  late_shipments = mgr.delayed(current_day=5)
  for s in late_shipments:
      print(f"{s.shipment_id} is {s.days_late(5)} day(s) late")
  ```
