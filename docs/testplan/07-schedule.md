## 7. Test Schedule

Testing runs alongside development. Automated tests were written with each feature and run in CI on pull requests and pushes to `main`. Sections 7.1–7.3 preserve the original baseline plan; §7.4 records the actual schedule and current status. All dates are in 2026 (DD-MM-YYYY).

### 7.1 Schedule of Test Activities

| # | Activity | Start | End | Responsible | Output / milestone | Status |
|---|---|---|---|---|---|---|
| 1 | Set up test environment: `requirements.txt` (pytest, pytest-cov), `pytest.ini`, CI workflow `.github/workflows/ci.yml` (job `test`) | 10-10-2026 | 10-10-2026 | Rohith | **M1: environment and CI ready.** First CI run (#1) green | Done |
| 2 | Write unit tests with each feature, run locally and in CI on every PR | 10-10-2026 | 11-10-2026 | Each module owner | `test_inventory.py`, `test_orders.py`, `test_shipments.py`, `test_analytics.py` | Done |
| 3 | Automated execution on feature PRs: #2 orders, #3 inventory policies, #5 shipments, #6 analytics | 10-10-2026 | 11-10-2026 | Each PR author; reviewer checks CI | `test` check green before each merge | Done |
| 4 | Integration and system tests for the Simulation Engine and CLI (PR #7) | 11-10-2026 | 11-10-2026 | Rohith | `test_simulator.py`; M2 baseline suite completed (historical; see final evidence in `docs/test-reports/`) | Done |
| 5 | Test design: write the 15 test-case specifications and this Test Plan | 11-10-2026 | 12-10-2026 | All (see §9) | `docs/testplan/` and `docs/testplan/test-cases/`; **M3: Test Plan v1.0 submitted** (docs deadline 12-10-2026) | Done |
| 6 | Manual test cases: TC-PERF-01, TC-SEC-02, and manual parts of TC-COV-01 / TC-REP-01 | 13-10-2026 | 20-10-2026 | Rohanth (PERF), Rohith (SEC-02), Pranav (COV, REP) | Results recorded; Windows and Linux tested, macOS not tested, so SCM-NF-004 remains partial | Done (with macOS portability outstanding) |
| 7 | Defect fixing and re-testing for any failures from activity 6 | 13-10-2026 | 22-10-2026 | Owner of the affected module | No failing test results were reported; no defect-fix cycle was required | Not required |
| 8 | Regression testing: full suite re-run by CI on every later PR and every push to `main` | 10-10-2026 | End of project | Automatic (CI); PR reviewer verifies | Green `test` check on each PR | Ongoing |
| 9 | Test summary report: metrics from §14, defect summary and exit-criteria check | 23-10-2026 | 09-11-2026 | Rohanth (QA Lead) with Rohith | Metrics and test reports recorded; final System Validation Report merged by PR #89 | Done |

### 7.2 Milestones

| Milestone | Date | Criterion |
|---|---|---|
| M1 – Environment and CI ready | 10-10-2026 | CI workflow merged; first run green |
| M2 – Initial automated baseline on `main` | 11-10-2026 | Baseline at `b3702ef`; CI run #20 green (73 passed, 97% coverage). Final suite evidence is in `docs/test-reports/`. |
| M3 – Test Plan v1.0 submitted | 12-10-2026 | All Test Plan sections and 15 test-case files merged to `main` |
| M4 – Test case execution recorded | 20-10-2026 | All 15 test cases have recorded results; TC-COV-01 is partial because macOS was not tested |
| M5 – Final system validation report | 09-11-2026 | Rishi's final report with E1–E6 was merged in PR #89; its requirement matrix is reconciled to SCM-F-034, SCM-F-043 and SCM-F-044 |

### 7.3 Dependencies of the Schedule

- Activities 2–4 depend on M1 (CI must exist before PRs can be gated).
- Activity 6 depends on M2 (manual tests run against commit `b3702ef` or a later green `main`).
- Activity 9 depends on M4 and on all defects from activity 7 being closed or accepted.
- If testing is suspended (§12), the end dates of activities 6–9 move back by the length of the suspension; M3 is fixed by the course deadline.

### 7.4 Actual Schedule

| Phase / Activity | Start | End | Outputs & Milestones | Status |
|---|---|---|---|---|
| Sprint 1 | 01-11-2026 | 06-11-2026 | Packaging, order ID validation (#68), back-orders first (#69), arrivals overflow fix (#70), per-item thresholds (#71), Sprint 1 video (#75) | Done |
| Testing week | 02-11-2026 | 06-11-2026 | v1 test reports; manual test cases TC-REP-01, TC-PERF-01, and TC-SEC-02 executed and passed on 05-11-2026 | Done |
| Sprint 2 | 07-11-2026 | 09-11-2026 | Run summary (#79), CSV export (#80), coverage gap tests (#81, #84), test case updates (#83), CI report workflows (#82), unit and coverage reports | Done |
| Release v1.0 | 09-11-2026 | Pending | Deviations and final test/coverage/system-validation evidence are available; GitHub release/freeze issue #58 and Sprint 2 demo video issue #57 remain open | In progress |
