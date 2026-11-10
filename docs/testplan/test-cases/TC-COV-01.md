| Field | Content |
| :--- | :--- |
| **TC ID** | TC-COV-01 |
| **Title** | Test Coverage Gate and Cross-Platform Portability |
| **Requirement(s)** | SCM-NF-003, SCM-NF-004 |
| **Type** | Maintainability |
| **Objective** | Verify that the automated suite passes and maintains at least 90% line coverage of `scm_sim` as required by SCM-NF-003, that the configured CI coverage gate passes, and that the simulator runs on Windows, Linux and macOS on Python 3.11 or later using only the standard library at runtime. Branch coverage is also measured and reported. |
| **Preconditions** | *Automated part:* the repository is hosted on GitHub and the GitHub Actions `test` job is enabled for the `main` branch and for pull requests. *Manual part:* a Windows 11 machine with Python 3.11 and a Linux machine with Python 3.11, each with `pytest` and `pytest-cov` installed from `requirements.txt`. |
| **Test data** | The complete test suite across all test files; standard demo scenario `build_demo(seed=42)` for manual runs. `requirements.txt` inspected for dependencies. |
| **Steps** | *Automated part.* 1. Push a commit to a feature branch and open a pull request to `main`.<br>2. Wait for the `test` job on `ubuntu-latest` with Python 3.11 to complete.<br>3. Inspect the job summary and coverage reports for `scm_sim`.<br>4. Confirm that merging is blocked if tests or the 90% coverage threshold fails.<br>*Manual part.* 5. On Windows 11, install dependencies and run `pytest --cov=scm_sim --cov-branch`.<br>6. On Windows 11, execute `scm-sim --days 10 --seed 42`.<br>7. Repeat steps 5 and 6 on a Linux environment.<br>8. Inspect `requirements.txt` and `pyproject.toml` to verify zero runtime dependencies.<br>9. Run the simulator in an environment containing only standard library packages.<br>10. Record host OS and Python version in test records. |
| **Expected result** | CI job passes with 0 failures and the configured `--cov-fail-under=90` gate; PR merge is blocked on failure; test suite and CLI execute cleanly on each tested platform; runtime dependencies are zero. |
| **Pass/fail criteria** | SCM-NF-003 passes when the tests pass and line coverage is at least 90%; report branch coverage and CI's configured combined coverage gate separately. SCM-NF-004 is fully passed only after Windows, Linux and macOS testing; without macOS evidence, mark it partial. |
| **Automated by** | GitHub Actions `test` job in `.github/workflows/ci.yml`, running `pytest -v --cov=scm_sim --cov-branch --cov-fail-under=90` on `ubuntu-latest` with Python 3.11 on every push to `main` and every pull request. |
| **Actual result** | 100 automated tests passed; line coverage 99.79%, branch coverage 99.17%, combined coverage 99.66%. Windows 11, Linux and CI Ubuntu evidence is recorded; macOS was not tested. See [unit-test report](../../test-reports/unit/unit-test-report.md), [line-coverage report](../../test-reports/coverage/code-coverage-report.md) and [branch-coverage report](../../test-reports/branch-coverage/branch-coverage-report.md). |
| **Status** | SCM-NF-003 Passed; SCM-NF-004 Partially validated (macOS not tested) |

Updated 09-11-2026: reconciled 100-test and exact coverage evidence; explicitly retained SCM-NF-004 as partial because macOS was not tested.
