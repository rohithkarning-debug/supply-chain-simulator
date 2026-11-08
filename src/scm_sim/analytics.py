"""Analytics over plain data: delays, stock problems, order metrics, reports."""
from __future__ import annotations

from typing import Any, Mapping, Optional

# Anything with ``reorder_point`` and ``max_level`` attributes, e.g. inventory.StockPolicy.
# Typed as Any so analytics keeps no dependency on the inventory module.
Policies = Optional[Mapping[tuple[str, str], Any]]


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


def _threshold(policies: Policies, key: tuple[str, str], name: str, default: int) -> int:
    """Return the item's own threshold from ``policies``, or ``default`` if it has none."""
    if policies is not None and key in policies:
        return getattr(policies[key], name)
    return default


def find_low_stock(
    stock: dict[tuple[str, str], int], reorder_point: int = 20, policies: Policies = None
) -> list[tuple[str, str, int]]:
    """Return (warehouse_id, sku, qty) with 0 < qty <= reorder point, sorted.

    The reorder point is the item's own ``policies[(wh, sku)].reorder_point``
    when given, otherwise the global ``reorder_point`` (SAD 4.6 L1).
    """
    return sorted(
        (wh, sku, qty)
        for (wh, sku), qty in stock.items()
        if 0 < qty <= _threshold(policies, (wh, sku), "reorder_point", reorder_point)
    )


def find_excess(
    stock: dict[tuple[str, str], int], max_level: int = 500, policies: Policies = None
) -> list[tuple[str, str, int, int]]:
    """Return (warehouse_id, sku, qty, surplus) with qty > max level, sorted.

    The max level is the item's own ``policies[(wh, sku)].max_level`` when
    given, otherwise the global ``max_level``. surplus = qty - that max level.
    """
    result = []
    for (wh, sku), qty in stock.items():
        limit = _threshold(policies, (wh, sku), "max_level", max_level)
        if qty > limit:
            result.append((wh, sku, qty, qty - limit))
    return sorted(result)


def order_metrics(orders: list[Any]) -> dict[str, Any]:
    """Count orders by status and compute the fill rate.

    fill_rate = fulfilled / (total - cancelled), rounded to 2 dp.
    It is 0.0 when that denominator is 0 (no orders, or all cancelled).
    """
    counts = {"PENDING": 0, "FULFILLED": 0, "BACKORDERED": 0, "CANCELLED": 0}
    for o in orders:
        status = getattr(o.status, "value", o.status)
        if status in counts:
            counts[status] += 1

    total = len(orders)
    active = total - counts["CANCELLED"]
    fill_rate = round(counts["FULFILLED"] / active, 2) if active > 0 else 0.0

    return {
        "total": total,
        "pending": counts["PENDING"],
        "fulfilled": counts["FULFILLED"],
        "backordered": counts["BACKORDERED"],
        "cancelled": counts["CANCELLED"],
        "fill_rate": fill_rate,
    }


def build_report(
    stock: dict[tuple[str, str], int],
    shipments: list[Any],
    orders: list[Any],
    current_day: int,
    reorder_point: int = 20,
    max_level: int = 500,
    policies: Policies = None,
) -> dict[str, Any]:
    """Combine all analytics into a single report dict.

    ``policies`` optionally maps (warehouse_id, sku) to that item's thresholds;
    items not in it use the global ``reorder_point`` and ``max_level``.
    """
    return {
        "day": current_day,
        "delayed_shipments": find_delayed_shipments(shipments, current_day),
        "stockouts": find_stockouts(stock),
        "low_stock": find_low_stock(stock, reorder_point, policies),
        "excess": find_excess(stock, max_level, policies),
        "orders": order_metrics(orders),
    }


def format_report(report: dict[str, Any]) -> str:
    """Render a report dict as readable multi-line text.

    Each section shows a count; empty sections print "No issues".
    """
    lines = [f"=== Supply Chain Report: Day {report['day']} ==="]

    def section(title: str, items: list[Any], describe) -> None:
        lines.append("")
        lines.append(f"{title} ({len(items)})")
        if not items:
            lines.append("  No issues")
        for item in items:
            lines.append("  - " + describe(item))

    section(
        "Delayed shipments",
        report["delayed_shipments"],
        lambda d: f"{d['shipment_id']}: {d['sku']} to {d['warehouse_id']}, "
        f"{d['days_late']} day(s) late",
    )
    section("Stockouts", report["stockouts"], lambda t: f"{t[0]} / {t[1]}")
    section(
        "Low stock",
        report["low_stock"],
        lambda t: f"{t[0]} / {t[1]}: {t[2]} left",
    )
    section(
        "Excess",
        report["excess"],
        lambda t: f"{t[0]} / {t[1]}: {t[2]} (surplus {t[3]})",
    )

    o = report["orders"]
    lines.append("")
    lines.append(f"Orders ({o['total']})")
    lines.append(
        f"  pending {o['pending']}, fulfilled {o['fulfilled']}, "
        f"backordered {o['backordered']}, cancelled {o['cancelled']}"
    )
    lines.append(f"  fill rate: {o['fill_rate']}")

    return "\n".join(lines)


def summarize_run(history: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarise a simulation run over all daily reports.

    Args:
        history: List of daily report dicts (from Simulation.history).

    Returns:
        Dict containing summary metrics across the entire run:
            days: Total number of daily reports.
            days_with_delays: Number of days with at least one delayed shipment.
            days_with_stockouts: Number of days with at least one stockout.
            days_with_low_stock: Number of days with at least one low-stock SKU.
            days_with_excess: Number of days with at least one excess SKU.
            peak_delayed: Highest number of delayed shipments on any single day.
            final_fill_rate: Order fill rate from the final day's report (0.0 if empty).
    """
    if not history:
        return {
            "days": 0,
            "days_with_delays": 0,
            "days_with_stockouts": 0,
            "days_with_low_stock": 0,
            "days_with_excess": 0,
            "peak_delayed": 0,
            "final_fill_rate": 0.0,
        }

    return {
        "days": len(history),
        "days_with_delays": sum(1 for r in history if r["delayed_shipments"]),
        "days_with_stockouts": sum(1 for r in history if r["stockouts"]),
        "days_with_low_stock": sum(1 for r in history if r["low_stock"]),
        "days_with_excess": sum(1 for r in history if r["excess"]),
        "peak_delayed": max(len(r["delayed_shipments"]) for r in history),
        "final_fill_rate": history[-1]["orders"]["fill_rate"],
    }


def format_run_summary(summary: dict[str, Any]) -> str:
    """Render a run summary dict as readable multi-line text."""
    lines = [
        "=== Run Summary ===",
        f"  days: {summary['days']}",
        f"  days_with_delays: {summary['days_with_delays']}",
        f"  days_with_stockouts: {summary['days_with_stockouts']}",
        f"  days_with_low_stock: {summary['days_with_low_stock']}",
        f"  days_with_excess: {summary['days_with_excess']}",
        f"  peak_delayed: {summary['peak_delayed']}",
        f"  final_fill_rate: {summary['final_fill_rate']}",
    ]
    return "\n".join(lines)


# Aliases for backward compatibility
summarize_history = summarize_run
format_summary = format_run_summary	
