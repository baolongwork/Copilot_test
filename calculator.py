#!/usr/bin/env python3
"""
Calculator for 3 numbers
Performs basic arithmetic operations on three input numbers
"""

def calculator_3_numbers():
    """
    Simple calculator that takes 3 numbers and performs operations
    """
    print("=" * 50)
    print("Calculator for 3 Numbers")
    print("=" * 50)
    
    try:
        # Get input from user
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        num3 = float(input("Enter third number: "))
        
        # Display menu
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
            result = num1 + num2 + num3
            print(f"\n{num1} + {num2} + {num3} = {result}")
        elif choice == '2':
            result = num1 - num2 - num3
            print(f"\n{num1} - {num2} - {num3} = {result}")
        elif choice == '3':
            result = num1 * num2 * num3
            print(f"\n{num1} × {num2} × {num3} = {result}")
        elif choice == '4':
            if num2 == 0 or num3 == 0:
                print("\nError: Cannot divide by zero!")
            else:
                result = num1 / num2 / num3
                print(f"\n{num1} ÷ {num2} ÷ {num3} = {result}")
        elif choice == '5':
            result = (num1 + num2 + num3) / 3
            print(f"\nAverage of {num1}, {num2}, {num3} = {result}")
        elif choice == '6':
            result = max(num1, num2, num3)
            print(f"\nMaximum of {num1}, {num2}, {num3} = {result}")
        elif choice == '7':
            result = min(num1, num2, num3)
            print(f"\nMinimum of {num1}, {num2}, {num3} = {result}")
        else:
            print("\nInvalid choice! Please select between 1-7.")
            
    except ValueError:
        print("\nError: Please enter valid numbers!")

if __name__ == "__main__":
    calculator_3_numbers()
