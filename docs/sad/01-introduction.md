# Software Architecture Document
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
2. Document Overview
   - 2.1 How to Use This Document
   - 2.2 Related Documents
3. Architecture
   - 3.1 Architectural Goals and Constraints
   - 3.2 Stakeholders and Concerns
   - 3.3 Component Diagram and Domain Class Diagram
   - 3.4 Component Descriptions
   - 3.5 Architecture Pattern and Rationale
   - 3.6 Technology Stack and Data Stores
   - 3.7 Risks and Mitigations
   - 3.8 Traceability to Requirements
   - 3.9 Security Architecture
4. Design
   - 4.1 Design Overview
   - 4.2 UML Sequence Diagrams
   - 4.3 API Design
   - 4.4 Error Handling and Logging
   - 4.5 UX Design
   - 4.6 Open Issues and Next Steps
5. Appendices
   - 5.1 Glossary
   - 5.2 References
   - 5.3 Tools

---

## 1. Introduction

### 1.1 Purpose

This Software Architecture Document (SAD) describes the architecture and detailed design of the **Supply Chain Management Simulator** (Python package `scm_sim`), version 1.0. It explains how the system is decomposed into components, how those components depend on and interact with each other, which architectural pattern was chosen and why, and how each component's public interface behaves, including its errors.

The SAD is the bridge between the requirements in the Software Requirements Specification (SRS v1.0) and the verification described in the Test Plan (Test Plan v1.0). Every design element is traced back to requirement IDs from `docs/requirements-registry.md` (`SCM-F-xxx`, `SCM-NF-xxx`, `SCM-SR-xxx`).

The architecture described here is the one **actually implemented and merged** on the `main` branch at commit `b3702ef`. All component, class, method, exception and file names match the source code in `src/scm_sim/`. This document follows the viewpoint-based approach of ISO/IEC/IEEE 42010:2011, adapted to the course template.

### 1.2 Scope

The document covers:

- The **static structure** of the system: seven components (Inventory, Order Manager, Shipment Manager, Analytics, Simulation Engine, CLI, CI Pipeline), the domain classes inside them, and their dependencies (§3.3, §3.4).
- The **architecture pattern**, a layered, modular architecture inside one Python package, together with the alternatives that were rejected (§3.5).
- The **dynamic behaviour** of one simulated day and two key scenarios, order fulfilment with back-ordering and detection of a delayed shipment, as UML sequence diagrams (§4.1, §4.2).
- The **API design** of all five code components: signature, parameters, return value, exceptions and an example for every public call (§4.3).
- **Error handling**, the command-line **user experience**, **security architecture** (STRIDE) and **open issues** (§3.9, §4.4–§4.6).

The following are outside the scope of this document, because the system does not have them: graphical or web user interfaces, databases or files used for storage, network services, user accounts and authentication. The development pipeline (GitHub, pull requests and GitHub Actions CI) is covered only where it supports the quality and security requirements.

### 1.3 Intended Audience

| Reader | Sections of most interest |
|---|---|
| Course Coordinator / Instructor / Evaluator | §3.3–§3.5 (structure and pattern), §3.8 (traceability), §4.2 (sequence diagrams) |
| Developers (team members) | §3.4 (component responsibilities), §4.3 (API), §4.4 (error handling), §4.6 (open issues) |
| Testers / QA Lead | §4.3 (expected behaviour and exceptions to test), §3.8 (requirement-to-component mapping) |
| Security Test Engineer | §3.9 (STRIDE threat model), §4.4 (validation and invariants) |
| Supply Chain Analyst | §4.1 (how a simulated day works), §4.5 (CLI usage and output) |

### 1.4 Definitions, Acronyms and Abbreviations

| Term | Definition |
|---|---|
| **Component** | A cohesive unit of the system with a defined responsibility and public interface; here, one Python module (or the CI workflow) |
| **Domain layer** | The components that hold supply-chain state and rules: Inventory, Order Manager, Shipment Manager |
| **Orchestration** | Coordinating the domain components in a fixed order; done by the Simulation Engine |
| **Pure function** | A function whose result depends only on its arguments and which changes no state; all Analytics functions are pure |
| **Snapshot** | An independent copy of all stock levels, `{(warehouse, sku): qty}`, returned by `Inventory.snapshot()` |
| **Daily step** | One call to `Simulation.step()`, which simulates exactly one day |
| **Replenishment** | A shipment from a supplier to a warehouse, dispatched automatically when an item reaches its reorder point |
| **Invariant** | A condition that always holds, e.g. stock is never negative |
| **SKU** | Stock Keeping Unit, e.g. `WIDGET` |
| **SCM** | Supply Chain Management |
| **Lead time / Reliability** | Supplier's base delivery time in days / probability (0.0–1.0) of arriving on the expected day |
| **Stockout / Back-order / Excess** | Stock exactly 0 / an order waiting for stock / stock above an item's max level |
| **Fill rate** | Fulfilled orders ÷ (total − cancelled orders) |
| **Dataclass** | A Python class declared with `@dataclass`, used for plain data records (`Order`, `Shipment`, `Supplier`, `StockPolicy`, `ScheduledOrder`, `DayLog`) |
| **STRIDE** | Threat categories: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege |
| **CI** | Continuous Integration (GitHub Actions job `test`) |
| **CLI** | Command-Line Interface (`python -m scm_sim`) |
| **PR** | Pull Request |
| **UML** | Unified Modeling Language |
| **SRS / SAD** | Software Requirements Specification / Software Architecture Document |
