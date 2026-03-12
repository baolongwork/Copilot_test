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
    '1': ('Add all three numbers', add),
    '2': ('Subtract (num1 - num2 - num3)', subtract),
    '3': ('Multiply all three numbers', multiply),
    '4': ('Divide (num1 / num2 / num3)', divide),
    '5': ('Average of three numbers', average),
    '6': ('Find maximum', max),
    '7': ('Find minimum', min),
}

# Expression templates - computed once at module load time
EXPRESSION_TEMPLATES = {
    '1': "{num1} + {num2} + {num3}",
    '2': "{num1} - {num2} - {num3}",
    '3': "{num1} × {num2} × {num3}",
    '4': "{num1} ÷ {num2} ÷ {num3}",
    '5': "Average of {num1}, {num2}, {num3}",
    '6': "Maximum of {num1}, {num2}, {num3}",
    '7': "Minimum of {num1}, {num2}, {num3}",
}


def format_expression(operation_name, num1, num2, num3):
    """Format the operation expression for display."""
    template = EXPRESSION_TEMPLATES.get(operation_name, "")
    return template.format(num1=num1, num2=num2, num3=num3) if template else ""


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
            result = OPERATIONS[choice][1](num1, num2, num3)
            expr = format_expression(choice, num1, num2, num3)
            print(f"\n{expr} = {result}")
        except ZeroDivisionError as e:
            print(f"\nError: {e}")

    except ValueError:
        print("\nError: Please enter valid numbers!")


if __name__ == "__main__":
    calculator_3_numbers()

