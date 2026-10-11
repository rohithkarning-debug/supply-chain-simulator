import random
import pytest

from scm_sim.inventory import Inventory
from scm_sim.shipments import Shipment, ShipmentManager, ShipmentStatus, Supplier


def test_supplier_validation():
    """Verify default values, valid bounds, and error handling for Supplier."""
    sup = Supplier(supplier_id="SUP-01", name="Acme Corp")
    assert sup.lead_time_days == 2
    assert sup.reliability == 1.0

    # Valid boundary values
    assert Supplier("SUP-02", "Min", lead_time_days=0, reliability=0.0).lead_time_days == 0
    assert Supplier("SUP-03", "Max", lead_time_days=10, reliability=1.0).reliability == 1.0

    # Invalid negative lead time
    with pytest.raises(ValueError, match="lead_time_days must not be negative"):
        Supplier("SUP-INV1", "Bad Lead", lead_time_days=-1)

    # Invalid reliability < 0.0
    with pytest.raises(ValueError, match="reliability must be between 0.0 and 1.0"):
        Supplier("SUP-INV2", "Bad Rel Low", reliability=-0.1)

    # Invalid reliability > 1.0
    with pytest.raises(ValueError, match="reliability must be between 0.0 and 1.0"):
        Supplier("SUP-INV3", "Bad Rel High", reliability=1.05)


def test_add_supplier_and_reject_duplicate_and_unknown():
    """Verify supplier registration, duplicate rejection, and unknown supplier handling."""
    inv = Inventory()
    mgr = ShipmentManager(inv)

    sup = Supplier("SUP-01", "Acme Corp")
    mgr.add_supplier(sup)

    # Duplicate supplier registration
    with pytest.raises(ValueError, match="already exists"):
        mgr.add_supplier(sup)

    # Unknown supplier dispatch
    with pytest.raises(KeyError, match="Unknown supplier"):
        mgr.dispatch("SUP-999", "WH-01", "SKU-01", quantity=10, day=1)


def test_expected_day_calculated_from_lead_time():
    """Verify expected_day is day + supplier.lead_time_days."""
    inv = Inventory()
    mgr = ShipmentManager(inv)
    mgr.add_supplier(Supplier("SUP-01", "Acme", lead_time_days=3))

    shp_on_time = mgr.dispatch("SUP-01", "WH-01", "SKU-01", quantity=50, day=2, delay=0)
    assert shp_on_time.dispatch_day == 2
    assert shp_on_time.expected_day == 5
    assert shp_on_time.arrival_day == 5

    shp_delayed = mgr.dispatch("SUP-01", "WH-01", "SKU-01", quantity=50, day=2, delay=2)
    assert shp_delayed.dispatch_day == 2
    assert shp_delayed.expected_day == 5
    assert shp_delayed.arrival_day == 7


def test_on_time_arrival_adds_stock():
    """Verify on-time arrival marks shipment as DELIVERED and adds stock to inventory."""
    inv = Inventory()
    mgr = ShipmentManager(inv)
    mgr.add_supplier(Supplier("SUP-01", "Acme", lead_time_days=2))

    shp = mgr.dispatch("SUP-01", "WH-01", "SKU-01", quantity=100, day=1, delay=0)
    assert shp.expected_day == 3
    assert shp.arrival_day == 3
    assert shp.status == ShipmentStatus.IN_TRANSIT
    assert inv.level("WH-01", "SKU-01") == 0

    # Day 2: Not arrived yet
    delivered_d2 = mgr.process_arrivals(2)
    assert delivered_d2 == []
    assert shp.status == ShipmentStatus.IN_TRANSIT
    assert inv.level("WH-01", "SKU-01") == 0

    # Day 3: Arrived on time
    delivered_d3 = mgr.process_arrivals(3)
    assert delivered_d3 == [shp]
    assert shp.status == ShipmentStatus.DELIVERED
    assert shp.actual_day == 3
    assert shp.delay_days == 0
    assert shp.days_late(3) == 0
    assert inv.level("WH-01", "SKU-01") == 100


def test_delayed_shipment_not_delivered_early():
    """Verify delayed shipments do not arrive early or modify inventory prematurely."""
    inv = Inventory()
    mgr = ShipmentManager(inv)
    mgr.add_supplier(Supplier("SUP-01", "Acme", lead_time_days=2))

    # Expected day = 3, but delayed by 2 days -> arrival_day = 5
    shp = mgr.dispatch("SUP-01", "WH-01", "SKU-01", quantity=75, day=1, delay=2)
    assert shp.expected_day == 3
    assert shp.arrival_day == 5

    # Day 3: Expected day, but delayed, so must NOT be delivered
    assert mgr.process_arrivals(3) == []
    assert shp.status == ShipmentStatus.IN_TRANSIT
    assert inv.level("WH-01", "SKU-01") == 0

    # Day 4: Still in transit
    assert mgr.process_arrivals(4) == []
    assert shp.status == ShipmentStatus.IN_TRANSIT
    assert inv.level("WH-01", "SKU-01") == 0

    # Day 5: Actually arrives
    delivered = mgr.process_arrivals(5)
    assert delivered == [shp]
    assert shp.status == ShipmentStatus.DELIVERED
    assert shp.actual_day == 5
    assert inv.level("WH-01", "SKU-01") == 75


