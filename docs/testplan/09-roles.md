## 9. Roles and Responsibilities

### 9.1 Team Roles

| Name | SRN | GitHub | Test Plan role | Code module owned | Responsibilities in testing |
|---|---|---|---|---|---|
| Rohith Karning | `<SRN>` | rohithkarning-debug | **Product Owner** (also Test Engineer) | Inventory; Simulation Engine, CLI and CI Pipeline (integration); repository owner | Owns the requirements baseline and the requirements registry; decides whether a requirement is accepted. Set up the test environment and CI. Writes and executes TC-INV-01, TC-INV-02, TC-SIM-01 and TC-SEC-02. Approves the Test Plan and the final test summary. |
| Rohanth Ganesha C | `<SRN>` | rohanth3 | **QA Lead** (also Test Engineer) | Order Manager | Owns this Test Plan's approach, entry and exit criteria and suspension criteria. Tracks test progress and defects, and writes the test summary report (§7, M5). Writes and executes TC-ORD-01, TC-ORD-02 and TC-PERF-01. |
| Rishi J Mule | `<SRN>` | Rishi-Jayprakash06 | **Security Test Engineer** (also Test Engineer) | Shipment Manager | Owns security validation (§5.1) and the security requirements SCM-SR-001 to SCM-SR-007. Writes and executes TC-SHP-01, TC-SHP-02, TC-SEC-01 and the CLI system test TC-SIM-02. |
| Pranav Achar | `<SRN>` | achar-pranav | **Dev Lead** (also Test Engineer) | Analytics | Owns code quality and the coverage target (SCM-NF-003). Checks that tests stay in step with the code, and fixes defects in Analytics. Writes and executes TC-ANA-01, TC-ANA-02, TC-REP-01 and TC-COV-01. |

Every team member is a **Test Engineer** for the test cases they own: they write the test-case specification, keep the automated pytest tests for it passing, execute any manual steps, and record the actual result and status.

### 9.2 Test Case Ownership

| Owner | Test cases | Requirements covered |
|---|---|---|
| Rohith Karning | TC-INV-01, TC-INV-02, TC-SIM-01, TC-SEC-02 | SCM-F-001 – F-004, SCM-F-041, SCM-F-042, SCM-SR-005, SCM-SR-006 |
| Rohanth Ganesha C | TC-ORD-01, TC-ORD-02, TC-PERF-01 | SCM-F-010 – F-013, SCM-NF-001 |
| Rishi J Mule | TC-SHP-01, TC-SHP-02, TC-SEC-01, TC-SIM-02 | SCM-F-020 – F-023, SCM-SR-001 – SR-004, SCM-SR-007, SCM-F-040, SCM-F-043, SCM-NF-005 |
| Pranav Achar | TC-ANA-01, TC-ANA-02, TC-REP-01, TC-COV-01 | SCM-F-030 – F-033, SCM-NF-002, SCM-NF-003, SCM-NF-004 |

### 9.3 Responsibility Matrix (RACI)

R = Responsible (does the work), A = Accountable (approves), C = Consulted, I = Informed.

| Activity | Rohith (Product Owner) | Rohanth (QA Lead) | Rishi (Security Test Eng.) | Pranav (Dev Lead) |
|---|---|---|---|---|
| Requirements baseline and registry | A, R | C | C | C |
| Test Plan approach, entry and exit criteria | C | A, R | C | C |
| Test environment and CI pipeline | A, R | I | C | C |
| Writing test cases for own module | R | R | R | R |
| Security validation (§5.1) | C | I | A, R | C |
| Performance test (TC-PERF-01) | I | A, R | I | C |
| Coverage and reproducibility (TC-COV-01, TC-REP-01) | I | C | I | A, R |
| Branch-protection and secrets check (TC-SEC-02) | R | I | A | I |
| Code review of PRs (every PR needs one approval from a non-author) | R | R | R | R |
| Defect fixing | R (own modules) | R (own module) | R (own module) | A, R (own module) |
| Test summary report | C | A, R | C | C |
| Final approval of the Test Plan (§15) | A | R | I | R |

### 9.4 Review Responsibilities

Every test-plan and test-case file reaches `main` through a pull request that needs one approval from a teammate other than its author, plus a green `test` CI check. For the Test Plan, reviewers rotate as follows:

| PR author | Test Plan PR reviewed by |
|---|---|
| Rohith | Pranav |
| Rohanth | Rohith |
| Rishi | Rohanth |
| Pranav | Rishi |

The reviewer checks that every requirement and test-case ID matches `docs/requirements-registry.md`, that each automated test case names pytest tests that actually exist in `tests/`, and leaves at least one review comment before approving.
