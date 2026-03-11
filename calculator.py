"""
Simple Calculator for 2 Numbers
Performs basic arithmetic operations on two numbers
"""

def add(a, b):
    """Add two numbers"""
    return a + b


def subtract(a, b):
    """Subtract two numbers"""
    return a - b


def multiply(a, b):
    """Multiply two numbers"""
    return a * b


def divide(a, b):
    """Divide two numbers"""
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b


def main():
    """Main calculator interface"""
    print("=" * 40)
    print("        Simple 2-Number Calculator")
    print("=" * 40)
    
    try:
        # Get input from user
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        print("\nSelect operation:")
        print("1. Add (+)")
        print("2. Subtract (-)")
        print("3. Multiply (*)")
        print("4. Divide (/)")
        
        operation = input("Enter operation (1/2/3/4): ")
        
        # Perform calculation based on operation
        if operation == '1':
            result = add(num1, num2)
            print(f"\n{num1} + {num2} = {result}")
        elif operation == '2':
            result = subtract(num1, num2)
            print(f"\n{num1} - {num2} = {result}")
        elif operation == '3':
            result = multiply(num1, num2)
            print(f"\n{num1} * {num2} = {result}")
        elif operation == '4':
            result = divide(num1, num2)
            print(f"\n{num1} / {num2} = {result}")
        else:
            print("\nInvalid operation selected!")
    
    except ValueError:
        print("\nError: Please enter valid numbers!")


if __name__ == "__main__":
    main()
