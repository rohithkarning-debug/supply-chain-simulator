### Test Case Specification: TC-PERF-01

| Field | Content |
|---|---|
| **TC ID** | TC-PERF-01 |
| **Title** | System Execution Performance Benchmark for Long-Horizon and CLI Demo Runs |
| **Requirement(s)** | SCM-NF-001 |
| **Type** | Performance |
| **Preconditions** | Python 3.11 installed; clean operating system state on developer laptop; terminal session open. |
| **Test data** | 365-day programmatic scenario (`build_demo().run(365)`) and 10-day CLI scenario (`python -m scm_sim --days 10 --seed 42`). |
| **Objective** | Verify that a full 365-day simulation run executes in $\le 1.0$ second and the 10-day CLI invocation (including interpreter startup and formatting) executes in $\le 1.0$ second across 3 trials. |
| **Steps** | 1. Execute `python -c "import time; from scm_sim.simulator import build_demo; t0=time.perf_counter(); build_demo().run(365); print(time.perf_counter()-t0)"` 3 times.<br>2. Execute `Measure-Command { python -m scm_sim --days 10 --seed 42 }` (or `time python -m scm_sim ...` on Linux/macOS) 3 times.<br>3. Record the execution time for each iteration and compute averages. |
| **Expected result** | 1. 365-day programmatic run finishes in $< 1.0$ s (measured baseline: ~0.02 s).<br>2. 10-day CLI run finishes in $< 1.0$ s (measured baseline: ~0.10 s). |
| **Pass/fail criteria** | Pass if all trial execution times remain $\le 1.0$ second; Fail if any execution exceeds 1.0 second. |
| **Automated by** | Manual benchmark execution using Python `time.perf_counter()` and terminal `Measure-Command` / `time`. |
| **Actual result** | Pass (Average programmatic run: 0.021 s; Average CLI execution: 0.114 s on Windows 11, commit `b3702ef`) |
| **Status** | Passed |
