### 3. Architecture

#### 3.1 Goals and Constraints

The architectural design of the Supply Chain Management Simulator balances rigorous academic software engineering objectives with practical operational constraints.

##### 3.1.1 Architectural Goals
1. **Functional Correctness & Invariant Enforcement:** Ensure supply chain physical realities are strictly upheld. Inventory quantities cannot drop below zero, warehouse storage cannot exceed declared capacity limits, and orders cannot experience partial fulfillment or invalid state transitions. All mutating operations follow fail-fast semantics, guaranteeing state remains completely unchanged if an exception is raised.
2. **Deterministic Reproducibility:** Ensure identical execution outcomes given the same initial scenario configuration and random seed (`SCM-NF-002`). By centralizing all stochastic delay decisions within a single pseudo-random generator (`random.Random(seed)`), simulations produce reproducible audit logs and metrics across platforms.
3. **High Testability & Verification:** Architect all components as modular, decoupled units capable of being tested in isolation without requiring external database drivers, web servers, or network mocks (`SCM-NF-003`). Testability targets $\ge 90\%$ branch/statement coverage in continuous integration.
4. **Parallel Team Development:** Establish clean, one-way dependency contracts enabling a 4-person engineering team to construct and test domain modules (`inventory.py`, `orders.py`, `shipments.py`, `analytics.py`) concurrently before integration into the simulation orchestrator (`simulator.py`).

##### 3.1.2 Architectural Constraints
1. **Standard Library Runtime Only:** The runtime environment must utilize exclusively the Python 3.11 standard library (`dataclasses`, `enum`, `random`, `argparse`). No third-party packages are permitted at runtime (`SCM-NF-004`). External libraries are restricted strictly to testing (`pytest`, `pytest-cov`).
2. **In-Memory Volatile Storage:** The simulator operates purely in RAM using in-memory data structures (Python dictionaries and lists). There are no external databases, file persistence engines, or caching daemons.
3. **Command-Line Interface (CLI):** The software interacts with users strictly through a console CLI entry point (`python -m scm_sim`) and programmatic Python APIs. Web graphical user interfaces, microservices, and network protocols are explicitly out of scope.
4. **Academic Semester Timeline:** The project scope is constrained to the academic course schedule, prioritizing robust core domain logic, deterministic simulation stepping, and comprehensive documentation over commercial distributed deployment.
