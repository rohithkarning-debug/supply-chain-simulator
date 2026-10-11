### 3. External Interface Requirements

#### 3.1 User Interfaces
The system provides a command-line interface (CLI) as its sole user-facing interface. There is no graphical user interface (GUI) or web interface.

1. **Invocation and Command-Line Arguments:**
   - The user executes the simulator via the standard Python module entry point:
     ```bash
     python -m scm_sim [--days N] [--seed S]
     ```
   - **`--days N`:** The duration of the simulation run in simulated days (integer). If omitted, the demo defaults to 10 days. The system shall validate that `N >= 1`; if `N < 1`, the CLI shall display a standard usage error message and terminate with exit code 2.
   - **`--seed S`:** The integer seed for the pseudorandom number generator (defaults to 42). Enables deterministic reproducibility across multiple runs.
   - **`--help` / `-h`:** Displays usage syntax, available argument flags, and default parameter values, terminating with exit code 0.

2. **Output Formatting and Execution Log:**
   - During simulation execution, the system shall stream a day-by-day progress line for each simulated day step to standard output (`stdout`), detailing day index, arriving shipments, orders placed, fulfillments, and replenishments dispatched.
   - Upon completing the specified duration, the system shall render a multi-line formatted summary report (`=== Supply Chain Report: Day N ===`) containing itemized counts for:
     - **Delayed shipments:** Count and item details (shipment ID, SKU, destination warehouse, and days late).
     - **Stockouts:** Count and item details (warehouse ID and SKU with stock level equal to 0).
     - **Low stock:** Count and item details (warehouse ID, SKU, and remaining stock level at or below reorder point).
     - **Excess:** Count and item details (warehouse ID, SKU, total quantity, and surplus units exceeding maximum level).
     - **Orders:** Total orders, counts categorized by status (`pending`, `fulfilled`, `backordered`, `cancelled`), and calculated aggregate fill rate rounded to two decimal places.
   - If any reporting category contains zero problem instances, the system shall explicitly print `  No issues` under that category header.
   - On successful completion of the run, the process shall terminate with exit code 0.

#### 3.2 Hardware Interfaces
The system requires no specialized hardware interfaces or external physical device controllers. The simulator executes entirely in user-space memory on standard computing hardware:
- **Processor:** Standard x86-64 or ARM64 architecture processor.
- **Memory (RAM):** Minimum 512 MB available physical RAM (in-memory footprint is negligible, consuming < 50 MB during a 365-day simulation).
- **Storage:** Minimum 100 MB free disk space for repository files, Python environment, and test caches.
- **Input/Output Devices:** Standard keyboard for CLI input and terminal display / console standard output (`stdout` / `stderr`) for text rendering.

#### 3.3 Software Interfaces
The system interfaces strictly with standard local software components and development tools:
- **Operating System:** Platform-independent execution supporting Windows 10/11, Ubuntu Linux (20.04+), and macOS (12+).
- **Python Runtime:** Python 3.11 or higher runtime interpreter (`python >= 3.11.0`). The system relies strictly on standard library modules (`dataclasses`, `enum`, `typing`, `random`, `argparse`, `sys`).
- **Test Automation Framework:** `pytest` (version >= 8.0) and `pytest-cov` (version >= 5.0) for executing unit, integration, and system test suites and computing statement coverage metrics.
- **Continuous Integration Service:** GitHub Actions hosted runners (`ubuntu-latest`) executing the `.github/workflows/ci.yml` workflow on every pull request and push to `main`.
- **Data Persistence:** None. All entities (inventories, orders, shipments, policies) reside in in-memory Python data structures (`dict`, `list`). No external database management systems (DBMS) or file storage drivers are utilized.

#### 3.4 Communications Interfaces
- **Runtime Communications:** None. The application operates strictly as an isolated, standalone local process. No network protocols, sockets, HTTP servers, REST APIs, or remote procedure calls (RPC) are opened or consumed at runtime.
- **Development Communications:** Git version control over HTTPS (`https://github.com/rohithkarning-debug/supply-chain-simulator.git`) and GitHub remote APIs for pull requests, automated CI dispatch, code reviews, and issue tracking during project development.
