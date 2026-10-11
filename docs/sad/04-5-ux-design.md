### 4.5 User Experience (UX) Design: Command-Line Interface

The Supply Chain Management Simulator provides a command-line interface (CLI) executed as an executable Python module (`python -m scm_sim`). The user experience is designed for clarity, deterministic inspection, self-documentation, and concise reporting.

#### 4.5.1 Command-Line Arguments and Options
The CLI uses Python's standard `argparse` library to accept operational parameters:

| Argument | Type | Default | Description |
|---|---|---|---|
| `--days` | `int` | `10` | Number of simulated days to run. Must be an integer $\ge 1$. Supplying a value $< 1$ triggers a usage error. |
| `--seed` | `int` | `42` | Random seed controlling supplier dispatch delays. Ensures deterministic reproducibility across runs. |
| `-h`, `--help` | flag | – | Prints full usage syntax, description, and available parameter flags, then exits with code 0. |

**Invocation Example:**
```bash
python -m scm_sim --days 10 --seed 42
```

#### 4.5.2 Day-by-Day Console Output Format
During execution, each simulation day emits a concise summary log line reflecting the core domain events:
```text
Day  1: arrivals=0, orders_placed=2, fulfilled=1, backordered=1, replenishments=1
Day  2: arrivals=1, orders_placed=1, fulfilled=2, backordered=0, replenishments=0
...
Day 10: arrivals=0, orders_placed=1, fulfilled=1, backordered=0, replenishments=1
```
Each entry displays the simulation day followed by the count of shipment arrivals, customer orders placed, orders fulfilled, active backorders, and replenishment shipments dispatched.

#### 4.5.3 Final Summary Report Layout
Upon simulation completion, the CLI prints a structured report partitioned into clear operational sections. Empty anomaly sections explicitly print `"No issues"` rather than remaining blank:

```text
============================================================
              FINAL SIMULATION REPORT (Day 10)              
============================================================

DELAYED SHIPMENTS (Count: 1):
  - Shipment SHP-0002 (SKU: GADGET, Warehouse: WH-SOUTH): 2 days late

STOCKOUTS (Count: 1):
  - Warehouse: WH-NORTH, SKU: GIZMO (Level: 0)

LOW STOCK (Count: 1):
  - Warehouse: WH-SOUTH, SKU: WIDGET (Level: 15, Reorder Point: 20)

EXCESS INVENTORY (Count: 0):
  No issues

ORDER METRICS:
  - Total Orders:      14
  - Pending:            0
  - Fulfilled:         12
  - Backordered:        1
  - Cancelled:          1
  - Customer Fill Rate: 92.31%
============================================================
```

#### 4.5.4 Process Exit Codes
The CLI conforms to standard POSIX exit status conventions:
- **`0` (Success):** Simulation completed all days normally and rendered the summary report.
- **`2` (Usage Error):** Invalid command-line arguments provided (e.g., `--days 0`, unknown flags, or non-integer values). A syntax error message and usage synopsis are printed to standard error.
