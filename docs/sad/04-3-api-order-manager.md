### 4.3.2 Order Manager API (`scm_sim.orders`)

This section documents the public interface, parameters, return types, exception behaviors, and usage examples for `OrderManager`, `Order`, and `OrderStatus`.

---

#### 1. `OrderStatus` (Enum)
String-backed enumeration representing the lifecycle progression of customer orders.
- **Values:**
  - `OrderStatus.PENDING`: Initial status upon order creation.
  - `OrderStatus.FULFILLED`: Order has been satisfied in full from inventory.
  - `OrderStatus.BACKORDERED`: Fulfillment attempted but deferred due to insufficient stock.
  - `OrderStatus.CANCELLED`: Order was revoked before fulfillment.

---

#### 2. `Order` (Dataclass)
Data model encapsulating customer order state.
- **Fields:**
  - `order_id: str`: Unique identifier formatted as `"ORD-NNNN"` (e.g., `"ORD-0001"`).
  - `customer_id: str`: Identifier for the placing customer (e.g., `"C-ACME"`).
  - `warehouse_id: str`: Target warehouse fulfilling the order (e.g., `"WH-NORTH"`).
  - `sku: str`: Item SKU requested (e.g., `"WIDGET"`).
  - `quantity: int`: Positive integer quantity requested.
  - `created_day: int`: Simulation day on which the order was created.
  - `status: OrderStatus`: Current lifecycle state (defaults to `OrderStatus.PENDING`).
  - `fulfilled_day: Optional[int]`: Day of successful fulfillment (defaults to `None`).
- **Raises:**
  - `ValueError`: If `quantity <= 0` during initialization.

---

#### 3. `OrderManager(inventory)`
Instantiates an `OrderManager` bound to an `Inventory` instance.
- **Signature:** `OrderManager(inventory: Inventory) -> OrderManager`
- **Parameters:**
  - `inventory` (`Inventory`): The active inventory component used for stock checks and deductions.
- **Returns:** A new `OrderManager` instance.
- **Raises:** None.
- **Example:**
```python
from scm_sim.inventory import Inventory
from scm_sim.orders import OrderManager

inv = Inventory()
orders = OrderManager(inv)
```

---

#### 4. `create(customer_id, warehouse_id, sku, quantity, day)`
Creates, assigns a sequential identifier to, and records a new customer order.
- **Signature:** `create(customer_id: str, warehouse_id: str, sku: str, quantity: int, day: int) -> Order`
- **Parameters:**
  - `customer_id` (`str`): Unique customer identifier.
  - `warehouse_id` (`str`): Fulfilling warehouse identifier.
  - `sku` (`str`): SKU of the requested item.
  - `quantity` (`int`): Quantity demanded (must be $> 0$).
  - `day` (`int`): Current simulation day.
- **Returns:** The newly instantiated `Order` object with status `OrderStatus.PENDING`.
- **Raises:**
  - `ValueError`: If `quantity <= 0`.
- **Example:**
```python
order = orders.create("C-ACME", "WH-NORTH", "WIDGET", 50, day=1)
assert order.order_id == "ORD-0001"
assert order.status == OrderStatus.PENDING
```

---

#### 5. `get(order_id)`
Retrieves an order by its unique identifier.
- **Signature:** `get(order_id: str) -> Order`
- **Parameters:**
  - `order_id` (`str`): Identifier of the order to look up (e.g., `"ORD-0001"`).
- **Returns:** The matching `Order` object.
- **Raises:**
  - `KeyError`: If `order_id` is not tracked by the manager.
- **Example:**
```python
order = orders.get("ORD-0001")
print(order.status)
```

---

#### 6. `try_fulfil(order, day)`
Attempts to fulfill an order immediately against warehouse inventory.
- **Signature:** `try_fulfil(order: Order, day: int) -> bool`
- **Parameters:**
  - `order` (`Order`): The order to fulfill.
  - `day` (`int`): Current simulation day.
- **Returns:**
  - `True`: If stock was sufficient, stock was deducted via `inventory.remove()`, and status changed to `FULFILLED`.
  - `False`: If stock was insufficient (status set to `BACKORDERED`, stock untouched) or if the order was already `FULFILLED` or `CANCELLED` (state unchanged).
- **Raises:** None.
- **Example:**
```python
success = orders.try_fulfil(order, day=1)
if not success:
    print(f"Order {order.order_id} backordered.")
```

---

#### 7. `process_open(day)`
Retries fulfillment for all `PENDING` and `BACKORDERED` orders using strict oldest-first FIFO priority.
- **Signature:** `process_open(day: int) -> list[Order]`
- **Parameters:**
  - `day` (`int`): Current simulation day.
- **Returns:** A list containing all `Order` objects newly transitioned to `FULFILLED` during this retry pass.
- **Raises:** None.
- **Example:**
```python
newly_fulfilled = orders.process_open(day=3)
for o in newly_fulfilled:
    print(f"Fulfilled {o.order_id} on day {o.fulfilled_day}")
```

---

#### 8. `cancel(order_id)`
Revokes an unfulfilled order.
- **Signature:** `cancel(order_id: str) -> Order`
- **Parameters:**
  - `order_id` (`str`): Identifier of the order to cancel.
- **Returns:** The cancelled `Order` object with status `OrderStatus.CANCELLED`.
- **Raises:**
  - `ValueError`: If the order has already achieved `OrderStatus.FULFILLED`.
  - `KeyError`: If `order_id` is unknown.
- **Example:**
```python
cancelled_order = orders.cancel("ORD-0001")
assert cancelled_order.status == OrderStatus.CANCELLED
```

---

#### 9. `by_status(status)`
Returns all tracked orders matching the specified lifecycle state.
- **Signature:** `by_status(status: OrderStatus) -> list[Order]`
- **Parameters:**
  - `status` (`OrderStatus`): Target status filter.
- **Returns:** A list of `Order` objects whose current status matches `status`.
- **Raises:** None.
- **Example:**
```python
backorders = orders.by_status(OrderStatus.BACKORDERED)
print(f"Total active backorders: {len(backorders)}")
```
