# Copilot_test

## Calculator CLI (`calculator.py`)

`calculator.py` is a command-line calculator that operates on **three numbers** at a time.

### Features

- **Add** – sum of all three numbers
- **Subtract** – `num1 - num2 - num3`
- **Multiply** – product of all three numbers
- **Divide** – `num1 / num2 / num3` (raises an error if any divisor is zero)
- **Average** – arithmetic mean of the three numbers
- **Maximum** – largest of the three numbers
- **Minimum** – smallest of the three numbers

### Usage

```bash
python3 calculator.py
```

You will be prompted to enter three numbers and then choose an operation (1–7).

### Example

```
==================================================
Calculator for 3 Numbers
==================================================
Enter first number: 10
Enter second number: 4
Enter third number: 2

Select operation:
1. Add all three numbers
2. Subtract (num1 - num2 - num3)
3. Multiply all three numbers
4. Divide (num1 / num2 / num3)
5. Average of three numbers
6. Find maximum
7. Find minimum

Enter operation number (1-7): 1

10.0 + 4.0 + 2.0 = 16
```

---

## Calculator Web App

`calculator.html` now includes an accessible login flow before users can use the calculator.

### Login details (demo)

- Username: `admin`
- Password: `password123`

### Accessibility highlights

- Proper form labels and semantic sections
- Keyboard-friendly interactions for form and calculator actions
- `aria-live` announcements for login state, errors, and calculation updates
- Focus management on login, logout, and form validation errors