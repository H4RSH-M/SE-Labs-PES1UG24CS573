TOPPINGS = {"cheese": 40, "olives": 30, "onion": 20, "paneer": 50}
SIZES = {"S": 8, "M": 10, "L": 12}


def toppings_price(toppings_csv):
    """Sum the price of known toppings. Non-strings, empty and unknown
    toppings are ignored instead of crashing."""
    if not isinstance(toppings_csv, str):
        return 0
    total = 0
    for t in toppings_csv.split(','):
        total += TOPPINGS.get(t.strip().lower(), 0)
    return total


def pizza_inches(size):
    """Return the size in inches, or None for invalid input."""
    if not isinstance(size, str):
        return None
    return SIZES.get(size.strip().upper())


def split_bill(text):
    """Return the per-person amount, or None for invalid input."""
    if not isinstance(text, str):
        return None
    parts = text.split('/')
    if len(parts) != 2:
        return None
    try:
        total = int(parts[0])
        people = int(parts[1])
        if total < 0 or people <= 0:
            return None
        return round(total / people, 2)
    except (ValueError, OverflowError):
        return None


def main():
    print("==== Running toppings_price ====")
    user_input = input("Enter toppings as CSV (e.g. cheese,olives): ")
    result = toppings_price(user_input)
    print("Toppings Price:", result)

    print("\n==== Running pizza_inches ====")
    user_input = input("Enter pizza size (S/M/L): ")
    result = pizza_inches(user_input)
    print("Size in Inches:", result if result is not None else "Invalid size")

    print("\n==== Running split_bill ====")
    user_input = input("Enter total and people (e.g. 900/3): ")
    result = split_bill(user_input)
    print("Per Person:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()