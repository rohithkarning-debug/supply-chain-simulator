### 4.6 Open Issues and Next Steps

Resolved implementation deviations are recorded in `docs/deviations.md`. The open items below reflect the current evidence and remaining work: macOS portability has not been tested, and the final System Validation Report E1–E6 is still assigned to Rishi under issue #65. No final E1–E6 results are asserted here.

#### 4.6.1 Known Limitations of the Current Implementation

| # | Limitation | Affected component | Current behaviour | Impact | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- |
| L1 | **macOS portability not yet verified.** Windows 11 and Linux runs are recorded, but a macOS run is not. | Test process | SCM-NF-004 remains partially validated; the supported-runtime code uses the Python standard library. | The cross-platform claim remains incomplete until macOS is tested. | Pranav Achar |
| L2 | **Final system validation report pending.** | Test process | Rishi is responsible for issue #65, which will deliver the final System Validation Report and its E1–E6 evidence. | Final system-level evidence remains outstanding; no E1–E6 results are inferred in this SAD. | Rishi J Mule |

#### 4.6.2 Planned Improvements

The following improvements are the intended direction for a subsequent iteration. They are not scheduled work and are not committed deliverables; they record the thinking behind the limitations above.

| # | Planned improvement | Addresses | Sketch of the approach |
| :--- | :--- | :--- | :--- |
| P1 | **Data-driven scenarios.** Replace the hard-coded `build_demo` scenario with CSV or JSON input. | General usability | A scenario file describing suppliers, warehouses, policies, opening stock and scheduled orders would let an analyst explore a different network without editing Python. |
| P2 | **Multi-echelon networks.** Extend the topology beyond supplier → warehouse to supplier → distribution centre → store. | General scope | A second inventory tier introduces location hierarchies, transfer orders between echelons and allocation rules on fulfilment. This is a scope increase, not a defect fix, and is out of scope for the current release. |
| P3 | **Demand forecasting and a cost model.** | General scope | Replace the scripted order schedule with a demand model, and attach a cost per unit held, ordered and shipped so that reports can quantify the cost of a stockout or excess inventory rather than only count them. |
| P4 | **Charted reporting.** | General scope | Render retained daily reports as time-series charts so trends are visible without post-processing. The current CLI may export daily metrics as CSV; charting is a future extension. |
| P5 | **Continuous delivery with a release package.** Extend the CI pipeline beyond the `test` job. | General process | A tagged-release build job could assemble a distributable artifact in addition to the current test and coverage reporting workflow. |
| P6 | **Richer temporal analytics.** | Run-level analytics | `summarize_run` reports day counts and peak/final values; it does not calculate trend series, average delay, or time-to-resolution. A future analytics extension could compute these measures from retained daily history and shipment lifecycle timestamps. |

#### 4.6.3 Immediate Next Steps

1. Complete issue #65 by preparing the final System Validation Report with its E1–E6 evidence; Rishi owns that report. This SAD does not pre-empt or infer its results.
2. Run and record the outstanding macOS portability test for SCM-NF-004 before claiming full cross-platform validation.