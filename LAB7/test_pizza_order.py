from hypothesis import given, strategies as st
from pizza_order import toppings_price, pizza_inches, split_bill, TOPPINGS, SIZES


# ---------- Fuzz tests: no function may crash on any input ----------

@given(st.text() | st.none())
def test_toppings_price_no_crash(s):
    try:
        toppings_price(s)
    except Exception as e:
        assert False, f"toppings_price crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_pizza_inches_no_crash(s):
    try:
        pizza_inches(s)
    except Exception as e:
        assert False, f"pizza_inches crashed with: {e!r} for input {s!r}"


@given(st.text() | st.none())
def test_split_bill_no_crash(s):
    try:
        split_bill(s)
    except Exception as e:
        assert False, f"split_bill crashed with: {e!r} for input {s!r}"


# ---------- Property tests: valid input must give correct results ----------

@given(st.lists(st.sampled_from(list(TOPPINGS))))
def test_toppings_price_valid(items):
    assert toppings_price(",".join(items)) == sum(TOPPINGS[i] for i in items)


@given(st.sampled_from(list(SIZES)))
def test_pizza_inches_valid(size):
    assert pizza_inches(size) == SIZES[size]


@given(st.integers(min_value=0, max_value=10**6),
       st.integers(min_value=1, max_value=1000))
def test_split_bill_valid(total, people):
    assert split_bill(f"{total}/{people}") == round(total / people, 2)