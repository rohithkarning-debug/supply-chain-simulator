| Field | Content |
| :--- | :--- |
| **TC ID** | TC-SIM-02 |
| **Title** | System-Level Scenario Validation, Multi-Issue Detection, and CLI Execution |
| **Requirement(s)** | SCM-F-040, SCM-F-043, SCM-NF-005 |
| **Type** | System |
| **Objective** | Perform end-to-end system verification on the Simulation and CLI modules to confirm that scenario scheduling rejects past days and invalid parameters, that the 10-day demo scenario detects all four supply chain issues (delays, stockouts, back-orders, and excess), and that the CLI runs successfully with clean exit codes and `--help` options. |
| **Preconditions** | Complete integrated package `scm_sim` installed with Python 3.11 environment. |
| **Test data** | 10-day standard demo scenario (`build_demo(seed=42)`): 2 suppliers (`SUP-RELIABLE`, `SUP-FLAKY`), 2 warehouses (`WH-NORTH`, `WH-SOUTH`), 3 SKUs (`WIDGET`, `GADGET`, `GIZMO`), 14 customer orders. |
| **Steps** | 1. Attempt scheduling an order for day 0 or past days (raises `ValueError`) and an unknown warehouse (raises `KeyError`).<br>2. Execute `build_demo(seed=42).run(10)` and examine reports across all 10 simulation days.<br>3. Verify that the simulation identifies delayed shipments, warehouse stockouts, back-ordered customer orders, and excess inventory.<br>4. Invoke the CLI entry point `scm_sim.__main__.main(["--days", "10", "--seed", "42"])` and verify output and exit code 0.<br>5. Execute Python sub-process module invocation `python -m scm_sim --days 1 --seed 42` and verify return code 0. |
| **Expected result** | `schedule_order` rejects non-future days and unknown warehouses; the 10-day demo scenario successfully triggers and reports delayed shipments, stockouts, back-ordered orders, and excess inventory; CLI executes cleanly with exit code 0; `--help` documentation displays all available options. |
| **Pass/fail criteria** | **Pass** if all system features execute without failure, all four issue types are detected in reports, and CLI subprocess execution succeeds with exit code 0; **Fail** if exceptions are unhandled, issues go undetected, or CLI execution crashes. |
| **Automated by** | `tests/test_simulator.py::test_schedule_order_validates_input`<br>`tests/test_simulator.py::test_demo_detects_delay_stockout_backorder_and_excess`<br>`tests/test_simulator.py::test_cli_main_runs`<br>`tests/test_simulator.py::test_cli_runs_as_module` |
| **Actual result** | Pass (CI run #20, commit `b3702ef`) |
| **Status** | Passed |
