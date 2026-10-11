# Test Plan
## Supply Chain Management Simulator

| Field | Value |
|---|---|
| Project | Supply Chain Management Simulator |
| Version | 1.0 |
| Authors | Team NN – Rohith Karning, Rohanth Ganesha C, Rishi J Mule, Pranav Achar |
| Date | 11-10-2026 |
| Status | Draft |

### Revision History

| Version | Date | Author(s) | Description of change | Approval |
|---|---|---|---|---|
| 1.0 | 11-10-2026 | Team NN | Initial draft | Pending |

### Table of Contents

1. Introduction
2. Test Items
3. Features to Be Tested
4. Features Not to Be Tested
5. Test Approach
   - 5.1 Security Validation
6. Test Environment
7. Test Schedule
8. Test Deliverables
9. Roles and Responsibilities
10. Risks and Mitigation
11. Assumptions and Dependencies
12. Suspension and Resumption Criteria
13. Test Case Management and Traceability
14. Test Metrics and Reporting
15. Approvals

Appendix: Test Cases (TC-INV-01, TC-INV-02, TC-SIM-01, TC-SIM-02, TC-ORD-01, TC-ORD-02, TC-PERF-01, TC-COV-01, TC-SHP-01, TC-SHP-02, TC-SEC-01, TC-SEC-02, TC-ANA-01, TC-ANA-02, TC-REP-01)

---

## 1. Introduction

### 1.1 Purpose

This Test Plan describes how the **Supply Chain Management Simulator** (Python package `scm_sim`), version 1.0, is verified against its Software Requirements Specification. It defines what is tested and what is not, the test levels and techniques used, the environment, the schedule, the people responsible, the entry, exit, suspension and resumption criteria, and how results are recorded and traced back to requirements.

The plan has two goals:

1. To show that every functional requirement (SCM-F-001 to SCM-F-043), non-functional requirement (SCM-NF-001 to SCM-NF-005) and security requirement (SCM-SR-001 to SCM-SR-007) in the SRS is covered by at least one test case.
2. To give evaluators and team members a repeatable procedure: each automated test case names the pytest tests that implement it, so anyone can re-run them with `pytest -v --cov=scm_sim` and get the same result.

### 1.2 Scope

**In scope.** The plan covers the seven test items listed in §2 at commit `b3702ef` of the `main` branch: the Inventory, Order Manager, Shipment Manager, Analytics, Simulation Engine and CLI components, and the CI Pipeline. It includes:

- **Unit testing** of each module through its own test file in `tests/`.
- **Integration testing** of the modules working together in the Simulation Engine (`tests/test_simulator.py`).
- **System testing** of the command-line interface, both by calling `main()` directly and by running `python -m scm_sim` in a subprocess.
- **Acceptance testing** of the demo scenario against the problem statement: goods move from suppliers to warehouses to customers, and delays, stockouts and excess inventory are detected.
- **Non-functional testing**: performance (SCM-NF-001), reproducibility (SCM-NF-002), coverage and maintainability (SCM-NF-003), portability (SCM-NF-004) and usability (SCM-NF-005).
- **Security validation** of data-integrity requirements (input validation, invariants, guarded status changes, unknown-ID rejection, copies of returned data) and of the development process (branch protection, no secrets, no runtime dependencies).

The plan contains **15 test cases**. Eleven are fully automated and run on every push and pull request by the CI `test` job. TC-PERF-01 and TC-SEC-02 are manual, and TC-COV-01 and TC-REP-01 combine automated checks with a manual part.

**Out of scope.** The features listed in §4 are not tested, including the Python interpreter and standard library, pytest and GitHub Actions themselves, and functions the system does not provide (graphical or web interfaces, storage, networking).

### 1.3 References

| ID | Document | Version / Date |
|---|---|---|
| [SRS] | Software Requirements Specification: Supply Chain Management Simulator | 1.0, 11-10-2026 |
| [SAD] | Software Architecture Document: Supply Chain Management Simulator | 1.0, 11-10-2026 |
| [REG] | Requirements registry, `docs/requirements-registry.md` | 11-10-2026 |
| [IEEE829] | IEEE Std 829-2008, Standard for Software and System Test Documentation | 2008 |
| [IEEE29119] | ISO/IEC/IEEE 29119-3, Software Testing: Test Documentation | 2021 |
| [REPO] | Team repository, https://github.com/rohithkarning-debug/supply-chain-simulator (`README.md`, `tests/`, `.github/workflows/ci.yml`) | commit `b3702ef` |
| [PYTEST] | pytest documentation, https://docs.pytest.org | pytest ≥ 8.0 |
| [PYCOV] | pytest-cov documentation, https://pytest-cov.readthedocs.io | pytest-cov ≥ 5.0 |

### 1.4 Definitions, Acronyms and Abbreviations

| Term | Definition |
|---|---|
| **Test item** | A software component (or the CI workflow) that is the object of testing |
| **Test case (TC)** | A set of preconditions, inputs, steps and expected results for verifying one or more requirements, identified as `TC-<area>-NN` |
| **Automated test** | A pytest function in `tests/` that checks expected results with `assert` and runs without human action |
| **Manual test** | A test executed and recorded by a person following the written steps |
| **Unit / Integration / System / Acceptance test** | Testing one module on its own / modules working together / the whole program through its CLI / the demo run against the problem statement |
| **Boundary-value testing** | Testing at and just beyond a limit, e.g. stock levels 20 and 21 for a reorder point of 20 |
| **Regression testing** | Re-running the whole suite after every change to detect newly broken behaviour; done automatically by CI on every pull request |
| **Coverage** | The percentage of executable lines of `scm_sim` run by the test suite, measured by pytest-cov |
| **CI run** | One execution of the GitHub Actions workflow `CI` (job `test`) |
| **Entry / Exit criteria** | Conditions that must hold before testing starts / before testing is considered complete |
| **Defect** | A difference between actual and expected results, recorded as a GitHub Issue |
| **Pass / Fail** | The actual result matches / does not match the expected result in every step |
| **Not run** | A manual test case that has not yet been executed |
| **SKU, Stockout, Back-order, Fill rate, Seed** | As defined in [SRS] §1.4 |
| **SRS / SAD / RTM** | Software Requirements Specification / Software Architecture Document / Requirements Traceability Matrix |
| **CI / CLI / PR** | Continuous Integration / Command-Line Interface / Pull Request |
