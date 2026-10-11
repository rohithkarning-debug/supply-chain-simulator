### 3.4.3 Shipment Manager Component

#### Component Overview
The **Shipment Manager** (`scm_sim.shipments.ShipmentManager`) is the domain component responsible for supplier registries, dispatching inbound replenishment shipments, simulating lead times and stochastic transit delays, delivering arriving shipments into warehouse inventory, and tracking overdue physical movements.

#### Architectural Responsibilities
1. **Supplier Registration and Validation:** Maintains the registry of external supply partners, enforcing uniqueness and validating operational parameters (non-negative lead times and valid reliability probability bounds).
2. **Replenishment Dispatching:** Instantiates and schedules inbound shipments from suppliers to destination warehouses, generating sequential IDs (`SHP-0001`, `SHP-0002`, ...), calculating scheduled arrival days, and initializing status to `IN_TRANSIT`.
3. **Stochastic Transit Delay Simulation:** Employs an injected pseudorandom number generator (`random.Random`) to simulate realistic supply chain delivery variability based on individual supplier reliability ratings.
4. **Physical Inbound Receiving (Arrival Processing):** Delivers due shipments on or after their arrival day, transferring stock into warehouse inventory solely via `Inventory.add()` and transitioning status to `DELIVERED`.
5. **Overdue and In-Transit Inquiries:** Exposes query operations for active in-transit stock movements and overdue shipments for downstream analytics and exception monitoring.

#### Inputs and Outputs
- **Inputs:**
  - `Supplier` definitions: `supplier_id` (str), `name` (str), `lead_time_days` (int >= 0), `reliability` (float in [0.0, 1.0]).
  - Dispatch parameters: `supplier_id`, `warehouse_id`, `sku`, `quantity` (> 0), `day` (current simulation day), and optional explicit `delay` (int).
  - Daily progression triggers: `day` (current simulation day).
- **Outputs:**
  - Created `Shipment` instances.
  - Lists of `Shipment` objects delivered on a given day (`process_arrivals(day)`).
  - Lists of currently in-transit shipments (`in_transit()`).
  - Lists of currently overdue shipments (`delayed(current_day)`).

#### Collaborators and Dependencies
- **`scm_sim.inventory.Inventory`:** Collaborates with inventory by invoking `inventory.add(warehouse_id, sku, quantity)` when inbound shipments reach their destination. Never directly manipulates internal inventory dictionaries.
- **`random.Random` (Python Standard Library):** Utilizes an injected instance of `random.Random` (defaulting to seed 42) to ensure repeatable, deterministic delay modeling across simulation executions.

#### Internal State Structures
- `_suppliers: Dict[str, Supplier]`: Hash map storing registered `Supplier` objects keyed by `supplier_id`.
- `_shipments: Dict[str, Shipment]`: Hash map storing all created shipments keyed by `shipment_id`.
- `_next_id: int`: Internal auto-increment integer counter ensuring sequential, non-colliding shipment IDs formatted as `SHP-{self._next_id:04d}`.

#### Delay Model Specification
The delivery timeline for each dispatched shipment is computed as follows:
1. **Expected Arrival Day:** `expected_day = day + supplier.lead_time_days`
2. **Delay Calculation:**
   - If an explicit `delay` integer is provided: `delay = delay`
   - If `delay is None`:
     $$\text{delay} = \begin{cases} \text{rng.randint}(1, 3), & \text{if } \text{rng.random}() > \text{supplier.reliability} \\ 0, & \text{otherwise} \end{cases}$$
3. **Actual Arrival Day:** `arrival_day = expected_day + delay`
4. **Reliability Invariant:** When `supplier.reliability == 1.0`, `rng.random() > 1.0` is mathematically impossible, guaranteeing `delay = 0` and on-time arrival.

#### Traceability to Requirements
- **Functional Requirements:** SCM-F-020, SCM-F-021, SCM-F-022, SCM-F-023.
- **Security & Quality Requirements:** SCM-SR-001 (fail-fast input validation), SCM-SR-004 (KeyError on unknown supplier), SCM-NF-002 (deterministic reproducibility via seeded PRNG).
