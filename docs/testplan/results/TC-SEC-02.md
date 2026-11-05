# Test Result: TC-SEC-02 Branch Protection, Secrets and Dependency Check

| Field | Value |
|---|---|
| Test case | TC-SEC-02 |
| Requirement(s) | SCM-SR-005, SCM-SR-006 (SCM-SO-2) |
| Executed by | Rohith Karning |
| Date | 05-11-2026 |
| Commit tested | c6040d8 |
| Environment | Windows 11, PowerShell, Git; GitHub web, logged in as the repository owner (admin) |
| Result | PASS |

## Steps and observations

| # | Step | Expected | Actual | Result |
|---|---|---|---|---|
| 1 | Branch rule for main (Settings > Branches) | PR required, 1 approval, stale approvals dismissed, required check `test`, up to date, no bypass, no force push, no deletion | All as expected: PR required, 1 approval, dismiss stale approvals on, required status check `test` (GitHub Actions), branches must be up to date, "Do not allow bypassing the above settings" on, force pushes off, deletions off. Code-owner review, signed commits and linear history are off (not required by the test). | PASS |
| 2 | Direct push and force push to main as admin | Both rejected | Both rejected with "GH006: Protected branch update failed for refs/heads/main. Changes must be made through a pull request. Required status check "test" is expected." (protected branch hook declined) | PASS |
| 3 | PR without approval (PR #76) | Merge blocked ("Review required"); author cannot self-approve | All 4 checks passed (test, commits, label, title), but the merge box showed "Review required. At least 1 approving review is required by reviewers with write access. Merging is blocked." The merge button was disabled. Approve was disabled: "Pull request authors can't approve their own pull requests." PR #76 was closed without merging and the sec-check branch deleted. | PASS |
| 4 | Secrets scan of full git history + GitHub secret scanning | No secrets | The only matches are the search patterns written in docs/testplan/test-cases/TC-SEC-02.md itself (in its different versions); no real credentials. GitHub secret scanning is enabled: 0 open, 0 closed alerts ("No secrets found."). | PASS |
| 5 | Network code in src/scm_sim | No matches | No matches for socket, urllib, http or requests. | PASS |
| 6 | Dependencies | Test-only requirements; standard-library-only imports | requirements.txt: pytest>=8.0, pytest-cov>=5.0 (test tools only). pyproject.toml: dependencies = []. Imports: __future__, argparse, dataclasses, enum, random, typing, and the package's own scm_sim modules. | PASS |

## Evidence

- TC-SEC-02-settings.png: branch rule showing the required status check `test`
- Step 2 push output: "remote: error: GH006: Protected branch update failed for refs/heads/main." / "! [remote rejected] sec-check -> main (protected branch hook declined)" (both the normal and the force push)
- PR #76: closed with unmerged commits, comment "TC-SEC-02 step 3 complete: merge blocked without an approving review; author cannot approve their own PR."

## Notes

- Step 3 was observed by the repository owner only; no second team member checked the merge button. The branch rule applies to everyone ("Do not allow bypassing"), so the result is the same for every account.
- The secrets-scan pattern matches its own definition in the test case file. This is expected and is not a secret.