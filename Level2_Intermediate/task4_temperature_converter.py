"""
Cognifyz Technologies - Software Development Internship
Level 2 - Task 4: Temperature converter

Lets the user enter a temperature and choose the conversion direction
between Celsius, Fahrenheit (and Kelvin as a bonus).
"""

ABSOLUTE_ZERO = {"C": -273.15, "F": -459.67, "K": 0.0}
UNIT_NAMES = {"C": "Celsius", "F": "Fahrenheit", "K": "Kelvin"}


def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32


def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9


def celsius_to_kelvin(c):
    return c + 273.15


def kelvin_to_celsius(k):
    return k - 273.15


def convert(value, from_unit, to_unit):
    """Convert value between C, F and K by going through Celsius."""
    if value < ABSOLUTE_ZERO[from_unit]:
        raise ValueError(
            f"{value}°{from_unit} is below absolute zero "
            f"({ABSOLUTE_ZERO[from_unit]}°{from_unit}).")

    if from_unit == "C":
        celsius = value
    elif from_unit == "F":
        celsius = fahrenheit_to_celsius(value)
    else:
        celsius = kelvin_to_celsius(value)

    if to_unit == "C":
        return celsius
    elif to_unit == "F":
        return celsius_to_fahrenheit(celsius)
    else:
        return celsius_to_kelvin(celsius)


CONVERSIONS = {
    "1": ("C", "F"),
    "2": ("F", "C"),
    "3": ("C", "K"),
    "4": ("K", "C"),
    "5": ("F", "K"),
    "6": ("K", "F"),
}


def run_tests():
    """Test the conversion logic with known values."""
    def close(a, b):
        return abs(a - b) < 1e-9

    assert close(convert(0, "C", "F"), 32)
    assert close(convert(100, "C", "F"), 212)
    assert close(convert(-40, "C", "F"), -40)
    assert close(convert(98.6, "F", "C"), 37)
    assert close(convert(0, "C", "K"), 273.15)
    assert close(convert(0, "K", "F"), -459.67)
    try:
        convert(-300, "C", "F")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    print("All conversion tests passed.")


def main():
    run_tests()
    while True:
        print("\n===== TEMPERATURE CONVERTER =====")
        for key, (src, dst) in CONVERSIONS.items():
            print(f"  {key}. {UNIT_NAMES[src]} -> {UNIT_NAMES[dst]}")
        print("  0. Exit")
        choice = input("Choose conversion: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        if choice not in CONVERSIONS:
            print("Invalid choice.")
            continue

        src, dst = CONVERSIONS[choice]
        text = input(f"Enter temperature in {UNIT_NAMES[src]}: ").strip()
        try:
            value = float(text)
            result = convert(value, src, dst)
            print(f"\n{value:g}°{src} = {result:.2f}°{dst}")
        except ValueError as e:
            if "absolute zero" in str(e):
                print(f"Error: {e}")
            else:
                print("Error: please enter a valid number.")


if __name__ == "__main__":
    main()
