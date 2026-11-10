| Field | Content |
| :--- | :--- |
| **TC ID** | TC-REP-01 |
| **Title** | Seeded Reproducibility of Daily Reports and CLI Output |
| **Requirement(s)** | SCM-NF-002 |
| **Type** | Reliability |
| **Objective** | Verify that supplying the same random seed with the same scenario produces byte-for-byte identical daily reports and identical console output on every run, and that a different seed changes the simulated delays deterministically — so that any reported failure can be reproduced exactly from its seed. |
| **Preconditions** | The `scm_sim` package is installed (`pip install -e .`) and the demo scenario is available through `build_demo(seed)`. For the manual part, commands are run as `scm-sim --days 10 --seed 42` and `scm-sim --days 10 --seed 1`. |
| **Test data** | Demo scenario built by `build_demo(seed=42)`: suppliers `SUP-RELIABLE` (reliability 1.0) and `SUP-FLAKY` (reliability 0.3); warehouses `WH-NORTH` (capacity 1200) and `WH-SOUTH` (capacity 500); SKUs `WIDGET`, `GADGET`, `GIZMO`; 14 customer orders including customer `C-ACME`. Seed 42 for the identity check; seed 1 for the variation check. |
| **Steps** | *Automated part.* 1. Build the demo with `build_demo(seed=42)` and call `run(10)`; keep the list of daily reports.<br>2. Build a second, independent demo with `build_demo(seed=42)` and call `run(10)`.<br>3. Compare the two lists of reports day by day.<br>*Manual part.* 4. Run `scm-sim --days 10 --seed 42` twice, redirecting each run's full output to a separate file.<br>5. Compare the two output files with `fc` / `diff`.<br>6. Run `scm-sim --days 10 --seed 1` and compare the delayed-shipment lines against the seed-42 output.<br>7. Record the host operating system and Python version used for the manual runs. |
| **Expected result** | 1. Ten reports are produced, one per simulated day.<br>2. Ten reports are produced from the second, independent instance.<br>3. The two lists are equal: every report for day *n* is identical in every key.<br>4. Each run prints a day-by-day log and a final report and exits with code 0.<br>5. The two files are identical (`fc` / `diff` reports no differences).<br>6. The seed-1 run produces different shipment delays from the seed-42 run, and the difference is deterministic.<br>7. The host details are recorded in the test report. |
| **Pass/fail criteria** | **Pass** if the automated test passes and both seed-42 manual runs produce identical output while the seed-1 run produces repeatable variations; **Fail** if any values differ between identical seeds or match across different seeds. |
| **Automated by** | `tests/test_simulator.py::test_same_seed_gives_identical_reports` |
| **Actual result** | Pass; automated report equality and manual CLI comparisons passed. Final automated suite: 100 tests passed. See [reproducibility results](../results/TC-REP-01.md) and [final unit-test report](../../test-reports/unit/unit-test-report.md). |
| **Status** | Passed |

Updated 08-11-2026: recorded manual test results and updated status to Passed (#61); final suite evidence reconciled 09-11-2026.
