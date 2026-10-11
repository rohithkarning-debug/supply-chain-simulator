### 6. Quality Attributes & Acceptance Tests

This section establishes the quality standards, project exit criteria, and individual acceptance test suites required for system verification before release.

#### 6.1 Exit Criteria
The simulator software and its deliverables are considered ready for acceptance when all of the following conditions are satisfied:
1. **100% Test Case Execution:** All planned functional and non-functional test cases (TC-INV-01 through TC-REP-01) are executed.
2. **Zero Defect Tolerance:** Zero open High or Critical severity defects exist in the codebase.
3. **Automated Test Pass Rate:** 100% pass rate achieved across all automated test cases in the test suite (73/73 tests passing).
4. **Code Coverage Threshold:** Line coverage across `src/scm_sim/` reaches or exceeds 90%, verified by `pytest-cov` (current baseline: 97%).
5. **CI Pipeline Stability:** GitHub Actions CI job `test` passes with a green check on every pull request targeting `main`.
6. **Peer Review Governance:** Every pull request receives at least one formal review and approval from a designated peer reviewer prior to merging.

#### 6.2 Acceptance Test Suites

| Acceptance Test Suite | Scope & Target Requirements | Measurable Acceptance Test |
|---|---|---|
| **Inventory Acceptance Suite** | Stock level adjustments, warehouse capacity limits, per-item policy evaluation, reorder suggestions, and state snapshots (`SCM-F-001`–`SCM-F-004`). | Executing `pytest tests/test_inventory.py` passes all unit tests, confirming that negative additions and capacity breaches raise appropriate exceptions (`ValueError`, `CapacityExceededError`) while leaving inventory state intact. |
| **Orders Acceptance Suite** | Customer order creation, sequential ID assignment, full-quantity fulfillment, FIFO backorder retries, and guarded cancellation (`SCM-F-010`–`SCM-F-013`). | Executing `pytest tests/test_orders.py` passes all unit tests, confirming that invalid order quantities ($\le 0$) raise `ValueError`, fulfilled orders cannot be cancelled, and `process_open()` strictly fulfills oldest orders first. |
| **Shipments Acceptance Suite** | Supplier registry, lead-time tracking, probabilistic delay injection, arrival processing, and late shipment detection (`SCM-F-020`–`SCM-F-023`). | Executing `pytest tests/test_shipments.py` passes all unit tests, confirming that zero-reliability suppliers incur 1–3 days delay while reliability 1.0 suppliers arrive strictly on time. |
| **Analytics Acceptance Suite** | Detection of delayed shipments, stockouts, low stock, excess inventory, fill rate computation, and report formatting (`SCM-F-030`–`SCM-F-033`). | Executing `pytest tests/test_analytics.py` passes all unit tests, confirming that fill rate accurately discounts cancelled orders and formatted reports display explicit counts with "No issues" for empty sections. |
| **Simulation & CLI Acceptance Suite** | End-to-end scenario orchestration, 5-step daily simulation loop, automatic replenishment, and CLI interface (`SCM-F-040`–`SCM-F-043`). | Executing `pytest tests/test_simulator.py` passes all integration and system tests, and running `python -m scm_sim --days 10 --seed 42` returns exit code 0 while producing the complete daily log and summary report. |
| **Performance Acceptance Suite** | Runtime execution efficiency and benchmark thresholds (`SCM-NF-001`). | Running `build_demo().run(365)` completes in $\le 1.0$ s (measured: ~0.02 s), and running the 10-day CLI demo completes in $\le 1.0$ s (measured: ~0.10 s) across 3 consecutive trials on Python 3.11. |
| **Reproducibility Acceptance Suite** | Deterministic simulation execution across runs and platforms (`SCM-NF-002`). | Two executions of `python -m scm_sim --days 10 --seed 42` produce 100% identical outputs and analytics metrics; running with `--seed 7` produces a deterministically distinct set of delay and stockout events. |
| **Security & Integrity Acceptance Suite** | Input parameter validation, state invariants, secret avoidance, and branch protection (`SCM-SO-1`, `SCM-SO-2`, `SCM-SR-001`–`SCM-SR-007`). | Direct pushes to `main` are blocked by GitHub branch protection rules; invalid state mutations raise exceptions leaving memory untouched; no credentials or runtime third-party packages exist in the repository. |
