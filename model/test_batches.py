from model.model import Batch, OrderLine


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch(ref="abatch", sku=sku, qty=batch_qty),
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
    batch = Batch(ref="abatch", sku="asku", qty=10)
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
