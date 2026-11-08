| Field | Content |
| :--- | :--- |
| **TC ID** | TC-COV-01 |
| **Title** | Test Coverage Gate and Cross-Platform Portability |
| **Requirement(s)** | SCM-NF-003, SCM-NF-004 |
| **Type** | Maintainability |
| **Objective** | Verify that the automated suite maintains at least 90% line and branch coverage of the `scm_sim` package and that all tests pass before a merge is permitted, and that the simulator runs unchanged on Windows, Linux and macOS on Python 3.11 or later using only the standard library at runtime. |
| **Preconditions** | *Automated part:* the repository is hosted on GitHub and the GitHub Actions `test` job is enabled for the `main` branch and for pull requests. *Manual part:* a Windows 11 machine with Python 3.11 and a Linux machine with Python 3.11, each with `pytest` and `pytest-cov` installed from `requirements.txt`. |
| **Test data** | The complete test suite across all test files; standard demo scenario `build_demo(seed=42)` for manual runs. `requirements.txt` inspected for dependencies. |
| **Steps** | *Automated part.* 1. Push a commit to a feature branch and open a pull request to `main`.<br>2. Wait for the `test` job on `ubuntu-latest` with Python 3.11 to complete.<br>3. Inspect the job summary and coverage reports for `scm_sim`.<br>4. Confirm that merging is blocked if tests or the 90% coverage threshold fails.<br>*Manual part.* 5. On Windows 11, install dependencies and run `pytest --cov=scm_sim --cov-branch`.<br>6. On Windows 11, execute `scm-sim --days 10 --seed 42`.<br>7. Repeat steps 5 and 6 on a Linux environment.<br>8. Inspect `requirements.txt` and `pyproject.toml` to verify zero runtime dependencies.<br>9. Run the simulator in an environment containing only standard library packages.<br>10. Record host OS and Python version in test records. |
| **Expected result** | CI job passes with 0 failures, enforcing `--cov-fail-under=90`; PR merge blocked on failure; test suite and CLI execute cleanly without platform errors across Windows 11 and Linux; runtime dependencies are strictly zero. |
| **Pass/fail criteria** | **Pass** if CI test job passes with $\ge 90\%$ line and branch coverage, merge protection is enforced, and suite runs on Windows and Linux; **Fail** if coverage drops below 90%, tests fail, or runtime third-party dependencies are required. |
| **Automated by** | GitHub Actions `test` job in `.github/workflows/ci.yml`, running `pytest -v --cov=scm_sim --cov-branch --cov-fail-under=90` on `ubuntu-latest` with Python 3.11 on every push to `main` and every pull request. |
| **Actual result** | Pass (99% line + branch, CI gate --cov-fail-under=90; Windows 11, Linux and CI ubuntu; macOS not run), evidence docs/test-reports/coverage/ and docs/test-reports/branch-coverage/. |
| **Status** | Passed (Windows 11 and Linux; macOS not run) |

Updated 08-11-2026: recorded coverage and portability results (#61)
