#!/usr/bin/env python3
"""
Calculator for 3 numbers
Performs basic arithmetic operations on three input numbers
"""


def add(a, b, c):
    """Return the sum of three numbers."""
    return a + b + c


def subtract(a, b, c):
    """Return a - b - c."""
    return a - b - c


def multiply(a, b, c):
    """Return the product of three numbers."""
    return a * b * c


def divide(a, b, c):
    """Return a / b / c. Raises ZeroDivisionError if b or c is zero."""
    if b == 0 or c == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b / c


def average(a, b, c):
    """Return the average of three numbers."""
    return (a + b + c) / 3


def maximum(a, b, c):
    """Return the largest of three numbers."""
    return max(a, b, c)


def minimum(a, b, c):
    """Return the smallest of three numbers."""
    return min(a, b, c)


def calculator_3_numbers():
    """
    Simple calculator that takes 3 numbers and performs operations
    """
    print("=" * 50)
    print("Calculator for 3 Numbers")
    print("=" * 50)

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        num3 = float(input("Enter third number: "))

        print("\nSelect operation:")
        print("1. Add all three numbers")
        print("2. Subtract (num1 - num2 - num3)")
        print("3. Multiply all three numbers")
        print("4. Divide (num1 / num2 / num3)")
        print("5. Average of three numbers")
        print("6. Find maximum")
        print("7. Find minimum")

        choice = input("\nEnter operation number (1-7): ").strip()

        if choice == '1':
            result = add(num1, num2, num3)
            print(f"\n{num1} + {num2} + {num3} = {result}")
        elif choice == '2':
            result = subtract(num1, num2, num3)
            print(f"\n{num1} - {num2} - {num3} = {result}")
        elif choice == '3':
            result = multiply(num1, num2, num3)
            print(f"\n{num1} × {num2} × {num3} = {result}")
        elif choice == '4':
            try:
                result = divide(num1, num2, num3)
                print(f"\n{num1} ÷ {num2} ÷ {num3} = {result}")
            except ZeroDivisionError:
                print("\nError: Cannot divide by zero!")
        elif choice == '5':
            result = average(num1, num2, num3)
            print(f"\nAverage of {num1}, {num2}, {num3} = {result}")
        elif choice == '6':
            result = maximum(num1, num2, num3)
            print(f"\nMaximum of {num1}, {num2}, {num3} = {result}")
        elif choice == '7':
            result = minimum(num1, num2, num3)
            print(f"\nMinimum of {num1}, {num2}, {num3} = {result}")
        else:
            print("\nInvalid choice! Please select between 1-7.")

    except ValueError:
        print("\nError: Please enter valid numbers!")


if __name__ == "__main__":
    calculator_3_numbers()
