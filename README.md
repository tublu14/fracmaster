# Fracmaster

fracmaster is a lightweight python module that you can use to handle fractions like 1/2 or 3/4 
without Python automatically turning it into a float.

You can also perform math calculations with it. And no, its not like theres .add() and .substract() methods 
for basic math, you can do this all with **OPERATORS** (+, -, *, /).
It also includes **right hand calculations** (__radd__, __rsub__) out of the box!

## Features

- **Float conversion**: You can convert any fraction to float!
- **Fraction from float**: You can convert any float to fraction!
- **Comparison With Numbers**: You can compare a fraction to an integer or float with operators (>, ==, etc.)!
- **Proper/Improper Fractions**: You can convert any proper fractions to improper and vice versa!
- **Mixed Fractions**: You can use mixed fractions too! And yes, you can convert them to improper.
- **Simplifying**: When working with large fractions, simplifying is very important for readability and speed.
- **Mini Algebra Functions**: Comes in handy when you have to deal with problems like: fraction * x = 3, find x.

### How to use it:
Note: You do not need to install any dependencies (pip install ...), fracmaster.py only uses builtin modules.
1. Clone it in your workspace:
```bash
git clone https://github.com/tublu14/fracmaster
```
2. Copy `fracmaster.py` directly into your project folder.
3. Import it in your code and use it!

## Example

```python

from fracmaster import *

a = Fraction(1, 3)
b = Fraction(2, 3)
c = Fraction(16, 48)

print(a) # Output: Fraction(0 + 1/3)
print(a + b) # Output: Fraction(1 + 0/1)

print(c.simplified()) # Output: Fraction(0 + 1/3)
c.simplify() # Modifies the Fraction itself, so c is now 1/3

print(0.5 > c) # Output: True, because 1/2 is greater than 1/3

d = Fraction.from_float(0.5)

print(d) # Output: Fraction(0 + 1/2)