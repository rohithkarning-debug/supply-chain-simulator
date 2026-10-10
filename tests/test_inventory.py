import pytest
from scm_sim.inventory import (
    CapacityExceededError,
    InsufficientStockError,
    Inventory,
    StockPolicy,
)

def test_add_and_level():
    inv = Inventory()
    assert inv.add("WH1", "SKU1", 50) == 50

def test_remove_reduces_stock():
    inv = Inventory()
    inv.add("WH1", "SKU1", 50)
    assert inv.remove("WH1", "SKU1", 20) == 30

def test_remove_too_much_raises():
    inv = Inventory()
    inv.add("WH1", "SKU1", 5)
    with pytest.raises(InsufficientStockError):
        inv.remove("WH1", "SKU1", 10)

def test_stockout_detected():
    inv = Inventory()
    assert inv.is_stockout("WH1", "SKU1")


def test_stock_policy_defaults():
    policy = StockPolicy()
    assert (policy.reorder_point, policy.reorder_quantity, policy.max_level) == (20, 100, 500)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"reorder_point": -1},
        {"reorder_quantity": -1},
        {"max_level": -1},
        {"reorder_point": 50, "max_level": 49},
    ],
)
def test_stock_policy_rejects_invalid_values(kwargs):
    with pytest.raises(ValueError):
        StockPolicy(**kwargs)


def test_stock_policy_allows_max_level_equal_to_reorder_point():
    assert StockPolicy(reorder_point=50, max_level=50).max_level == 50


def test_register_warehouse_rejects_non_positive_capacity():
    inv = Inventory()
    with pytest.raises(ValueError):
        inv.register_warehouse("WH1", 0)
    with pytest.raises(ValueError):
        inv.register_warehouse("WH1", -5)


def test_total_in_warehouse_sums_all_skus():
    inv = Inventory()
    inv.add("WH1", "SKU1", 30)
    inv.add("WH1", "SKU2", 20)
    inv.add("WH2", "SKU1", 99)
    assert inv.total_in_warehouse("WH1") == 50
    assert inv.total_in_warehouse("WH3") == 0


def test_add_up_to_exact_capacity_is_allowed():
    inv = Inventory()
    inv.register_warehouse("WH1", 100)
    inv.add("WH1", "SKU1", 60)
    assert inv.add("WH1", "SKU2", 40) == 40
    assert inv.total_in_warehouse("WH1") == 100


def test_add_beyond_capacity_raises_and_leaves_stock_unchanged():
    inv = Inventory()
    inv.register_warehouse("WH1", 100)
    inv.add("WH1", "SKU1", 60)
    with pytest.raises(CapacityExceededError):
        inv.add("WH1", "SKU2", 41)
    assert inv.level("WH1", "SKU1") == 60
    assert inv.level("WH1", "SKU2") == 0
    assert inv.total_in_warehouse("WH1") == 60


def test_unregistered_warehouse_has_unlimited_capacity():
    inv = Inventory()
    inv.register_warehouse("WH1", 10)
    assert inv.add("WH2", "SKU1", 1_000_000) == 1_000_000


def test_get_policy_returns_default_when_unset():
    inv = Inventory()
    assert inv.get_policy("WH1", "SKU1") == StockPolicy()


def test_set_policy_is_per_warehouse_and_sku():
    inv = Inventory()
    custom = StockPolicy(reorder_point=5, reorder_quantity=10, max_level=50)
    inv.set_policy("WH1", "SKU1", custom)
    assert inv.get_policy("WH1", "SKU1") == custom
    assert inv.get_policy("WH1", "SKU2") == StockPolicy()
    assert inv.get_policy("WH2", "SKU1") == StockPolicy()


def test_needs_reorder_at_boundary():
    inv = Inventory()
    inv.set_policy("WH1", "SKU1", StockPolicy(reorder_point=20))
    inv.add("WH1", "SKU1", 21)
    assert not inv.needs_reorder("WH1", "SKU1")
    inv.remove("WH1", "SKU1", 1)  # exactly at reorder point
    assert inv.needs_reorder("WH1", "SKU1")


def test_is_excess_only_above_max_level():
    inv = Inventory()
    inv.set_policy("WH1", "SKU1", StockPolicy(reorder_point=0, max_level=100))
    inv.add("WH1", "SKU1", 100)
    assert not inv.is_excess("WH1", "SKU1")
    inv.add("WH1", "SKU1", 1)
    assert inv.is_excess("WH1", "SKU1")


def test_reorder_suggestions_sorted_and_only_tracked_items():
    inv = Inventory()
    inv.add("WH2", "SKU1", 5)  # below default reorder point -> suggested
    inv.add("WH1", "SKU9", 300)  # healthy -> not suggested
    inv.add("WH1", "SKU2", 10)
    inv.remove("WH1", "SKU2", 10)  # sold out, still tracked -> suggested
    inv.set_policy("WH1", "SKU1", StockPolicy(reorder_quantity=40))  # policy only, no stock
    assert inv.reorder_suggestions() == [
        ("WH1", "SKU1", 40),
        ("WH1", "SKU2", 100),
        ("WH2", "SKU1", 100),
    ]


def test_reorder_suggestions_empty_for_new_inventory():
    assert Inventory().reorder_suggestions() == []


def test_snapshot_returns_independent_copy():
    inv = Inventory()
    inv.add("WH1", "SKU1", 10)
    inv.add("WH2", "SKU2", 5)
    snap = inv.snapshot()
    assert snap == {("WH1", "SKU1"): 10, ("WH2", "SKU2"): 5}
    snap[("WH1", "SKU1")] = 999
    snap[("WH3", "SKU3")] = 1
    assert inv.level("WH1", "SKU1") == 10
    assert inv.level("WH3", "SKU3") == 0
    assert inv.snapshot() == {("WH1", "SKU1"): 10, ("WH2", "SKU2"): 5}


def test_existing_behaviour_unchanged_with_capacity_registered():
    inv = Inventory()
    inv.register_warehouse("WH1", 100)
    with pytest.raises(ValueError):
        inv.add("WH1", "SKU1", 0)
    assert inv.add("WH1", "SKU1", 50) == 50
    assert inv.remove("WH1", "SKU1", 50) == 0
    assert inv.is_stockout("WH1", "SKU1")
    with pytest.raises(InsufficientStockError):
        inv.remove("WH1", "SKU1", 1)
    # removing stock frees up capacity again
    assert inv.add("WH1", "SKU2", 100) == 100
