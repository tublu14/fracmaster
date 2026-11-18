from __future__ import annotations

from math import gcd, lcm
from typing import SupportsFloat


class Fraction:
    def __init__(
        self,
        numerator: int,
        denominator: int,
        whole: int = 0,
        proper: bool = True,
        simple: bool = False,
    ):
        self.numerator = int(numerator)
        self.denominator = int(denominator)
        self.whole = int(whole)
        self.is_proper = bool(proper)
        self.is_simplified = bool(simple)

        if self.is_proper:
            self.whole += self.numerator // self.denominator
            self.numerator = self.numerator % self.denominator
            self.denominator = 1 if not self.numerator else self.denominator

        if not self.is_proper:
            self.numerator += self.denominator * self.whole
            self.whole = 0

        if self.is_simplified and self.numerator != 0:
            self.numerator, self.denominator = (
                self.numerator // gcd(self.numerator, self.denominator),
                self.denominator // gcd(self.numerator, self.denominator),
            )

    @classmethod
    def from_float(cls, fraction: float, proper: bool = True, simple: bool = True):
        numerator, denominator = float(fraction).as_integer_ratio()

        return Fraction(numerator, denominator, proper=proper, simple=simple)

    def convert_improper(self):
        if not self.is_proper:
            return

        self.numerator += self.denominator * self.whole
        self.whole = 0
        self.is_proper = False

    def convert_proper(self):
        if self.is_proper:
            return

        self.whole += self.numerator // self.denominator
        self.numerator = self.numerator % self.denominator
        self.denominator = 1 if not self.numerator else self.denominator
        self.is_proper = True

    def simplify(self):
        if self.is_simplified:
            return

        if self.numerator != 0:
            self.numerator, self.denominator = (
                self.numerator // gcd(self.numerator, self.denominator),
                self.denominator // gcd(self.numerator, self.denominator),
            )

            self.is_simplified = True

    def as_improper(self) -> Fraction:
        return Fraction(self.numerator, self.denominator, self.whole, False)

    def as_proper(self) -> Fraction:
        return Fraction(self.numerator, self.denominator, self.whole, True)

    def simplified(self) -> Fraction:
        return Fraction(self.numerator, self.denominator, self.whole, simple=True)

    def reciprocal(self) -> Fraction:
        imp = self.as_improper()

        return Fraction(imp.denominator, imp.numerator, proper=False)

    def __str__(self) -> str:
        return f"Fraction({self.whole} + {self.numerator}/{self.denominator})"

    def __repr__(self) -> str:
        return str(self)

    def __float__(self) -> float:
        return self.whole + self.numerator / self.denominator

    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, SupportsFloat):
            return float(self) == float(value)
        return False

    def __ne__(self, value: object, /) -> bool:
        return not self == value

    def __gt__(self, other) -> bool:
        if isinstance(other, SupportsFloat):
            return float(self) > float(other)
        return False

    def __lt__(self, other) -> bool:
        if isinstance(other, SupportsFloat):
            return float(self) < float(other)
        return False

    def __ge__(self, other) -> bool:
        return self > other or self == other

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __add__(self, other: SupportsFloat) -> Fraction:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, Fraction):
            imp_self = self.as_improper()
            imp_other = other.as_improper()

            denominator = lcm(imp_self.denominator, imp_other.denominator)

            numerator = ((denominator // imp_self.denominator) * imp_self.numerator) + (
                (denominator // imp_other.denominator) * imp_other.numerator
            )

            return Fraction(numerator, denominator)
        return Fraction.from_float(float(self) + float(other))

    def __radd__(self, other: SupportsFloat):
        return self + other

    def __sub__(self, other: SupportsFloat) -> Fraction:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, Fraction):
            imp_self = self.as_improper()
            imp_other = other.as_improper()

            denominator = lcm(imp_self.denominator, imp_other.denominator)

            numerator = ((denominator // imp_self.denominator) * imp_self.numerator) - (
                (denominator // imp_other.denominator) * imp_other.numerator
            )

            return Fraction(numerator, denominator)
        return Fraction.from_float(float(self) - float(other))

    def __rsub__(self, other: SupportsFloat):
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, int):
            frac_other = Fraction(other, 1)
            return frac_other - self

        return Fraction.from_float(float(other) - float(self))

    def __mul__(self, other: SupportsFloat) -> Fraction:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, Fraction):
            numerator = self.as_improper().numerator * other.as_improper().numerator
            denominator = (
                self.as_improper().denominator * other.as_improper().denominator
            )

            return Fraction(numerator, denominator)
        return Fraction.from_float(float(self) * float(other))

    def __rmul__(self, other: SupportsFloat):
        return self * other

    def __truediv__(self, other: SupportsFloat) -> Fraction:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, Fraction):
            return self * other.reciprocal()
        return Fraction.from_float(float(self) / float(other))

    def __rtruediv__(self, other: SupportsFloat):
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, int):
            frac_other = Fraction(other, 1)
            return frac_other / self

        return Fraction.from_float(float(other) / float(self))


def find_numerator(base_fraction: Fraction, denominator: int) -> int:
    if not isinstance(base_fraction, Fraction):
        raise TypeError(
            f"'{type(base_fraction).__name__}' object cannot be interpreted as a Fraction"
        )

    if not isinstance(denominator, int):
        raise TypeError(
            f"'{type(denominator).__name__}' object cannot be interpreted as an integer"
        )
    simplified_base = base_fraction.simplified()

    if denominator % simplified_base.denominator == 0:
        numerator = simplified_base.numerator * (
            denominator // simplified_base.denominator
        )
        return numerator

    else:
        raise ValueError(
            "arg 'denominator' must be perfectly divisible by simplified base_fraction's denominator"
        )


def find_denominator(base_fraction: Fraction, numerator: int) -> int:
    if not isinstance(base_fraction, Fraction):
        raise TypeError(
            f"'{type(base_fraction).__name__}' object cannot be interpreted as a Fraction"
        )

    if not isinstance(numerator, int):
        raise TypeError(
            f"'{type(numerator).__name__}' object cannot be interpreted as an integer"
        )

    simplified_base = base_fraction.simplified()

    if numerator % simplified_base.numerator == 0:
        denominator = simplified_base.denominator * (
            numerator // simplified_base.numerator
        )
        return denominator

    else:
        raise ValueError(
            "arg 'numerator' must be perfectly divisible by simplified base_fraction's numerator"
        )


def find_total(fraction_times_x: Fraction, equal_to: SupportsFloat):
    if not isinstance(fraction_times_x, Fraction):
        raise TypeError(
            f"'{type(fraction_times_x).__name__}' object cannot be interpreted as a Fraction"
        )

    if not isinstance(equal_to, SupportsFloat):
        raise TypeError(
            f"'{type(equal_to).__name__}' object is not an instance of 'SupportsFloat' class"
        )

    if isinstance(equal_to, int):
        total = fraction_times_x.reciprocal() * Fraction(equal_to, 1)
        return total

    else:
        total = fraction_times_x.reciprocal() * equal_to
        return total
