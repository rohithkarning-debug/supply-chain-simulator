"""Analytics over plain data: delays, stock problems, order metrics, reports."""
from __future__ import annotations

from typing import Any


def find_delayed_shipments(shipments: list[Any], current_day: int) -> list[dict[str, Any]]:
    """Return shipments that are late, worst first.

    days_late = (actual_day if arrived else current_day) - expected_day.
    Only shipments with days_late > 0 are included.
    """
    delayed = []
    for s in shipments:
        end_day = s.actual_day if s.actual_day is not None else current_day
        days_late = end_day - s.expected_day
        if days_late > 0:
            delayed.append({
                "shipment_id": s.shipment_id,
                "sku": s.sku,
                "warehouse_id": s.warehouse_id,
                "days_late": days_late,
            })
    delayed.sort(key=lambda d: (-d["days_late"], d["shipment_id"]))
    return delayed

def find_stockouts(stock: dict[tuple[str, str], int]) -> list[tuple[str, str]]:
    """Return (warehouse_id, sku) pairs with exactly zero stock, sorted."""
    return sorted(key for key, qty in stock.items() if qty == 0)


def find_low_stock(
    stock: dict[tuple[str, str], int], reorder_point: int = 20
) -> list[tuple[str, str, int]]:
    """Return (warehouse_id, sku, qty) with 0 < qty <= reorder_point, sorted."""
    return sorted(
        (wh, sku, qty)
        for (wh, sku), qty in stock.items()
        if 0 < qty <= reorder_point
    )


def find_excess(
    stock: dict[tuple[str, str], int], max_level: int = 500
) -> list[tuple[str, str, int, int]]:
    """Return (warehouse_id, sku, qty, surplus) with qty > max_level, sorted.

    surplus = qty - max_level.
    """
    return sorted(
        (wh, sku, qty, qty - max_level)
        for (wh, sku), qty in stock.items()
        if qty > max_level
    )
