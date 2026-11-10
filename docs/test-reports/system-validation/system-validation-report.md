# System Validation Report — Final (v1.0)

| Field | Value |
|---|---|
| Report | System Validation Report |
| Version | Final (v1.0) |
| Prepared by | Rishi J Mule (Security Test Engineer) |
| Reviewed by | Rohanth Ganesha C |
| Date | 09-11-2026 |
| Commit tested | b87fd55 |
| Environment | Windows 11 (10.0.26300), Python 3.11.9, pytest 9.2.0 |
| Command | scm-sim --days 10 --seed 42 (plus E2-E6 below) and python -m pytest -q |

## 1. Scope
The complete simulator (all modules and the scm-sim command) validated end to end against SRS v1.1: SCM-F-001 to SCM-F-044, SCM-NF-001 to SCM-NF-005, SCM-SO-1, SCM-SO-2 and SCM-SR-001 to SCM-SR-007. Evidence comes from the end-to-end runs below, the automated suite (100 tests passed) and the four manual test cases.

## 2. End-to-end runs
| # | Command | Expected | Actual | Result |
|---|---|---|---|---|
| E1 | scm-sim --days 10 --seed 42 | Exit 0, 10 day blocks, final report | Exit 0; 2 delayed, 0 stockouts, 0 low, 1 excess, 14 fulfilled, fill rate 1.0 | PASS |
| E2 | scm-sim --days 0 | Usage error, exit 2 | scm-sim: error: --days must be at least 1, exit 2 | PASS |
| E3 | scm-sim --help | Lists options including --days, --seed, --summary, --csv; exit 0 | Lists options: -h/--help, --days DAYS (default 10), --seed SEED (default 42), --summary, --csv PATH; exit 0 | PASS |
| E4 | python -m scm_sim --days 10 --seed 42 | Same output as E1 | FC: no differences encountered | PASS |
| E5 | scm-sim --days 10 --seed 42 --summary | Exit 0, prints "=== Run Summary ===" with multi-day metric counts | Exit 0; prints === Run Summary === with days: 10, days_with_delays: 6, days_with_stockouts: 3, days_with_low_stock: 3, days_with_excess: 10, peak_delayed: 2, final_fill_rate: 1.0 | PASS |
| E6 | scm-sim --days 3 --seed 42 --csv m.csv | Exit 0, m.csv created with header day,delayed,stockouts,low_stock,excess,pending,fulfilled,backordered,cancelled,fill_rate plus 3 data rows | Exit 0; m.csv created with daily metrics header and 3 data rows matching day-by-day metrics | PASS |

