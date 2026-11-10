# TC-REP-01 — Deterministic reproducibility

| Field | Value |
|---|---|
| Test case | TC-REP-01 — Same seed produces identical output |
| Requirement | SCM-NF-002 |
| Executed by | Pranav / Rishi J Mule (Security Test Engineer) |
| Date | 10-11-2026 |
| Commit | 6147266 |
| Environment | Windows 11 (10.0.26300), Python 3.11.9, pytest 9.2.0 |
| Result | PASS |

## Steps and observations

1. `scm-sim --days 10 --seed 42 > run1.txt` — run completed with exit code 0.
2. `scm-sim --days 10 --seed 42 > run2.txt` — run completed with exit code 0.
3. `cmd /c fc run1.txt run2.txt` — files are identical (FC: no differences encountered).
4. `scm-sim --days 10 --seed 1 > run3.txt` — run completed with exit code 0 (comparison seed 1).
5. `cmd /c fc run1.txt run3.txt` — files differ deterministically, reflecting different probabilistic delay outcomes for SUP-FLAKY:
   - Seed 42: SHP-0001 delayed by 1 day (arrives Day 5); Day 10 report lists 2 delayed shipments (SHP-0001, SHP-0002).
   - Seed 1: SHP-0001 arrives on time (Day 4); Day 10 report lists 1 delayed shipment (SHP-0002).
   - Day 4 fill rate is 0.86 in seed 42 (backorder ORD-0005 unfilled until Day 5) vs 1.0 in seed 1 (ORD-0005 filled on arrival Day 4).

## Evidence

### Identical seed comparison (Seed 42 vs Seed 42):
```
Comparing files run1.txt and run2.txt
FC: no differences encountered
```

### Different seed comparison (Seed 42 vs Seed 1):
```
Comparing files run1.txt and run3.txt
Differences:
- Seed 42: Day 5 arrival SHP-0001 (1 day late), Day 10 delayed shipments: 2 (SHP-0001, SHP-0002)
- Seed 1:  Day 4 arrival SHP-0001 (on time), Day 10 delayed shipments: 1 (SHP-0002)
```
