### 14. Test Metrics and Reporting

#### 14.1 Quality Metrics and Target Thresholds
The Software Engineering testing process monitors five key quality indicators to evaluate product release readiness:

| Metric Category | Specific Indicator | Project Target | Final evidence status (09-11-2026) | Compliance Status |
| :--- | :--- | :--- | :--- | :--- |
| **Execution Rate** | Test-case specifications with recorded execution results | 100% | 15 / 15 have recorded results; TC-COV-01 is partial because macOS was not tested | **Recorded; portability partial** |
| **Pass Rate** | Percentage of executed automated tests passing | 100% | 100 / 100 automated tests passed | **Met** |
| **Code Coverage** | Statement and branch coverage measured by `pytest-cov` | $\ge 90\%$ (SCM-NF-003) | 99.79% line, 99.17% branch; combined 99.66% | **Met** |
| **CI Gate** | Automated suite and configured coverage threshold on PRs and pushes to `main` | Required | Workflow runs pytest with branch coverage and `--cov-fail-under=90` | **Configured; no run count asserted here** |

#### 14.2 Code Coverage Breakdown by Subsystem Module

The line-coverage counts in the final report are detailed below. The exact combined line-and-branch percentage is reported in §14.4.

| Module Under Test | Statements | Missed Statements | Statement Coverage (%) | Module Owner |
| :--- | :--- | :--- | :--- | :--- |
| `src/scm_sim/__init__.py` | 1 | 0 | **100%** | Shared |
| `src/scm_sim/__main__.py` | 33 | 1 | **96.97%** | Rohith Karning |
| `src/scm_sim/analytics.py` | 67 | 0 | **100%** | Pranav Achar |
| `src/scm_sim/inventory.py` | 59 | 0 | **100%** | Rohith Karning |
| `src/scm_sim/orders.py` | 66 | 0 | **100%** | Rohanth Ganesha C |
| `src/scm_sim/shipments.py` | 88 | 0 | **100%** | Rishi J Mule |
| `src/scm_sim/simulator.py` | 155 | 0 | **100%** | Rohith Karning |
| **Project Total** | **469** | **1** | **99.79%** | **Team 02** |

#### 14.3 Test Reporting Protocol
1. **Pull Request Status Checks:** Every pull request targeting `main` executes the GitHub Actions `test` job. The job reports pass/fail status, writes line and branch coverage percentages to the Actions step summary, and uploads JUnit XML plus HTML/XML coverage artifacts.
2. **Defect Tracking via GitHub Issues:** Any failing test or edge-case regression is logged as a GitHub Issue labeled with the affected subsystem (`inventory`, `orders`, `shipments`, `analytics`, `simulator`) and assigned to the module owner.
3. **Formal System Validation Report:** Rishi's final E1–E6 report was merged in PR #89. Its evidence is recorded in `docs/test-reports/system-validation/system-validation-report.md`; the requirement matrix maps E5 to SCM-F-034, E6 to SCM-F-044, and SCM-F-043 to CLI invocation and exit behavior. This Test Plan records the report's existence and mapping without independently claiming that its manual E1–E6 runs were reproduced here.

#### 14.4 Final Metrics (09-11-2026)

| Metric | Target | Final Value | Evidence |
|---|---|---|---|
| **Automated Tests Executed** | 100% | 100 / 100 | Unit Test Report, commit `30702f8`; System Validation Report, commit `b87fd55` |
| **Automated Tests Passed** | 100% | 100 / 100 (0 failed, 0 skipped, 0 errors) | Unit Test Report, commit `30702f8`; System Validation Report, commit `b87fd55` |
| **Statement Coverage** | $\ge 90\%$ (SCM-NF-003) | **99.79%** (468 / 469 statements; one missed entrypoint statement) | Code Coverage Report, commit `f4dc0e8` |
| **Branch Coverage** | Reported | **99.17%** (119 / 120 branches; one partial) | Branch Coverage Report, commit `f4dc0e8` |
| **Combined line + branch coverage** | $\ge 90\%$ (SCM-NF-003) | **99.66%** (587 / 589 measured opportunities) | Code and Branch Coverage Reports, commit `f4dc0e8` |
| **Test Cases with Results** | 15 / 15 documented | 15 / 15 have a recorded result; 14 passed and TC-COV-01 is partial because macOS was not tested | Test Plan case records and this metrics report |
| **Manual Test Cases** | Results recorded | TC-PERF-01, TC-REP-01 and TC-SEC-02 passed; TC-COV-01 passed on Windows/Linux, macOS not run | System Validation Report, commit `b87fd55`; individual result records |
| **Final system validation E1–E6** | PR #89 / issue #65 | Rishi's report is merged and records E1–E6; SCM-F-034, SCM-F-043 and SCM-F-044 are mapped separately | System Validation Report, commit `b87fd55`; manual runs not independently repeated for this metrics table |

**Evidence provenance:** the unit-test report identifies commit `30702f8`, both coverage reports identify `f4dc0e8`, and the System Validation Report identifies `b87fd55`. Their reported test totals and coverage figures are consistent (the System Validation Report rounds coverage to whole percentages), but they are not evidence from a single common commit or identical pytest versions.

#### 14.5 Formal Reports and Deliverables
The available test evidence and verification reports are documented in `docs/test-reports/`:
1. [Unit Test Report](../test-reports/unit/unit-test-report.md): Execution summary of all 100 unit, integration, and CLI tests.
2. [Code Coverage Report](../test-reports/coverage/code-coverage-report.md): Statement-level line coverage breakdown and missed-line analysis.
3. [Branch Coverage Report](../test-reports/branch-coverage/branch-coverage-report.md): Decision-level branch execution analysis.
4. [Final System Validation Report v1.0](../test-reports/system-validation/system-validation-report.md): Rishi's final E1–E6 report, merged in PR #89; the report records E5 for SCM-F-034, E6 for SCM-F-044, and E1–E4 for SCM-F-043.
