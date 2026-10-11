# Software Requirements Specification
## Supply Chain Management Simulator

| Field | Value |
|---|---|
| Project | Supply Chain Management Simulator |
| Version | 1.0 |
| Authors | Team NN – Rohith Karning, Rohanth Ganesha C, Rishi J Mule, Pranav Achar |
| Date | 11-10-2026 |
| Status | Draft |

### Revision History

| Version | Date | Author(s) | Description of change | Approval |
|---|---|---|---|---|
| 1.0 | 11-10-2026 | Team NN | Initial draft | Pending |

### Approvals

| Name | Role | Signature | Date |
|---|---|---|---|
| | Course Coordinator | | |
| Rohith Karning | Product Owner / Integrator | | |
| Rohanth Ganesha C | QA Lead | | |
| Rishi J Mule | Security Test Engineer | | |
| Pranav Achar | Dev Lead | | |

### Table of Contents

1. Introduction
   - 1.1 Purpose
   - 1.2 Scope
   - 1.3 Intended Audience
   - 1.4 Definitions, Acronyms and Abbreviations
2. Overall Description
   - 2.1 Product Perspective
   - 2.2 Major Product Functions
   - 2.3 User Classes and Characteristics
   - 2.4 Operating Environment
   - 2.5 Design and Implementation Constraints
   - 2.6 Assumptions and Dependencies
3. External Interface Requirements
   - 3.1 User Interface
   - 3.2 Hardware Interfaces
   - 3.3 Software Interfaces
   - 3.4 Communications Interfaces
4. System Features
   - 4.1 Inventory Management
   - 4.2 Order Management
   - 4.3 Shipment & Supplier Management
   - 4.4 Analytics & Reporting
   - 4.5 Simulation Engine & CLI
5. Non-Functional Requirements
   - 5.1 Security (5.1.1 Security Objectives, 5.1.2 Security Requirements)
6. Quality Attributes & Acceptance Tests
7. System Models
   - 7.1 UML Use-Case Diagrams
8. Requirements Traceability Matrix

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) defines the functional, non-functional and security requirements of the **Supply Chain Management Simulator** (package `scm_sim`), version 1.0. The simulator models the movement of goods from suppliers to warehouses and on to customers, one simulated day at a time. It manages inventory, customer orders and replenishment shipments, and it identifies delayed shipments, stockouts and excess inventory.

The document serves three purposes:

1. It is the agreed baseline of what the system shall do, against which the design (Software Architecture Document, SAD v1.0) and the verification activities (Test Plan v1.0) are traced.
2. It assigns every requirement a fixed identifier (`SCM-F-xxx`, `SCM-NF-xxx`, `SCM-SO-x`, `SCM-SR-xxx`) and a measurable acceptance criterion (`AC-SCM-…`) linked to a test case (`TC-XXX-NN`). These identifiers are registered in `docs/requirements-registry.md` and are used unchanged in all three project documents.
3. It describes the system **as built and merged** on the `main` branch of the team repository (commit `b3702ef`), not a planned or hypothetical product.

This SRS follows the structure of IEEE Std 830-1998 and ISO/IEC/IEEE 29148:2018, adapted to the course template.

### 1.2 Scope

The Supply Chain Management Simulator is a standalone, command-line Python program. A user configures a scenario (suppliers, warehouses, stock policies, initial stock and scheduled customer demand), runs it for a number of days, and receives a day-by-day log plus an analytics report. All data is held in memory for the duration of a run; nothing is stored in files, databases or over a network.

**In scope**

| Area | What the system does |
|---|---|
| Suppliers | Registers suppliers with a lead time (days) and an on-time reliability (0.0–1.0) |
| Warehouses | Registers warehouses with a total capacity in units across all SKUs |
| Inventory | Tracks stock per (warehouse, SKU); applies per-item stock policies (reorder point, reorder quantity, max level) |
| Customer orders | Creates orders, fulfils them in full when stock allows, back-orders them otherwise, retries back-orders oldest first, and supports cancellation |
| Shipments with delays | Dispatches replenishment shipments from suppliers to warehouses; delays are drawn from a seeded random generator according to supplier reliability |
| Automatic replenishment | Each day, dispatches one replenishment per item at or below its reorder point that has nothing already in transit, trimmed to warehouse capacity |
| Analytics reports | Reports delayed shipments, stockouts, low stock, excess inventory and order metrics (including fill rate) for every simulated day |
| CLI demo | `python -m scm_sim --days N --seed S` runs a built-in demonstration scenario and prints the daily log and the final report |

