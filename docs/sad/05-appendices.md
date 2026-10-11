### 5. Appendices

#### 5.1 Glossary

| Term | Definition |
| :--- | :--- |
| **Back-order** | A customer order that could not be fulfilled immediately due to insufficient on-hand inventory and remains open in the backlog to be retried on subsequent simulation days. |
| **CI (Continuous Integration)** | Automated pipeline (implemented via GitHub Actions) that builds, tests, and validates code changes on every pull request and push to `main`. |
| **Days Late** | The number of days a shipment is delayed beyond its scheduled `expected_day`. If delivered, evaluated as `actual_day - expected_day`; if in transit, evaluated as `max(0, current_day - expected_day)`. |
| **Excess Inventory** | Units of stock held in a warehouse that exceed the configured maximum threshold (`max_level`) for a specific SKU. |
| **FIFO (First-In, First-Out)** | Allocation priority rule ensuring open back-orders with the oldest creation day (`created_day`) are fulfilled first during inventory replenishment passes. |
| **Fill Rate** | Operational service level metric computed as $\frac{\text{Fulfilled Orders}}{\text{Total Orders} - \text{Cancelled Orders}}$, rounded to two decimal places. |
| **Lead Time** | The standard transit duration in simulated days required for goods to travel from a supplier to a destination warehouse. |
| **PRNG** | Pseudorandom Number Generator. Uses an injected `random.Random(seed)` instance to achieve deterministic stochastic simulations. |
| **Reliability** | The probability ($p \in [0.0, 1.0]$) that a supplier delivers a dispatched shipment on time without transit delay. |
| **Reorder Point** | Inventory threshold level at or below which an automated replenishment reorder is triggered. |
| **Reorder Quantity** | Fixed batch size of units ordered from a supplier when replenishment is initiated. |
| **RTM** | Requirements Traceability Matrix; bidirectional mapping connecting requirements to architecture modules and test cases. |
| **SKU** | Stock Keeping Unit; unique alphanumeric identifier representing a distinct product item. |
| **Stockout** | Operational condition where available warehouse inventory for an active SKU is exactly zero (`level == 0`). |

#### 5.2 References

1. **IEEE Std 42010-2011:** *Systems and software engineering — Architecture description*. Institute of Electrical and Electronics Engineers.
2. **IEEE Std 29148-2018 (superseding IEEE Std 830-1998):** *Systems and software engineering — Life cycle processes — Requirements engineering*.
3. **IEEE Std 829-2008:** *Standard for Software and System Test Documentation*.
4. **Python Software Foundation:** *The Python Standard Library Documentation (Version 3.11)*. Available at: https://docs.python.org/3.11/
5. **pytest Documentation:** *pytest: helps you write better programs (Version 8.0)*. Available at: https://docs.pytest.org/
6. **GitHub Actions Documentation:** *Automating your workflow with GitHub Actions*. Available at: https://docs.github.com/en/actions
7. **Open Web Application Security Project (OWASP):** *Top 10 CI/CD Security Risks*. Available at: https://owasp.org/www-project-cicd-top-10/

#### 5.3 Tools and Environment

| Tool / Technology | Version / Platform | Architectural Purpose |
| :--- | :--- | :--- |
| **Python** | 3.11.9 (64-bit) | Primary development language and runtime execution environment. |
| **pytest** | 9.1.1 (>= 8.0) | Automated testing framework for executing unit, integration, and system test suites. |
| **pytest-cov** | 7.1.0 (>= 5.0) | Code coverage measurement tool producing statement coverage reports. |
| **Git** | 2.51.1 | Distributed version control tracking commits, branches, and development history. |
| **GitHub** | Cloud Platform | Remote repository hosting, branch protection enforcement, code reviews, and issue tracking. |
| **GitHub Actions** | Hosted `ubuntu-latest` | Continuous Integration runner executing automated test verification on every pull request. |
| **PlantUML** | Standard Syntax (planttext.com) | Unified Modeling Language (UML) diagram generation for sequence and component models. |
| **Visual Studio Code / Antigravity IDE** | Modern IDE | Development environment, linting, terminal execution, and markdown editing. |
