### 2. Document Overview

This section describes the organization of the Software Architecture Document (SAD) and lists associated project specifications.

#### 2.1 How to Use This Document
This document defines the architectural blueprint, component design, runtime execution model, and interface contracts for the Supply Chain Management Simulator. It serves as the primary technical reference for engineers, evaluators, and system architects:
- **System Evaluators & Instructors:** Review Section 3.1 (Goals and Constraints), Section 3.3 (Component and Class Diagrams), Section 3.5 (Architecture Pattern), and Section 4.5 (UX Design) to verify architectural compliance, modularity, and runtime simplicity.
- **Developers & Integrators:** Consult Section 3.4 (Component Descriptions), Section 4.1 (Design Overview), Section 4.2 (Sequence Diagrams), and Section 4.3 (API Design) for concrete class interactions, method signatures, parameter types, error handling, and lifecycle semantics.
- **QA & Test Engineers:** Reference Section 3.8 (Traceability to Requirements) and Section 4.4 (Error Handling and Invariants) to corroborate architectural boundaries against the corresponding verification suites defined in the Test Plan.

#### 2.2 Related Documents
The architecture documented herein directly realizes the functional requirements, quality attributes, and verification plans defined across the core engineering deliverables:
1. **Software Requirements Specification (SRS) v1.0:** Defines the 20 functional requirements (`SCM-F-001`–`SCM-F-043`), 5 non-functional requirements (`SCM-NF-001`–`SCM-NF-005`), and security requirements (`SCM-SR-001`–`SCM-SR-007`).
2. **Test Plan v1.0:** Establishes the 15 system test cases (`TC-INV-01`–`TC-REP-01`), coverage criteria, entry/exit criteria, and automated test automation mapping.
3. **Requirements Traceability Matrix (RTM) (SRS Section 8):** Maps each requirement ID to its architectural module, design section, and verifying test suite.
4. **Repository Documentation (`README.md`):** Outlines repository structure, execution instructions, CLI usage parameters, and developer setup.
