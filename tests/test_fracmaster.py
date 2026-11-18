import unittest

from fracmaster import Fraction, find_numerator, find_total


class TestFracmaster(unittest.TestCase):
    def test_initialization_and_proper(self):
        f = Fraction(5, 2)
        self.assertEqual(f.whole, 2)
        self.assertEqual(f.numerator, 1)
        self.assertEqual(f.denominator, 2)

    def test_addition(self):
        f1 = Fraction(1, 3)
        f2 = Fraction(2, 3)
        result = f1 + f2
        self.assertEqual(result.whole, 1)
        self.assertEqual(result.numerator, 0)

    def test_subtraction(self):
        f1 = Fraction(3, 4)
        f2 = Fraction(1, 4)
        result = f1 - f2
        self.assertEqual(result.numerator, 2)
        self.assertEqual(result.denominator, 4)

    def test_multiplication_and_reciprocal(self):
        f = Fraction(1, 2)
        rec = f.reciprocal()
        self.assertEqual(rec.numerator, 2)
        self.assertEqual(rec.denominator, 1)

    def test_comparisons(self):
        f1 = Fraction(1, 3)
        f2 = Fraction(2, 3)
        self.assertTrue(f1 < f2)
        self.assertTrue(f2 > f1)
        self.assertEqual(Fraction.from_float(0.5), 0.5)
        self.assertTrue(0.5 > f1)

    def test_from_float(self):
        f = Fraction.from_float(0.5)
        self.assertEqual(float(f), 0.5)

    def test_helper_find_numerator(self):
        f = Fraction(1, 3)
        num = find_numerator(f, 6)
        self.assertEqual(num, 2)

    def test_helper_find_total(self):
        total = find_total(Fraction(1, 2), 5)
        self.assertEqual(float(total), 10.0)


if __name__ == "__main__":
    unittest.main()
