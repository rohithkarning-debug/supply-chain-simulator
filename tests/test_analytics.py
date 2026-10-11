from enum import Enum
from types import SimpleNamespace

from scm_sim.analytics import find_delayed_shipments, find_excess, find_low_stock, find_stockouts, order_metrics

def ship(shipment_id, expected_day, actual_day=None, sku="A", warehouse_id="W1"):
    return SimpleNamespace(
        shipment_id=shipment_id,
        sku=sku,
        warehouse_id=warehouse_id,
        expected_day=expected_day,
        actual_day=actual_day,
    )


def test_in_transit_late_uses_current_day():
    result = find_delayed_shipments([ship("S1", expected_day=5)], current_day=8)
    assert result == [
        {"shipment_id": "S1", "sku": "A", "warehouse_id": "W1", "days_late": 3}
    ]


def test_delivered_late_uses_actual_day_not_current_day():
    result = find_delayed_shipments([ship("S1", 5, actual_day=7)], current_day=20)
    assert result[0]["days_late"] == 2


def test_on_time_and_early_are_excluded():
    shipments = [ship("S1", 5, actual_day=5), ship("S2", 5, actual_day=3)]
    assert find_delayed_shipments(shipments, current_day=10) == []


def test_in_transit_not_yet_due_is_excluded():
    assert find_delayed_shipments([ship("S1", expected_day=5)], current_day=5) == []


def test_arrival_on_day_zero_is_not_treated_as_in_transit():
    result = find_delayed_shipments([ship("S1", expected_day=-1, actual_day=0)], current_day=50)
    assert result[0]["days_late"] == 1


def test_sorted_by_days_late_descending():
    shipments = [ship("S1", 5, actual_day=6), ship("S2", 5, actual_day=9)]
    result = find_delayed_shipments(shipments, current_day=10)
    assert [d["shipment_id"] for d in result] == ["S2", "S1"]


STOCK = {
    ("W1", "A"): 0,
    ("W1", "B"): 1,
    ("W1", "C"): 20,
    ("W1", "D"): 21,
    ("W2", "A"): 500,
    ("W2", "B"): 501,
    ("W2", "C"): 0,
}


def test_stockouts_only_exact_zero_and_sorted():
    assert find_stockouts(STOCK) == [("W1", "A"), ("W2", "C")]


def test_low_stock_boundaries_zero_excluded_and_20_included():
    assert find_low_stock(STOCK) == [("W1", "B", 1), ("W1", "C", 20)]


def test_low_stock_respects_custom_reorder_point():
    assert find_low_stock(STOCK, reorder_point=21) == [
        ("W1", "B", 1),
        ("W1", "C", 20),
        ("W1", "D", 21),
    ]


def test_excess_boundaries_500_excluded_and_501_included():
    assert find_excess(STOCK) == [("W2", "B", 501, 1)]


def test_excess_surplus_with_custom_max_level():
    assert find_excess({("W1", "A"): 120}, max_level=100) == [("W1", "A", 120, 20)]


def test_empty_stock_gives_empty_results():
    assert find_stockouts({}) == []
    assert find_low_stock({}) == []
    assert find_excess({}) == []


class Status(Enum):
    PENDING = "PENDING"
    FULFILLED = "FULFILLED"
    BACKORDERED = "BACKORDERED"
    CANCELLED = "CANCELLED"


def order(order_id, status):
    return SimpleNamespace(order_id=order_id, status=status)


def test_order_metrics_counts_with_string_statuses():
    orders = [
        order(1, "PENDING"),
        order(2, "FULFILLED"),
        order(3, "FULFILLED"),
        order(4, "BACKORDERED"),
        order(5, "CANCELLED"),
    ]
    m = order_metrics(orders)
    assert m["total"] == 5
    assert m["pending"] == 1
    assert m["fulfilled"] == 2
    assert m["backordered"] == 1
    assert m["cancelled"] == 1


def test_order_metrics_accepts_enum_statuses():
    orders = [order(1, Status.FULFILLED), order(2, Status.PENDING)]
    m = order_metrics(orders)
    assert m["fulfilled"] == 1
    assert m["pending"] == 1
    assert m["fill_rate"] == 0.5


def test_enum_and_string_statuses_can_be_mixed():
    orders = [order(1, Status.FULFILLED), order(2, "FULFILLED")]
    assert order_metrics(orders)["fulfilled"] == 2


def test_fill_rate_excludes_cancelled_orders():
    orders = [
        order(1, "FULFILLED"),
        order(2, "FULFILLED"),
        order(3, "PENDING"),
        order(4, "CANCELLED"),
    ]
    assert order_metrics(orders)["fill_rate"] == 0.67


def test_fill_rate_is_zero_with_no_orders():
    m = order_metrics([])
    assert m["total"] == 0
    assert m["fill_rate"] == 0.0


def test_fill_rate_is_zero_when_all_cancelled():
    m = order_metrics([order(1, "CANCELLED"), order(2, "CANCELLED")])
    assert m["fill_rate"] == 0.0
