## 7. Test Schedule

Testing runs alongside development. Automated tests were written together with each feature and ran in CI on every pull request; the remaining work is the manual test cases and the final test summary. All dates are in 2026 (DD-MM-YYYY).

### 7.1 Schedule of Test Activities

| # | Activity | Start | End | Responsible | Output / milestone | Status |
|---|---|---|---|---|---|---|
| 1 | Set up test environment: `requirements.txt` (pytest, pytest-cov), `pytest.ini`, CI workflow `.github/workflows/ci.yml` (job `test`) | 10-10-2026 | 10-10-2026 | Rohith | **M1: environment and CI ready.** First CI run (#1) green | Done |
| 2 | Write unit tests with each feature, run locally and in CI on every PR | 10-10-2026 | 11-10-2026 | Each module owner | `test_inventory.py`, `test_orders.py`, `test_shipments.py`, `test_analytics.py` | Done |
| 3 | Automated execution on feature PRs: #2 orders, #3 inventory policies, #5 shipments, #6 analytics | 10-10-2026 | 11-10-2026 | Each PR author; reviewer checks CI | `test` check green before each merge | Done |
| 4 | Integration and system tests for the Simulation Engine and CLI (PR #7) | 11-10-2026 | 11-10-2026 | Rohith | `test_simulator.py`; **M2: full suite on `main`.** CI run #20 on commit `b3702ef`: 73 passed, 97% coverage | Done |
| 5 | Test design: write the 15 test-case specifications and this Test Plan | 11-10-2026 | 12-10-2026 | All (see §9) | `docs/testplan/` and `docs/testplan/test-cases/`; **M3: Test Plan v1.0 submitted** (docs deadline 12-10-2026) | In progress |
| 6 | Manual test cases: TC-PERF-01, TC-SEC-02, the manual part of TC-COV-01 (Windows + Linux run) and of TC-REP-01 (CLI output comparison) | 13-10-2026 | 20-10-2026 | Rohanth (PERF), Rohith (SEC-02), Pranav (COV, REP) | Actual results recorded in each test-case file; **M4: all 15 TCs executed** | Not started |
| 7 | Defect fixing and re-testing for any failures from activity 6 | 13-10-2026 | 22-10-2026 | Owner of the affected module | Fix PRs with green CI; defect issues closed | Not started |
| 8 | Regression testing: full suite re-run by CI on every later PR and every push to `main` | 10-10-2026 | End of project | Automatic (CI); PR reviewer verifies | Green `test` check on each PR | Ongoing |
| 9 | Test summary report: metrics from §14, defect summary and exit-criteria check | 23-10-2026 | 25-10-2026 | Rohanth (QA Lead) with Rohith | **M5: test summary report** | Not started |

### 7.2 Milestones

| Milestone | Date | Criterion |
|---|---|---|
| M1 – Environment and CI ready | 10-10-2026 | CI workflow merged; first run green |
| M2 – Full automated suite on `main` | 11-10-2026 | All feature PRs merged; CI run #20 on `b3702ef` green (73 passed, 97% coverage) |
| M3 – Test Plan v1.0 submitted | 12-10-2026 | All Test Plan sections and 15 test-case files merged to `main` |
| M4 – All test cases executed | 20-10-2026 | Every TC has an actual result of Pass or Fail (none "Not run") |
| M5 – Test summary report | 25-10-2026 | Exit criteria in §5 checked and reported |

### 7.3 Dependencies of the Schedule

- Activities 2–4 depend on M1 (CI must exist before PRs can be gated).
- Activity 6 depends on M2 (manual tests run against commit `b3702ef` or a later green `main`).
- Activity 9 depends on M4 and on all defects from activity 7 being closed or accepted.
- If testing is suspended (§12), the end dates of activities 6–9 move back by the length of the suspension; M3 is fixed by the course deadline.
