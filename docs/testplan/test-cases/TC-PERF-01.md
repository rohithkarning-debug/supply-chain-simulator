### Test Case Specification: TC-PERF-01

| Field | Content |
|---|---|
| **TC ID** | TC-PERF-01 |
| **Title** | System Execution Performance Benchmark for Long-Horizon and CLI Demo Runs |
| **Requirement(s)** | SCM-NF-001 |
| **Type** | Performance |
| **Preconditions** | Python 3.11 installed; clean operating system state on developer laptop; terminal session open. |
| **Test data** | 365-day programmatic scenario (`build_demo(42).run(365)`) and 10-day CLI scenario (`scm-sim --days 10 --seed 42`). |
| **Objective** | Verify that a full 365-day simulation run executes in $\le 1.0$ second and the 10-day CLI invocation (including interpreter startup and formatting) executes in $\le 1.0$ second across 3 trials. |
| **Steps** | 1. Execute `python -c "import time; from scm_sim.simulator import build_demo; s=build_demo(42); t=time.perf_counter(); s.run(365); print(round(time.perf_counter()-t,3),'s')"` 3 times.<br>2. Execute `Measure-Command { scm-sim --days 10 --seed 42 } | Select-Object TotalSeconds` (or `time scm-sim --days 10 --seed 42` on Linux/macOS) 3 times.<br>3. Record the execution time for each iteration and verify all trials remain under 1.0 second. |
| **Expected result** | 1. 365-day programmatic run finishes in $< 1.0$ s (measured baseline: ~0.014–0.027 s).<br>2. 10-day CLI run finishes in $< 1.0$ s (measured baseline: ~0.20–0.26 s). |
| **Pass/fail criteria** | Pass if all trial execution times remain $\le 1.0$ second; Fail if any execution exceeds 1.0 second. |
| **Automated by** | Manual benchmark execution using Python `time.perf_counter()` and terminal `Measure-Command` / `time`. |
| **Actual result** | Pass (10-day CLI 0.20-0.26 s, 365-day run 0.014-0.027 s; evidence docs/testplan/results/TC-PERF-01.md) |
| **Status** | Passed |

Updated 08-11-2026: Actual result = Pass, Status = Passed, evidence docs/testplan/results/TC-PERF-01.md (10-day CLI 0.20-0.26 s, 365-day run 0.014-0.027 s) (#59).
