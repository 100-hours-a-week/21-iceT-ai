# `itertools` — Functions creating iterators for efficient looping

This module implements a number of iterator building blocks inspired
by constructs from APL, Haskell, and SML. Each has been recast in a form
suitable for Python.

The module standardizes a core set of fast, memory efficient tools that are
useful by themselves or in combination. Together, they form an “iterator
algebra” making it possible to construct specialized tools succinctly and
efficiently in pure Python.

**Combinatoric iterators:**

| Iterator | Arguments | Results |
| --- | --- | --- |
| `product()` | p, q, … [repeat=1] | cartesian product, equivalent to a nested for-loop |
| `permutations()` | p[, r] | r-length tuples, all possible orderings, no repeated elements |
| `combinations()` | p, r | r-length tuples, in sorted order, no repeated elements |
| `combinations\_with\_replacement()` | p, r | r-length tuples, in sorted order, with repeated elements |


| Examples | Results |
| --- | --- |
| `product('ABCD', repeat=2)` | `AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD` |
| `permutations('ABCD', 2)` | `AB AC AD BA BC BD CA CB CD DA DB DC` |
| `combinations('ABCD', 2)` | `AB AC AD BC BD CD` |
| `combinations\_with\_replacement('ABCD', 2)` | `AA AB AC AD BB BC BD CC CD DD` |


## Itertool Functions


The following functions all construct and return iterators. Some provide
streams of infinite length, so they should only be accessed by functions or
loops that truncate the stream.


### itertools.combinations(*iterable*, *r*)

Return *r* length subsequences of elements from the input *iterable*.

The output is a subsequence of `product()` keeping only entries that
are subsequences of the *iterable*. The length of the output is given
by `math.comb()` which computes `n! / r! / (n - r)!` when `0 ≤ r
≤ n` or zero when `r > n`.

The combination tuples are emitted in lexicographic order according to
the order of the input *iterable*. If the input *iterable* is sorted,
the output tuples will be produced in sorted order.

Elements are treated as unique based on their position, not on their
value. If the input elements are unique, there will be no repeated
values within each combination.

Roughly equivalent to:
```python
def combinations(iterable, r):
    # combinations('ABCD', 2) → AB AC AD BC BD CD
    # combinations(range(4), 3) → 012 013 023 123

    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))

    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)

```



### itertools.combinations\\_with\\_replacement(*iterable*, *r*)

Return *r* length subsequences of elements from the input *iterable*
allowing individual elements to be repeated more than once.

The output is a subsequence of `product()` that keeps only entries
that are subsequences (with possible repeated elements) of the
*iterable*. The number of subsequence returned is `(n + r - 1)! / r! /
(n - 1)!` when `n > 0`.

The combination tuples are emitted in lexicographic order according to
the order of the input *iterable*. if the input *iterable* is sorted,
the output tuples will be produced in sorted order.

Elements are treated as unique based on their position, not on their
value. If the input elements are unique, the generated combinations
will also be unique.

Roughly equivalent to:
```python
def combinations\_with\_replacement(iterable, r):
    # combinations\_with\_replacement('ABC', 2) → AA AB AC BB BC CC

    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r

    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)

```




### itertools.permutations(*iterable*, *r=None*)

Return successive *r* length permutations of elements from the *iterable*.

If *r* is not specified or is `None`, then *r* defaults to the length
of the *iterable* and all possible full-length permutations
are generated.

The output is a subsequence of `product()` where entries with
repeated elements have been filtered out. The length of the output is
given by `math.perm()` which computes `n! / (n - r)!` when
`0 ≤ r ≤ n` or zero when `r > n`.

The permutation tuples are emitted in lexicographic order according to
the order of the input *iterable*. If the input *iterable* is sorted,
the output tuples will be produced in sorted order.

Elements are treated as unique based on their position, not on their
value. If the input elements are unique, there will be no repeated
values within a permutation.

Roughly equivalent to:
```python 
def permutations(iterable, r=None):
    # permutations('ABCD', 2) → AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) → 012 021 102 120 201 210

    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return

    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])

    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return

```



### itertools.product(**iterables*, *repeat=1*)

Cartesian product of the input iterables.

Roughly equivalent to nested for-loops in a generator expression. For example,
`product(A, B)` returns the same as `((x,y) for x in A for y in B)`.

The nested loops cycle like an odometer with the rightmost element advancing
on every iteration. This pattern creates a lexicographic ordering so that if
the input’s iterables are sorted, the product tuples are emitted in sorted
order.

To compute the product of an iterable with itself, specify the number of
repetitions with the optional *repeat* keyword argument. For example,
`product(A, repeat=4)` means the same as `product(A, A, A, A)`.

This function is roughly equivalent to the following code, except that the
actual implementation does not build up intermediate results in memory:

```python
def product(*iterables, repeat=1):
    # product('ABCD', 'xy') → Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) → 000 001 010 011 100 101 110 111

    if repeat < 0:
        raise ValueError('repeat argument cannot be negative')
    pools = [tuple(pool) for pool in iterables] * repeat

    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]

    for prod in result:
        yield tuple(prod)

```

Before [`product()`](#itertools.product "itertools.product") runs, it completely consumes the input iterables,
keeping pools of values in memory to generate the products. Accordingly,
it is only useful with finite inputs.