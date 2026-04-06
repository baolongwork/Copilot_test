"""Unit tests for calculator.py"""
import unittest
from calculator import add, subtract, multiply, divide, average, format_expression


class TestAdd(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add(1, 2, 3), 6)

    def test_negative_numbers(self):
        self.assertEqual(add(-1, -2, -3), -6)

    def test_mixed_numbers(self):
        self.assertEqual(add(-1, 2, 3), 4)

    def test_floats(self):
        self.assertAlmostEqual(add(1.5, 2.5, 3.0), 7.0)

    def test_zeros(self):
        self.assertEqual(add(0, 0, 0), 0)


class TestSubtract(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(subtract(10, 3, 2), 5)

    def test_negative_numbers(self):
        self.assertEqual(subtract(-1, -2, -3), 4)

    def test_zeros(self):
        self.assertEqual(subtract(0, 0, 0), 0)

    def test_floats(self):
        self.assertAlmostEqual(subtract(10.0, 2.5, 1.5), 6.0)


class TestMultiply(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(multiply(2, 3, 4), 24)

    def test_with_zero(self):
        self.assertEqual(multiply(5, 0, 3), 0)

    def test_negative_numbers(self):
        self.assertEqual(multiply(-2, -3, 4), 24)

    def test_floats(self):
        self.assertAlmostEqual(multiply(2.0, 2.5, 4.0), 20.0)


class TestDivide(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertAlmostEqual(divide(100, 4, 5), 5.0)

    def test_floats(self):
        self.assertAlmostEqual(divide(10.0, 2.0, 2.5), 2.0)

    def test_divide_by_zero_second_arg(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0, 5)

    def test_divide_by_zero_third_arg(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 5, 0)

    def test_divide_both_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0, 0)


class TestAverage(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertAlmostEqual(average(1, 2, 3), 2.0)

    def test_zeros(self):
        self.assertAlmostEqual(average(0, 0, 0), 0.0)

    def test_negative_numbers(self):
        self.assertAlmostEqual(average(-3, 0, 3), 0.0)

    def test_floats(self):
        self.assertAlmostEqual(average(1.5, 2.5, 3.0), 7.0 / 3)


class TestFormatExpression(unittest.TestCase):
    def test_add_expression(self):
        self.assertEqual(format_expression('1', 1, 2, 3), "1 + 2 + 3")

    def test_subtract_expression(self):
        self.assertEqual(format_expression('2', 10, 3, 2), "10 - 3 - 2")

    def test_multiply_expression(self):
        self.assertEqual(format_expression('3', 2, 3, 4), "2 × 3 × 4")

    def test_divide_expression(self):
        self.assertEqual(format_expression('4', 10, 2, 5), "10 ÷ 2 ÷ 5")

    def test_average_expression(self):
        self.assertEqual(format_expression('5', 1, 2, 3), "Average of 1, 2, 3")

    def test_max_expression(self):
        self.assertEqual(format_expression('6', 1, 2, 3), "Maximum of 1, 2, 3")

    def test_min_expression(self):
        self.assertEqual(format_expression('7', 1, 2, 3), "Minimum of 1, 2, 3")

    def test_invalid_operation(self):
        self.assertEqual(format_expression('99', 1, 2, 3), "")


if __name__ == "__main__":
    unittest.main()
