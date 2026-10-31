import os
import subprocess
import sys
from pathlib import Path

import pytest

from scm_sim.__main__ import main
from scm_sim.inventory import StockPolicy
from scm_sim.orders import OrderStatus
from scm_sim.shipments import ShipmentStatus
from scm_sim.simulator import Simulation, build_demo

SRC = Path(__file__).resolve().parents[1] / "src"


def make_sim(stock: int = 50, reorder_point: int = 20, reorder_quantity: int = 100) -> Simulation:
    """One reliable supplier (lead time 2), one warehouse, one SKU."""
    sim = Simulation(seed=1)
    sim.add_supplier("SUP", "Reliable", lead_time_days=2, reliability=1.0)
    sim.add_warehouse("WH", capacity=1000)
    sim.set_policy("WH", "SKU", "SUP", StockPolicy(reorder_point, reorder_quantity, 500))
    sim.add_stock("WH", "SKU", stock)
    return sim


def test_step_advances_day_counter():
    sim = make_sim()
    assert sim.day == 0
    report = sim.step()
    assert sim.day == 1 and report["day"] == 1
    sim.run(3)
    assert sim.day == 4
    assert [r["day"] for r in sim.history] == [1, 2, 3, 4]


def test_shipment_arrives_after_lead_time_and_increases_stock():
    sim = make_sim(stock=100)
    sim.step()  # day 1
    shipment = sim.shipments.dispatch("SUP", "WH", "SKU", 40, day=sim.day)
    assert shipment.expected_day == 3
    sim.step()  # day 2: not yet
    assert sim.inventory.level("WH", "SKU") == 100
    sim.step()  # day 3: arrives
    assert shipment.status == ShipmentStatus.DELIVERED
    assert shipment.actual_day == 3
    assert sim.inventory.level("WH", "SKU") == 140


def test_large_order_is_backordered_then_fulfilled_after_replenishment():
    sim = make_sim(stock=30, reorder_quantity=100)
    sim.schedule_order(1, "C1", "WH", "SKU", 60)
    sim.step()  # day 1: 30 < 60 -> back-order; 30 <= 20? no, so no reorder yet
    order = sim.orders.get("ORD-0001")
    assert order.status == OrderStatus.BACKORDERED
    assert sim.shipments.in_transit() == []

    sim.schedule_order(2, "C2", "WH", "SKU", 15)
    sim.step()  # day 2: 15 fulfilled, stock 15 -> reorder dispatched, due day 4
    assert len(sim.shipments.in_transit()) == 1
    sim.step()  # day 3
    assert order.status == OrderStatus.BACKORDERED
    sim.step()  # day 4: 100 arrive, back-order retried
    assert order.status == OrderStatus.FULFILLED
    assert order.fulfilled_day == 4
    assert sim.inventory.level("WH", "SKU") == 15 + 100 - 60


def test_low_stock_triggers_exactly_one_reorder_while_in_transit():
    sim = make_sim(stock=10)  # already below reorder point
    sim.run(1)
    assert len(sim.shipments.in_transit()) == 1
    assert len(sim.logs[0].reorders) == 1
    sim.run(1)  # day 2: still low, but the shipment is in transit
    assert len(sim.shipments.in_transit()) == 1
    assert sim.logs[1].reorders == []
    sim.run(1)  # day 3: it arrives (10 + 100 = 110), no new reorder needed
    assert sim.shipments.in_transit() == []
    assert sim.inventory.level("WH", "SKU") == 110
    assert sum(len(log.reorders) for log in sim.logs) == 1


def test_reorder_is_trimmed_to_fit_warehouse_capacity():
    sim = Simulation()
    sim.add_supplier("SUP", "Reliable", lead_time_days=1)
    sim.add_warehouse("WH", capacity=50)
    sim.set_policy("WH", "SKU", "SUP", StockPolicy(20, 100, 50))
    sim.add_stock("WH", "SKU", 10)
    sim.run(3)  # must not raise CapacityExceededError on arrival
    assert sim.inventory.level("WH", "SKU") == 50


def test_same_seed_gives_identical_reports():
    assert build_demo(seed=7).run(10) == build_demo(seed=7).run(10)


def test_demo_detects_delay_stockout_backorder_and_excess():
    sim = build_demo(seed=42)
    reports = sim.run(10)
    assert any(r["delayed_shipments"] for r in reports)
    assert any(r["stockouts"] for r in reports)
    assert any(r["orders"]["backordered"] for r in reports)
    assert any(r["excess"] for r in reports)
    assert "=== Supply Chain Report: Day 10 ===" in sim.final_summary()


def test_schedule_order_validates_input():
    sim = make_sim()
    with pytest.raises(KeyError):
        sim.schedule_order(1, "C", "NOWHERE", "SKU", 5)
    with pytest.raises(ValueError):
        sim.schedule_order(1, "C", "WH", "SKU", 0)
    sim.step()
    with pytest.raises(ValueError):
        sim.schedule_order(1, "C", "WH", "SKU", 5)  # day 1 already simulated


def test_cli_main_runs(capsys):
    assert main(["--days", "3", "--seed", "42"]) == 0
    out = capsys.readouterr().out
    assert "Day 1:" in out and "Day 3:" in out
    assert "=== Supply Chain Report: Day 3 ===" in out


def test_cli_runs_as_module():
    env = {**os.environ, "PYTHONPATH": str(SRC)}
    result = subprocess.run(
        [sys.executable, "-m", "scm_sim", "--days", "10", "--seed", "42"],
        capture_output=True, text=True, env=env, timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert "=== Supply Chain Report: Day 10 ===" in result.stdout


def test_older_backorder_is_served_before_new_order_on_same_day():
    """Issue #27 / SAD 4.6 L4: back-orders are retried before today's new orders.

    Day 1: C1 wants 60 but only 30 are in stock -> back-ordered.
    Day 2: a 50-unit shipment arrives (stock 80) and C2 orders 40 the same day.
    Oldest-first: C1's 60 is filled first (stock 20), so C2's 40 is back-ordered.
    The old order (new orders first) would have filled C2 and kept C1 waiting.
    """
    sim = Simulation(seed=1)
    sim.add_supplier("SUP", "Reliable", lead_time_days=1, reliability=1.0)
    sim.add_warehouse("WH", capacity=1000)
    # reorder point 0 so the simulation never dispatches its own replenishment
    sim.set_policy("WH", "SKU", "SUP", StockPolicy(0, 100, 500))
    sim.add_stock("WH", "SKU", 30)
    sim.schedule_order(1, "C1", "WH", "SKU", 60)
    sim.step()
    first = sim.orders.get("ORD-0001")
    assert first.status == OrderStatus.BACKORDERED

    sim.shipments.dispatch("SUP", "WH", "SKU", 50, day=1)  # arrives day 2
    sim.schedule_order(2, "C2", "WH", "SKU", 40)
    sim.step()
    second = sim.orders.get("ORD-0002")

    assert first.status == OrderStatus.FULFILLED and first.fulfilled_day == 2
    assert second.status == OrderStatus.BACKORDERED
    assert sim.inventory.level("WH", "SKU") == 20
    assert [o.order_id for o in sim.logs[1].backorders_filled] == ["ORD-0001"]
    assert [o.order_id for o in sim.logs[1].backordered] == ["ORD-0002"]
