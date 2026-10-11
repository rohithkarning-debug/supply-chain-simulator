### 6. Test Environment

#### 6.1 Hardware Configuration
Test execution is performed across local development workstations and hosted cloud runners:
- **Local Developer Machines:** Standard engineering laptops running Windows 11 (64-bit) and Ubuntu 22.04 LTS; minimum 8 GB physical RAM, 2.0 GHz multi-core processor, and 500 MB available disk storage.
- **Continuous Integration Runners:** GitHub Actions cloud runners running `ubuntu-latest` with standard 2-core virtual CPU and 7 GB RAM.

#### 6.2 Software Configuration and Runtime
- **Operating Systems:**
  - Local: Microsoft Windows 11 (Build 22631) and Ubuntu Linux 22.04 LTS.
  - Remote CI: Ubuntu Linux (latest release).
- **Python Runtime:** Python 3.11.9 (64-bit). All team members and CI runners operate on Python 3.11 to maintain exact interpreter parity.
- **Virtual Environment:** Dedicated `.venv` created via Python standard library `venv` module to isolate test packages from global system interpreters.

#### 6.3 Test Tools and Utilities
- **Test Framework:** `pytest >= 8.0` (active version: 9.1.1) executing unit, integration, and system test suites.
- **Coverage Tool:** `pytest-cov >= 5.0` (active version: 7.1.0) generating statement and branch coverage metrics.
- **Defect Tracking:** GitHub Issues integrated into the team repository for logging, prioritizing, and resolving defects.
- **Version Control:** Git 2.51.1 coordinating local development and GitHub remote repository synchronization.

#### 6.4 Test Data and Fixtures
All test data is purely synthetic and generated deterministically in memory:
- **Pre-configured Simulation Scenario (`build_demo(seed=42)`):**
  - **Suppliers:** `SUP-RELIABLE` (lead time: 2, reliability: 1.0), `SUP-FLAKY` (lead time: 2, reliability: 0.3).
  - **Warehouses:** `WH-NORTH` (capacity: 1200), `WH-SOUTH` (capacity: 500).
  - **SKUs:** `WIDGET`, `GADGET`, `GIZMO`.
  - **Orders:** 14 scheduled customer orders distributed across simulation days 1 to 10.
- **Unit Test Fixtures:** Isolated in-memory objects initialized per test function (`WH1`, `WH2`, `SKU1`, `C-ACME`) with zero persistent filesystem or database state.
