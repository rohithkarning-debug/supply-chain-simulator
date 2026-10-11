from types import SimpleNamespace

from scm_sim.analytics import find_delayed_shipments


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
