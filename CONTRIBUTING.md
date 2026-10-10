# Team Workflow
1. Clone the repo; don't fork it: `git clone <repo-url>`
2. Always start from the latest main: `git checkout main && git pull`
3. Create a feature branch: `git checkout -b feature/<short-name>`
4. Write the feature and its test case(s) in `tests/`.
5. Run the tests locally: `pip install -r requirements.txt && pytest`
6. Push the branch: `git push -u origin feature/<short-name>`
7. Open a Pull Request into main and request a teammate's review.
8. Merge only after CI passes and at least one approval.
9. After merging, everyone runs `git checkout main && git pull`.
Direct pushes to main are blocked.