def test_delayed_detection_both_in_transit_late_and_delivered_late():
    """Verify delayed() identifies both in-transit late and delivered late shipments."""
    inv = Inventory()
    mgr = ShipmentManager(inv)
    mgr.add_supplier(Supplier("SUP-01", "Acme", lead_time_days=2))

    # Dispatched day 0, expected day 2, arrival day 4 (2 days late)
    shp = mgr.dispatch("SUP-01", "WH-01", "SKU-01", quantity=40, day=0, delay=2)

    # Day 1: In transit, not past expected day -> not late
    assert shp.days_late(1) == 0
    assert mgr.delayed(1) == []

    # Day 2: Expected day, still in transit -> not late
    assert shp.days_late(2) == 0
    assert mgr.delayed(2) == []

    # Day 3: In transit, past expected day (3 > 2) -> in-transit late!
    assert shp.status == ShipmentStatus.IN_TRANSIT
    assert shp.delay_days == 0  # not delivered yet
    assert shp.days_late(3) == 1
    assert mgr.delayed(3) == [shp]

    # Day 4: Still late before arrival processing
    assert shp.days_late(4) == 2

    # Process arrival on day 4 -> now DELIVERED late!
    mgr.process_arrivals(4)
    assert shp.status == ShipmentStatus.DELIVERED
    assert shp.actual_day == 4
    assert shp.delay_days == 2
    assert shp.days_late(4) == 2
    assert mgr.delayed(4) == [shp]

    # Day 5: Remains tracked as delivered late
    assert shp.days_late(5) == 2
    assert mgr.delayed(5) == [shp]


def test_reliability_one_means_never_delayed():
    """Verify supplier with reliability=1.0 is never delayed when delay is sampled."""
    inv = Inventory()
    # Test across multiple seeded RNG instances to guarantee determinism
    for seed in [1, 42, 99, 1234]:
        mgr = ShipmentManager(inv, rng=random.Random(seed))
        mgr.add_supplier(Supplier("SUP-PERF", "Reliable Supplier", lead_time_days=3, reliability=1.0))

        for d in range(10):
            shp = mgr.dispatch("SUP-PERF", "WH-01", f"SKU-{d}", quantity=10, day=d)
            assert shp.expected_day == d + 3
            assert shp.arrival_day == shp.expected_day
            assert shp.days_late(shp.expected_day) == 0


def test_shipment_id_sequence_and_in_transit_filtering():
    """Verify sequential ID generation and in_transit list filtering."""
    inv = Inventory()
    mgr = ShipmentManager(inv)
    mgr.add_supplier(Supplier("SUP-01", "Acme", lead_time_days=2))

    s1 = mgr.dispatch("SUP-01", "WH-01", "SKU-01", quantity=10, day=0, delay=0)
    s2 = mgr.dispatch("SUP-01", "WH-01", "SKU-02", quantity=20, day=0, delay=2)
    s3 = mgr.dispatch("SUP-01", "WH-02", "SKU-03", quantity=30, day=1, delay=0)

    assert s1.shipment_id == "SHP-0001"
    assert s2.shipment_id == "SHP-0002"
    assert s3.shipment_id == "SHP-0003"

    assert mgr.in_transit() == [s1, s2, s3]

    # Arrive s1 at day 2
    mgr.process_arrivals(2)
    assert s1.status == ShipmentStatus.DELIVERED
    assert mgr.in_transit() == [s2, s3]


def test_reject_non_positive_quantity():
    """Verify dispatch and Shipment validate quantity > 0."""
    inv = Inventory()
    mgr = ShipmentManager(inv)
    mgr.add_supplier(Supplier("SUP-01", "Acme", lead_time_days=2))

    with pytest.raises(ValueError, match="quantity must be greater than 0"):
        mgr.dispatch("SUP-01", "WH-01", "SKU-01", quantity=0, day=1)

    with pytest.raises(ValueError, match="quantity must be greater than 0"):
        mgr.dispatch("SUP-01", "WH-01", "SKU-01", quantity=-10, day=1)

    with pytest.raises(ValueError, match="quantity must be greater than 0"):
        Shipment(
            shipment_id="SHP-X",
            supplier_id="SUP-01",
            warehouse_id="WH-01",
            sku="SKU-01",
            quantity=0,
            dispatch_day=1,
            expected_day=3,
            arrival_day=3,
        )


def test_probabilistic_delay_with_zero_reliability():
    """Verify supplier with reliability 0.0 always experiences delay in [1, 3]."""
    inv = Inventory()
    rng = random.Random(42)
    mgr = ShipmentManager(inv, rng=rng)
    mgr.add_supplier(Supplier("SUP-SLOW", "Slow Supplier", lead_time_days=2, reliability=0.0))

    for day in range(5):
        shp = mgr.dispatch("SUP-SLOW", "WH-01", "SKU-01", quantity=10, day=day)
        delay = shp.arrival_day - shp.expected_day
        assert 1 <= delay <= 3
