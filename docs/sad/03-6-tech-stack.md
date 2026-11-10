### 3.6 Technology Stack and Data Stores

#### 3.6.1 Technology Stack
The simulator is engineered intentionally with minimal runtime complexity to maximize execution speed, maintainability, and cross-platform portability.

| Technology Dimension | Selection | Version / Standard | Architectural Role & Rationale |
|---|---|---|---|
| Programming Language | Python | $\ge 3.11$ | Core language runtime; uses type hints, dataclasses, enums and standard-library CLI, CSV and random-number facilities. |
| Packaging | setuptools / `pyproject.toml` | `setuptools>=68` build backend | Installable `src`-layout package `scm-sim`; exposes the `scm-sim` console script and `python -m scm_sim` module entry point. Build tooling is not a runtime dependency. |
| Runtime Dependencies | Python Standard Library | Standard Library Only | Zero third-party runtime dependencies. Uses `dataclasses`, `enum`, `random`, `argparse`, `csv` and `typing`. |
| Testing Framework | pytest | $\ge 8.0$ | Automated test discovery, test parameterization, fixture execution, and assertion introspection. |
| Code Coverage Tool | pytest-cov | $\ge 5.0$ | CI measures statement and branch coverage and fails the test job below the configured 90% coverage threshold. |
| Continuous Integration | GitHub Actions | `ubuntu-latest`, Python 3.11 | Workflow installs test dependencies and the package, then runs the full suite with branch coverage on pushes to `main` and pull requests targeting `main`; test and coverage artifacts are uploaded. |
| Version Control | Git / GitHub | Git v2.40+ | Distributed source control with protected branch policies, peer-reviewed pull requests, and commit traceability. |
| Modeling & Diagrams | PlantUML | PlantUML 1.2023+ | Text-as-code modeling tool generating UML component, class, and sequence diagrams. |

#### 3.6.2 Data Stores
Simulation state is held in **in-memory data structures**; there is no database or runtime network storage. The CLI's optional `--csv PATH` flag writes an explicit user-requested metrics export, and CI writes test/coverage artifacts:
1. **Inventory Stock Map:** Stored within `Inventory._stock` as a Python dictionary keyed by composite tuple `(warehouse_id: str, sku: str)` mapping to current integer quantity (`int >= 0`).
2. **Warehouse Capacity Registry:** Stored within `Inventory._capacity` as a Python dictionary keyed by `warehouse_id: str` mapping to maximum integer capacity (`int > 0`).
3. **Stock Policies Registry:** Stored within `Inventory._policies` as a dictionary keyed by `(warehouse_id: str, sku: str)` mapping to `StockPolicy` dataclass instances.
4. **Order Registry:** Stored within `OrderManager._orders` as a dictionary keyed by `order_id: str` (e.g., `"ORD-0001"`) mapping to `Order` dataclass instances.
5. **Shipment Collection:** Stored within `ShipmentManager._shipments` as a Python list containing tracked `Shipment` dataclass instances.
6. **Supplier Registry:** Stored within `ShipmentManager._suppliers` as a dictionary keyed by `supplier_id: str` mapping to `Supplier` dataclass instances.

The simulation data stores are volatile and reside within process memory. Each new `Simulation` initializes fresh state; CSV and CI artifacts are outputs, not simulation-state stores.
