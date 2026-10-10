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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the team workflow (feature branches, pull requests, reviews and CI).

## docs/

Project documentation will live in `docs/`. The SRS (Software Requirements Specification), SAD (Software Architecture Document) and Test Plan will be added there.
