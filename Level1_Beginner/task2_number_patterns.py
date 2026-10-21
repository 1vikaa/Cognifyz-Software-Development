"""
Cognifyz Technologies - Software Development Internship
Level 1 - Task 2: Generate and print simple number patterns

Uses nested loops to control the structure of each pattern.
Each function returns the pattern as a list of lines so it can be
both printed and verified automatically.
"""


def right_triangle(n):
    # 1 / 1 2 / 1 2 3 ...
    lines = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, i + 1):
            row.append(str(j))
        lines.append(" ".join(row))
    return lines


def pyramid(n):
    # Centered pyramid: 1 / 1 2 1 / 1 2 3 2 1 ...
    lines = []
    for i in range(1, n + 1):
        spaces = "  " * (n - i)
        row = []
        for j in range(1, i + 1):
            row.append(str(j))
        for j in range(i - 1, 0, -1):
            row.append(str(j))
        lines.append(spaces + " ".join(row))
    return lines


def inverted_triangle(n):
    # n n-1 ... 1 / ... / 1
    lines = []
    for i in range(n, 0, -1):
        row = []
        for j in range(i, 0, -1):
            row.append(str(j))
        lines.append(" ".join(row))
    return lines


def floyds_triangle(n):
    # 1 / 2 3 / 4 5 6 ...
    lines = []
    num = 1
    for i in range(1, n + 1):
        row = []
        for _ in range(i):
            row.append(str(num))
            num += 1
        lines.append(" ".join(row))
    return lines


def pascals_triangle(n):
    lines = []
    row = [1]
    for i in range(n):
        spaces = " " * (n - i - 1) * 2
        lines.append(spaces + "   ".join(str(x) for x in row))
        next_row = [1]
        for k in range(len(row) - 1):
            next_row.append(row[k] + row[k + 1])
        next_row.append(1)
        row = next_row
    return lines


PATTERNS = {
    "1": ("Right-angled triangle", right_triangle),
    "2": ("Number pyramid", pyramid),
    "3": ("Inverted triangle", inverted_triangle),
    "4": ("Floyd's triangle", floyds_triangle),
    "5": ("Pascal's triangle", pascals_triangle),
}


def verify_patterns():
    """Check the generated patterns against known correct output."""
    assert right_triangle(3) == ["1", "1 2", "1 2 3"]
    assert inverted_triangle(3) == ["3 2 1", "2 1", "1"]
    assert floyds_triangle(3) == ["1", "2 3", "4 5 6"]
    assert [l.strip() for l in pyramid(3)] == ["1", "1 2 1", "1 2 3 2 1"]
    assert pascals_triangle(5)[-1].split() == ["1", "4", "6", "4", "1"]
    print("All pattern checks passed.")


def main():
    verify_patterns()
    while True:
        print("\n=== NUMBER PATTERN GENERATOR ===")
        for key, (name, _) in PATTERNS.items():
            print(f"  {key}. {name}")
        print("  0. Exit")
        choice = input("Choose a pattern: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        if choice not in PATTERNS:
            print("Invalid choice.")
            continue

        size = input("Number of rows (1-15): ").strip()
        if not size.isdigit() or not 1 <= int(size) <= 15:
            print("Please enter a number between 1 and 15.")
            continue

        name, func = PATTERNS[choice]
        print(f"\n{name} with {size} rows:\n")
        for line in func(int(size)):
            print(line)


if __name__ == "__main__":
    main()
