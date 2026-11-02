"""Day-by-day simulation engine that wires inventory, orders, shipments and analytics together.

Each call to :meth:`Simulation.step` advances the clock by one day and runs the
supply chain in a fixed order: receive arrivals, retry back-orders (oldest
first), serve today's demand, replenish low stock, then record an analytics
report.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from scm_sim.analytics import build_report, format_report
from scm_sim.inventory import Inventory, StockPolicy
from scm_sim.orders import Order, OrderManager, OrderStatus
from scm_sim.shipments import Shipment, ShipmentManager, Supplier

Report = Dict[str, Any]


@dataclass(frozen=True)
class ScheduledOrder:
    """Customer demand queued for a future day."""

    customer_id: str
    warehouse_id: str
    sku: str
    quantity: int


@dataclass
class DayLog:
    """What happened during one simulated day (used for the day-by-day printout)."""

    day: int
    delivered: List[Shipment] = field(default_factory=list)
    blocked: List[Shipment] = field(default_factory=list)
    fulfilled: List[Order] = field(default_factory=list)
    backordered: List[Order] = field(default_factory=list)
    backorders_filled: List[Order] = field(default_factory=list)
    reorders: List[Shipment] = field(default_factory=list)


class Simulation:
    """Discrete, day-by-day supply chain simulation.

    Day 0 is setup time; the first call to :meth:`step` simulates day 1.
    All randomness (shipment delays) comes from one ``random.Random(seed)``,
    so the same seed and setup always produce the same reports.
    """

    def __init__(self, seed: int = 42, reorder_point: int = 20, max_level: int = 500) -> None:
        """Create the inventory, order manager and seeded shipment manager.

        Args:
            seed: Seed for the shipment-delay random number generator.
            reorder_point: Low-stock threshold used in analytics reports.
            max_level: Excess-stock threshold used in analytics reports.
                (Analytics takes one global threshold; per-item policies still
                drive the actual reorder decisions.)
        """
        self.seed = seed
        self.reorder_point = reorder_point
        self.max_level = max_level
        self.day = 0
        self.inventory = Inventory()
        self.orders = OrderManager(self.inventory)
        self.shipments = ShipmentManager(self.inventory, rng=random.Random(seed))
        self.history: List[Report] = []
        self.logs: List[DayLog] = []
        self._warehouses: Dict[str, int] = {}
        self._suppliers: Dict[str, Supplier] = {}
        self._item_supplier: Dict[Tuple[str, str], str] = {}
        self._schedule: Dict[int, List[ScheduledOrder]] = {}

    # ----- setup -----------------------------------------------------------

    def add_supplier(
        self, supplier_id: str, name: str, lead_time_days: int = 2, reliability: float = 1.0
    ) -> Supplier:
        """Register a supplier with its base lead time and on-time probability."""
        supplier = Supplier(supplier_id, name, lead_time_days, reliability)
        self.shipments.add_supplier(supplier)
        self._suppliers[supplier_id] = supplier
        return supplier

    def add_warehouse(self, warehouse_id: str, capacity: int) -> None:
        """Register a warehouse and its total capacity (units across all SKUs)."""
        self.inventory.register_warehouse(warehouse_id, capacity)
        self._warehouses[warehouse_id] = capacity

    def set_policy(
        self, warehouse_id: str, sku: str, supplier_id: str, policy: Optional[StockPolicy] = None
    ) -> None:
        """Set the stock policy for an item and the supplier that replenishes it.

        Raises:
            KeyError: If the warehouse or supplier has not been added.
        """
        self._require_warehouse(warehouse_id)
        if supplier_id not in self._suppliers:
            raise KeyError(f"Unknown supplier: '{supplier_id}'")
        self.inventory.set_policy(warehouse_id, sku, policy or StockPolicy())
        self._item_supplier[(warehouse_id, sku)] = supplier_id

    def add_stock(self, warehouse_id: str, sku: str, quantity: int) -> int:
        """Place initial stock in a warehouse; returns the new level."""
        self._require_warehouse(warehouse_id)
        return self.inventory.add(warehouse_id, sku, quantity)

    def schedule_order(
        self, day: int, customer_id: str, warehouse_id: str, sku: str, quantity: int
    ) -> None:
        """Queue customer demand to be created and fulfilled on ``day``.

        Raises:
            ValueError: If ``day`` has already been simulated or quantity <= 0.
            KeyError: If the warehouse has not been added.
        """
        if day <= self.day:
            raise ValueError(f"day {day} is not in the future (current day is {self.day})")
        if quantity <= 0:
            raise ValueError("quantity must be greater than 0")
        self._require_warehouse(warehouse_id)
        self._schedule.setdefault(day, []).append(
            ScheduledOrder(customer_id, warehouse_id, sku, quantity)
        )

    # ----- running ---------------------------------------------------------

    def step(self) -> Report:
        """Advance one day and return that day's analytics report.

        Order of events:
            1. deliver shipments arriving today into inventory
            2. retry open back-orders (oldest first), so earlier customers
               are served before today's new demand (issue #27, SAD 4.6 L4)
            3. create today's customer orders and try to fulfil each
            4. dispatch a replenishment for each item needing a reorder
               that has nothing already in transit
            5. build and store the analytics report
        """
        self.day += 1
        day = self.day
        log = DayLog(day)

        log.delivered = self.shipments.process_arrivals(day)
        log.blocked = list(self.shipments.last_blocked)

        log.backorders_filled = self.orders.process_open(day)

        for demand in self._schedule.pop(day, []):
            order = self.orders.create(
                demand.customer_id, demand.warehouse_id, demand.sku, demand.quantity, day
            )
            if self.orders.try_fulfil(order, day):
                log.fulfilled.append(order)
            else:
                log.backordered.append(order)

        log.reorders = self._replenish(day)

        report = build_report(
            self.inventory.snapshot(),
            self.shipments.delayed(day),
            self.all_orders(),
            day,
            reorder_point=self.reorder_point,
            max_level=self.max_level,
        )
        self.history.append(report)
        self.logs.append(log)
        return report

    def run(self, days: int) -> List[Report]:
        """Simulate ``days`` more days and return their reports in order."""
        if days < 0:
            raise ValueError("days must not be negative")
        return [self.step() for _ in range(days)]

    def final_summary(self) -> str:
        """Return the latest report formatted by analytics' ``format_report``."""
        report = self.history[-1] if self.history else build_report(
            self.inventory.snapshot(),
            self.shipments.delayed(self.day),
            self.all_orders(),
            self.day,
            reorder_point=self.reorder_point,
            max_level=self.max_level,
        )
        return format_report(report)

    def all_orders(self) -> List[Order]:
        """Return every order ever created, in ID order."""
        orders = [o for status in OrderStatus for o in self.orders.by_status(status)]
        return sorted(orders, key=lambda o: o.order_id)

    # ----- internals -------------------------------------------------------

    def _replenish(self, day: int) -> List[Shipment]:
        """Dispatch one replenishment per item that needs it and has none in transit.

        The quantity is trimmed so stock on hand plus everything in transit to
        the warehouse never exceeds its capacity. Stock only rises through
        arrivals, so every dispatched shipment is guaranteed to fit on arrival.
        """
        in_transit = self.shipments.in_transit()
        pending_items = {(s.warehouse_id, s.sku) for s in in_transit}
        dispatched: List[Shipment] = []
        for warehouse_id, sku, quantity in self.inventory.reorder_suggestions():
            supplier_id = self._item_supplier.get((warehouse_id, sku))
            if supplier_id is None or (warehouse_id, sku) in pending_items:
                continue
            incoming = sum(s.quantity for s in in_transit if s.warehouse_id == warehouse_id)
            incoming += sum(s.quantity for s in dispatched if s.warehouse_id == warehouse_id)
            free = (
                self._warehouses[warehouse_id]
                - self.inventory.total_in_warehouse(warehouse_id)
                - incoming
            )
            quantity = min(quantity, free)
            if quantity <= 0:
                continue
            dispatched.append(
                self.shipments.dispatch(supplier_id, warehouse_id, sku, quantity, day)
            )
        return dispatched

    def _require_warehouse(self, warehouse_id: str) -> None:
        """Raise KeyError if the warehouse has not been added."""
        if warehouse_id not in self._warehouses:
            raise KeyError(f"Unknown warehouse: '{warehouse_id}'")


