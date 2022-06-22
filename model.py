from dataclasses import dataclass
from typing import Set


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int):
        self.ref = ref
        self.sku = sku
        self._purchased_quantity = qty
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
