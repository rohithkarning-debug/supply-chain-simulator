from dataclasses import dataclass
from typing import Dict, List, Tuple


class InsufficientStockError(Exception):
    pass


class CapacityExceededError(Exception):
    """Raised when adding stock would exceed a warehouse's registered capacity."""


@dataclass(frozen=True)
class StockPolicy:
    """Replenishment thresholds for a single (warehouse, sku) pair.

    Attributes:
        reorder_point: Reorder when stock falls to this level or below.
        reorder_quantity: How many units to order when reordering.
        max_level: Stock above this level is considered excess.
    """

    reorder_point: int = 20
    reorder_quantity: int = 100
    max_level: int = 500

    def __post_init__(self) -> None:
        """Validate that the thresholds are non-negative and consistent."""
        for name in ("reorder_point", "reorder_quantity", "max_level"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must not be negative")
        if self.max_level < self.reorder_point:
            raise ValueError("max_level must be >= reorder_point")


class Inventory:
    def __init__(self):
        self._stock = {}
        self._capacity: Dict[str, int] = {}
        self._policies: Dict[Tuple[str, str], StockPolicy] = {}

    def level(self, warehouse, sku):
        return self._stock.get((warehouse, sku), 0)

    def add(self, warehouse, sku, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        capacity = self._capacity.get(warehouse)
        if capacity is not None and self.total_in_warehouse(warehouse) + qty > capacity:
            raise CapacityExceededError(
                f"adding {qty} {sku} would exceed capacity {capacity} at {warehouse}"
            )
        self._stock[(warehouse, sku)] = self.level(warehouse, sku) + qty
        return self.level(warehouse, sku)

    def remove(self, warehouse, sku, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        if qty > self.level(warehouse, sku):
            raise InsufficientStockError(f"not enough {sku} at {warehouse}")
        self._stock[(warehouse, sku)] -= qty
        return self.level(warehouse, sku)

    def is_stockout(self, warehouse, sku):
        return self.level(warehouse, sku) == 0

    def register_warehouse(self, warehouse: str, capacity: int) -> None:
        """Set the maximum total units (across all SKUs) a warehouse can hold.

        Warehouses that are never registered have unlimited capacity.

        Raises:
            ValueError: If capacity is not positive.
        """
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity[warehouse] = capacity

    def total_in_warehouse(self, warehouse: str) -> int:
        """Return the total units held in a warehouse, summed over all SKUs."""
        return sum(qty for (wh, _), qty in self._stock.items() if wh == warehouse)

    def set_policy(self, warehouse: str, sku: str, policy: StockPolicy) -> None:
        """Assign a stock policy to a (warehouse, sku) pair, replacing any existing one."""
        self._policies[(warehouse, sku)] = policy

    def get_policy(self, warehouse: str, sku: str) -> StockPolicy:
        """Return the policy for a (warehouse, sku) pair, or the default StockPolicy if none is set."""
        return self._policies.get((warehouse, sku), StockPolicy())

    def needs_reorder(self, warehouse: str, sku: str) -> bool:
        """Return True if the stock level is at or below the item's reorder point."""
        return self.level(warehouse, sku) <= self.get_policy(warehouse, sku).reorder_point

    def is_excess(self, warehouse: str, sku: str) -> bool:
        """Return True if the stock level is strictly above the item's max level."""
        return self.level(warehouse, sku) > self.get_policy(warehouse, sku).max_level

    def reorder_suggestions(self) -> List[Tuple[str, str, int]]:
        """Return (warehouse, sku, reorder_quantity) for every tracked item that needs reordering.

        An item is tracked if it has ever been stocked or has a policy set.
        The result is sorted by warehouse, then sku.
        """
        tracked = set(self._stock) | set(self._policies)
        return [
            (warehouse, sku, self.get_policy(warehouse, sku).reorder_quantity)
            for warehouse, sku in sorted(tracked)
            if self.needs_reorder(warehouse, sku)
        ]

    def snapshot(self) -> Dict[Tuple[str, str], int]:
        """Return a copy of all stock levels as {(warehouse, sku): qty}.

        Modifying the returned dict does not affect the inventory.
        """
        return dict(self._stock)
