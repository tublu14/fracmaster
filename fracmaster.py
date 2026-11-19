from __future__ import annotations

from math import gcd, lcm
from typing import SupportsFloat


class Frac:
    """
    Handles fractional numbers without turning them into a float value.

    Float values sometimes are really messy becuase computers store numbers in base-2 instead of
    human-readable base-10, and some numbers can't be stored cleanly in base-2, and that's where
    the Frac class shines. It represents fractions in clean base-10 integers with numerators,
    denominators and whole numbers.

    These can also be converted into float values.

    Attributes:
        numerator: Numerator of fraction.
        denominator: Denominator of fraction.
        whole: Whole number part of fraction.
        proper: Decides if the fraction is proper or not.
        simple: Decides if the fraction is simplified or not.

    Example:
        ```python
        frac1 = Frac(1, 2)
        frac2 = Frac(2, 3)

        print(frac1 + frac2) # Output: Frac(1 + 1/6)
        ```
    """

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
    def from_float(
        cls, fraction: float, proper: bool = True, simple: bool = True
    ) -> Frac:
        """
        Returns a Frac object that represents the float value `fraction`.

        Args:
            `fraction`: The float value from which the Frac obj will be created.
            `proper`: Decides if the fraction is proper or not.
            `simple`: Decides if the fraction is simple or not.

        Returns:
            A Frac object equal to the float value.

        Examples:
            ```python
            >>> Frac.from_float(0.5)
            Frac(0 + 1/2)
            >>> Frac.from_float(1.9)
            Frac(1 + 9/10)
            ```
        """

        numerator = float(fraction)
        denominator = 1
        decimal_part = str(numerator).split(".")[1]

        for _ in range(len(decimal_part)):
            numerator *= 10
            denominator *= 10

        return Frac(int(numerator), denominator, proper=proper, simple=simple)

    def convert_improper(self) -> None:
        """
        Converts `self` to improper if not already.

        Examples:
            ```python
            frac = Frac(2, 3, 2)

            frac.convert_improper()

            print(frac) # Output: Frac(0 + 8/3)
            ```
        """

        if not self.is_proper:
            return

        self.numerator += self.denominator * self.whole
        self.whole = 0
        self.is_proper = False

    def convert_proper(self):
        """
        Converts `self` to proper if not already.

        **Example**:
            ```python
            frac = Frac(5, 3, proper=False)

            frac.convert_proper()

            print(frac) # Output: Frac(1 + 2/3)
            ```
        """

        if self.is_proper:
            return

        self.whole += self.numerator // self.denominator
        self.numerator = self.numerator % self.denominator
        self.denominator = 1 if not self.numerator else self.denominator
        self.is_proper = True

    def simplify(self):
        """
        Simplifies `self` if not already.

        Reduces `self` to the lowest terms (where `GCD(numerator, denominator)` is 1).

        **Example**:
            ```python
            frac = Frac(2, 4)

            frac.simplify()

            print(frac) # Output: Frac(1, 2)
            ```
        """

        if self.is_simplified:
            return

        if self.numerator != 0:
            self.numerator, self.denominator = (
                self.numerator // gcd(self.numerator, self.denominator),
                self.denominator // gcd(self.numerator, self.denominator),
            )

            self.is_simplified = True

    def as_improper(self) -> Frac:
        """Returns the improper version of `self`."""

        return Frac(self.numerator, self.denominator, self.whole, False)

    def as_proper(self) -> Frac:
        """Returns the proper version of `self`."""

        return Frac(self.numerator, self.denominator, self.whole, True)

    def simplified(self) -> Frac:
        """Returns the simplified version of `self`."""

        return Frac(self.numerator, self.denominator, self.whole, simple=True)

    def reciprocal(self) -> Frac:
        """
        Returns the reciprocal of `self`.

        Returns the fraction which multiplied by `self` equals 1.
        """

        imp = self.as_improper()

        return Frac(imp.denominator, imp.numerator)

    def __str__(self) -> str:
        return f"Frac({self.whole} + {self.numerator}/{self.denominator})"

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

    def __add__(self, other: SupportsFloat) -> Frac:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, Frac):
            imp_self = self.as_improper()
            imp_other = other.as_improper()

            denominator = lcm(imp_self.denominator, imp_other.denominator)

            numerator = ((denominator // imp_self.denominator) * imp_self.numerator) + (
                (denominator // imp_other.denominator) * imp_other.numerator
            )

            return Frac(numerator, denominator)
        return Frac.from_float(float(self) + float(other))

    def __radd__(self, other: SupportsFloat):
        return self + other

    def __sub__(self, other: SupportsFloat) -> Frac:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, Frac):
            imp_self = self.as_improper()
            imp_other = other.as_improper()

            denominator = lcm(imp_self.denominator, imp_other.denominator)

            numerator = ((denominator // imp_self.denominator) * imp_self.numerator) - (
                (denominator // imp_other.denominator) * imp_other.numerator
            )

            return Frac(numerator, denominator)
        return Frac.from_float(float(self) - float(other))

    def __rsub__(self, other: SupportsFloat):
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, int):
            frac_other = Frac(other, 1)
            return frac_other - self

        return Frac.from_float(float(other) - float(self))

    def __mul__(self, other: SupportsFloat) -> Frac:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, Frac):
            numerator = self.as_improper().numerator * other.as_improper().numerator
            denominator = (
                self.as_improper().denominator * other.as_improper().denominator
            )

            return Frac(numerator, denominator)
        return Frac.from_float(float(self) * float(other))

    def __rmul__(self, other: SupportsFloat):
        return self * other

    def __truediv__(self, other: SupportsFloat) -> Frac:
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, Frac):
            return self * other.reciprocal()
        return Frac.from_float(float(self) / float(other))

    def __rtruediv__(self, other: SupportsFloat):
        if not isinstance(other, SupportsFloat):
            return NotImplemented

        if isinstance(other, int):
            frac_other = Frac(other, 1)
            return frac_other / self

        return Frac.from_float(float(other) / float(self))