def describe_day(log: DayLog, report: Report) -> str:
    """Return a one-paragraph, human-readable summary of a simulated day."""
    lines = [f"Day {log.day}:"]
    for s in log.delivered:
        late = f", {s.delay_days} day(s) late" if s.delay_days else ""
        lines.append(f"  arrived   {s.shipment_id}: {s.quantity} {s.sku} -> {s.warehouse_id}{late}")
    for s in log.blocked:
        lines.append(
            f"  BLOCKED   {s.shipment_id}: {s.quantity} {s.sku} -> {s.warehouse_id}, "
            f"no capacity; retry tomorrow"
        )
    for o in log.backorders_filled:
        lines.append(
            f"  filled    {o.order_id}: back-order from day {o.created_day} now shipped"
        )
    for o in log.fulfilled:
        lines.append(f"  fulfilled {o.order_id}: {o.quantity} {o.sku} from {o.warehouse_id}")
    for o in log.backordered:
        lines.append(f"  BACKORDER {o.order_id}: {o.quantity} {o.sku} from {o.warehouse_id}")
    for s in log.reorders:
        lines.append(
            f"  reorder   {s.shipment_id}: {s.quantity} {s.sku} from {s.supplier_id} "
            f"-> {s.warehouse_id}, due day {s.expected_day}"
        )
    o = report["orders"]
    lines.append(
        f"  flags: {len(report['delayed_shipments'])} delayed, "
        f"{len(report['stockouts'])} stockout, {len(report['low_stock'])} low, "
        f"{len(report['excess'])} excess | fill rate {o['fill_rate']}"
    )
    return "\n".join(lines)


