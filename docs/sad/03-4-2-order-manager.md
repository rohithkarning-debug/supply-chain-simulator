### 3.4.2 Order Manager (`scm_sim.orders`)

#### Responsibility
The `OrderManager` component is the domain authority for customer demand lifecycle management. It encapsulates the creation, indexing, state tracking, fulfillment, retry scheduling, and cancellation of customer orders. It serves as an intermediary between simulation demand events and warehouse physical stock, enforcing the business rule that order quantities must be fulfilled in their entirety or backordered without partial deduction.

#### Inputs and Outputs
- **Inputs:**
  - Order creation parameters: `customer_id` (str), `warehouse_id` (str), `sku` (str), `quantity` (int > 0), and simulation `day` (int).
  - Fulfillment and retry invocations: simulation `day` (int) and target `Order` instances.
  - Query and cancellation parameters: `order_id` (str) and `OrderStatus` filter criteria.
- **Outputs:**
  - Newly instantiated `Order` records assigned sequential IDs (`ORD-0001`, `ORD-0002`, ...).
  - Boolean fulfillment status flags (`True` for success, `False` for shortage/ineligibility).
  - Lists of newly fulfilled `Order` objects returned by batch retry operations (`process_open()`).
  - Filtered collections of orders partitioned by current lifecycle state (`by_status()`).

#### Dependencies
- **Depends on:** `scm_sim.inventory.Inventory`. The `OrderManager` directly queries `Inventory.level(warehouse, sku)` to evaluate stock availability and calls `Inventory.remove(warehouse, sku, qty)` to atomically deduct stock upon successful fulfillment.
- **Depended on by:** `scm_sim.simulator.Simulation`. The simulation orchestrator calls `OrderManager.create()`, `OrderManager.try_fulfil()`, and `OrderManager.process_open()` during its daily execution cycle.
- **Read by:** `scm_sim.analytics.order_metrics()`. The analytics engine consumes lists of `Order` entities to evaluate fill rate performance.

#### Requirements Satisfied
- `SCM-F-010`: Sequential order ID assignment (`ORD-0001`...) and positive quantity validation.
- `SCM-F-011`: Full-quantity fulfillment against inventory; automatic transition to `BACKORDERED` upon stock shortfall.
- `SCM-F-012`: FIFO batch retry of open (`PENDING` and `BACKORDERED`) orders sorted by `(created_day, order_id)`.
- `SCM-F-013`: Guarded cancellation (forbidding cancellation of `FULFILLED` orders), unique lookup (`get`), and status filtering (`by_status`).
- `SCM-SR-001`, `SCM-SR-003`: Fail-fast input validation and protected state transitions.
