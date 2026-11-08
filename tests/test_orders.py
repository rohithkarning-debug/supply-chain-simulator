import pytest
from scm_sim.inventory import Inventory
from scm_sim.orders import OrderManager, OrderStatus, Order

def test_create_order_id_sequence():
    inv = Inventory()
    mgr = OrderManager(inv)
    o1 = mgr.create("C1", "W1", "SKU1", 10, day=1)
    o2 = mgr.create("C1", "W1", "SKU1", 5, day=1)
    
    assert o1.order_id == "ORD-0001"
    assert o2.order_id == "ORD-0002"

def test_invalid_quantity():
    inv = Inventory()
    mgr = OrderManager(inv)
    with pytest.raises(ValueError, match="quantity must be greater than 0"):
        mgr.create("C1", "W1", "SKU1", 0, day=1)

def test_fulfil_enough_stock():
    inv = Inventory()
    inv.add("W1", "SKU1", 20)
    mgr = OrderManager(inv)
    
    o1 = mgr.create("C1", "W1", "SKU1", 10, day=1)
    fulfilled = mgr.try_fulfil(o1, 1)
    
    assert fulfilled is True
    assert o1.status == OrderStatus.FULFILLED
    assert o1.fulfilled_day == 1
    assert inv.level("W1", "SKU1") == 10

def test_backorder_when_short():
    inv = Inventory()
    inv.add("W1", "SKU1", 5)
    mgr = OrderManager(inv)
    
    o1 = mgr.create("C1", "W1", "SKU1", 10, day=1)
    fulfilled = mgr.try_fulfil(o1, 1)
    
    assert fulfilled is False
    assert o1.status == OrderStatus.BACKORDERED
    assert inv.level("W1", "SKU1") == 5

def test_backorder_later_fulfilled_by_process_open():
    inv = Inventory()
    inv.add("W1", "SKU1", 5)
    mgr = OrderManager(inv)
    
    o1 = mgr.create("C1", "W1", "SKU1", 10, day=1)
    mgr.try_fulfil(o1, day=1)
    assert o1.status == OrderStatus.BACKORDERED
    
    # Restock inventory
    inv.add("W1", "SKU1", 10)
    
    # Process open orders
    newly_fulfilled = mgr.process_open(day=2)
    
    assert len(newly_fulfilled) == 1
    assert newly_fulfilled[0] == o1
    assert o1.status == OrderStatus.FULFILLED
    assert o1.fulfilled_day == 2
    assert inv.level("W1", "SKU1") == 5

def test_oldest_first_priority():
    inv = Inventory()
    mgr = OrderManager(inv)
    
    # Create two orders that would need 15 units total
    o1 = mgr.create("C1", "W1", "SKU1", 10, day=1)
    o2 = mgr.create("C2", "W1", "SKU1", 10, day=2)
    
    mgr.try_fulfil(o1, 1)
    mgr.try_fulfil(o2, 2)
    
    assert o1.status == OrderStatus.BACKORDERED
    assert o2.status == OrderStatus.BACKORDERED
    
    # Restock only enough for one order
    inv.add("W1", "SKU1", 15)
    
    newly_fulfilled = mgr.process_open(day=3)
    
    # Oldest (o1) should be fulfilled
    assert len(newly_fulfilled) == 1
    assert newly_fulfilled[0] == o1
    assert o1.status == OrderStatus.FULFILLED
    assert o2.status == OrderStatus.BACKORDERED
    assert inv.level("W1", "SKU1") == 5

def test_cancel_rules():
    inv = Inventory()
    inv.add("W1", "SKU1", 20)
    mgr = OrderManager(inv)
    
    # Cancel an unfulfilled order
    o1 = mgr.create("C1", "W1", "SKU1", 10, day=1)
    canceled_order = mgr.cancel(o1.order_id)
    assert canceled_order == o1
    assert o1.status == OrderStatus.CANCELLED
    
    # Attempt to cancel a fulfilled order
    o2 = mgr.create("C2", "W1", "SKU1", 10, day=1)
    mgr.try_fulfil(o2, 1)
    assert o2.status == OrderStatus.FULFILLED
    
    with pytest.raises(ValueError, match="Cannot cancel an already fulfilled order"):
        mgr.cancel(o2.order_id)


def test_rejected_order_does_not_consume_an_id():
    """SAD 4.6 L3: a rejected create() must not leave a gap in the ORD-NNNN sequence."""
    inv = Inventory()
    om = OrderManager(inv)
    with pytest.raises(ValueError, match="quantity must be greater than 0"):
        om.create("C1", "WH1", "SKU1", 0, day=1)
    with pytest.raises(ValueError):
        om.create("C1", "WH1", "SKU1", -5, day=1)
    first = om.create("C1", "WH1", "SKU1", 10, day=1)
    second = om.create("C2", "WH1", "SKU1", 5, day=1)
    assert first.order_id == "ORD-0001"
    assert second.order_id == "ORD-0002"
    assert [o.order_id for o in om.by_status(OrderStatus.PENDING)] == ["ORD-0001", "ORD-0002"]


def test_order_dataclass_rejects_non_positive_quantity_directly():
    """Order validates itself even when built without OrderManager.create."""
    with pytest.raises(ValueError, match="quantity must be greater than 0"):
        Order("ORD-9999", "C1", "WH1", "SKU1", 0, created_day=1)


def test_get_unknown_order_raises_key_error():
    om = OrderManager(Inventory())
    with pytest.raises(KeyError, match="ORD-0042"):
        om.get("ORD-0042")


def test_fulfilled_or_cancelled_orders_are_never_reprocessed():
    """SCM-SR-003: try_fulfil leaves FULFILLED and CANCELLED orders and the stock untouched."""
    inv = Inventory()
    inv.add("WH1", "SKU1", 100)
    om = OrderManager(inv)
    done = om.create("C1", "WH1", "SKU1", 10, day=1)
    assert om.try_fulfil(done, day=1) is True
    cancelled = om.create("C2", "WH1", "SKU1", 10, day=1)
    om.cancel(cancelled.order_id)

    assert om.try_fulfil(done, day=2) is False
    assert om.try_fulfil(cancelled, day=2) is False
    assert done.status == OrderStatus.FULFILLED
    assert cancelled.status == OrderStatus.CANCELLED
    assert inv.level("WH1", "SKU1") == 90

