### 4.1 Design Overview

#### Simulation Paradigm
The Supply Chain Management Simulator employs a **discrete-time, day-by-day stepped simulation engine**. Rather than continuous time or complex asynchronous event queues, the simulation clock advances strictly in discrete integer units of simulated days ($t = 0, 1, 2, \dots, N$).

The primary facade orchestrating this lifecycle is `scm_sim.simulator.Simulation`. On each day tick, the simulation executes a deterministic, 5-stage sequence designed to model real-world physical and commercial supply chain flows.

#### The 5-Stage Daily Execution Sequence (`Simulation.step()`)

Every call to `Simulation.step()` advances the internal day counter by 1 and executes the following operations in a strictly enforced order:

```
  +------------------------------------------------------------------------+
  |                   Day t: Simulation.step() Pipeline                   |
  +------------------------------------------------------------------------+
                                      |
  [Stage 1: Inbound Receiving]        v
  ShipmentManager.process_arrivals(day) ---> Inventory.add(warehouse, sku, qty)
                                      |
  [Stage 2: Customer Orders]          v
  For orders scheduled for day:
    OrderManager.create(...) ---------> OrderManager.try_fulfil(...)
                                      |
  [Stage 3: Back-order Retry]         v
  OrderManager.process_open(day) -----> Inventory.remove(...) [FIFO Priority]
                                      |
  [Stage 4: Automated Replenishment]  v
  Inventory.reorder_suggestions() ---> Check in-transit & trim to capacity
                                  ---> ShipmentManager.dispatch(...)
                                      |
  [Stage 5: Analytics & Logging]      v
  analytics.build_report(...) -------> Stored in DayLog event history
                                      v
                             [Return Day Report]
```

1. **Stage 1: Inbound Receiving (Shipment Arrivals):**
   - The engine triggers `ShipmentManager.process_arrivals(self.day)`.
   - Any shipment in transit whose `arrival_day <= self.day` is delivered.
   - For each arriving shipment, units are credited to warehouse inventory via `Inventory.add(warehouse_id, sku, quantity)`.
   - The shipment status transitions to `DELIVERED` and `actual_day` is set to `self.day`.
   - *Rationale:* Stock must physically arrive at the warehouse before customer orders for the day are evaluated.

2. **Stage 2: Customer Order Processing:**
   - The engine iterates through customer orders pre-scheduled for the current day.
   - For each scheduled order, `OrderManager.create(...)` registers the order with initial status `PENDING`.
   - `OrderManager.try_fulfil(...)` immediately attempts fulfillment:
     - If `Inventory.level(warehouse, sku) >= quantity`: units are removed from inventory via `Inventory.remove()`, status is set to `FULFILLED`, and `fulfilled_day` is recorded.
     - If stock is insufficient: status transitions to `BACKORDERED` with stock level left unchanged (no partial fulfillment).

3. **Stage 3: Back-order Re-evaluation:**
   - The engine calls `OrderManager.process_open(self.day)` to re-evaluate all unresolved `PENDING` and `BACKORDERED` orders.
   - Orders are processed in strict priority sequence: oldest `created_day` first, with ties broken by ascending `order_id` (FIFO fairness).
   - Any newly replenished stock from Stage 1 that was not consumed in Stage 2 is allocated to older backlog orders.

4. **Stage 4: Automated Replenishment Evaluation:**
   - The engine queries `Inventory.reorder_suggestions()` to identify tracked items whose stock is at or below their configured `StockPolicy.reorder_point`.
   - For each candidate item, the engine verifies that no replenishment shipment is already in transit for that `(warehouse, sku)` pair (preventing redundant double-orders).
   - The replenishment quantity (`StockPolicy.reorder_quantity`) is evaluated against warehouse storage limits: if adding the full batch would breach warehouse capacity, the order quantity is trimmed to fit available capacity.
   - If positive capacity exists, `ShipmentManager.dispatch(...)` is invoked to schedule the shipment with the designated supplier, computing lead time and stochastic delays.

5. **Stage 5: Analytics & Reporting:**
   - The engine queries `Inventory.snapshot()`, `ShipmentManager._shipments.values()`, and `OrderManager._orders.values()`.
   - It invokes the pure function `analytics.build_report(...)`, compiling stockout lists, low-stock alerts, excess inventory levels, late shipment delays, and order fill-rate statistics.
   - The resulting report dictionary is stored in the simulation history (`DayLog`) and returned to the caller.

#### Data Flow and Subsystem Decoupling
The architecture enforces unidirectional data dependencies to maximize testability and eliminate circular couplings:
- `Inventory`: Fundamental state provider; has zero dependencies on other simulation modules.
- `OrderManager`: Depends strictly on `Inventory` for stock balance queries and withdrawals.
- `ShipmentManager`: Depends strictly on `Inventory` for crediting arrived goods.
- `Analytics`: Completely stateless; accepts raw data structures and snapshots, with no dependencies on internal manager state.
- `Simulation`: High-level orchestrator mediating interactions between domain managers and the analytics pipeline.
