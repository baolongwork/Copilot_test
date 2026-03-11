#!/usr/bin/env python3
"""
Calculator for 3 numbers
Performs basic arithmetic operations on three input numbers
"""


def add(a, b, c):
    return a + b + c


def subtract(a, b, c):
    return a - b - c


def multiply(a, b, c):
    return a * b * c


def divide(a, b, c):
    if b == 0 or c == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return a / b / c


def average(a, b, c):
    return (a + b + c) / 3


OPERATIONS = {
    '1': ('Add all three numbers',       lambda a, b, c: (add(a, b, c),      f"{a} + {b} + {c}")),
    '2': ('Subtract (num1 - num2 - num3)', lambda a, b, c: (subtract(a, b, c), f"{a} - {b} - {c}")),
    '3': ('Multiply all three numbers',   lambda a, b, c: (multiply(a, b, c), f"{a} × {b} × {c}")),
    '4': ('Divide (num1 / num2 / num3)',  lambda a, b, c: (divide(a, b, c),   f"{a} ÷ {b} ÷ {c}")),
    '5': ('Average of three numbers',    lambda a, b, c: (average(a, b, c),  f"Average of {a}, {b}, {c}")),
    '6': ('Find maximum',                lambda a, b, c: (max(a, b, c),      f"Maximum of {a}, {b}, {c}")),
    '7': ('Find minimum',                lambda a, b, c: (min(a, b, c),      f"Minimum of {a}, {b}, {c}")),
}


def calculator_3_numbers():
    """Simple calculator that takes 3 numbers and performs operations."""
    print("=" * 50)
    print("Calculator for 3 Numbers")
    print("=" * 50)

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        num3 = float(input("Enter third number: "))

        print("\nSelect operation:")
        for key, (label, _) in OPERATIONS.items():
            print(f"{key}. {label}")

        choice = input("\nEnter operation number (1-7): ").strip()

        if choice not in OPERATIONS:
            print("\nInvalid choice! Please select between 1-7.")
            return

        try:
            result, expr = OPERATIONS[choice][1](num1, num2, num3)
            print(f"\n{expr} = {result}")
        except ZeroDivisionError as e:
            print(f"\nError: {e}")

    except ValueError:
        print("\nError: Please enter valid numbers!")


if __name__ == "__main__":
    calculator_3_numbers()
