# TC-REP-01 — Deterministic reproducibility

| Field | Value |
|---|---|
| Test case | TC-REP-01 — Same seed produces identical output |
| Requirement | SCM-NF-002 |
| Executed by | Pranav |
| Date | 2026-11-05 |
| Commit | 3354d63 |
| Environment | Linux 6.18.55-2-cachyos-lts, Python 3.14.9 |
| Result | PASS |

## Steps and observations

1. scm-sim --days 10 --seed 42 > run1.txt — run completed.
2. scm-sim --days 10 --seed 42 > run2.txt — run completed.
3. diff -q run1.txt run2.txt — files are identical (no differences).
4. scm-sim --days 10 --seed 7 > run3.txt — run completed.
5. diff -q run1.txt run3.txt — files differ, as expected for a different seed.

## Evidence

diff -q run1.txt run2.txt
Files run1.txt and run2.txt are identical

diff -q run1.txt run3.txt
Files run1.txt and run3.txt differ
