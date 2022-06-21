from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int):
        self.ref = ref
        self.sku = sku
        self.available_quantity = qty

    def allocate(self, order_line: OrderLine):
        self.available_quantity -= order_line.qty

    def can_allocate(self, order_line: OrderLine):
        return self.sku == order_line.sku and self.available_quantity >= order_line.qty