## 3. Requirement validation matrix
| Requirement | Short name | Test case(s) | Automated result | Manual result | Verdict |
|---|---|---|---|---|---|
| SCM-F-001 | Stock tracking with validated add/remove | TC-INV-01 | PASS | - | Validated |
| SCM-F-002 | Warehouse capacity limits | TC-INV-01 | PASS | - | Validated |
| SCM-F-003 | Per-item stock policy | TC-INV-02 | PASS | - | Validated |
| SCM-F-004 | Reorder suggestions and stock snapshot | TC-INV-02 | PASS | - | Validated |
| SCM-F-010 | Create orders with ORD-0001 IDs | TC-ORD-01 | PASS | - | Validated |
| SCM-F-011 | Fulfil in full or back-order | TC-ORD-01 | PASS | E1 (ORD-0005 back-ordered, then filled) | Validated |
| SCM-F-012 | Retry open orders oldest-first | TC-ORD-02 | PASS | - | Validated |
| SCM-F-013 | Cancel, look up and list orders | TC-ORD-02 | PASS | - | Validated |
| SCM-F-020 | Register suppliers | TC-SHP-01 | PASS | - | Validated |
| SCM-F-021 | Dispatch shipments with SHP-0001 IDs | TC-SHP-01 | PASS | - | Validated |
| SCM-F-022 | Delays from supplier reliability | TC-SHP-02 | PASS | E1 (SHP-0001, SHP-0002 1 day late) | Validated |
| SCM-F-023 | Deliver arrivals; overflowing arrival stays in transit (#70) | TC-SHP-02 | PASS | - | Validated |
| SCM-F-030 | Report delayed shipments | TC-ANA-01 | PASS | E1 | Validated |
| SCM-F-031 | Stockouts, low stock, excess (per-item limits, #71) | TC-ANA-01 | PASS | E1 (GIZMO excess) | Validated |
| SCM-F-032 | Order metrics and fill rate | TC-ANA-02 | PASS | E1 (fill rate 1.0) | Validated |
| SCM-F-033 | Daily report and text format | TC-ANA-02 | PASS | E1 | Validated |
| SCM-F-034 | Multi-day run summary | TC-ANA-02 | PASS | E5 | Validated |
| SCM-F-040 | Configure a scenario | TC-SIM-02 | PASS | - | Validated |
| SCM-F-041 | Daily step order (back-orders first, #69) | TC-SIM-01 | PASS | - | Validated |
| SCM-F-042 | Automatic replenishment trimmed to capacity | TC-SIM-01 | PASS | - | Validated |
| SCM-F-043 | CLI invocation, usage/help and exit behavior | TC-SIM-02 | PASS | E1-E4 | Validated |
| SCM-F-044 | Daily metrics CSV export | TC-SIM-02 | PASS | E6 | Validated |
| SCM-NF-001 | 365-day run and 10-day demo each <= 1 s | TC-PERF-01 | - | PASS (TC-PERF-01.md) | Validated |
| SCM-NF-002 | Same seed gives identical output | TC-REP-01 | PASS | PASS (TC-REP-01.md) | Validated |
| SCM-NF-003 | >= 90% coverage, tests pass before merge | TC-COV-01 | PASS (CI gate) | 99% line, 99% line + branch (coverage reports) | Validated |
| SCM-NF-004 | Python >= 3.11 on Windows, Linux, macOS; stdlib only | TC-COV-01 | PASS (CI on Ubuntu, Python 3.11) | Windows 11 (Python 3.11.9) and Linux (Python 3.14.9) runs pass; macOS not run | Partially validated (macOS not run) |
| SCM-NF-005 | Usability (one command, report counts, "No issues", --help) | TC-SIM-02 | PASS | E1, E3 | Validated |
| SCM-SO-1 | Integrity of simulation data | TC-SEC-01 | PASS | - | Validated (through SR-001 to SR-004, SR-007) |
| SCM-SO-2 | Integrity and traceability of the codebase | TC-SEC-02 | - | PASS (TC-SEC-02.md) | Validated (through SR-005, SR-006) |
| SCM-SR-001 | Input validation before state change | TC-SEC-01 | PASS | E2 | Validated |
| SCM-SR-002 | Stock never below 0 or above capacity | TC-SEC-01 | PASS | - | Validated |
| SCM-SR-003 | Guarded order status changes | TC-SEC-01 | PASS | - | Validated |
| SCM-SR-004 | Unknown references raise KeyError | TC-SEC-01 | PASS | - | Validated |
| SCM-SR-005 | Protected main branch | TC-SEC-02 | - | PASS (TC-SEC-02.md) | Validated |
| SCM-SR-006 | No secrets, no network, no runtime dependencies | TC-SEC-02 | - | PASS (TC-SEC-02.md) | Validated |
| SCM-SR-007 | Returned data is a copy | TC-SEC-01 | PASS | - | Validated |

## 4. Manual test cases and automated test suite
The automated test suite contains **100 tests** (increased from 84 in v1), all passing (100% pass rate in 1.32s). Total statement coverage is **99%** (469 statements, 1 missed in `__main__.py` entry-point guard); combined branch coverage is **99%** (120 branches, 1 partial).

| TC-ID | Executed by | Date | Result | Evidence |
|---|---|---|---|---|
| TC-REP-01 | Pranav Hareesh Achar | 05-11-2026 | PASS | docs/testplan/results/TC-REP-01.md |
| TC-PERF-01 | Rohanth Ganesha C | 05-11-2026 | PASS | docs/testplan/results/TC-PERF-01.md |
| TC-SEC-02 | Rohith Karning | 05-11-2026 | PASS | docs/testplan/results/TC-SEC-02.md |
| TC-COV-01 | Pranav Hareesh Achar | 05-11-2026 | PASS (Windows and Linux); macOS not run | docs/test-reports/coverage/ (99% line), docs/test-reports/branch-coverage/ (99% branch) |

## 5. Related reports
- Final Unit Test Report: docs/test-reports/unit/unit-test-report.md (100 passed, 0 failed, #64)
- Final Code Coverage Report: docs/test-reports/coverage/code-coverage-report.md (99% line, #66)
- Final Branch Coverage Report: docs/test-reports/branch-coverage/branch-coverage-report.md (99% line + branch, #66)
- Deviations Document: docs/deviations.md (#56)

## 6. Open defects and conclusion
No open defects. 33 of 34 requirements are fully validated; SCM-NF-004 is partially validated because the macOS run has not been conducted. TC-PERF-01, TC-REP-01 and TC-SEC-02 passed; TC-COV-01 passed on Windows and Linux but remains partially validated because macOS was not tested. All 100 automated unit and integration tests passed; the report records coverage rounded to whole percentages.

**Sign-off:**
- Prepared by: Rishi J Mule (Security Test Engineer) — 09-11-2026
- Reviewer: Rohanth Ganesha C (Test Lead)

## 7. Evidence
- demo-run.txt (output of E1)
