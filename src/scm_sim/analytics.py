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
