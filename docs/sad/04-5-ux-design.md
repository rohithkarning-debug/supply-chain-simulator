### 4.5 User Experience (UX) Design: Command-Line Interface

The Supply Chain Management Simulator exposes a command-line interface via the installed console script `scm-sim` and, for source-tree execution, `python -m scm_sim`. The user experience is designed for clarity, deterministic inspection, self-documentation, and concise reporting.

#### 4.5.1 Command-Line Arguments and Options
The CLI uses Python's standard `argparse` library to accept operational parameters:

| Argument | Type | Default | Description |
|---|---|---|---|
| `--days` | `int` | `10` | Number of simulated days to run. Must be an integer $\ge 1$. Supplying a value $< 1$ triggers a usage error. |
| `--seed` | `int` | `42` | Random seed controlling supplier dispatch delays. Ensures deterministic reproducibility across runs. |
| `--summary` | flag | off | Prints `=== Run Summary ===` with aggregated counts for the entire simulation run. |
| `--csv PATH` | path | none | Writes a CSV file with one row per day and the columns `day,delayed,stockouts,low_stock,excess,pending,fulfilled,backordered,cancelled,fill_rate`. |
| `-h`, `--help` | flag | – | Prints full usage syntax, description, and available parameter flags, then exits with code 0. |

**Invocation Example:**
```bash
scm-sim --days 10 --seed 42 --summary
```

#### 4.5.2 Day-by-Day Console Output Format
During execution, each simulation day emits a concise summary log line reflecting the core domain events:
```text
Day 10:
  fulfilled ORD-0014: 15 WIDGET from WH-SOUTH
  flags: 2 delayed, 0 stockout, 0 low, 1 excess | fill rate 1.0
```
This is the actual day-10 line from the verified `scm-sim --days 10 --seed 42 --summary` run. Other days similarly report any arrivals (including capacity-blocked arrivals), fulfilled or back-ordered orders, back-orders filled and replenishment dispatches, followed by their day-level flags.

#### 4.5.3 Final Summary Report Layout
Upon simulation completion, the CLI prints the formatted daily report for the last simulated day, and optionally the `=== Run Summary ===` block when `--summary` is supplied. Empty anomaly sections explicitly print `"No issues"` rather than remaining blank:

```text
=== Supply Chain Report: Day 10 ===

Delayed shipments (2)
  - SHP-0001: GADGET to WH-SOUTH, 1 day(s) late
  - SHP-0002: WIDGET to WH-SOUTH, 1 day(s) late

Stockouts (0)
  No issues

Low stock (0)
  No issues

Excess (1)
  - WH-NORTH / GIZMO: 600 (surplus 100)

Orders (14)
  pending 0, fulfilled 14, backordered 0, cancelled 0
  fill rate: 1.0
```

The output above is from `scm-sim --days 10 --seed 42 --summary`. When `--summary` is enabled, the following verified block is printed after the final report:

```text
=== Run Summary ===
  days: 10
  days_with_delays: 6
  days_with_stockouts: 3
  days_with_low_stock: 3
  days_with_excess: 10
  peak_delayed: 2
  final_fill_rate: 1.0
```

#### 4.5.4 Process Exit Codes
The CLI conforms to standard POSIX exit status conventions:
- **`0` (Success):** Simulation completed all days normally and rendered the normal day-by-day output; an optional run summary was printed if requested.
- **`2` (Usage Error):** Invalid command-line arguments provided (e.g., `--days 0`, unknown flags, or non-integer values). A syntax error message and usage synopsis are printed to standard error.