**Out of scope**

- Graphical or web user interface
- Integration with real ERP (Enterprise Resource Planning) or WMS (Warehouse Management System) products
- Databases or any persistent storage
- Cost, pricing and profit calculations
- Demand forecasting (demand is scheduled in advance by the user)
- Multi-echelon networks (for example supplier → distribution centre → store)
- Real-time tracking of physical shipments

**Benefits.** The simulator lets a supply chain analyst or student observe, in a reproducible way, how lead times, supplier reliability and stock policies lead to delays, stockouts, back-orders and excess inventory, without needing real company data.

### 1.3 Intended Audience

| Reader | How to use this document |
|---|---|
| Course Coordinator / Instructor / Evaluator | Assess completeness and quality of the requirements; use §6 and §8 to check that every requirement is tested |
| Supply Chain Analyst (primary user) | Understand what the simulator can and cannot model (§1.2, §2, §4) |
| Developers (team members) | Implement and extend modules according to §4 and §5; keep IDs consistent with the SAD and Test Plan |
| Testers / QA Lead | Derive and maintain test cases from the acceptance criteria in §4–§6 and the traceability matrix in §8 |
| Security Test Engineer | Verify the security objectives and requirements in §5.1 |

Readers new to the project should read §1 and §2 first, then the feature section relevant to them in §4.

### 1.4 Definitions, Acronyms and Abbreviations

| Term | Definition |
|---|---|
| **SCM** | Supply Chain Management: planning and controlling the flow of goods from suppliers through warehouses to customers |
| **SKU** | Stock Keeping Unit: an identifier for one distinct product, e.g. `WIDGET`, `GADGET`, `GIZMO` |
| **Lead time** | The number of days between a shipment's dispatch and its expected arrival (`Supplier.lead_time_days`) |
| **Reliability** | A supplier's probability, between 0.0 and 1.0, that a shipment arrives on its expected day; a delayed shipment arrives 1–3 days late |
| **Stockout** | The state of an item whose stock level at a warehouse is exactly 0 |
| **Back-order** | A customer order that could not be fulfilled in full because of insufficient stock; it has status `BACKORDERED` and is retried on later days |
| **Reorder point** | The stock level at or below which an item needs replenishment (default 20) |
| **Reorder quantity** | The number of units requested when an item is replenished (default 100) |
| **Max level** | The stock level above which an item is considered excess (default 500) |
| **Excess inventory** | Stock of an item above its max level; the amount above is the *surplus* |
| **Fill rate** | Fulfilled orders ÷ (total orders − cancelled orders), rounded to 2 decimal places; 0.0 when there are no eligible orders |
| **Seed** | The integer used to initialise the random number generator (`random.Random(seed)`); the same seed and scenario always produce the same output |
| **Day / step** | One discrete simulated day; day 0 is set-up time and the first step simulates day 1 |
| **CI** | Continuous Integration: automatic execution of the test suite (GitHub Actions job `test`) on every push to `main` and every pull request |
| **PR** | Pull Request: a proposed change on a branch that must be reviewed and approved before merging into `main` |
| **CLI** | Command-Line Interface: the program is run from a terminal as `python -m scm_sim` |
| **RTM** | Requirements Traceability Matrix: the table in §8 linking each requirement to design, module and test cases |
| **FR / NFR** | Functional Requirement / Non-Functional Requirement |
| **SO / SR** | Security Objective / Security Requirement |
| **AC** | Acceptance Criterion, identified as `AC-<Req ID>` |
| **TC** | Test Case, identified as `TC-<area>-NN` |
| **SAD** | Software Architecture Document (companion document, v1.0) |
