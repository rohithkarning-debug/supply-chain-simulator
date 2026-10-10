"""Shipments module for Supply Chain Simulator.

Handles supplier definitions, shipment tracking, dispatching with probabilistic
lead-time delays, arrival processing into inventory, and delay detection.
"""

from dataclasses import dataclass
from enum import Enum
import random
from typing import Dict, List, Optional

from scm_sim.inventory import Inventory


class ShipmentStatus(str, Enum):
    """Lifecycle statuses for a shipment."""

    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"


@dataclass
class Supplier:
    """Represents an external goods supplier.

    Attributes:
        supplier_id: Unique supplier identifier.
        name: Name of the supplier.
        lead_time_days: Base delivery duration in days (default: 2).
        reliability: Probability of arriving on time in [0.0, 1.0] (default: 1.0).
    """

    supplier_id: str
    name: str
    lead_time_days: int = 2
    reliability: float = 1.0

    def __post_init__(self) -> None:
        """Validate lead_time_days and reliability bounds."""
        if self.lead_time_days < 0:
            raise ValueError("lead_time_days must not be negative")
        if not (0.0 <= self.reliability <= 1.0):
            raise ValueError("reliability must be between 0.0 and 1.0")


@dataclass
class Shipment:
    """Represents a replenishment shipment between a supplier and a warehouse.

    Attributes:
        shipment_id: Unique shipment identifier (e.g., 'SHP-0001').
        supplier_id: ID of the dispatching supplier.
        warehouse_id: Destination warehouse identifier.
        sku: Stock keeping unit code.
        quantity: Number of units being shipped.
        dispatch_day: Simulation day when shipment was dispatched.
        expected_day: Simulation day when shipment is scheduled to arrive.
        arrival_day: Actual simulation day when shipment will arrive (including delays).
        actual_day: Simulation day when shipment was delivered and stocked.
        status: Current shipment status.
    """

    shipment_id: str
    supplier_id: str
    warehouse_id: str
    sku: str
    quantity: int
    dispatch_day: int
    expected_day: int
    arrival_day: int
    actual_day: Optional[int] = None
    status: ShipmentStatus = ShipmentStatus.IN_TRANSIT

    def __post_init__(self) -> None:
        """Validate shipment quantity."""
        if self.quantity <= 0:
            raise ValueError("quantity must be greater than 0")

    @property
    def delay_days(self) -> int:
        """Return days delayed if delivered, otherwise 0."""
        if self.status != ShipmentStatus.DELIVERED or self.actual_day is None:
            return 0
        return max(0, self.actual_day - self.expected_day)

    def days_late(self, current_day: int) -> int:
        """Calculate days late relative to expected arrival day.

        If delivered, returns delay_days.
        If still in transit, returns max(0, current_day - expected_day).
        """
        if self.status == ShipmentStatus.DELIVERED:
            return self.delay_days
        return max(0, current_day - self.expected_day)


class ShipmentManager:
    """Manages suppliers, dispatching shipments, and receiving arrivals into inventory."""

    def __init__(self, inventory: Inventory, rng: Optional[random.Random] = None) -> None:
        """Initialize ShipmentManager with an inventory instance and deterministic RNG."""
        self.inventory: Inventory = inventory
        self.rng: random.Random = rng if rng is not None else random.Random(42)
        self._suppliers: Dict[str, Supplier] = {}
        self._shipments: Dict[str, Shipment] = {}
        self._next_id: int = 1

    def add_supplier(self, supplier: Supplier) -> None:
        """Register a new supplier.

        Raises:
            ValueError: If a supplier with the same ID is already registered.
        """
        if supplier.supplier_id in self._suppliers:
            raise ValueError(f"Supplier with ID '{supplier.supplier_id}' already exists")
        self._suppliers[supplier.supplier_id] = supplier

    def dispatch(
        self,
        supplier_id: str,
        warehouse_id: str,
        sku: str,
        quantity: int,
        day: int,
        delay: Optional[int] = None,
    ) -> Shipment:
        """Dispatch a shipment from a supplier to a warehouse.

        Args:
            supplier_id: ID of registered supplier.
            warehouse_id: ID of destination warehouse.
            sku: Product SKU.
            quantity: Number of units to ship (must be > 0).
            day: Current simulation day of dispatch.
            delay: Optional explicit delay days. If None, delay is sampled probabilistically.

        Returns:
            The created Shipment instance.

        Raises:
            KeyError: If supplier_id is not registered.
            ValueError: If quantity <= 0.
        """
        if supplier_id not in self._suppliers:
            raise KeyError(f"Unknown supplier: '{supplier_id}'")
        if quantity <= 0:
            raise ValueError("quantity must be greater than 0")

        supplier = self._suppliers[supplier_id]
        expected_day = day + supplier.lead_time_days

        if delay is None:
            delay = self.rng.randint(1, 3) if self.rng.random() > supplier.reliability else 0

        arrival_day = expected_day + delay
        shipment_id = f"SHP-{self._next_id:04d}"
        self._next_id += 1

        shipment = Shipment(
            shipment_id=shipment_id,
            supplier_id=supplier_id,
            warehouse_id=warehouse_id,
            sku=sku,
            quantity=quantity,
            dispatch_day=day,
            expected_day=expected_day,
            arrival_day=arrival_day,
            actual_day=None,
            status=ShipmentStatus.IN_TRANSIT,
        )
        self._shipments[shipment_id] = shipment
        return shipment

    def process_arrivals(self, day: int) -> List[Shipment]:
        """Deliver all in-transit shipments whose arrival_day has arrived.

        For each arriving shipment, adds quantity to inventory, updates status
        to DELIVERED, and records actual_day.

        Returns:
            List of shipments delivered today.
        """
        delivered_today: List[Shipment] = []
        for shipment in self._shipments.values():
            if shipment.status == ShipmentStatus.IN_TRANSIT and shipment.arrival_day <= day:
                self.inventory.add(shipment.warehouse_id, shipment.sku, shipment.quantity)
                shipment.status = ShipmentStatus.DELIVERED
                shipment.actual_day = day
                delivered_today.append(shipment)
        return delivered_today

    def in_transit(self) -> List[Shipment]:
        """Return list of all shipments currently IN_TRANSIT."""
        return [s for s in self._shipments.values() if s.status == ShipmentStatus.IN_TRANSIT]

    def delayed(self, current_day: int) -> List[Shipment]:
        """Return list of all shipments that are currently late (days_late > 0)."""
        return [s for s in self._shipments.values() if s.days_late(current_day) > 0]
