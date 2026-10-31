import pytest
from pizza_order import pizza_price, order_discount, delivery_status


def test_plain_medium_pizza():
    assert pizza_price("medium", 0, False) == 350


def test_on_time_delivery():
    assert delivery_status(20, 3) == "on time"


def test_unknown_size():
    with pytest.raises(ValueError):
        pizza_price("huge", 1, False)


def test_negative_toppings():
    with pytest.raises(ValueError):
        pizza_price("small", -1, False)


def test_many_toppings():
    assert pizza_price("large", 5, False) == 500 + 120 + 60


def test_cheese_burst_small():
    with pytest.raises(ValueError):
        pizza_price("small", 1, True)


def test_cheese_burst_medium():
    assert pizza_price("medium", 1, True) == 350 + 40 + 100


def test_small_order_no_discount():
    assert order_discount(200, "monday", False) == 0


def test_tuesday_discount():
    assert order_discount(400, "tuesday", False) == 200


def test_weekend_no_discount():
    assert order_discount(400, "saturday", False) == 0


def test_weekday_student_discount():
    assert order_discount(500, "monday", True) == 100


def test_not_deliverable():
    assert delivery_status(10, 15) == "not deliverable"


def test_late_delivery():
    assert delivery_status(40, 5) == "late"


def test_free_pizza():
    assert delivery_status(60, 5) == "free pizza"
