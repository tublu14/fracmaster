# Fracmaster

fracmaster is a lightweight Python module that you can use to handle fractions like 1/2 or 3/4 
without Python automatically turning them into a float.

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

frac1 = Frac(1, 3)
frac2 = Frac(2, 3)
frac3 = Frac(16, 48)

print(frac1) # Output: Frac(0 + 1/3)
print(frac1 + frac2) # Output: Frac(1 + 0/1)

print(frac3.simplified()) # Output: Frac(0 + 1/3)
frac3.simplify() # Modifies the Frac itself, so frac3 is now 1/3

print(0.5 > frac3) # Output: True, because 1/2 is greater than 1/3

frac4 = Frac.from_float(0.5)

print(frac4) # Output: Frac(0 + 1/2)

frac5 = Frac(2, 5)

print(find_total(frac5, equal_to=10)) # Output: Frac(25 + 0/1), becuase this multiplied by frac5 equals 10
print(find_numerator(Frac(1, 4), denominator=16)) # Output: 4, becuase 1/4 is equal to 4/16
print(find_denominator(Frac(3, 5), numerator=12)) # Output: 20, because 3/5 is equal to 12/20