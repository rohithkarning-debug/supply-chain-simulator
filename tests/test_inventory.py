import pytest
from scm_sim.inventory import Inventory, InsufficientStockError

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
