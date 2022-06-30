from model import model


def test_orderline_mapper_can_load_lines(session):
    session.execute(
        "INSERT INTO order_lines (orderid, sku, qty) VALUES"
        '("order_1", "RED-CHAIR", 12),'
        '("order_1", "RED-TABLE", 13),'
        '("order_2", "BLUE-LIPSTICK", 14)'
    )
    expected = [
        model.OrderLine("order_1", "RED-CHAIR", 12),
        model.OrderLine("order_1", "RED-TABLE", 13),
        model.OrderLine("order_2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(model.OrderLine).all() == expected
