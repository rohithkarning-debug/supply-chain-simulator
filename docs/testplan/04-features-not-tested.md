### 4. Features Not to Be Tested

To optimize engineering resources and maintain strict alignment with the system boundary, the following aspects are intentionally excluded from testing:

| Excluded Area | Justification / Boundary Rationale |
|---|---|
| **Python 3.11 Runtime & Standard Library Internals** | Internal mechanisms of Python core data structures (e.g., hash collision handling in `dict`, memory allocation in `dataclasses`, or internal parsing of `argparse`) are verified by CPython's upstream test suite. The project assumes standard library primitives operate according to specification. |
| **Testing & CI Infrastructure Internals** | The internal test discovery algorithms of `pytest`, coverage collection engines of `pytest-cov`, and virtual runner virtualization inside GitHub Actions (`ubuntu-latest`) are assumed correct. Verification focuses on our test assertions and code, not testing the test framework itself. |
| **GUI, Web Interfaces, and Network Stacks** | The simulator is strictly a local command-line and programmatic library. There are no web endpoints, HTTP servers, browser interfaces, REST APIs, or socket listeners implemented. Testing non-existent network interfaces is out of scope. |
| **Persistent Databases & Storage Systems** | All simulation state resides in volatile memory. There are no SQL databases, NoSQL engines, file-based persistence mechanisms, or ORM mappers. |
| **Statistical Distribution of `random.Random`** | The mathematical uniform distribution properties of the Mersenne Twister RNG (`random.Random`) are assumed correct as provided by the language runtime. Verification validates that the seed controls dispatch determinism and delay boundaries ($1 \le \text{delay} \le 3$), not statistical randomness across millions of draws. |
| **Out-of-Scope Domain Features (SRS §1.2)** | Commercial supply chain capabilities—such as real-time GPS fleet tracking, automated purchase order EDI integrations, multi-currency financial accounting, labor scheduling, and multi-echelon DC-to-store routing—are explicitly excluded from the educational project scope. |