def find_numerator(base_fraction: Frac, denominator: int) -> int:
    """
    Finds the numerator of `base_fraction` scaled to `denominator` as its denominator.

    Args:
        `base_fraction`: The initial fraction which will be used to calculate the numerator.
        `denominator`: The incomplete fraction's denominator.

    Returns:
        The numerator of the incomplete fraction.

    Raises:
        TypeError: If `base_fraction` is not an instance of `Frac` **or** `denominator` is not
          an instance of `int`.
        ValueError: If `denominator` is not perfectly divisible by the denominator of
          `base_fraction.simplified().as_improper()`.

    Example:
        ```python
        >>> find_numerator(Frac(2, 3), 6)
        4
        >>> find_numerator(Frac(24, 48), 12)
        6
        ```
    """

    if not isinstance(base_fraction, Frac):
        raise TypeError(
            f"'{type(base_fraction).__name__}' object cannot be interpreted as a Frac object"
        )

    if not isinstance(denominator, int):
        raise TypeError(
            f"'{type(denominator).__name__}' object cannot be interpreted as an integer"
        )
    simplified_base = base_fraction.simplified().as_improper()

    if denominator % simplified_base.denominator == 0:
        numerator = simplified_base.numerator * (
            denominator // simplified_base.denominator
        )
        return numerator

    else:
        raise ValueError(
            "arg 'denominator' must be perfectly divisible by simplified base_fraction's denominator"
        )


def find_denominator(base_fraction: Frac, numerator: int) -> int:
    """
    Finds the denominator of `base_fraction` scaled to `numerator` as its numerator.

    Args:
        `base_fraction`: The initial fraction which will be used to calculate the numerator.
        `numerator`: The incomplete fraction's numerator.

    Returns:
        The denominator of the incomplete fraction.

    Raises:
        TypeError: If `base_fraction` is not an instance of `Frac` **or** `numerator` is not
          an instance of `int`.
        ValueError: If `numerator` is not perfectly divisible by the numerator of
          `base_fraction.simplified().as_improper()`.

    Example:
        ```python
        >>> find_denominator(Frac(1, 4), 5)
        20
        >>> find_denominator(Frac(32, 48), 8)
        12
        ```
    """

    if not isinstance(base_fraction, Frac):
        raise TypeError(
            f"'{type(base_fraction).__name__}' object cannot be interpreted as a Frac"
        )

    if not isinstance(numerator, int):
        raise TypeError(
            f"'{type(numerator).__name__}' object cannot be interpreted as an integer"
        )

    simplified_base = base_fraction.simplified().as_improper()

    if numerator % simplified_base.numerator == 0:
        denominator = simplified_base.denominator * (
            numerator // simplified_base.numerator
        )
        return denominator

    else:
        raise ValueError(
            "arg 'numerator' must be perfectly divisible by simplified base_fraction's numerator"
        )


def find_total(fraction_times_x: Frac, equal_to: SupportsFloat) -> Frac:
    """
    Finds which fraction multiplied by `fraction_times_x` equals `equal_to`.

    Args:
        `fraction_times_x`: The fraction from which the total will be calculated.
        `equal_to`: The number which multiplied by `fraction_times_x` equals the total.

    Returns:
        The base number.

    Raises:
        TypeError: If `fraction_times_x` is not an instance of `Frac` **or** `equal_to` is not
          an instance of `SupportsFloat`.

    Example:
        ```python
        >>> find_total(Frac(1, 4), 8)
        Frac(32 + 0/1)
        >>> find_total(Frac(3, 4), 8)
        Frac(10 + 2/3)
        ```
    """

    if not isinstance(fraction_times_x, Frac):
        raise TypeError(
            f"'{type(fraction_times_x).__name__}' object cannot be interpreted as a Frac"
        )

    if not isinstance(equal_to, SupportsFloat):
        raise TypeError(
            f"'{type(equal_to).__name__}' object is not an instance of 'SupportsFloat' class"
        )

    if isinstance(equal_to, int):
        total = fraction_times_x.reciprocal() * Frac(equal_to, 1)
        return total

    else:
        total = fraction_times_x.reciprocal() * equal_to
        return total
