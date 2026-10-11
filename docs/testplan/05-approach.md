### 5. Test Approach

The testing strategy establishes a multi-tiered verification framework designed to guarantee domain correctness, state invariant enforcement, and regression protection across all development phases.

#### 5.1 Test Levels
1. **Unit Testing:** Conducted independently for each isolated domain module (`test_inventory.py`, `test_orders.py`, `test_shipments.py`, and `test_analytics.py`). Focuses on individual class methods, function inputs/outputs, boundary edge cases, and exception triggers.
2. **Integration Testing:** Conducted within `tests/test_simulator.py`. Validates the interaction contracts between domain components when orchestrated by `Simulation.step()` (e.g., verifying that shipment arrivals replenish inventory which subsequently allows `process_open()` to fulfill previously backordered customer orders).
3. **System Testing:** Exercises the software end-to-end via the CLI entry point (`python -m scm_sim`) and `build_demo()` scenario execution. Verifies parameter parsing, argument validation, day-by-day logging, and full report generation.
4. **Acceptance Testing:** Evaluates the complete 10-day benchmark scenario against the course problem statement, validating that delays, stockouts, excess inventory, and fill rates are accurately identified and reported.

#### 5.2 Test Types
- **Functional Testing:** Verifies requirement compliance against SCM-F-001 through SCM-F-043.
- **Boundary-Value Analysis:** Tests edge thresholds such as zero quantity, exact capacity matches, boundary reorder levels (level == reorder_point vs. level == reorder_point + 1), and excess boundaries (level > max_level).
- **Regression Testing:** Automated suite executed on every pull request via GitHub Actions to ensure code additions do not degrade existing functionality.
- **Performance Testing (`TC-PERF-01`):** Execution timing of 365-day simulations and 10-day CLI runs ensuring completion within 1.0 second.
- **Reproducibility Testing (`TC-REP-01`):** Verifies that seed-controlled executions yield deterministic, bit-for-bit identical outputs across environments.
- **Security & Process Validation (`TC-SEC-01`, `TC-SEC-02`):** Validates input sanitization, non-negative stock invariants, branch protection rules, and secret absence.

#### 5.3 Entry Criteria
Testing of a component or feature branch may commence only when:
1. Feature module code and corresponding unit tests are authored and syntactically clean.
2. The local Python virtual environment is configured with `pytest` and `pytest-cov`.
3. The baseline continuous integration pipeline on GitHub Actions is active and reporting green on `main`.

#### 5.4 Exit Criteria
The test phase is considered complete and approved for release when:
1. **100% Execution:** All 15 planned test cases (TC-INV-01 through TC-REP-01) have been executed.
2. **Defect-Free Status:** Zero unresolved High or Critical severity defects exist.
3. **Automated Pass Rate:** 100% of automated tests pass (73/73 tests passing in CI).
4. **Coverage Target:** Overall code coverage on `src/scm_sim` reaches $\ge 90\%$ (current verified coverage: 97%).
5. **Quality Review:** Peer review approval is documented for all contributing pull requests.
