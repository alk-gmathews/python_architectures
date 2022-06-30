from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Set


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.ref = ref
        self.sku = sku
        self._purchased_quantity = qty
        self.eta = eta
        self._allocations: Set[OrderLine] = set()

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - sum([line.qty for line in self._allocations])

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return (
            self.sku == order_line.sku
            and self.available_quantity >= order_line.qty
            and order_line not in self._allocations
        )

    def deallocate(self, order_line: OrderLine):
        if self.can_deallocate(order_line):
            self._allocations.remove(order_line)

    def can_deallocate(self, order_line: OrderLine) -> bool:
        return order_line in self._allocations

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


def allocate(order_line: OrderLine, batches: List[Batch]):
    available_batches = [batch for batch in batches if batch.can_allocate(order_line)]
    if not available_batches:
        raise OutOfStock(
            f"We cannot allocate order line: <order id: {order_line.orderid}>, <sku: {order_line.sku}>, <quantity: {order_line.qty}>"
        )
    earliest_batch = min(available_batches)
    earliest_batch.allocate(order_line)
    return earliest_batch.ref


class OutOfStock(Exception):
    pass