def build_demo(seed: int = 42) -> Simulation:
    """Return a ready-to-run 10-day scenario.

    Designed so a run shows every kind of problem analytics detects:
      * delay: SUP-FLAKY ships late 70% of the time and replenishes WH-SOUTH.
      * stockout / back-order: GADGET at WH-SOUTH sells out on day 2 while its
        replenishment is still in transit, so day 3 demand is back-ordered.
      * excess: WH-NORTH starts with 650 GIZMO against a max level of 500.
    """
    sim = Simulation(seed=seed)
    sim.add_supplier("SUP-RELIABLE", "Reliable Parts Ltd", lead_time_days=2, reliability=1.0)
    sim.add_supplier("SUP-FLAKY", "Flaky Freight Co", lead_time_days=2, reliability=0.3)
    sim.add_warehouse("WH-NORTH", capacity=1200)
    sim.add_warehouse("WH-SOUTH", capacity=500)

    sim.set_policy("WH-NORTH", "WIDGET", "SUP-RELIABLE", StockPolicy(20, 150, 500))
    sim.set_policy("WH-NORTH", "GIZMO", "SUP-RELIABLE", StockPolicy(20, 100, 500))
    sim.set_policy("WH-SOUTH", "GADGET", "SUP-FLAKY", StockPolicy(20, 120, 500))
    sim.set_policy("WH-SOUTH", "WIDGET", "SUP-FLAKY", StockPolicy(20, 100, 500))

    sim.add_stock("WH-NORTH", "WIDGET", 100)
    sim.add_stock("WH-NORTH", "GIZMO", 650)
    sim.add_stock("WH-SOUTH", "GADGET", 40)
    sim.add_stock("WH-SOUTH", "WIDGET", 50)

    demand = [
        (1, "C-ACME", "WH-NORTH", "WIDGET", 30),
        (1, "C-BOLT", "WH-SOUTH", "WIDGET", 25),
        (2, "C-ACME", "WH-SOUTH", "GADGET", 40),
        (2, "C-CORE", "WH-NORTH", "GIZMO", 20),
        (3, "C-BOLT", "WH-SOUTH", "GADGET", 30),
        (3, "C-DYNA", "WH-NORTH", "WIDGET", 45),
        (4, "C-CORE", "WH-SOUTH", "WIDGET", 20),
        (5, "C-ACME", "WH-NORTH", "WIDGET", 20),
        (5, "C-DYNA", "WH-SOUTH", "GADGET", 25),
        (6, "C-BOLT", "WH-NORTH", "GIZMO", 30),
        (7, "C-CORE", "WH-SOUTH", "WIDGET", 30),
        (8, "C-ACME", "WH-SOUTH", "GADGET", 35),
        (9, "C-DYNA", "WH-NORTH", "WIDGET", 40),
        (10, "C-BOLT", "WH-SOUTH", "WIDGET", 15),
    ]
    for day, customer, warehouse, sku, qty in demand:
        sim.schedule_order(day, customer, warehouse, sku, qty)
    return sim
