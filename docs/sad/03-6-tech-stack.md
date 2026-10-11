### 3.6 Technology Stack and Data Stores

#### 3.6.1 Technology Stack
The simulator is engineered intentionally with minimal runtime complexity to maximize execution speed, maintainability, and cross-platform portability.

| Technology Dimension | Selection | Version / Standard | Architectural Role & Rationale |
|---|---|---|---|
| Programming Language | Python | $\ge 3.11$ | Core language runtime. Employs modern type hinting, pattern matching, dataclasses, and optimized CPython execution. |
| Runtime Dependencies | Python Standard Library | Standard Library Only | Zero third-party runtime dependencies. Uses `dataclasses` for domain models, `enum` for typed states, `random` for seed-driven determinism, and `argparse` for CLI commands. |
| Testing Framework | pytest | $\ge 8.0$ | Automated test discovery, test parameterization, fixture execution, and assertion introspection. |
| Code Coverage Tool | pytest-cov | $\ge 5.0$ | Continuous verification of test coverage across statement and branch paths (enforcing the $\ge 90\%$ threshold). |
| Continuous Integration | GitHub Actions | Ubuntu Latest | Continuous integration engine triggering automated test suites and coverage analysis on every push and pull request. |
| Version Control | Git / GitHub | Git v2.40+ | Distributed source control with protected branch policies, peer-reviewed pull requests, and commit traceability. |
| Modeling & Diagrams | PlantUML | PlantUML 1.2023+ | Text-as-code modeling tool generating UML component, class, and sequence diagrams. |

#### 3.6.2 Data Stores
The system operates exclusively using **in-memory data structures**, with zero reliance on external database servers, disk files, or network services:
1. **Inventory Stock Map:** Stored within `Inventory._stock` as a Python dictionary keyed by composite tuple `(warehouse_id: str, sku: str)` mapping to current integer quantity (`int >= 0`).
2. **Warehouse Capacity Registry:** Stored within `Inventory._capacities` as a Python dictionary keyed by `warehouse_id: str` mapping to maximum integer capacity (`int > 0`).
3. **Stock Policies Registry:** Stored within `Inventory._policies` as a dictionary keyed by `(warehouse_id: str, sku: str)` mapping to `StockPolicy` dataclass instances.
4. **Order Registry:** Stored within `OrderManager._orders` as a dictionary keyed by `order_id: str` (e.g., `"ORD-0001"`) mapping to `Order` dataclass instances.
5. **Shipment Collection:** Stored within `ShipmentManager._shipments` as a Python list containing tracked `Shipment` dataclass instances.
6. **Supplier Registry:** Stored within `ShipmentManager._suppliers` as a dictionary keyed by `supplier_id: str` mapping to `Supplier` dataclass instances.

All data stores are volatile and reside within process heap memory. Simulation re-execution initializes brand-new empty data structures, ensuring absolute test isolation and zero state pollution between simulation runs.
