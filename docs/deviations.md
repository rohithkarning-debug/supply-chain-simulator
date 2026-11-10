# Deviations from the Submitted SRS, SAD and Test Plan

This document lists every change made during Sprint 1 and Sprint 2 compared with the submitted documents (SRS v1.0, SAD v1.0, Test Plan v1.0). It details what the submitted documents originally specified, what was implemented instead, the rationale for the change, the corresponding sprint and pull request, and the responsible owner.

## Deviations Table

| # | Area / ID | Submitted document said | What we did instead | Why | Sprint / PR | Owner |
|---|---|---|---|---|---|---|
| D1 | SCM-F-041 | Today's orders were served before older back-orders | Back-orders are retried first | Fairness to earlier customers (SAD 4.6) | S1 / #69 | Rohanth |
| D2 | SCM-F-010 | An invalid order used up an order ID | Quantity is validated before the ID is assigned | IDs stay sequential (SAD 4.6) | S1 / #68 | Rohanth |
| D3 | SCM-F-023 | An arrival over capacity stopped the remaining arrivals | It stays in transit, shows BLOCKED and is retried next day; other arrivals continue | No lost deliveries (SAD 4.6) | S1 / #70 | Rishi |
| D4 | SCM-F-031 | One global low/excess threshold | Each item's own stock policy, 20/500 as fallback | Accurate alerts (SAD 4.6) | S1 / #71 | Pranav |
| D5 | SCM-F-043, SRS 2.5 | CLI needed PYTHONPATH=src | Installable package with the scm-sim command (pyproject.toml) | One-command setup | S1 / #67 | Rohith |
| D6 | SCM-NF-003, SAD tech stack | CI only ran tests | CI enforces 90% line + branch coverage, auto-labels PRs, checks PR titles and commit messages, publishes test and coverage reports | Automate PR quality | S1 / #73, S2 / #80, #82 | Rohith |
| D7 | New features (SCM-F-034, SCM-F-044) | No run summary or CSV export in CLI | Run summary (--summary) and daily metrics CSV export (--csv) added to the CLI | Enhanced analysis and reporting | S2 / #79, #80 | Rishi, Rohith |
| D8 | Test Plan schedule | Testing after both sprints | Testing week ran alongside Sprint 1 (v1 reports), final reports in Sprint 2 | Instructor's 2-6 Nov testing week | S1, S2 | all |
| D9 | Process | Sprint 2 planned for 7-12 Nov | Run as a 3-day sprint (7-9 Nov) | Allowed by the instructor | S2 | all |
| D10 | Process | Original task assignments | #53 and #61 reassigned from Pranav to Rishi, #47 to Rohanth, #66 to Rohith | Pranav unavailable from 08-11 | S2 | all |
| D11 | Process | Repository owner reviews and merges all PRs | PRs #67, #70, #71, #73 and #74 were merged by a teammate other than the repository owner. PRs #70, #71 and #73 were already recorded; GitHub history also shows #67 merged by Pranav and #74 merged by Rishi. Each had a non-author approval, but those approvals and merges do not satisfy the repository-owner criterion. | Team decision | S1 | all |
| D12 | Process | Direct board transitions | Sprint 1 cards went from Todo straight to Done; In Progress was used from Sprint 2 | Improved sprint tracking | S1 | all |
| D13 | Process | Normal PR integration workflow | The #55 CI change first reached main while resolving a merge conflict in PR #80 (commit f005900); PR #82 then closed the issue | Merge conflict resolution on main | S2 | Rohith |

## Sections Without Deviations

The following specification sections were implemented exactly as originally designed with no deviations:
- **Inventory Module (SCM-F-001 – SCM-F-004):** Warehouse stock tracking, capacity validation, per-item policy definitions, reorder calculations, and immutable defensive snapshot operations match the SRS and SAD designs without alteration.
- **Security & Domain Invariants (SCM-SR-001 – SCM-SR-007, SCM-SO-1, SCM-SO-2):** Public boundary validation before mutation, non-negative stock guards, warehouse capacity limits, strict order status state-machine transitions, unknown entity KeyError exceptions, and data isolation follow the original security architecture without changes.
- **Architectural Patterns (SAD §3.5):** Layered domain model architecture, dependency structure, and pure-function analytics design operate exactly as specified.

## Impact on the documents

SRS 4.2, 4.3, 4.4, 4.5 and 2.5 and SAD 4.6 are updated in #31; the test cases are updated in #59, #60, #61 and #62.
