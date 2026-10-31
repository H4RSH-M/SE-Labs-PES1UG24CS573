import pytest
from pizza_order import pizza_price, order_discount, delivery_status


# pizza_price: every size and both sides of each decision
@pytest.mark.parametrize("size, price", [("small", 200), ("medium", 350), ("large", 500)])
def test_all_sizes_no_toppings(size, price):
    assert pizza_price(size, 0, False) == price


def test_unknown_size():
    with pytest.raises(ValueError, match="unknown size"):
        pizza_price("huge", 1, False)


def test_negative_toppings():
    with pytest.raises(ValueError, match="invalid toppings"):
        pizza_price("small", -1, False)


def test_toppings_boundary_three():
    assert pizza_price("medium", 3, False) == 350 + 3 * 40


def test_toppings_above_three():
    assert pizza_price("large", 5, False) == 500 + 3 * 40 + 2 * 30


def test_cheese_burst_small_not_allowed():
    with pytest.raises(ValueError, match="cheese burst"):
        pizza_price("small", 0, True)


def test_cheese_burst_medium():
    assert pizza_price("medium", 1, True) == 350 + 40 + 100


def test_cheese_burst_large():
    assert pizza_price("large", 4, True) == 500 + 120 + 30 + 100


# order_discount: both sides of every decision
def test_total_below_threshold():
    assert order_discount(299, "monday", True) == 0


def test_total_at_threshold():
    assert order_discount(300, "monday", False) == 30


def test_tuesday_no_student():
    assert order_discount(400, "tuesday", False) == 200


def test_tuesday_student():
    assert order_discount(400, "tuesday", True) == 250


@pytest.mark.parametrize("day", ["saturday", "sunday"])
def test_weekend_no_discount(day):
    assert order_discount(500, day, False) == 0


def test_weekend_student():
    assert order_discount(500, "sunday", True) == 50


def test_weekday_no_student():
    assert order_discount(500, "friday", False) == 50


def test_weekday_student():
    assert order_discount(500, "friday", True) == 100


# delivery_status: boundaries of each decision
def test_too_far():
    assert delivery_status(10, 11) == "not deliverable"


def test_distance_boundary_ten():
    assert delivery_status(20, 10) == "on time"


def test_on_time_boundary():
    assert delivery_status(30, 5) == "on time"


def test_late_lower_boundary():
    assert delivery_status(31, 5) == "late"


def test_late_upper_boundary():
    assert delivery_status(45, 5) == "late"


def test_free_pizza():
    assert delivery_status(46, 5) == "free pizza"
