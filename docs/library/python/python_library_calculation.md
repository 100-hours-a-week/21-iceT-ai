# `math` — Essential Mathematical Functions

This module provides access to the mathematical functions defined by the C
standard.

These functions cannot be used with complex numbers; use the functions of the
same name from the `cmath` module if you require support for complex
numbers. The distinction between functions which support complex numbers and
those which don’t is made since most users do not want to learn quite as much
mathematics as required to understand complex numbers. Receiving an exception
instead of a complex result allows earlier detection of the unexpected complex
number used as a parameter, so that the programmer can determine how and why it
was generated in the first place.

The following functions are provided by this module. Except when explicitly
noted otherwise, all return values are floats.

| **Number-theoretic functions** |
| `comb(n, k)` | Number of ways to choose *k* items from *n* items without repetition and without order |
| `factorial(n)` | *n* factorial |
| `gcd(*integers)` | Greatest common divisor of the integer arguments |
| `isqrt(n)` | Integer square root of a nonnegative integer *n* |
| `lcm(*integers)` | Least common multiple of the integer arguments |
| `perm(n, k)` | Number of ways to choose *k* items from *n* items without repetition and with order |
| **Floating point arithmetic** |
| `ceil(x)` | Ceiling of *x*, the smallest integer greater than or equal to *x* |
| `fabs(x)` | Absolute value of *x* |
| **Power, exponential and logarithmic functions** |
| `sqrt(x)` | Square root of *x* |



## Number-theoretic functions¶

### math.comb(*n*, *k*)¶
Return the number of ways to choose *k* items from *n* items without repetition
and without order.

Evaluates to `n! / (k! * (n - k)!)` when `k <= n` and evaluates
to zero when `k > n`.

Also called the binomial coefficient because it is equivalent
to the coefficient of k-th term in polynomial expansion of
`(1 + x)ⁿ`.

Raises `TypeError` if either of the arguments are not integers.
Raises `ValueError` if either of the arguments are negative.



### math.factorial(*n*)¶
Return *n* factorial as an integer. Raises `ValueError` if *n* is not integral or
is negative.


### math.gcd(**integers*)¶
Return the greatest common divisor of the specified integer arguments.
If any of the arguments is nonzero, then the returned value is the largest
positive integer that is a divisor of all arguments. If all arguments
are zero, then the returned value is `0`. `gcd()` without arguments
returns `0`.



### math.isqrt(*n*)¶
Return the integer square root of the nonnegative integer *n*. This is the
floor of the exact square root of *n*, or equivalently the greatest integer
*a* such that *a*² ≤ *n*.

For some applications, it may be more convenient to have the least integer
*a* such that *n* ≤ *a*², or in other words the ceiling of
the exact square root of *n*. For positive *n*, this can be computed using
`a = 1 + isqrt(n - 1)`.




### math.lcm(**integers*)¶
Return the least common multiple of the specified integer arguments.
If all arguments are nonzero, then the returned value is the smallest
positive integer that is a multiple of all arguments. If any of the arguments
is zero, then the returned value is `0`. `lcm()` without arguments
returns `1`.



### math.perm(*n*, *k=None*)¶
Return the number of ways to choose *k* items from *n* items
without repetition and with order.

Evaluates to `n! / (n - k)!` when `k <= n` and evaluates
to zero when `k > n`.

If *k* is not specified or is `None`, then *k* defaults to *n*
and the function returns `n!`.

Raises `TypeError` if either of the arguments are not integers.
Raises `ValueError` if either of the arguments are negative.




## Floating point arithmetic¶

### math.ceil(*x*)¶
Return the ceiling of *x*, the smallest integer greater than or equal to *x*.
If *x* is not a float, delegates to `x.\_\_ceil\_\_`,
which should return an `Integral` value.

### math.fabs(*x*)¶
Return the absolute value of *x*.

## Power, exponential and logarithmic functions

### math.sqrt(*x*)¶
Return the square root of *x*.




# `functools.reduce` - Cumulative Reduction Function

Apply function of two arguments cumulatively to the items of iterable, from left to right, so as to reduce the iterable to a single value. For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates ((((1+2)+3)+4)+5). The left argument, x, is the accumulated value and the right argument, y, is the update value from the iterable. If the optional initial is present, it is placed before the items of the iterable in the calculation, and serves as a default when the iterable is empty. If initial is not given and iterable contains only one item, the first item is returned.

Roughly equivalent to:

```python
initial_missing = object()

def reduce(function, iterable, initial=initial_missing, /):
    it = iter(iterable)
    if initial is initial_missing:
        value = next(it)
    else:
        value = initial
    for element in it:
        value = function(value, element)
    return value
```