def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return the quotient of a divided by b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


if __name__ == "__main__":
    print("Calculator for 2 Numbers")
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    print(f"  {a} + {b} = {add(a, b)}")
    print(f"  {a} - {b} = {subtract(a, b)}")
    print(f"  {a} * {b} = {multiply(a, b)}")
    if b != 0:
        print(f"  {a} / {b} = {divide(a, b)}")
    else:
        print(f"  {a} / {b} = Cannot divide by zero")
