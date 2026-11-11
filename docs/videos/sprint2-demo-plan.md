# Sprint 2 Two-Minute Demo Video Plan & Execution Script

| Field | Value |
|---|---|
| Document | Sprint 2 Demo Video Plan & Execution Script |
| Target File | `docs/videos/sprint2-demo.mp4` |
| Presenter | Rishi J Mule (Security Test Engineer, Team 02) |
| Target Duration | ~120 seconds (2:00) |
| Status | **Recorded & Uploaded** (`docs/videos/sprint2-demo.mp4`, 7.6 MB) |

---

## Demonstration Scope & Requirements Checklist

| Requirement | Section | Demonstration Action |
|---|---|---|
| 1. One-command installation | Scene 1 (0:00 - 0:20) | `pip install -e .` from repo root |
| 2. Running SCM demo | Scene 2 (0:20 - 0:45) | `scm-sim --days 10 --seed 42` showing arrivals, back-orders, deliveries |
| 3. Multi-day run summary | Scene 3 (0:45 - 1:05) | `scm-sim --days 10 --seed 42 --summary` showing `=== Run Summary ===` |
| 4. CSV export | Scene 4 (1:05 - 1:25) | `scm-sim --days 10 --seed 42 --csv metrics.csv` and inspect CSV in Excel / editor |
| 5. Per-item stock thresholds | Scene 5 (1:25 - 1:45) | Highlight `GIZMO` (threshold 500) vs `WIDGET`/`GADGET` in report and test |
| 6. Docs & Reports showcase | Scene 6 (1:45 - 2:00) | Show `docs/test-reports/`, `docs/deviations.md`, and passing 100 tests |

---

## Scene-by-Scene Script (120 Seconds)

### Scene 1: Introduction & Single-Command Installation (0:00 – 0:20)
- **Visual:** Terminal window open at the repository root.
- **Spoken / Action:**
  > *"Hello, I am Rishi, Security Test Engineer for Team 02. In this Sprint 2 walkthrough, we demonstrate the Supply Chain Management Simulator v1.0. First, installation is executed with one single command using pip:"*
- **Command:**
  ```powershell
  python -m pip install -e .
  ```
- **Expected Outcome:** Package installs cleanly with console script `scm-sim` registered on PATH.

### Scene 2: Running the Standard 10-Day Demo (0:20 – 0:45)
- **Visual:** Terminal execution of the installed console entry point.
- **Spoken / Action:**
  > *"Next, we execute the standard 10-day discrete event simulation using seed 42:"*
- **Command:**
  ```powershell
  scm-sim --days 10 --seed 42
  ```
- **Key Highlights:**
  - Day 1–10 daily event logs (shipment arrivals, order fulfillments, reorders).
  - Backorder behavior: `ORD-0005` backordered on Day 3 and fulfilled upon arrival on Day 5.
  - Final Day 10 report: 2 delayed shipments, 0 stockouts, 1 excess item, 14 orders fulfilled (100% fill rate).

### Scene 3: Multi-Day Run Summary (0:45 – 1:05)
- **Visual:** Terminal execution with the new `--summary` flag (Feature #53 / SCM-F-034).
- **Spoken / Action:**
  > *"New in Sprint 2 is the multi-day run summary flag, `--summary`, aggregating metrics across the whole timeline:"*
- **Command:**
  ```powershell
  scm-sim --days 10 --seed 42 --summary
  ```
- **Key Highlights:**
  - Point to the `=== Run Summary ===` block at the end:
    - `days: 10`
    - `days_with_delays: 6`
    - `days_with_stockouts: 3`
    - `days_with_low_stock: 3`
    - `days_with_excess: 10`
    - `peak_delayed: 2`
    - `final_fill_rate: 1.0`

### Scene 4: CSV Export & Spreadsheet Inspection (1:05 – 1:25)
- **Visual:** Exporting metrics to CSV and opening in Excel or terminal viewer.
- **Spoken / Action:**
  > *"We can also export day-by-day telemetry to a standard CSV file using the `--csv` option:"*
- **Command:**
  ```powershell
  scm-sim --days 10 --seed 42 --csv metrics.csv
  Get-Content metrics.csv -Head 6
  ```
- **Key Highlights:**
  - Show CSV header: `day,delayed,stockouts,low_stock,excess,pending,fulfilled,backordered,cancelled,fill_rate`.
  - Show daily flat telemetry rows suitable for business intelligence analysis.

### Scene 5: Per-Item Stock Thresholds & Defect Fixes (1:25 – 1:45)
- **Visual:** Show code / Day 10 excess output for `WH-NORTH / GIZMO`.
- **Spoken / Action:**
  > *"In Sprint 1, global thresholds flagged false alerts. In Sprint 2 (SCM-F-031), each SKU evaluates against its individual stock policy—here GIZMO has a max level of 500, correctly flagging 100 surplus units. Overflowing arrivals also stay safely in transit without aborting other deliveries (SCM-F-023)."*

### Scene 6: Documentation, Test Reports & 100% Suite (1:45 – 2:00)
- **Visual:** Run pytest and switch to VS Code file explorer.
- **Spoken / Action:**
  > *"Finally, we run our full automated regression suite:"*
- **Command:**
  ```powershell
  python -m pytest -q
  ```
- **Key Highlights:**
  - Terminal shows: `100 passed, 0 failures` with 99% line and branch coverage.
  - Quick glance at `docs/deviations.md` and `docs/test-reports/system-validation/system-validation-report.md`.
  - Conclude: *"All 34 requirements are validated and production-ready. Thank you."*

---

## Recording Instructions for User
1. Open terminal on your host machine.
2. Press **Win + Alt + R** (Windows Game Bar) or open Snipping Tool / OBS.
3. Follow the 6 scenes above following the exact commands.
4. Save the MP4 file to:
   ```
   docs/videos/sprint2-demo.mp4
   ```

