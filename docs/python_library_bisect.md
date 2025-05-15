# `bisect` — Array bisection algorithm


This module provides support for maintaining a list in sorted order without  
having to sort the list after each insertion. For long lists of items with  
expensive comparison operations, this can be an improvement over linear  
searches or frequent resorting.

The module is called **bisect** because it uses a basic bisection algorithm  
to do its work. Unlike other bisection tools that search for a specific  
value, the functions in this module are designed to locate an insertion point.  
Accordingly, the functions never call an `__eq__()` method to determine whether  
a value has been found. Instead, they only call `__lt__()` and return an  
insertion point between values in an array.


## bisect Functions

The following functions are provided:


### bisect.bisect_left(a, x, lo=0, hi=len(a), *, key=None)

Locate the insertion point for **x** in **a** to maintain sorted order.  
The parameters **lo** and **hi** may be used to specify a subset of the list;  
by default the entire list is used. If **x** is already present in **a**,  
the insertion point will be before (to the left of) any existing entries.  
The return value is suitable for use as the first parameter to  
`list.insert()` assuming that **a** is already sorted.

The returned insertion point `i` partitions the array **a** into two slices such that:
`all(elem < x for elem in a[lo:i])` is true for the left slice and
`all(elem >= x for elem in a[i:hi])` is true for the right slice.

key specifies a key function of one argument used to extract a comparison
key from each element in the array. To support searching complex records,
the key function is not applied to x. If key is None, elements are
compared directly.


### bisect.bisect_right(a, x, lo=0, hi=len(a), *, key=None) / bisect(a, x, lo=0, hi=len(a), *, key=None)

Similar to bisect_left(), but returns an insertion point which comes after
(to the right of) any existing entries of x in a. The returned insertion
point i partitions the array a into two slices such that:
`all(elem <= x for elem in a[lo:i])` is true for the left slice and
`all(elem > x for elem in a[i:hi])` is true for the right slice.


### bisect.insort_left(a, x, lo=0, hi=len(a), *, key=None)

Insert x in a in sorted order. First runs bisect_left() to locate an
insertion point, then calls a.insert() to place x. The key function,
if any, is applied only during the search step.

Keep in mind that the O(log n) search is dominated by the O(n) insertion step.



### insort_right(a, x, lo=0, hi=len(a), *, key=None) / insort(a, x, lo=0, hi=len(a), *, key=None)

Similar to insort_left(), but inserts x after any existing entries of x.
First runs bisect_right(), then calls a.insert(). The key function, if any,
is applied only during the search step.

Keep in mind that the O(log n) search is dominated by the O(n) insertion step.



## Performance Notes

When writing time-sensitive code using bisect() and insort(), keep these in mind:
- Bisection is effective for searching ranges of values; for locating specific
values, dictionaries are often faster.
- The insort() functions are O(n) because the linear insertion step
dominates the logarithmic search.
- The search functions are stateless and discard key results after use. If used
repeatedly in a loop, a slow key function may be called many times—consider
wrapping it with functools.cache() or precomputing a list of keys.

<aside>
**See also**  
- Sorted Collections: a high-performance module that uses `bisect` to manage sorted collections.  
- SortedCollection recipe: builds a full-featured collection class with precomputed keys.  
</aside>



## Searching Sorted Lists

The bisect functions are great for insertion points but can be awkward for lookups.
Here are five helper functions:

```python
def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError

def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect_left(a, x)
    if i:
        return a[i-1]
    raise ValueError

def find_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect_right(a, x)
    if i:
        return a[i-1]
    raise ValueError

def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect_right(a, x)
    if i != len(a):
        return a[i]
    raise ValueError

def find_ge(a, x):
    'Find leftmost item greater than or equal to x'
    i = bisect_left(a, x)
    if i != len(a):
        return a[i]
    raise ValueError
```

## Examples

Numeric table lookups—map scores to letter grades:

```python
>>> def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
...     i = bisect(breakpoints, score)
...     return grades[i]
...
>>> [grade(s) for s in [33, 99, 77, 70, 89, 90, 100]]
['F', 'A', 'C', 'C', 'B', 'A', 'A']
```
With tuples—it works with a key:
```python
>>> from collections import namedtuple
>>> from operator import attrgetter
>>> from bisect import bisect, insort
>>> from pprint import pprint

>>> Movie = namedtuple('Movie', ('name', 'released', 'director'))

>>> movies = [
...     Movie('Jaws',    1975, 'Spielberg'),
...     Movie('Titanic', 1997, 'Cameron'),
...     Movie('The Birds',1963, 'Hitchcock'),
...     Movie('Aliens',  1986, 'Cameron')
... ]

>>> by_year = attrgetter('released')
>>> movies.sort(key=by_year)
>>> movies[bisect(movies, 1960, key=by_year)]
Movie(name='The Birds', released=1963, director='Hitchcock')

>>> romance = Movie('Love Story', 1970, 'Hiller')
>>> insort(movies, romance, key=by_year)
>>> pprint(movies)
[Movie(name='The Birds', released=1963, director='Hitchcock'),
 Movie(name='Love Story', released=1970, director='Hiller'),
 Movie(name='Jaws', released=1975, director='Spielberg'),
 Movie(name='Aliens', released=1986, director='Cameron'),
 Movie(name='Titanic', released=1997, director='Cameron')]
```

Precomputed keys to avoid repeated key() calls:

```python
>>> data = [('red', 5), ('blue', 1), ('yellow', 8), ('black', 0)]
>>> data.sort(key=lambda r: r[1])       # Or operator.itemgetter(1)
>>> keys = [r[1] for r in data]         # Precompute keys
>>> data[bisect_left(keys, 0)]
('black', 0)
>>> data[bisect_left(keys, 1)]
('blue', 1)
>>> data[bisect_left(keys, 5)]
('red', 5)
>>> data[bisect_left(keys, 8)]
('yellow', 8)
```
