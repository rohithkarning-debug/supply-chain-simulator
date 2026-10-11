### 12. Suspension and Resumption Criteria

This section outlines the operational conditions governing when testing activities must be paused and when they may safely resume.

#### 12.1 Suspension Criteria
Testing activities and pull request evaluations shall be formally suspended under any of the following conditions:
1. **Broken Continuous Integration Pipeline:** The `test` job on GitHub Actions fails on the `main` branch, indicating an unhandled regression or broken baseline environment.
2. **High Test Blockage Threshold:** More than 30% of automated test cases are failing or blocked due to breaking interface changes or uncoordinated domain signature modifications.
3. **Core Dependency Invalidation:** Critical foundational modules (such as `Inventory`) fail core state invariant checks (e.g., negative stock levels allowed or capacity exceptions unhandled), compromising downstream module verification.
4. **Environment Unavailability:** Severe disruptions to the primary developer environments or GitHub Actions CI runner infrastructure.

#### 12.2 Resumption Criteria
Testing activities shall resume once all blocking criteria have been addressed:
1. **CI Pipeline Restored:** A fix or revert is merged to `main`, restoring a green check status across the full automated test suite.
2. **Defect Rectification:** Blocking interface discrepancies are resolved, verified by local execution of `pytest -v`, and validated to pass with zero regressions.
3. **Baseline Re-verification:** The test suite pass rate returns to 100%, and coverage metrics are confirmed $\ge 90\%$ before downstream feature evaluation continues.
