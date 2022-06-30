from datetime import date, timedelta

import pytest

from model.model import Batch, OrderLine, OutOfStock, allocate


def make_batch_and_line(sku, batch_qty, line_qty, eta=None):
    return (
        Batch(ref="abatch", sku=sku, qty=batch_qty, eta=eta),
        OrderLine(orderid="anorder", sku=sku, qty=line_qty),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, order_line = make_batch_and_line(sku="sku", batch_qty=10, line_qty=9)
    batch.allocate(order_line)

    assert batch.available_quantity == 1


def test_cannot_allocate_to_a_batch_with_less_than_requested_quantity():
    batch, order_line = make_batch_and_line(sku="sku", batch_qty=10, line_qty=11)
    batch.allocate(order_line)

    assert batch.available_quantity == 10


def test_cannot_allocate_if_available_less_than_required():
    batch, order_line = make_batch_and_line(sku="sku", batch_qty=10, line_qty=11)
    result = batch.can_allocate(order_line)
    assert not result


def test_can_allocate_if_available_greater_than_required():
    batch, order_line = make_batch_and_line(sku="sku", batch_qty=10, line_qty=9)
    assert batch.can_allocate(order_line)


def test_can_allocate_if_available_equal_to_required():
    batch, order_line = make_batch_and_line(sku="sku", batch_qty=10, line_qty=10)
    assert batch.can_allocate(order_line)


def test_can_allocate_if_sku_matches_in_batch():
    batch, order_line = make_batch_and_line(sku="sku", batch_qty=10, line_qty=10)
    assert batch.can_allocate(order_line)


def test_cannot_allocate_if_sku_does_not_match_in_batch():
    batch = Batch(ref="abatch", sku="asku", qty=10, eta=None)
    order_line = OrderLine(orderid="anorder", sku="bsku", qty=9)
    assert not batch.can_allocate(order_line)


def test_deallocating_an_allocated_line_increases_available_quantity():
    batch, order_line = make_batch_and_line(sku="sku", batch_qty=10, line_qty=10)
    batch.allocate(order_line)
    batch.deallocate(order_line)
    assert batch.available_quantity == 10


def test_can_only_deallocate_allocated_line():
    batch, unallocated_line = make_batch_and_line(sku="sku", batch_qty=10, line_qty=10)
    batch.deallocate(unallocated_line)
    assert batch.available_quantity == 10


def test_can_allocate_an_order_line_only_once():
    batch, order_line = make_batch_and_line(sku="sku", batch_qty=20, line_qty=10)
    batch.allocate(order_line)
    batch.allocate(order_line)
    assert batch.available_quantity == 10


def test_allocates_to_in_stock_batch():
    tomorrow = date.today() + timedelta(days=1)
    in_stock_batch = Batch(ref="in_stock_batch", sku="asku", qty=10, eta=None)
    shipment_batch = Batch(ref="shipment_batch", sku="asku", qty=10, eta=tomorrow)
    order_line = OrderLine(orderid="anorder", sku="asku", qty=10)
    allocate(order_line, [in_stock_batch, shipment_batch])
    assert in_stock_batch.available_quantity == 0
    assert shipment_batch.available_quantity == 10


def test_allocates_to_earliest_available_batch():
    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    today_batch = Batch(ref="in_stock_batch", sku="asku", qty=10, eta=today)
    tomorrow_batch = Batch(ref="shipment_batch", sku="asku", qty=10, eta=tomorrow)
    order_line = OrderLine(orderid="anorder", sku="asku", qty=10)
    allocate(order_line, [today_batch, tomorrow_batch])
    assert today_batch.available_quantity == 0
    assert tomorrow_batch.available_quantity == 10


def test_allocate_raises_out_of_stock_exception_if_cannot_allocate():
    batch, order_line = make_batch_and_line(sku="asku", batch_qty=10, line_qty=20)
    with pytest.raises(OutOfStock, match="asku"):
        allocate(order_line, [batch])


def test_allocate_returns_allocated_batch_reference():
    batch, order_line = make_batch_and_line(sku="asku", batch_qty=10, line_qty=10)
    allocated_batch_reference = allocate(order_line, [batch])
    assert allocated_batch_reference == batch.ref
