# Supply Chain Management Simulator

Supply Chain Management Simulator: simulates movement of goods from suppliers to warehouses and customers; manages inventory, orders and shipments; flags delays, stockouts and excess inventory.

## Planned modules

- **Inventory** – stock levels per warehouse and SKU
- **Orders** – customer and replenishment orders
- **Shipments** – movement of goods between suppliers, warehouses and customers
- **Suppliers / Warehouses** – network entities and their attributes
- **Simulation engine** – drives time steps and events through the supply chain
- **Analytics** – flags delays, stockouts and excess inventory

## Setup

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
pytest
```

## How to run

The package lives in `src/`, so either run from there or put it on `PYTHONPATH`:

```bash
cd src
python -m scm_sim --days 10 --seed 42
```

```powershell
# from the repo root (PowerShell); use `PYTHONPATH=src python -m scm_sim` in bash
$env:PYTHONPATH = "src"; python -m scm_sim --days 10 --seed 42
```

`--days` (default 10) sets how long to simulate; `--seed` (default 42) fixes the random
shipment delays, so the same seed always gives the same output.

### Sample output (abridged)

```text
Supply Chain Simulator demo: 10 day(s), seed 42

Day 2:
  fulfilled ORD-0003: 40 GADGET from WH-SOUTH
  fulfilled ORD-0004: 20 GIZMO from WH-NORTH
  reorder   SHP-0001: 120 GADGET from SUP-FLAKY -> WH-SOUTH, due day 4
  flags: 0 delayed, 1 stockout, 0 low, 1 excess | fill rate 1.0
Day 3:
  fulfilled ORD-0006: 45 WIDGET from WH-NORTH
  BACKORDER ORD-0005: 30 GADGET from WH-SOUTH
  flags: 0 delayed, 1 stockout, 0 low, 1 excess | fill rate 0.83
...
Day 5:
  arrived   SHP-0001: 120 GADGET -> WH-SOUTH, 1 day(s) late
  fulfilled ORD-0008: 20 WIDGET from WH-NORTH
  fulfilled ORD-0009: 25 GADGET from WH-SOUTH
  filled    ORD-0005: back-order from day 3 now shipped
  reorder   SHP-0003: 150 WIDGET from SUP-RELIABLE -> WH-NORTH, due day 7
  flags: 1 delayed, 0 stockout, 2 low, 1 excess | fill rate 1.0
...

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

## Architecture

`Inventory` (**Rohith**) is the single source of truth for stock: levels, warehouse
capacity and per-item stock policies (reorder point, reorder quantity, max level).
`OrderManager` (**Rohanth Ganesha C**) and `ShipmentManager` (**Rishi J Mule**) share that one
`Inventory` object: orders remove stock when fulfilled (or are back-ordered), and shipments from
suppliers add stock when they arrive, with delays drawn from a seeded random generator.
`analytics` (**Pranav Achar**) is a set of pure functions that turn plain data (a stock snapshot,
shipments and orders) into a report of delays, stockouts, low stock, excess and fill rate.
`Simulation` in `simulator.py` (integration: **Rohith**) owns all of these and drives them one day
at a time: deliver arrivals, then serve today's orders, then retry back-orders, then dispatch
replenishments, then record the day's analytics report. `__main__.py` exposes this as a CLI.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the team workflow (feature branches, pull requests, reviews and CI).

## docs/

Project documentation will live in `docs/`. The SRS (Software Requirements Specification), SAD (Software Architecture Document) and Test Plan will be added there.
