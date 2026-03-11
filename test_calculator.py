"""Tests for calculator.py pure arithmetic functions."""

import pytest
from calculator import add, subtract, multiply, divide, average, maximum, minimum


class TestAdd:
    def test_positive_numbers(self):
        assert add(1, 2, 3) == 6

    def test_with_zero(self):
        assert add(0, 0, 0) == 0

    def test_negative_numbers(self):
        assert add(-1, -2, -3) == -6

    def test_floats(self):
        assert add(1.5, 2.5, 3.0) == 7.0


class TestSubtract:
    def test_positive_numbers(self):
        assert subtract(10, 3, 2) == 5

    def test_result_negative(self):
        assert subtract(1, 5, 5) == -9

    def test_zeros(self):
        assert subtract(0, 0, 0) == 0


class TestMultiply:
    def test_positive_numbers(self):
        assert multiply(2, 3, 4) == 24

    def test_with_zero(self):
        assert multiply(5, 0, 5) == 0

    def test_negative_numbers(self):
        assert multiply(-2, 3, 4) == -24

    def test_floats(self):
        assert multiply(1.5, 2.0, 2.0) == 6.0


class TestDivide:
    def test_even_division(self):
        assert divide(24, 4, 2) == 3.0

    def test_float_result(self):
        assert divide(10, 4, 1) == 2.5

    def test_divide_by_zero_second(self):
        with pytest.raises(ZeroDivisionError):
            divide(10, 0, 2)

    def test_divide_by_zero_third(self):
        with pytest.raises(ZeroDivisionError):
            divide(10, 2, 0)


class TestAverage:
    def test_basic(self):
        assert average(1, 2, 3) == 2.0

    def test_same_values(self):
        assert average(5, 5, 5) == 5.0

    def test_floats(self):
        assert average(0.0, 1.5, 4.5) == 2.0


class TestMaximum:
    def test_last_is_max(self):
        assert maximum(1, 2, 3) == 3

    def test_first_is_max(self):
        assert maximum(9, 3, 5) == 9

    def test_all_equal(self):
        assert maximum(4, 4, 4) == 4

    def test_negative_numbers(self):
        assert maximum(-3, -1, -2) == -1


class TestMinimum:
    def test_first_is_min(self):
        assert minimum(1, 2, 3) == 1

    def test_last_is_min(self):
        assert minimum(5, 3, 2) == 2

    def test_all_equal(self):
        assert minimum(7, 7, 7) == 7

    def test_negative_numbers(self):
        assert minimum(-3, -1, -2) == -3
